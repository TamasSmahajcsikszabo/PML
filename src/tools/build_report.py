"""Build Report.md (and Report.pdf) from the template and the outputs of the pipeline: nothing in the text is typed in by hand where it is a number.

    PYTHONPATH=src .venv/bin/python -m tools.build_report [RUN_ID] [--no-pdf]

Inputs: src/report/Report.template.md ({{placeholders}}), docs/report/data_facts.json (tools.data_report), final_metrics.json (tools.report_numbers), comparisons.json (tools.evidence),
the promoted parts run and its parent run (metrics, importances, config). Fails if a placeholder has no value. Then the pdf is built by
tools.build_report_pdf (no appendix: the predictor table is docs/features.md, written by tools.feature_table). This is the LAST stage of src/pipeline.py: after any code change the whole pipeline is rerun, so the report always describes the code that ran."""
import argparse
import json
import pathlib
import re
import subprocess
import sys

import pandas as pd

from common import ROOT, run_dir
from predict import MAX_LEN

REPORT = ROOT / "docs" / "report"
NAMES = {"xgboost": "XGBoost", "random_forest": "random forest", "adaboost": "AdaBoost", "mlp": "MLP", "knn": "k-NN", "log_reg": "logistic regression", "svm": "SVM",
         "decision_tree": "decision tree", "naive_bayes": "naive Bayes"}
f3 = lambda x: f"{x:.3f}"
f2 = lambda x: f"{x:.2f}"
pct = lambda x, d=1: f"{100 * x:.{d}f}"
sgn = lambda x: "0.000" if abs(x) < 0.0005 else f"{x:+.3f}"


def rejected_urls():
    """supplied URLs the grammar rejects (their features are all missing)"""
    import urlfeat
    from common import load
    return sum(int(urlfeat.featurize(load(n).url.tolist()).isna().all(axis=1).sum()) for n in ("train", "test", "external_test"))


def ci_txt(c):
    return f"95% interval {sgn(c[0])} to {sgn(c[1])}"


def extra_data(run):
    """docs/report/extra_data.json when it describes this run, else None"""
    f = REPORT / "extra_data.json"
    if not f.exists():
        return None
    E = json.loads(f.read_text())
    return E if E["run"] == run else None


def training_sentence(E):
    if not E:
        return "It was trained on the supplied `train.csv` only."
    return f"It was trained on the supplied `train.csv` and {E['extra_rows']:,} additional public URLs ({E['rows']:,} URLs in total)."


def extra_data_text(E):
    """the paragraph on the extra public training data of the delivered run"""
    if not E:
        return "No additional data was used for the delivered model."
    c = E["comparison"]
    hs = E["host_share"]["external_test"]
    return (f"To widen the training data, {E['extra_rows']:,} URLs from {E['n_sources']} public collections were added to `train.csv` ({E['ratio']:.0f} times its size, half of "
            f"them phishing): Ebbu2017, several Kaggle phishing datasets, public phishing feeds, a Common Crawl sample and Tranco homepages (collected by "
            f"`src/tools/build_corpus.py`; the sources are listed in `CLAUDE.md`). Every URL that also appears in `test.csv` or `external_test.csv` under the task's normalisation "
            f"was removed beforehand ({E['corpus_rows_removed_for_overlap']:,} rows), and a second check while sampling found {E['extra_rows_matching_an_evaluation_url']} left. "
            f"The model was therefore trained on {E['rows']:,} URLs. Compared on identical URLs with the same pipeline trained on `train.csv` alone, the AUC on the independent "
            f"collection rose from {f3(c['external_test']['auc'][0])} to {f3(c['external_test']['auc'][1])} ({ci_txt(c['external_test']['auc_diff_ci'])}), on the test set it "
            f"moved from {f3(c['test']['auc'][0])} to {f3(c['test']['auc'][1])} ({ci_txt(c['test']['auc_diff_ci'])}), and in cross-validation on the `train.csv` rows it went from "
            f"{f3(c['train_csv_rows_oof']['auc'][0])} to {f3(c['train_csv_rows_oof']['auc'][1])}. The extra data therefore helps most on a new source and costs a little on data "
            f"like `train.csv`. Part of the gain may come from the public sources resembling the independent collection: {pct(hs['train_plus_extra'], 0)}% of its rows now sit on "
            f"a website seen in training, against {pct(hs['train_only'], 0)}% with `train.csv` alone.")


def mixed_domain_text(S):
    """the paragraph on websites that carry both labels (final_metrics.json: sets.*.mixed_domains)"""
    o, te = S["train_oof"]["mixed_domains"], S["test"]["mixed_domains"]
    big = list(o["largest"].items())
    flagged = [g for g, v in big[:10] if v["fpr"] >= 0.2]
    missed = [g for g, v in big[:10] if v["recall"] == 0]
    code = lambda gs: ", ".join(f"`{g}`" for g in gs)
    return (f"**Same website, both labels.** {o['n_domains']} websites in the training data carry both phishing and legitimate URLs ({pct(o['share_of_rows'], 0)}% of the rows), "
            f"and so do {te['n_domains']} in the test set (mostly {code(te['largest'])}). On these rows the model is clearly weaker: out of fold the AUC is {f3(o['mixed']['auc'])} "
            f"against {f3(o['single']['auc'])} on the other websites, and on the test set {f3(te['mixed']['auc'])} against {f3(te['single']['auc'])}. Of two URLs from the same "
            f"website, the phishing one is scored higher in {pct(o['pair_auc_within_domain'], 0)}% of the pairs in training and {pct(te['pair_auc_within_domain'], 0)}% on the test set. "
            f"These websites produce {pct(o['share_of_false_positives'], 0)}% of the false alarms in training (and {pct(te['share_of_false_positives'], 0)}% on the test set). "
            f"The model largely gives one verdict per website: on websites such as {code(flagged)} many of the legitimate URLs are flagged, while on large popular domains "
            f"such as {code(missed)} not one phishing URL is caught. {o['same_page_both_labels']} pages appear in training with both labels; "
            f"{pct(o['same_page_identical_score'], 0)}% of them are the identical URL, which no URL-based model can separate. "
            f"The conclusion is that the model judges the website far better than the individual page; telling pages apart within one website needs features of the "
            f"sub-domain and path that do not depend on the website (one site per platform tenant, character patterns of the path), and a missing alert on a popular domain "
            f"should not be read as \"safe\".")


def normalised_text(cfg):
    """the paragraph on the visitor's normalised view (docs/report/normalised.json)"""
    head = ("The task's rule for \"the same page\" (lower-case, no scheme, no leading `www.`, no trailing slash) is not a preprocessing step of the delivered pipeline: "
            "the scheme and `www` carry information, and URLs are never rewritten. As an option, the visitor can compute every feature on that normalised view instead "
            "(`URLVisitor(normalised=True)`, `pipeline.py --normalised`), so that URLs which differ only in these respects get identical features; this was checked on all "
            "supplied URLs.")
    f = REPORT / "normalised.json"
    if not f.exists():
        return head
    N = json.loads(f.read_text())
    s, cv = N["sensitivity_of_delivered"], N["cv_auc"]
    worse = sum(v["normalised"] < v["as_given"] for v in cv.values())
    view = "The delivered model reads every URL as given." if not cfg.get("normalised") else "The delivered model uses the normalised view."
    return head + (f" The spelling does matter to a model trained on URLs as given: for the delivered model, adding or removing `www.` changes the label of "
                   f"{pct(s['test']['www']['flip_share'])}% of {N['sample']} sampled test URLs and {pct(s['external_test']['www']['flip_share'])}% of independent ones, and "
                   f"reducing a URL to the task's form changes {pct(s['test']['normal_form']['flip_share'])}% and {pct(s['external_test']['normal_form']['flip_share'])}%. "
                   f"The option was tested on `train.csv` with the same folds: cross-validated AUC was lower for {worse} of the {len(cv)} models (XGBoost "
                   f"{f3(cv['xgboost']['as_given'])} to {f3(cv['xgboost']['normalised'])}, logistic regression {f3(cv['log_reg']['as_given'])} to "
                   f"{f3(cv['log_reg']['normalised'])}), so it was not adopted. " + view)


def values(run):
    d = run_dir(run)
    cfg = json.loads((d / "config.json").read_text())
    D, M, C = (json.loads((REPORT / f).read_text()) for f in ("data_facts.json", "final_metrics.json", "comparisons.json"))
    assert M["run"] == run and C["run"] == run, "docs/report/*.json belong to another run: rerun tools.report_numbers and tools.evidence"
    par = run_dir(cfg["parent"])
    S, tr, fs = M["sets"], D["train_issues"], D["feature_shares"]
    te, ex, oof = S["test"], S["external_test"], S["train_oof"]
    fi = pd.read_csv(par / "feature_importance.csv").groupby("feature").permutation_auc_drop.mean().sort_values(ascending=False)
    lg = M["parent_models"]["log_reg"]
    hosts = list(tr["largest_host_groups"].items())[:3]
    pe, fe, cv = C["parts_effect"], C["filter_effect"], C["cv_optimism"]
    cand = pe["candidate"]
    n_match = round(D["overlap"]["test"]["task_norm"]["share_of_rows"] * te["n"])
    agree = D["overlap"]["test"]["task_norm_label_agreement"]
    ci = te["ci"]
    V = {
        "mixed_domain_text": mixed_domain_text(S),
        "auc_test_2": f2(te["auc"]), "auc_ext_2": f2(ex["auc"]), "recall_test_2": f2(te["recall"]), "recall_ext_2": f2(ex["recall"]),
        "alerts_n": f"{round(1 / te['precision_at_prevalence'])}", "alerts_false": f"{round(1 / te['precision_at_prevalence']) - 1}",
        "train_rows": f"{tr['rows']:,}", "train_phish_pct": pct(D["sets"]["train"]["phishing_share"]), "repeated_url_rows": tr["rows_repeating_an_earlier_url"],
        "dup_same_label": tr["exact_duplicate_rows"], "conflict_urls": tr["urls_with_conflicting_labels_exact"], "conflict_rows": tr["rows_of_conflicting_urls_exact"],
        "norm_extra_rows": tr["extra_rows_duplicated_under_task_norm"], "norm_conflict_keys": tr["keys_with_conflicting_labels_task_norm"], "norm_conflict_rows": tr["rows_of_conflicting_keys_task_norm"],
        "top_hosts": ", ".join(f"`{h}` {n}" for h, n in hosts), "share_hosts5_pct": pct(tr["rows_in_hosts_with_5_or_more_rows"] / tr["rows"], 0),
        "columns": C["counts"]["columns"], "kept_features": C["counts"]["kept_features"], "platform_names": f"{C['counts']['platform_names']:,}", "tld_literals": f"{C['counts']['tld_literals']:,}",
        "ms_per_url": f"{C['speed']['ms_per_url_columns']:.1f}", "urls_checked": f"{C['label_cuts']['urls_checked']:,}", "urls_cut": C["label_cuts"]["urls_with_a_cut_label"],
        "blend_members": ", ".join(NAMES[m] for m in cfg["blend_members"]), "thr_raw": f3(cfg["threshold_raw"]),
        "label_agreement_text": f"All {n_match} matching test rows carried the training label." if agree == 1.0 else f"{pct(agree, 0)}% of the {n_match} matching test rows carried the training label.",
        "auc_seen_test": f3(te["auc_seen_hosts"]), "auc_unseen_test": f3(te["auc_unseen_hosts"]), "auc_seen_ext": f3(ex["auc_seen_hosts"]), "auc_unseen_ext": f3(ex["auc_unseen_hosts"]),
        "seen_share_ext_pct": pct(ex["share_hosts_seen_in_train"], 0), "recall_matched_ext_2": f2(ex["recall_at_1pct_fpr_on_this_set"]), "ece_test": f3(te["ece_calibrated_vs_set"]), "ece_ext": f3(ex["ece_calibrated_vs_set"]),
        "plat_ph": pct(fs["train"]["phishing"]["sfx_platform"]), "plat_lg": pct(fs["train"]["legitimate"]["sfx_platform"]), "emb_ph": pct(fs["train"]["phishing"]["emb_domain"]),
        "emb_lg": pct(fs["train"]["legitimate"]["emb_domain"]), "phrase_ph": pct(fs["train"]["phishing"]["suspicious_phrase"], 0), "phrase_lg": pct(fs["train"]["legitimate"]["suspicious_phrase"]),
        "path_lg_train": pct(D["sets"]["train"]["legitimate"]["has_path"], 0), "path_lg_test": pct(D["sets"]["test"]["legitimate"]["has_path"], 0), "path_lg_ext": pct(D["sets"]["external_test"]["legitimate"]["has_path"], 0),
        "recall_nopath_test": f2(te["by_shape"]["path-less"]["recall"]), "recall_nopath_ext": f2(ex["by_shape"]["path-less"]["recall"]), "recall_path_test": f2(te["by_shape"]["with path/query"]["recall"]),
        "pop_lg_train": pct(fs["train"]["legitimate"]["reg_popular"], 0), "pop_ph_train": pct(fs["train"]["phishing"]["reg_popular"], 0), "pop_lg_ext": pct(fs["external_test"]["legitimate"]["reg_popular"]),
        "pop_ph_ext": pct(fs["external_test"]["phishing"]["reg_popular"]), "imp1_name": fi.index[0], "imp1_val": f3(fi.iloc[0]), "imp2_name": fi.index[1], "imp2_val": f3(fi.iloc[1]),
        "prec_test_pct": pct(te["precision_at_prevalence"]), "prec_test_lo": pct(ci["precision_at_prevalence"][0]), "prec_test_hi": pct(ci["precision_at_prevalence"][1]), "prec_oof_pct": pct(oof["precision_at_prevalence"]),
        "n_legit_test": f"{te['tn'] + te['fp']:,}",
        "max_len": f"{MAX_LEN:,}", "thr_cal": f3(cfg["threshold"]),
        "seen_share_test_pct": pct(te["share_hosts_seen_in_train"], 0), "ext_lg_https_pct": pct(D["sets"]["external_test"]["legitimate"]["https"], 0),
        "ext_lg_www_pct": pct(D["sets"]["external_test"]["legitimate"]["www"], 0),
        "recall_test_pct": pct(te["recall"], 0), "recall_ext_pct": pct(ex["recall"], 0), "recall_matched_ext_pct": pct(ex["recall_at_1pct_fpr_on_this_set"], 0),
        "recall_nopath_test_pct": pct(te["by_shape"]["path-less"]["recall"], 0), "recall_path_test_pct": pct(te["by_shape"]["with path/query"]["recall"], 0),
        "top3_rows": f"{sum(n for _, n in hosts):,}", "cv_opt": f3(cv["optimism"]),
    }
    V.update({"auc_base_cv": f3(lg["cv_auc_oof"]), "auc_base_test": f3(lg["test_auc"]), "auc_base_ext": f3(lg["external_test_auc"]), "auc_oof": f3(oof["auc"]), "auc_test": f3(te["auc"]), "auc_ext": f3(ex["auc"])})
    rows = ["| data | AUC | phishing caught (recall) | legitimate flagged (false-positive rate) | flagged that are phishing (precision) |", "|---|---|---|---|---|",
            f"| training, cross-validated | {f3(oof['auc'])} [{f3(oof['ci']['auc'][0])}-{f3(oof['ci']['auc'][1])}] | {pct(oof['recall'])}% | {pct(oof['fpr'])}% | {pct(oof['precision'])}% |"]
    for n, label in (("test", "test set"), ("external_test", "independent collection")):
        s = S[n]
        c = s["ci"]
        fpr = f"{pct(s['fpr'])}% [{pct(c['fpr'][0])}-{pct(c['fpr'][1])}%]" if s["fp"] else f"none of {s['tn']:,} (below {pct(s['fpr_upper_95_rule_of_three'], 2)}%)"
        rows.append(f"| {label} | {f3(s['auc'])} [{f3(c['auc'][0])}-{f3(c['auc'][1])}] | {pct(s['recall'])}% [{pct(c['recall'][0])}-{pct(c['recall'][1])}%] | {fpr} | {pct(s['precision'])}% |")
    V["table_metrics"] = "\n".join(rows)
    V.update({"auc_parts_oof": f3(pe["train_oof"]["parts"]), "parts_gain_oof": sgn(pe["train_oof"][cand] - pe["train_oof"]["blend"]),
              "parts_gain_ext": sgn(pe["external_test"][cand] - pe["external_test"]["blend"]), "urls_rejected": rejected_urls()})
    go, ge = (pe[k][cand] - pe[k]["blend"] for k in ("train_oof", "external_test"))
    V["parts_gain_text"] = ((f"adding it left the cross-validated AUC unchanged" if abs(go) < 0.0005 else f"adding it changed the AUC by {sgn(go)} in cross-validation")
                            + f" and changed it by {sgn(ge)} on the independent collection")
    V["base_ext_join"] = "but only" if lg["external_test_auc"] < lg["test_auc"] else "and"
    if ex["fp"] == 0:
        V["ext_fp_text"] = (f"On the independent collection the model raised no false alarm at all, but with {ex['tn']:,} legitimate URLs this only tells us that the false-alarm "
                            f"rate is below about {pct(ex['fpr_upper_95_rule_of_three'], 2)}%; in that best case, at least {pct(ex['precision_at_prevalence_lower_bound'])}% of alerts would be phishing.")
    else:
        V["ext_fp_text"] = (f"On the independent collection {ex['fp']} of {ex['fp'] + ex['tn']:,} legitimate URLs {'was' if ex['fp'] == 1 else 'were'} flagged (a false-alarm rate of {pct(ex['fpr'], 2)}%), "
                            f"which at that prevalence means about {pct(ex['precision_at_prevalence'], 0)}% of alerts would be phishing"
                            + (f"; with so few false alarms the range is wide ({pct(ex['ci']['precision_at_prevalence'][0], 0)}% to {pct(ex['ci']['precision_at_prevalence'][1], 0)}%)." if ex["fp"] < 5 else "."))
    lo, hi = ci["fpr"]
    V["fpr_factor_text"] = f"within a factor of about {hi / lo:.0f}" if lo > 0 else f"better than somewhere between 0% and {pct(hi)}%"
    E = extra_data(run)
    V["extra_data_text"], V["training_sentence"] = extra_data_text(E), training_sentence(E)
    V["normalised_text"] = normalised_text(cfg)
    names = {"exact": "the identical string", "task_norm": "the same text after the task's rule (case, scheme, `www.`, trailing slash)", "norm_no_query": "the same page when the query string is also ignored",
             "host_first_segment": "the same host and the same first folder of the path", "registrable_host": "the same website (registrable domain)"}
    V["table_overlap"] = "\n".join(["| two URLs count as the same when they have ... | share of test rows | share of independent rows |", "|---|---|---|"]
                                    + [f"| {names[k]} | {pct(D['overlap']['test'][k]['share_of_rows'])}% | {pct(D['overlap']['external_test'][k]['share_of_rows'])}% |" for k in names])
    V["overlap_text"] = "; ".join(f"{names[k]} {f3(D['overlap']['test'][k]['share_of_rows'])} / {f3(D['overlap']['external_test'][k]['share_of_rows'])}" for k in names)
    dg = lambda k: sgn(pe[k][cand] - pe[k]["blend"])
    dec = [("The same few websites fill many rows of the training file.", "We validated with whole websites held out.",
            f"A random split would have overstated the AUC by {f3(cv['optimism'])} ({f3(cv['auc_random_folds'])} instead of {f3(cv['auc_grouped_folds'])})."),
           ("Hosting-platform names inside the grammar split real host names, for example `com.secureupdate` into `com.se` and `cureupdate`.",
            "We moved the platform names into a list that is matched against whole parts of the host.", f"{C['platform_fix']['rows_changed']} training URLs now get correct host features."),
           ("The remaining errors sit where both classes look alike in the URL-level features.", "We added the parts model, which scores each part of the URL separately, to the delivered average.",
            f"AUC changed by {dg('train_oof')} in cross-validation, {dg('test')} on the test set and {dg('external_test')} on the independent collection.")]
    if E:
        c = E["comparison"]
        dec.append(("The independent collection looks unlike `train.csv`, and the model's recall there was low.", f"We added {E['extra_rows']:,} public URLs to the training data.",
                    f"Independent AUC {sgn(c['external_test']['auc'][1] - c['external_test']['auc'][0])} ({ci_txt(c['external_test']['auc_diff_ci'])}), test AUC "
                    f"{sgn(c['test']['auc'][1] - c['test']['auc'][0])}, cross-validated AUC on the `train.csv` rows {sgn(c['train_csv_rows_oof']['auc'][1] - c['train_csv_rows_oof']['auc'][0])}."))
    if (REPORT / "normalised.json").exists():
        cvn = json.loads((REPORT / "normalised.json").read_text())["cv_auc"]
        dec.append(("The same page written with or without `www.` could get a different label.", "We tried computing all features on the task's normalised view of the URL.",
                    f"Cross-validated AUC fell for every model (XGBoost {sgn(cvn['xgboost']['normalised'] - cvn['xgboost']['as_given'])}), so the option was not adopted."))
    V["table_decisions"] = "\n".join(["| observation | action | effect |", "|--------------|-----------|--------------------|"] + [f"| {a} | {b} | {c} |" for a, b, c in dec])
    return V


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run", nargs="?", default=None)
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()
    run = run_dir(a.run).name
    V = values(run)
    txt = (ROOT / "src" / "report" / "Report.template.md").read_text(encoding="utf-8")
    for k, v in V.items():
        txt = txt.replace("{{" + k + "}}", str(v))
    left = set(re.findall(r"\{\{(\w+)\}\}", txt))
    assert not left, f"placeholders without a value: {left}"
    (ROOT / "Report.md").write_text(txt, encoding="utf-8")
    print(f"Report.md written from run {run} ({len(txt.split())} words)")
    env = {**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")}
    if not a.no_pdf:
        subprocess.run([sys.executable, "-m", "tools.build_report_pdf"], check=True, cwd=ROOT, env=env)


if __name__ == "__main__":
    main()
