# URL breakdown (grammar + applied rules)

```
URL: http://betasusgirisadresi.blogspot.com
  tokens : SCHEME_PREFIX:'http://' LABEL:'betasusgirisadresi' DOT:'.' LABEL:'blogspot' DOT:'.' SLD:'com'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(LABEL:'betasusgirisadresi') DOT:'.' registrable>hostLabel>labelTok(LABEL:'blogspot') DOT:'.' publicSuffix>tld(SLD:'com')))
  rule   : suffix 'blogspot.com' is a listed platform (whole labels) -> tenant 'betasusgirisadresi' is the registrable, sub-domains []
  parts  : scheme='http' host='betasusgirisadresi.blogspot.com' subdomains=[] registrable='betasusgirisadresi' suffix='blogspot.com' (platform) port=''
           path='' segments=[] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=1, sfx_platform_bare=0, sfx_icann2=0, n_sub=0, www=0, reg_len=2.94, reg_popular=0, reg_log_rank=6, host_len=3.47

URL: https://secure-login-portal-outlook.el.r.appspot.com/linkedrecruiter.html
  tokens : SCHEME_PREFIX:'https://' LABEL:'secure-login-portal-outlook' DOT:'.' LABEL:'el' DOT:'.' LABEL:'r' DOT:'.' LABEL:'appspot' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'linkedrecruiter' DOT:'.' EXT:'html'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(subdomain>hostLabel>labelTok(LABEL:'secure-login-portal-outlook') DOT:'.' subdomain>hostLabel>labelTok(LABEL:'el') DOT:'.' subdomain>hostLabel>labelTok(LABEL:'r') DOT:'.' registrable>hostLabel>labelTok(LABEL:'appspot') DOT:'.' publicSuffix>tld(SLD:' ...
  rule   : suffix 'r.appspot.com' is a listed platform (whole labels) -> tenant 'el' is the registrable, sub-domains ['secure-login-portal-outlook']
  parts  : scheme='https' host='secure-login-portal-outlook.el.r.appspot.com' subdomains=['secure-login-portal-outlook'] registrable='el' suffix='r.appspot.com' (platform) port=''
           path='/linkedrecruiter.html' segments=['linkedrecruiter.html'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=1, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=0, reg_len=1.1, reg_popular=0, reg_log_rank=6, host_len=3.81

URL: https://outlook-office365-signin.el.r.appspot.com/linkedrecruiter.html
  tokens : SCHEME_PREFIX:'https://' LABEL:'outlook-office365-signin' DOT:'.' LABEL:'el' DOT:'.' LABEL:'r' DOT:'.' LABEL:'appspot' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'linkedrecruiter' DOT:'.' EXT:'html'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(subdomain>hostLabel>labelTok(LABEL:'outlook-office365-signin') DOT:'.' subdomain>hostLabel>labelTok(LABEL:'el') DOT:'.' subdomain>hostLabel>labelTok(LABEL:'r') DOT:'.' registrable>hostLabel>labelTok(LABEL:'appspot') DOT:'.' publicSuffix>tld(SLD:'com ...
  rule   : suffix 'r.appspot.com' is a listed platform (whole labels) -> tenant 'el' is the registrable, sub-domains ['outlook-office365-signin']
  parts  : scheme='https' host='outlook-office365-signin.el.r.appspot.com' subdomains=['outlook-office365-signin'] registrable='el' suffix='r.appspot.com' (platform) port=''
           path='/linkedrecruiter.html' segments=['linkedrecruiter.html'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=1, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=0, reg_len=1.1, reg_popular=0, reg_log_rank=6, host_len=3.74

URL: https://neltfxix.blogspot.com/
  tokens : SCHEME_PREFIX:'https://' LABEL:'neltfxix' DOT:'.' LABEL:'blogspot' DOT:'.' SLD:'com' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(subdomain>hostLabel>labelTok(LABEL:'neltfxix') DOT:'.' registrable>hostLabel>labelTok(LABEL:'blogspot') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/'))
  rule   : suffix 'blogspot.com' is a listed platform (whole labels) -> tenant 'neltfxix' is the registrable, sub-domains []
  parts  : scheme='https' host='neltfxix.blogspot.com' subdomains=[] registrable='neltfxix' suffix='blogspot.com' (platform) port=''
           path='/' segments=[] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=1, sfx_platform_bare=0, sfx_icann2=0, n_sub=0, www=0, reg_len=2.2, reg_popular=0, reg_log_rank=6, host_len=3.09

URL: http://matbetgir1.blogspot.com
  tokens : SCHEME_PREFIX:'http://' LABEL:'matbetgir1' DOT:'.' LABEL:'blogspot' DOT:'.' SLD:'com'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(LABEL:'matbetgir1') DOT:'.' registrable>hostLabel>labelTok(LABEL:'blogspot') DOT:'.' publicSuffix>tld(SLD:'com')))
  rule   : suffix 'blogspot.com' is a listed platform (whole labels) -> tenant 'matbetgir1' is the registrable, sub-domains []
  parts  : scheme='http' host='matbetgir1.blogspot.com' subdomains=[] registrable='matbetgir1' suffix='blogspot.com' (platform) port=''
           path='' segments=[] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=1, sfx_platform_bare=0, sfx_icann2=0, n_sub=0, www=0, reg_len=2.4, reg_popular=0, reg_log_rank=6, host_len=3.18

URL: http://www.thefreedictionary.com/cladistics
  tokens : SCHEME_PREFIX:'http://' WWW:'www' DOT:'.' LABEL:'thefreedictionary' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'cladistics'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'thefreedictionary') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'cladistics')))
  rule   : no run of whole end labels of ['www', 'thefreedictionary', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='http' host='www.thefreedictionary.com' subdomains=['www'] registrable='thefreedictionary' suffix='com' (tld) port=''
           path='/cladistics' segments=['cladistics'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=2.89, reg_popular=1, reg_log_rank=3.55, host_len=3.26

URL: https://www.ingame.de/
  tokens : SCHEME_PREFIX:'https://' WWW:'www' DOT:'.' LABEL:'ingame' DOT:'.' TLD:'de' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'ingame') DOT:'.' publicSuffix>tld(TLD:'de')) path(SLASH:'/'))
  rule   : no run of whole end labels of ['www', 'ingame', 'de'] is a listed platform -> ordinary public suffix 'de' (tld)
  parts  : scheme='https' host='www.ingame.de' subdomains=['www'] registrable='ingame' suffix='de' (tld) port=''
           path='/' segments=[] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=1.95, reg_popular=0, reg_log_rank=5.2, host_len=2.64

URL: http://www.ehow.com/how_4898357_change-manual-transmission-fluid.html
  tokens : SCHEME_PREFIX:'http://' WWW:'www' DOT:'.' LABEL:'ehow' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'how_4898357_change-manual-transmission-fluid' DOT:'.' EXT:'html'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'ehow') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/' segment(segPiece(SEG_TEXT:'how_4898357_change-manual-transmission-fluid') fileExt(DOT:'.' EXT:'html'))))
  rule   : no run of whole end labels of ['www', 'ehow', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='http' host='www.ehow.com' subdomains=['www'] registrable='ehow' suffix='com' (tld) port=''
           path='/how_4898357_change-manual-transmission-fluid.html' segments=['how_4898357_change-manual-transmission-fluid.html'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=1.61, reg_popular=1, reg_log_rank=3.9, host_len=2.56

URL: http://www.nytimes.com/health/guides/symptoms/memory-loss/overview.html
  tokens : SCHEME_PREFIX:'http://' WWW:'www' DOT:'.' LABEL:'nytimes' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'health' SLASH:'/' SEG_TEXT:'guides' SLASH:'/' SEG_TEXT:'symptoms' SLASH:'/' SEG_TEXT:'memory-loss' SLASH:'/' SEG_TEXT:'overview' DOT:'.' EXT:'html'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'nytimes') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'health') SLASH:'/' segment>segPiece(SEG_TEXT:'guides') SLASH:'/' segment>se ...
  rule   : no run of whole end labels of ['www', 'nytimes', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='http' host='www.nytimes.com' subdomains=['www'] registrable='nytimes' suffix='com' (tld) port=''
           path='/health/guides/symptoms/memory-loss/overview.html' segments=['health', 'guides', 'symptoms', 'memory-loss', 'overview.html'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=2.08, reg_popular=1, reg_log_rank=2.21, host_len=2.77

URL: https://de-tailor.com/xleans/news/
  tokens : SCHEME_PREFIX:'https://' LABEL:'de-tailor' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'xleans' SLASH:'/' SEG_TEXT:'news' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(registrable>hostLabel>labelTok(LABEL:'de-tailor') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'xleans') SLASH:'/' segment>segPiece(SEG_TEXT:'news') SLASH:'/'))
  rule   : no run of whole end labels of ['de-tailor', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='https' host='de-tailor.com' subdomains=[] registrable='de-tailor' suffix='com' (tld) port=''
           path='/xleans/news/' segments=['xleans', 'news'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0, www=0, reg_len=2.3, reg_popular=0, reg_log_rank=6, host_len=2.64

URL: http://searchnetworking.techtarget.com/definition/network-interface-card
  tokens : SCHEME_PREFIX:'http://' LABEL:'searchnetworking' DOT:'.' LABEL:'techtarget' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'definition' SLASH:'/' SEG_TEXT:'network-interface-card'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(LABEL:'searchnetworking') DOT:'.' registrable>hostLabel>labelTok(LABEL:'techtarget') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'definition') SLASH:'/' segment>segPiece(SEG_TEXT:'network ...
  rule   : no run of whole end labels of ['searchnetworking', 'techtarget', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='http' host='searchnetworking.techtarget.com' subdomains=['searchnetworking'] registrable='techtarget' suffix='com' (tld) port=''
           path='/definition/network-interface-card' segments=['definition', 'network-interface-card'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=0, reg_len=2.4, reg_popular=1, reg_log_rank=3.3, host_len=3.47

URL: https://www.centurylink.com/fiber/plans-and-pricing/seattle-washington/
  tokens : SCHEME_PREFIX:'https://' WWW:'www' DOT:'.' LABEL:'centurylink' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'fiber' SLASH:'/' SEG_TEXT:'plans-and-pricing' SLASH:'/' SEG_TEXT:'seattle-washington' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'centurylink') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'fiber') SLASH:'/' segment>segPiece(SEG_TEXT:'plans-and-pricing') SLASH ...
  rule   : no run of whole end labels of ['www', 'centurylink', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='https' host='www.centurylink.com' subdomains=['www'] registrable='centurylink' suffix='com' (tld) port=''
           path='/fiber/plans-and-pricing/seattle-washington/' segments=['fiber', 'plans-and-pricing', 'seattle-washington'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=2.48, reg_popular=1, reg_log_rank=4.37, host_len=3

URL: http://odino.org/the-shortest-path-problem-in-php-demystifying-dijkstra-s-algorithm/
  tokens : SCHEME_PREFIX:'http://' LABEL:'odino' DOT:'.' SLD:'org' SLASH:'/' SEG_TEXT:'the-shortest-path-problem-in-php-demystifying-dijkstra-s-algorithm' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(registrable>hostLabel>labelTok(LABEL:'odino') DOT:'.' publicSuffix>tld(SLD:'org')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'the-shortest-path-problem-in-php-demystifying-dijkstra-s-algorithm') SLASH:'/'))
  rule   : no run of whole end labels of ['odino', 'org'] is a listed platform -> ordinary public suffix 'org' (tld)
  parts  : scheme='http' host='odino.org' subdomains=[] registrable='odino' suffix='org' (tld) port=''
           path='/the-shortest-path-problem-in-php-demystifying-dijkstra-s-algorithm/' segments=['the-shortest-path-problem-in-php-demystifying-dijkstra-s-algorithm'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0, www=0, reg_len=1.79, reg_popular=0, reg_log_rank=6, host_len=2.3

URL: https://blog.micumbre.com/
  tokens : SCHEME_PREFIX:'https://' TLD:'blog' DOT:'.' LABEL:'micumbre' DOT:'.' SLD:'com' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(subdomain>hostLabel>labelTok(TLD:'blog') DOT:'.' registrable>hostLabel>labelTok(LABEL:'micumbre') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/'))
  rule   : no run of whole end labels of ['blog', 'micumbre', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='https' host='blog.micumbre.com' subdomains=['blog'] registrable='micumbre' suffix='com' (tld) port=''
           path='/' segments=[] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=0, reg_len=2.2, reg_popular=0, reg_log_rank=6, host_len=2.89

URL: http://www.synergytas.com/
  tokens : SCHEME_PREFIX:'http://' WWW:'www' DOT:'.' LABEL:'synergytas' DOT:'.' SLD:'com' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'synergytas') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/'))
  rule   : no run of whole end labels of ['www', 'synergytas', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='http' host='www.synergytas.com' subdomains=['www'] registrable='synergytas' suffix='com' (tld) port=''
           path='/' segments=[] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=2.4, reg_popular=0, reg_log_rank=6, host_len=2.94

URL: https://en.wikipedia.org/wiki/List_of_Microsoft_software
  tokens : SCHEME_PREFIX:'https://' LABEL:'en' DOT:'.' LABEL:'wikipedia' DOT:'.' SLD:'org' SLASH:'/' SEG_TEXT:'wiki' SLASH:'/' SEG_TEXT:'List_of_Microsoft_software'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(subdomain>hostLabel>labelTok(LABEL:'en') DOT:'.' registrable>hostLabel>labelTok(LABEL:'wikipedia') DOT:'.' publicSuffix>tld(SLD:'org')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'wiki') SLASH:'/' segment>segPiece(SEG_TEXT:'List_of_Microsoft_software' ...
  rule   : no run of whole end labels of ['en', 'wikipedia', 'org'] is a listed platform -> ordinary public suffix 'org' (tld)
  parts  : scheme='https' host='en.wikipedia.org' subdomains=['en'] registrable='wikipedia' suffix='org' (tld) port=''
           path='/wiki/List_of_Microsoft_software' segments=['wiki', 'List_of_Microsoft_software'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=0, reg_len=2.3, reg_popular=1, reg_log_rank=1.58, host_len=2.83

URL: http://www.healthrid.org/
  tokens : SCHEME_PREFIX:'http://' WWW:'www' DOT:'.' LABEL:'healthrid' DOT:'.' SLD:'org' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'healthrid') DOT:'.' publicSuffix>tld(SLD:'org')) path(SLASH:'/'))
  rule   : no run of whole end labels of ['www', 'healthrid', 'org'] is a listed platform -> ordinary public suffix 'org' (tld)
  parts  : scheme='http' host='www.healthrid.org' subdomains=['www'] registrable='healthrid' suffix='org' (tld) port=''
           path='/' segments=[] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=2.3, reg_popular=0, reg_log_rank=6, host_len=2.89

URL: https://www.travelchinaguide.com/intro/focus/calendar.htm
  tokens : SCHEME_PREFIX:'https://' WWW:'www' DOT:'.' LABEL:'travelchinaguide' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'intro' SLASH:'/' SEG_TEXT:'focus' SLASH:'/' SEG_TEXT:'calendar' DOT:'.' EXT:'htm'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'travelchinaguide') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'intro') SLASH:'/' segment>segPiece(SEG_TEXT:'focus') SLASH:'/' se ...
  rule   : no run of whole end labels of ['www', 'travelchinaguide', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='https' host='www.travelchinaguide.com' subdomains=['www'] registrable='travelchinaguide' suffix='com' (tld) port=''
           path='/intro/focus/calendar.htm' segments=['intro', 'focus', 'calendar.htm'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=2.83, reg_popular=1, reg_log_rank=4.57, host_len=3.22

URL: http://www.textsfromlastnight.com/
  tokens : SCHEME_PREFIX:'http://' WWW:'www' DOT:'.' LABEL:'textsfromlastnight' DOT:'.' SLD:'com' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'textsfromlastnight') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/'))
  rule   : no run of whole end labels of ['www', 'textsfromlastnight', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='http' host='www.textsfromlastnight.com' subdomains=['www'] registrable='textsfromlastnight' suffix='com' (tld) port=''
           path='/' segments=[] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=2.94, reg_popular=0, reg_log_rank=6, host_len=3.3

URL: http://107.180.44.78/login.php?cmd=login_submit&id=9935941aa736b1f240b52ffbec44d57e9935941aa736b1f240b52ffbec44d57e&session=9935941aa736b1f240b52ffbec44d57e9935941aa736b1f240b52ffbec44d57e
  tokens : SCHEME_PREFIX:'http://' DIGITS:'107' DOT:'.' DIGITS:'180' DOT:'.' DIGITS:'44' DOT:'.' DIGITS:'78' SLASH:'/' SEG_TEXT:'login' DOT:'.' EXT:'php' QMARK:'?' QUERY_TEXT:'cmd' EQ:'=' QUERY_TEXT:'login_submit' AMP:'&' QUERY_TEXT:'id' EQ:'=' QUERY_TEXT:'9935941aa736b1f240b52ffbec44d57e9935941aa736b1f240b52ffbec44d57e' AMP:'&' QUERY_TEXT:'session' EQ:'=' QUERY_TEXT:'9935941aa736b1f240b52ffbec44d57e9935941aa736b1f240b52ffbec44d57e'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>ipv4(DIGITS:'107' DOT:'.' DIGITS:'180' DOT:'.' DIGITS:'44' DOT:'.' DIGITS:'78') path(SLASH:'/' segment(segPiece(SEG_TEXT:'login') fileExt(DOT:'.' EXT:'php'))) query(QMARK:'?' pair(key>qPiece(QUERY_TEXT:'cmd') EQ:'=' value>qPiece(QUERY_TEXT:'login_submit'))  ...
  rule   : host kind ipv4: no platform lookup
  parts  : scheme='http' host='107.180.44.78' subdomains=[] registrable='' suffix='' () port=''
           path='/login.php' segments=['login.php'] query keys=['cmd', 'id', 'session'] values=['login_submit', '9935941aa736b1f240b52ffbec44d57e9935941aa736b1f240b52ffbec44d57e', '9935941aa736b1f240b52ffbec44d57e9935941aa736b1f240b52ffbec44d57e'] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0, www=0, reg_len=0, reg_popular=0, reg_log_rank=6, host_len=2.64

URL: http://wtvpc.com/streaming-tv/discovery-family-kids-tv-streams/
  tokens : SCHEME_PREFIX:'http://' LABEL:'wtvpc' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'streaming-tv' SLASH:'/' SEG_TEXT:'discovery-family-kids-tv-streams' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(registrable>hostLabel>labelTok(LABEL:'wtvpc') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'streaming-tv') SLASH:'/' segment>segPiece(SEG_TEXT:'discovery-family-kids-tv-streams') SLASH:'/'))
  rule   : no run of whole end labels of ['wtvpc', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='http' host='wtvpc.com' subdomains=[] registrable='wtvpc' suffix='com' (tld) port=''
           path='/streaming-tv/discovery-family-kids-tv-streams/' segments=['streaming-tv', 'discovery-family-kids-tv-streams'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0, www=0, reg_len=1.79, reg_popular=0, reg_log_rank=6, host_len=2.3

URL: https://fr.imsly.com/direct/aHR0cHM6Ly93d3cuZmFjZWJvb2suY29tL2ltcHJlc3Npb24ucGhwL2YzNmZhYzcyMTM5Y2Y2NC8_bGlkPTExNSZwYXlsb2FkPSU3QiUyMnNvdXJjZSUyMiUzQSUyMmpzc2RrJTIyJTdE
  tokens : SCHEME_PREFIX:'https://' TLD:'fr' DOT:'.' LABEL:'imsly' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'direct' SLASH:'/' SEG_TEXT:'aHR0cHM6Ly93d3cuZmFjZWJvb2suY29tL2ltcHJlc3Npb24ucGhwL2YzNmZhYzcyMTM5Y2Y2NC8_bGlkPTExNSZwYXlsb2FkPSU3QiUyMnNvdXJjZSUyMiUzQSUyMmpzc2RrJTIyJTdE'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(subdomain>hostLabel>labelTok(TLD:'fr') DOT:'.' registrable>hostLabel>labelTok(LABEL:'imsly') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'direct') SLASH:'/' segment>segPiece(SEG_TEXT:'aHR0cHM6Ly93d3cuZmFjZWJvb2suY29 ...
  rule   : no run of whole end labels of ['fr', 'imsly', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='https' host='fr.imsly.com' subdomains=['fr'] registrable='imsly' suffix='com' (tld) port=''
           path='/direct/aHR0cHM6Ly93d3cuZmFjZWJvb2suY29tL2ltcHJlc3Npb24ucGhwL2YzNmZhYzcyMTM5Y2Y2NC8_bGlkPTExNSZwYXlsb2FkPSU3QiUyMnNvdXJjZSUyMiUzQSUyMmpzc2RrJTIyJTdE' segments=['direct', 'aHR0cHM6Ly93d3cuZmFjZWJvb2suY29tL2ltcHJlc3Npb24ucGhwL2YzNmZhYzcyMTM5Y2Y2NC8_bGlkPTExNSZwYXlsb2FkPSU3QiUyMnNvdXJjZSUyMiUzQSUyMmpzc2RrJTIyJTdE'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=0, reg_len=1.79, reg_popular=0, reg_log_rank=6, host_len=2.56

URL: https://www.moneyou.at/
  tokens : SCHEME_PREFIX:'https://' WWW:'www' DOT:'.' LABEL:'moneyou' DOT:'.' TLD:'at' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'https://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'moneyou') DOT:'.' publicSuffix>tld(TLD:'at')) path(SLASH:'/'))
  rule   : no run of whole end labels of ['www', 'moneyou', 'at'] is a listed platform -> ordinary public suffix 'at' (tld)
  parts  : scheme='https' host='www.moneyou.at' subdomains=['www'] registrable='moneyou' suffix='at' (tld) port=''
           path='/' segments=[] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=2.08, reg_popular=0, reg_log_rank=6, host_len=2.71

URL: http://www.slideserve.com/zizi/firewalls
  tokens : SCHEME_PREFIX:'http://' WWW:'www' DOT:'.' LABEL:'slideserve' DOT:'.' SLD:'com' SLASH:'/' SEG_TEXT:'zizi' SLASH:'/' SEG_TEXT:'firewalls'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'slideserve') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/' segment>segPiece(SEG_TEXT:'zizi') SLASH:'/' segment>segPiece(SEG_TEXT:'firewalls')))
  rule   : no run of whole end labels of ['www', 'slideserve', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='http' host='www.slideserve.com' subdomains=['www'] registrable='slideserve' suffix='com' (tld) port=''
           path='/zizi/firewalls' segments=['zizi', 'firewalls'] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=2.4, reg_popular=1, reg_log_rank=4.12, host_len=2.94

URL: http://www.pocketlegends.com/
  tokens : SCHEME_PREFIX:'http://' WWW:'www' DOT:'.' LABEL:'pocketlegends' DOT:'.' SLD:'com' SLASH:'/'
  parse  : url(SCHEME_PREFIX:'http://' authority>host>domain(subdomain>hostLabel>labelTok(WWW:'www') DOT:'.' registrable>hostLabel>labelTok(LABEL:'pocketlegends') DOT:'.' publicSuffix>tld(SLD:'com')) path(SLASH:'/'))
  rule   : no run of whole end labels of ['www', 'pocketlegends', 'com'] is a listed platform -> ordinary public suffix 'com' (tld)
  parts  : scheme='http' host='www.pocketlegends.com' subdomains=['www'] registrable='pocketlegends' suffix='com' (tld) port=''
           path='/' segments=[] query keys=[] values=[] fragment=''
  host features: host_platform=0, sfx_platform=0, sfx_platform_bare=0, sfx_icann2=0, n_sub=0.693, www=1, reg_len=2.64, reg_popular=0, reg_log_rank=6, host_len=3.09
```
