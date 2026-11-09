// URL lexer. One mode per URL component, so the same character (. = ? : /) means the right thing in each:
//   AUTHORITY (with an optional leading `scheme://` token) -> PATH -> QUERY -> FRAGMENT      (forward-only; `mode()` switches on the delimiter)
// Finite vocabularies (TLD, SLD, EXT) are tokens; everything open-ended is an opaque *_TEXT/LABEL token
// whose value is for a later step. Every mode ends in a catch-all, so the lexer never fails on dirty input.
lexer grammar UrlLexer;
import UrlVocab;
options { caseInsensitive = true; }

// ---- scheme (optional) + authority: [scheme://][userinfo@]host[:port] -------------------
// The default mode is the authority. A scheme is the token `abc://` at the start of the input (a second one inside the host, as in http://http://x.com, is read as host text); URLs without one
// (kaggle/phishtank style `www.x.com/a`) are read exactly as written, nothing is added or changed.
SCHEME_PREFIX : [a-z] [a-z0-9+.\-]* '://' ;

SLD        : SLD_NAMES;                  // com co ac gov ... (also valid as a TLD; see parser `tld`)
TLD        : TLD_NAMES;                  // must precede PUNYCODE: IANA has xn-- TLDs
WWW        : 'www';
PUNYCODE   : 'xn--' [a-z0-9\-]+;
DIGITS     : [0-9]+;
LABEL      : ([a-z0-9_\-] | NON_ASCII)+; // one dot-free host label (or userinfo word)
DOT        : '.';
COLON      : ':';
AT         : '@';
PCT        : '%' HEX HEX;
SLASH      : '/' -> mode(PATH);
QMARK      : '?' -> mode(QUERY);
HASH       : '#' -> mode(FRAGMENT);
AUTH_OTHER : ~[/?#];                     // [ ] \ space stray % etc.

// ---- path --------------------------------------------------------------------
mode PATH;
PATH_SLASH : '/' -> type(SLASH);
PATH_QMARK : '?' -> type(QMARK), mode(QUERY);
PATH_HASH  : '#' -> type(HASH), mode(FRAGMENT);
PATH_DOT   : '.' -> type(DOT);
EXT        : EXT_NAMES;                  // only a file extension to the parser when it follows DOT at segment end
PATH_EMAIL : EMAIL_SHAPE -> type(EMAIL);
PATH_AT_WORD : [a-z0-9._+\-]+ ('@' | '%40') [a-z0-9.\-]+ -> type(SEG_TEXT);  // lookahead substitute: logo@2x.png must not lex as EMAIL 'logo@2x.pn' + 'g'
PATH_PCT   : '%' HEX HEX -> type(PCT);
SEG_TEXT   : ~[/?#.%]+;
STRAY_PCT  : '%';

// ---- query -------------------------------------------------------------------
mode QUERY;
AMP_ESC    : '&amp;';                    // HTML-escaped separator (0.7% of phishing, ~0% of normal web); beats AMP by length
AMP        : '&';
EQ         : '=';
QUERY_HASH : '#' -> type(HASH), mode(FRAGMENT);
// Opaque tokens for a later step: re-parse NESTED_URL's text with this same grammar (percent-decode first if it has %3A%2F%2F).
// It outlasts QUERY_TEXT (which stops at = %), so it wins whenever it matches at a token start. Ends at & like the outer pair.
NESTED_URL : NEST_SCHEME (':' | '%3a') ('/' | '%2f') ('/' | '%2f') ~[&#]*;
QUERY_EMAIL : EMAIL_SHAPE -> type(EMAIL);
QUERY_PCT  : '%' HEX HEX -> type(PCT);
QUERY_TEXT : ~[&=#%]+;                   // may contain / ? : @ ; etc. (RFC 3986)
QUERY_STRAY_PCT : '%' -> type(STRAY_PCT);

// ---- fragment ----------------------------------------------------------------
mode FRAGMENT;
EMAIL      : EMAIL_SHAPE;                // the token type; PATH_EMAIL / QUERY_EMAIL retype into it
FRAG_PCT   : '%' HEX HEX -> type(PCT);
FRAG_TEXT  : ~[%]+;
FRAG_STRAY_PCT : '%' -> type(STRAY_PCT);

// user@host.tld, with the tld from the finite lists so img@2x.png is not an email. '@' may be %40.
fragment EMAIL_SHAPE : [a-z0-9._+\-]+ ('@' | '%40') [a-z0-9\-]+ ('.' [a-z0-9\-]+)* '.' (TLD_NAMES | SLD_NAMES);
fragment NEST_SCHEME : 'http' 's'? | 'ftp';
fragment HEX       : [0-9a-f];
fragment NON_ASCII : [\u0080-\u{10FFFF}];
