"""How much of the pipeline depends on ANTLR: (1) cost per URL, (2) which feature columns come from the parse tree / use its pieces / ignore it, with their importance share,
(3) [removed: the string split of the old code no longer exists], (4) XGBoost ablation on train.csv (host-grouped CV, test, external).

    PYTHONPATH=src .venv/bin/python -m tools.antlr_reliance            (about 5 minutes)"""
import time, collections, warnings
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from xgboost import XGBClassifier
from antlr4 import InputStream, CommonTokenStream
from common import load, host_group, RESULTS, SEED
from models.model import inputs
import urlfeat
from urlfeat import structure
from urlfeat.visitor import UrlLexer, UrlParser
warnings.filterwarnings("ignore")


def main():
    cols = urlfeat.COLUMNS
    TREE = set("""https ftp host_ipv4 host_platform host_other sfx_platform sfx_platform_bare sfx_icann2 has_ext port has_path trailing_slash path_len userinfo www punycode has_query n_amp_esc n_nested n_email has_frag
    pct_total stray_pct n_sub n_seg n_empty_seg n_pairs n_empty_val host_len reg_len reg_hyphens reg_digits max_seg_len query_len frag_len""".split())
    # columns that read the tree's pieces (host text, registrable, suffix, ext, segments, query keys/values) but compute from strings
    USES = set("""max_label_len mean_seg_len max_qkey_len max_qval_len mean_qval_len host_digit_rate path_digit_rate query_digit_rate rep_char_host rep_char_path rep_char_query rep_digit emb_ip emb_domain emb_hex emb_port
    n_dash_host n_dots_host ent_reg ent_max_seg ent_max_qval sc_delims_host sc_other_host sw_phrase_host brand_in_sub brand_in_reg brand_wrong_tld brand_typo brand_in_path brand_in_query reg_popular is_shortener
    www_extra_label host_legibility host_typo_rate host_leet sld_legibility sld_typo_rate sld_leet sld_vowel_ratio sld_consonant_run seg_min_legibility seg_max_typo qval_min_legibility qval_max_typo seg_max_leet seg_consonant_run
    tld_suspicious tld_cc tld_has_digit ext_php ext_html ext_htm ext_asp ext_aspx ext_jsp ext_exe ext_zip ratio_nonalnum_host host_n_scripts host_mixed_script host_confusable_chars brand_lookalike_reg brand_lookalike_host
    host_digit_in_word reg_log_rank longest_digit_run""".split())
    org = {c: "tree" if c in TREE else "uses tree pieces" if c in USES else "string only" for c in cols}
    
    urls = load("test").url.tolist()[:1500] + load("external_test").url.tolist()[:1500]
    def T(f, n=1):
        t=time.perf_counter(); [f(u) for u in urls]; return (time.perf_counter()-t)/len(urls)*1000
    # lexing only / parse only
    def lex(u): lx=UrlLexer(InputStream(u)); lx.removeErrorListeners(); ts=CommonTokenStream(lx); ts.fill(); return ts
    def parse(u):
        ts=lex(u); p=UrlParser(ts); p.removeErrorListeners(); return p.url()
    print("lexer only    ms/URL %.3f"%T(lex))
    print("lex+parse     ms/URL %.3f"%T(parse))
    print("structure()   ms/URL %.3f"%T(structure))
    V = urlfeat.get_visitor()
    print("URLVisitor.run, 141 columns only    ms/URL %.3f"%T(lambda u: V.run(u, parts=False)))
    print("URLVisitor.run, columns + parts rows ms/URL %.3f"%T(V.run))
    # rejection
    for n in ["train","test","external_test"]:
        d=load(n); rej=sum(structure(u) is None for u in d.url); print(n,"rejected by grammar:",rej,"of",len(d))
    # host kinds
    c=collections.Counter()
    for u in load("train").url[:3000]:
        s=structure(u); c[(s["host_kind"], s["suffix_kind"])]+=1
    print(c.most_common())
    
    print(pd.Series(org).value_counts().to_string())
    for run in ["20261104T1518_nine-models","v2_20261104T1749_corr-filter-0.75"]:
        w = pd.read_csv(RESULTS/run/"feature_importance_wide.csv", index_col=0)
        imp = w.mean_drop_top_models.clip(lower=0); imp = imp/imp.sum()
        g = imp.groupby(lambda c: org.get(c,"?")).sum().round(3)
        n = pd.Series({c: org.get(c,"?") for c in w.index}).value_counts()
        print(run, "importance share:", g.to_dict(), "kept columns:", n.to_dict())
    # (the string-based component split lexical.split_url was removed with the URLVisitor refactor: path / query / fragment now come from the tree)
    D = {n: load(n) for n in ["train","test","external_test"]}
    X = {n: inputs(d.url.values) for n, d in D.items()}
    y = D["train"].label.values; g = np.array([host_group(u) for u in D["train"].url])
    sets = {"all 141": cols, "without the 35 tree columns": [c for c in cols if org[c]!="tree"], "string-only 39": [c for c in cols if org[c]=="string only"],
            "tree 35 only": [c for c in cols if org[c]=="tree"], "tree + uses-tree 102 (no string-only)": [c for c in cols if org[c]!="string only"]}
    mk = lambda: XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, n_jobs=-1, random_state=SEED)
    for name, cs in sets.items():
        oof = np.zeros(len(y))
        for a, b in StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(X["train"], y, g):
            oof[b] = mk().fit(X["train"].iloc[a][cs], y[a]).predict_proba(X["train"].iloc[b][cs])[:,1]
        m = mk().fit(X["train"][cs], y)
        r = [roc_auc_score(D[n].label, m.predict_proba(X[n][cs])[:,1]) for n in ["test","external_test"]]
        print(f"{name:42s} cols {len(cs):3d}  CV AUC {roc_auc_score(y,oof):.4f}  test {r[0]:.4f}  external {r[1]:.4f}", flush=True)


if __name__ == "__main__":
    main()
