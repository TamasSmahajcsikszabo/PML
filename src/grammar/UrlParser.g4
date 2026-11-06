// URL parser: structure only. Generate the lexer first (tokenVocab).
//   url -> [scheme://] authority [path] [query] [fragmentPart]     (the scheme is one SCHEME_PREFIX token; URLs may have none)
// Components worth extracting: scheme, userinfo, host (ipv4 | domain: subdomain* registrable publicSuffix), port,
// (publicSuffix is a PLATFORM token for hosting platforms: registrable is then the tenant, e.g. evil.workers.dev),
// path segments (+ fileExt), query pairs (key/value), fragmentPart.
parser grammar UrlParser;
options { tokenVocab = UrlLexer; }

url : SCHEME_PREFIX? authority path? query? fragmentPart? EOF ;

// ---- authority ---------------------------------------------------------------
// userinfo may itself contain '@' and ':' (ftp://me@h.org:pw@h.org/); the host is whatever follows the last '@'.
authority : (userinfo AT)? host (COLON port?)? ;
userinfo  : (authTok | AT)* ;
port      : DIGITS ;

// Alternatives are tried in order on ambiguity: ipv4, recognised-suffix domain, bare platform, then anything else.
host      : ipv4 | domain | platformHost | otherHost ;
ipv4      : DIGITS DOT DIGITS DOT DIGITS DOT DIGITS ;     // octet range is a text-value check for later

// Non-greedy loop = fewest subdomains = longest public suffix (com.et beats et), as in the PSL.
domain    : (subdomain DOT)*? registrable DOT publicSuffix DOT? ;
subdomain   : hostLabel ;
registrable : hostLabel ;
publicSuffix : PLATFORM | SLD DOT tld | tld ;               // workers.dev (tenant = registrable) | co.uk | com
tld       : TLD | SLD ;
platformHost : PLATFORM DOT? ;                            // the platform itself, no tenant (cloudflare-ipfs.com, s3.us-east-2.amazonaws.com)

otherHost : hostLabel (DOT hostLabel)* DOT? ;             // localhost, unknown TLD, ...
hostLabel : labelTok+ ;                                   // >1 token only around %xx / stray chars
labelTok  : SCHEME_PREFIX | LABEL | DIGITS | WWW | PUNYCODE | TLD | SLD | PLATFORM | PCT | AUTH_OTHER ;
authTok   : labelTok | DOT | COLON ;

// ---- path --------------------------------------------------------------------
path      : (SLASH segment?)+ ;                           // '/', '/a', '/a/', '//a'
segment   : segPiece+? fileExt? ;                         // non-greedy so 'index.html' ends in fileExt
fileExt   : DOT EXT ;
segPiece  : SEG_TEXT | PCT | STRAY_PCT | DOT | EXT | EMAIL ;

// ---- query -------------------------------------------------------------------
query     : QMARK pair ((AMP | AMP_ESC) pair)* ;
pair      : key (EQ value)? ;                             // value may contain further '='
key       : qPiece* ;
value     : (qPiece | EQ)* ;
qPiece    : QUERY_TEXT | PCT | STRAY_PCT | EMAIL | NESTED_URL ;   // the last two are opaque; re-parse in a later step

// ---- fragment ----------------------------------------------------------------
fragmentPart : HASH (FRAG_TEXT | PCT | STRAY_PCT | EMAIL)* ;
