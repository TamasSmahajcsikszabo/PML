# Generated from UrlParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,26,214,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,1,0,3,0,54,
        8,0,1,0,1,0,3,0,58,8,0,1,0,3,0,61,8,0,1,0,3,0,64,8,0,1,0,1,0,1,1,
        1,1,1,1,3,1,71,8,1,1,1,1,1,1,1,3,1,76,8,1,3,1,78,8,1,1,2,1,2,5,2,
        82,8,2,10,2,12,2,85,9,2,1,3,1,3,1,4,1,4,1,4,1,4,3,4,93,8,4,1,5,1,
        5,1,5,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,5,6,106,8,6,10,6,12,6,109,
        9,6,1,6,1,6,1,6,1,6,3,6,115,8,6,1,7,1,7,1,8,1,8,1,9,1,9,1,9,1,9,
        1,9,3,9,126,8,9,1,10,1,10,1,11,1,11,3,11,132,8,11,1,12,1,12,1,12,
        5,12,137,8,12,10,12,12,12,140,9,12,1,12,3,12,143,8,12,1,13,4,13,
        146,8,13,11,13,12,13,147,1,14,1,14,1,15,1,15,1,15,3,15,155,8,15,
        1,16,1,16,3,16,159,8,16,4,16,161,8,16,11,16,12,16,162,1,17,4,17,
        166,8,17,11,17,12,17,167,1,17,3,17,171,8,17,1,18,1,18,1,18,1,19,
        1,19,1,20,1,20,1,20,1,20,5,20,182,8,20,10,20,12,20,185,9,20,1,21,
        1,21,1,21,3,21,190,8,21,1,22,5,22,193,8,22,10,22,12,22,196,9,22,
        1,23,1,23,5,23,200,8,23,10,23,12,23,203,9,23,1,24,1,24,1,25,1,25,
        5,25,209,8,25,10,25,12,25,212,9,25,1,25,2,107,167,0,26,0,2,4,6,8,
        10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,0,
        6,1,0,2,3,3,0,1,8,12,12,16,16,4,0,9,9,12,12,17,19,25,25,1,0,20,21,
        3,0,12,12,19,19,23,25,3,0,12,12,19,19,25,26,219,0,53,1,0,0,0,2,70,
        1,0,0,0,4,83,1,0,0,0,6,86,1,0,0,0,8,92,1,0,0,0,10,94,1,0,0,0,12,
        107,1,0,0,0,14,116,1,0,0,0,16,118,1,0,0,0,18,125,1,0,0,0,20,127,
        1,0,0,0,22,129,1,0,0,0,24,133,1,0,0,0,26,145,1,0,0,0,28,149,1,0,
        0,0,30,154,1,0,0,0,32,160,1,0,0,0,34,165,1,0,0,0,36,172,1,0,0,0,
        38,175,1,0,0,0,40,177,1,0,0,0,42,186,1,0,0,0,44,194,1,0,0,0,46,201,
        1,0,0,0,48,204,1,0,0,0,50,206,1,0,0,0,52,54,5,1,0,0,53,52,1,0,0,
        0,53,54,1,0,0,0,54,55,1,0,0,0,55,57,3,2,1,0,56,58,3,32,16,0,57,56,
        1,0,0,0,57,58,1,0,0,0,58,60,1,0,0,0,59,61,3,40,20,0,60,59,1,0,0,
        0,60,61,1,0,0,0,61,63,1,0,0,0,62,64,3,50,25,0,63,62,1,0,0,0,63,64,
        1,0,0,0,64,65,1,0,0,0,65,66,5,0,0,1,66,1,1,0,0,0,67,68,3,4,2,0,68,
        69,5,11,0,0,69,71,1,0,0,0,70,67,1,0,0,0,70,71,1,0,0,0,71,72,1,0,
        0,0,72,77,3,8,4,0,73,75,5,10,0,0,74,76,3,6,3,0,75,74,1,0,0,0,75,
        76,1,0,0,0,76,78,1,0,0,0,77,73,1,0,0,0,77,78,1,0,0,0,78,3,1,0,0,
        0,79,82,3,30,15,0,80,82,5,11,0,0,81,79,1,0,0,0,81,80,1,0,0,0,82,
        85,1,0,0,0,83,81,1,0,0,0,83,84,1,0,0,0,84,5,1,0,0,0,85,83,1,0,0,
        0,86,87,5,7,0,0,87,7,1,0,0,0,88,93,3,10,5,0,89,93,3,12,6,0,90,93,
        3,22,11,0,91,93,3,24,12,0,92,88,1,0,0,0,92,89,1,0,0,0,92,90,1,0,
        0,0,92,91,1,0,0,0,93,9,1,0,0,0,94,95,5,7,0,0,95,96,5,9,0,0,96,97,
        5,7,0,0,97,98,5,9,0,0,98,99,5,7,0,0,99,100,5,9,0,0,100,101,5,7,0,
        0,101,11,1,0,0,0,102,103,3,14,7,0,103,104,5,9,0,0,104,106,1,0,0,
        0,105,102,1,0,0,0,106,109,1,0,0,0,107,108,1,0,0,0,107,105,1,0,0,
        0,108,110,1,0,0,0,109,107,1,0,0,0,110,111,3,16,8,0,111,112,5,9,0,
        0,112,114,3,18,9,0,113,115,5,9,0,0,114,113,1,0,0,0,114,115,1,0,0,
        0,115,13,1,0,0,0,116,117,3,26,13,0,117,15,1,0,0,0,118,119,3,26,13,
        0,119,17,1,0,0,0,120,126,5,4,0,0,121,122,5,2,0,0,122,123,5,9,0,0,
        123,126,3,20,10,0,124,126,3,20,10,0,125,120,1,0,0,0,125,121,1,0,
        0,0,125,124,1,0,0,0,126,19,1,0,0,0,127,128,7,0,0,0,128,21,1,0,0,
        0,129,131,5,4,0,0,130,132,5,9,0,0,131,130,1,0,0,0,131,132,1,0,0,
        0,132,23,1,0,0,0,133,138,3,26,13,0,134,135,5,9,0,0,135,137,3,26,
        13,0,136,134,1,0,0,0,137,140,1,0,0,0,138,136,1,0,0,0,138,139,1,0,
        0,0,139,142,1,0,0,0,140,138,1,0,0,0,141,143,5,9,0,0,142,141,1,0,
        0,0,142,143,1,0,0,0,143,25,1,0,0,0,144,146,3,28,14,0,145,144,1,0,
        0,0,146,147,1,0,0,0,147,145,1,0,0,0,147,148,1,0,0,0,148,27,1,0,0,
        0,149,150,7,1,0,0,150,29,1,0,0,0,151,155,3,28,14,0,152,155,5,9,0,
        0,153,155,5,10,0,0,154,151,1,0,0,0,154,152,1,0,0,0,154,153,1,0,0,
        0,155,31,1,0,0,0,156,158,5,13,0,0,157,159,3,34,17,0,158,157,1,0,
        0,0,158,159,1,0,0,0,159,161,1,0,0,0,160,156,1,0,0,0,161,162,1,0,
        0,0,162,160,1,0,0,0,162,163,1,0,0,0,163,33,1,0,0,0,164,166,3,38,
        19,0,165,164,1,0,0,0,166,167,1,0,0,0,167,168,1,0,0,0,167,165,1,0,
        0,0,168,170,1,0,0,0,169,171,3,36,18,0,170,169,1,0,0,0,170,171,1,
        0,0,0,171,35,1,0,0,0,172,173,5,9,0,0,173,174,5,17,0,0,174,37,1,0,
        0,0,175,176,7,2,0,0,176,39,1,0,0,0,177,178,5,14,0,0,178,183,3,42,
        21,0,179,180,7,3,0,0,180,182,3,42,21,0,181,179,1,0,0,0,182,185,1,
        0,0,0,183,181,1,0,0,0,183,184,1,0,0,0,184,41,1,0,0,0,185,183,1,0,
        0,0,186,189,3,44,22,0,187,188,5,22,0,0,188,190,3,46,23,0,189,187,
        1,0,0,0,189,190,1,0,0,0,190,43,1,0,0,0,191,193,3,48,24,0,192,191,
        1,0,0,0,193,196,1,0,0,0,194,192,1,0,0,0,194,195,1,0,0,0,195,45,1,
        0,0,0,196,194,1,0,0,0,197,200,3,48,24,0,198,200,5,22,0,0,199,197,
        1,0,0,0,199,198,1,0,0,0,200,203,1,0,0,0,201,199,1,0,0,0,201,202,
        1,0,0,0,202,47,1,0,0,0,203,201,1,0,0,0,204,205,7,4,0,0,205,49,1,
        0,0,0,206,210,5,15,0,0,207,209,7,5,0,0,208,207,1,0,0,0,209,212,1,
        0,0,0,210,208,1,0,0,0,210,211,1,0,0,0,211,51,1,0,0,0,212,210,1,0,
        0,0,28,53,57,60,63,70,75,77,81,83,92,107,114,125,131,138,142,147,
        154,158,162,167,170,183,189,194,199,201,210
    ]

class UrlParser ( Parser ):

    grammarFileName = "UrlParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'www'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "':'", "'@'", "<INVALID>", "<INVALID>", 
                     "'?'", "'#'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'&amp;'", "'&'", "'='" ]

    symbolicNames = [ "<INVALID>", "SCHEME_PREFIX", "SLD", "TLD", "PLATFORM", 
                      "WWW", "PUNYCODE", "DIGITS", "LABEL", "DOT", "COLON", 
                      "AT", "PCT", "SLASH", "QMARK", "HASH", "AUTH_OTHER", 
                      "EXT", "SEG_TEXT", "STRAY_PCT", "AMP_ESC", "AMP", 
                      "EQ", "NESTED_URL", "QUERY_TEXT", "EMAIL", "FRAG_TEXT" ]

    RULE_url = 0
    RULE_authority = 1
    RULE_userinfo = 2
    RULE_port = 3
    RULE_host = 4
    RULE_ipv4 = 5
    RULE_domain = 6
    RULE_subdomain = 7
    RULE_registrable = 8
    RULE_publicSuffix = 9
    RULE_tld = 10
    RULE_platformHost = 11
    RULE_otherHost = 12
    RULE_hostLabel = 13
    RULE_labelTok = 14
    RULE_authTok = 15
    RULE_path = 16
    RULE_segment = 17
    RULE_fileExt = 18
    RULE_segPiece = 19
    RULE_query = 20
    RULE_pair = 21
    RULE_key = 22
    RULE_value = 23
    RULE_qPiece = 24
    RULE_fragmentPart = 25

    ruleNames =  [ "url", "authority", "userinfo", "port", "host", "ipv4", 
                   "domain", "subdomain", "registrable", "publicSuffix", 
                   "tld", "platformHost", "otherHost", "hostLabel", "labelTok", 
                   "authTok", "path", "segment", "fileExt", "segPiece", 
                   "query", "pair", "key", "value", "qPiece", "fragmentPart" ]

    EOF = Token.EOF
    SCHEME_PREFIX=1
    SLD=2
    TLD=3
    PLATFORM=4
    WWW=5
    PUNYCODE=6
    DIGITS=7
    LABEL=8
    DOT=9
    COLON=10
    AT=11
    PCT=12
    SLASH=13
    QMARK=14
    HASH=15
    AUTH_OTHER=16
    EXT=17
    SEG_TEXT=18
    STRAY_PCT=19
    AMP_ESC=20
    AMP=21
    EQ=22
    NESTED_URL=23
    QUERY_TEXT=24
    EMAIL=25
    FRAG_TEXT=26

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class UrlContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def authority(self):
            return self.getTypedRuleContext(UrlParser.AuthorityContext,0)


        def EOF(self):
            return self.getToken(UrlParser.EOF, 0)

        def SCHEME_PREFIX(self):
            return self.getToken(UrlParser.SCHEME_PREFIX, 0)

        def path(self):
            return self.getTypedRuleContext(UrlParser.PathContext,0)


        def query(self):
            return self.getTypedRuleContext(UrlParser.QueryContext,0)


        def fragmentPart(self):
            return self.getTypedRuleContext(UrlParser.FragmentPartContext,0)


        def getRuleIndex(self):
            return UrlParser.RULE_url

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUrl" ):
                listener.enterUrl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUrl" ):
                listener.exitUrl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUrl" ):
                return visitor.visitUrl(self)
            else:
                return visitor.visitChildren(self)




    def url(self):

        localctx = UrlParser.UrlContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_url)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 52
                self.match(UrlParser.SCHEME_PREFIX)


            self.state = 55
            self.authority()
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 56
                self.path()


            self.state = 60
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 59
                self.query()


            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==15:
                self.state = 62
                self.fragmentPart()


            self.state = 65
            self.match(UrlParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AuthorityContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def host(self):
            return self.getTypedRuleContext(UrlParser.HostContext,0)


        def userinfo(self):
            return self.getTypedRuleContext(UrlParser.UserinfoContext,0)


        def AT(self):
            return self.getToken(UrlParser.AT, 0)

        def COLON(self):
            return self.getToken(UrlParser.COLON, 0)

        def port(self):
            return self.getTypedRuleContext(UrlParser.PortContext,0)


        def getRuleIndex(self):
            return UrlParser.RULE_authority

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAuthority" ):
                listener.enterAuthority(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAuthority" ):
                listener.exitAuthority(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAuthority" ):
                return visitor.visitAuthority(self)
            else:
                return visitor.visitChildren(self)




    def authority(self):

        localctx = UrlParser.AuthorityContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_authority)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.state = 67
                self.userinfo()
                self.state = 68
                self.match(UrlParser.AT)


            self.state = 72
            self.host()
            self.state = 77
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==10:
                self.state = 73
                self.match(UrlParser.COLON)
                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 74
                    self.port()




        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UserinfoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def authTok(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UrlParser.AuthTokContext)
            else:
                return self.getTypedRuleContext(UrlParser.AuthTokContext,i)


        def AT(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.AT)
            else:
                return self.getToken(UrlParser.AT, i)

        def getRuleIndex(self):
            return UrlParser.RULE_userinfo

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUserinfo" ):
                listener.enterUserinfo(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUserinfo" ):
                listener.exitUserinfo(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUserinfo" ):
                return visitor.visitUserinfo(self)
            else:
                return visitor.visitChildren(self)




    def userinfo(self):

        localctx = UrlParser.UserinfoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_userinfo)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 81
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16]:
                        self.state = 79
                        self.authTok()
                        pass
                    elif token in [11]:
                        self.state = 80
                        self.match(UrlParser.AT)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 85
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PortContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DIGITS(self):
            return self.getToken(UrlParser.DIGITS, 0)

        def getRuleIndex(self):
            return UrlParser.RULE_port

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPort" ):
                listener.enterPort(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPort" ):
                listener.exitPort(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPort" ):
                return visitor.visitPort(self)
            else:
                return visitor.visitChildren(self)




    def port(self):

        localctx = UrlParser.PortContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_port)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(UrlParser.DIGITS)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HostContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ipv4(self):
            return self.getTypedRuleContext(UrlParser.Ipv4Context,0)


        def domain(self):
            return self.getTypedRuleContext(UrlParser.DomainContext,0)


        def platformHost(self):
            return self.getTypedRuleContext(UrlParser.PlatformHostContext,0)


        def otherHost(self):
            return self.getTypedRuleContext(UrlParser.OtherHostContext,0)


        def getRuleIndex(self):
            return UrlParser.RULE_host

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHost" ):
                listener.enterHost(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHost" ):
                listener.exitHost(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHost" ):
                return visitor.visitHost(self)
            else:
                return visitor.visitChildren(self)




    def host(self):

        localctx = UrlParser.HostContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_host)
        try:
            self.state = 92
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 88
                self.ipv4()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 89
                self.domain()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 90
                self.platformHost()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 91
                self.otherHost()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Ipv4Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DIGITS(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.DIGITS)
            else:
                return self.getToken(UrlParser.DIGITS, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.DOT)
            else:
                return self.getToken(UrlParser.DOT, i)

        def getRuleIndex(self):
            return UrlParser.RULE_ipv4

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIpv4" ):
                listener.enterIpv4(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIpv4" ):
                listener.exitIpv4(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIpv4" ):
                return visitor.visitIpv4(self)
            else:
                return visitor.visitChildren(self)




    def ipv4(self):

        localctx = UrlParser.Ipv4Context(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_ipv4)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.match(UrlParser.DIGITS)
            self.state = 95
            self.match(UrlParser.DOT)
            self.state = 96
            self.match(UrlParser.DIGITS)
            self.state = 97
            self.match(UrlParser.DOT)
            self.state = 98
            self.match(UrlParser.DIGITS)
            self.state = 99
            self.match(UrlParser.DOT)
            self.state = 100
            self.match(UrlParser.DIGITS)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DomainContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def registrable(self):
            return self.getTypedRuleContext(UrlParser.RegistrableContext,0)


        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.DOT)
            else:
                return self.getToken(UrlParser.DOT, i)

        def publicSuffix(self):
            return self.getTypedRuleContext(UrlParser.PublicSuffixContext,0)


        def subdomain(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UrlParser.SubdomainContext)
            else:
                return self.getTypedRuleContext(UrlParser.SubdomainContext,i)


        def getRuleIndex(self):
            return UrlParser.RULE_domain

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDomain" ):
                listener.enterDomain(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDomain" ):
                listener.exitDomain(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDomain" ):
                return visitor.visitDomain(self)
            else:
                return visitor.visitChildren(self)




    def domain(self):

        localctx = UrlParser.DomainContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_domain)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1+1:
                    self.state = 102
                    self.subdomain()
                    self.state = 103
                    self.match(UrlParser.DOT) 
                self.state = 109
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

            self.state = 110
            self.registrable()
            self.state = 111
            self.match(UrlParser.DOT)
            self.state = 112
            self.publicSuffix()
            self.state = 114
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 113
                self.match(UrlParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubdomainContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def hostLabel(self):
            return self.getTypedRuleContext(UrlParser.HostLabelContext,0)


        def getRuleIndex(self):
            return UrlParser.RULE_subdomain

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubdomain" ):
                listener.enterSubdomain(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubdomain" ):
                listener.exitSubdomain(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubdomain" ):
                return visitor.visitSubdomain(self)
            else:
                return visitor.visitChildren(self)




    def subdomain(self):

        localctx = UrlParser.SubdomainContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_subdomain)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.hostLabel()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RegistrableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def hostLabel(self):
            return self.getTypedRuleContext(UrlParser.HostLabelContext,0)


        def getRuleIndex(self):
            return UrlParser.RULE_registrable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRegistrable" ):
                listener.enterRegistrable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRegistrable" ):
                listener.exitRegistrable(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRegistrable" ):
                return visitor.visitRegistrable(self)
            else:
                return visitor.visitChildren(self)




    def registrable(self):

        localctx = UrlParser.RegistrableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_registrable)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.hostLabel()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PublicSuffixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLATFORM(self):
            return self.getToken(UrlParser.PLATFORM, 0)

        def SLD(self):
            return self.getToken(UrlParser.SLD, 0)

        def DOT(self):
            return self.getToken(UrlParser.DOT, 0)

        def tld(self):
            return self.getTypedRuleContext(UrlParser.TldContext,0)


        def getRuleIndex(self):
            return UrlParser.RULE_publicSuffix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPublicSuffix" ):
                listener.enterPublicSuffix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPublicSuffix" ):
                listener.exitPublicSuffix(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPublicSuffix" ):
                return visitor.visitPublicSuffix(self)
            else:
                return visitor.visitChildren(self)




    def publicSuffix(self):

        localctx = UrlParser.PublicSuffixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_publicSuffix)
        try:
            self.state = 125
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 120
                self.match(UrlParser.PLATFORM)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 121
                self.match(UrlParser.SLD)
                self.state = 122
                self.match(UrlParser.DOT)
                self.state = 123
                self.tld()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 124
                self.tld()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TLD(self):
            return self.getToken(UrlParser.TLD, 0)

        def SLD(self):
            return self.getToken(UrlParser.SLD, 0)

        def getRuleIndex(self):
            return UrlParser.RULE_tld

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTld" ):
                listener.enterTld(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTld" ):
                listener.exitTld(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTld" ):
                return visitor.visitTld(self)
            else:
                return visitor.visitChildren(self)




    def tld(self):

        localctx = UrlParser.TldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_tld)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            _la = self._input.LA(1)
            if not(_la==2 or _la==3):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PlatformHostContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLATFORM(self):
            return self.getToken(UrlParser.PLATFORM, 0)

        def DOT(self):
            return self.getToken(UrlParser.DOT, 0)

        def getRuleIndex(self):
            return UrlParser.RULE_platformHost

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPlatformHost" ):
                listener.enterPlatformHost(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPlatformHost" ):
                listener.exitPlatformHost(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPlatformHost" ):
                return visitor.visitPlatformHost(self)
            else:
                return visitor.visitChildren(self)




    def platformHost(self):

        localctx = UrlParser.PlatformHostContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_platformHost)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
            self.match(UrlParser.PLATFORM)
            self.state = 131
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 130
                self.match(UrlParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OtherHostContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def hostLabel(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UrlParser.HostLabelContext)
            else:
                return self.getTypedRuleContext(UrlParser.HostLabelContext,i)


        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.DOT)
            else:
                return self.getToken(UrlParser.DOT, i)

        def getRuleIndex(self):
            return UrlParser.RULE_otherHost

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOtherHost" ):
                listener.enterOtherHost(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOtherHost" ):
                listener.exitOtherHost(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOtherHost" ):
                return visitor.visitOtherHost(self)
            else:
                return visitor.visitChildren(self)




    def otherHost(self):

        localctx = UrlParser.OtherHostContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_otherHost)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 133
            self.hostLabel()
            self.state = 138
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 134
                    self.match(UrlParser.DOT)
                    self.state = 135
                    self.hostLabel() 
                self.state = 140
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

            self.state = 142
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 141
                self.match(UrlParser.DOT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HostLabelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def labelTok(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UrlParser.LabelTokContext)
            else:
                return self.getTypedRuleContext(UrlParser.LabelTokContext,i)


        def getRuleIndex(self):
            return UrlParser.RULE_hostLabel

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHostLabel" ):
                listener.enterHostLabel(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHostLabel" ):
                listener.exitHostLabel(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHostLabel" ):
                return visitor.visitHostLabel(self)
            else:
                return visitor.visitChildren(self)




    def hostLabel(self):

        localctx = UrlParser.HostLabelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_hostLabel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 145 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 144
                self.labelTok()
                self.state = 147 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 70142) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LabelTokContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SCHEME_PREFIX(self):
            return self.getToken(UrlParser.SCHEME_PREFIX, 0)

        def LABEL(self):
            return self.getToken(UrlParser.LABEL, 0)

        def DIGITS(self):
            return self.getToken(UrlParser.DIGITS, 0)

        def WWW(self):
            return self.getToken(UrlParser.WWW, 0)

        def PUNYCODE(self):
            return self.getToken(UrlParser.PUNYCODE, 0)

        def TLD(self):
            return self.getToken(UrlParser.TLD, 0)

        def SLD(self):
            return self.getToken(UrlParser.SLD, 0)

        def PLATFORM(self):
            return self.getToken(UrlParser.PLATFORM, 0)

        def PCT(self):
            return self.getToken(UrlParser.PCT, 0)

        def AUTH_OTHER(self):
            return self.getToken(UrlParser.AUTH_OTHER, 0)

        def getRuleIndex(self):
            return UrlParser.RULE_labelTok

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLabelTok" ):
                listener.enterLabelTok(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLabelTok" ):
                listener.exitLabelTok(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLabelTok" ):
                return visitor.visitLabelTok(self)
            else:
                return visitor.visitChildren(self)




    def labelTok(self):

        localctx = UrlParser.LabelTokContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_labelTok)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 149
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 70142) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AuthTokContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def labelTok(self):
            return self.getTypedRuleContext(UrlParser.LabelTokContext,0)


        def DOT(self):
            return self.getToken(UrlParser.DOT, 0)

        def COLON(self):
            return self.getToken(UrlParser.COLON, 0)

        def getRuleIndex(self):
            return UrlParser.RULE_authTok

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAuthTok" ):
                listener.enterAuthTok(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAuthTok" ):
                listener.exitAuthTok(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAuthTok" ):
                return visitor.visitAuthTok(self)
            else:
                return visitor.visitChildren(self)




    def authTok(self):

        localctx = UrlParser.AuthTokContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_authTok)
        try:
            self.state = 154
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 5, 6, 7, 8, 12, 16]:
                self.enterOuterAlt(localctx, 1)
                self.state = 151
                self.labelTok()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 2)
                self.state = 152
                self.match(UrlParser.DOT)
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 3)
                self.state = 153
                self.match(UrlParser.COLON)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.SLASH)
            else:
                return self.getToken(UrlParser.SLASH, i)

        def segment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UrlParser.SegmentContext)
            else:
                return self.getTypedRuleContext(UrlParser.SegmentContext,i)


        def getRuleIndex(self):
            return UrlParser.RULE_path

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPath" ):
                listener.enterPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPath" ):
                listener.exitPath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPath" ):
                return visitor.visitPath(self)
            else:
                return visitor.visitChildren(self)




    def path(self):

        localctx = UrlParser.PathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_path)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 160 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 156
                self.match(UrlParser.SLASH)
                self.state = 158
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 34476544) != 0):
                    self.state = 157
                    self.segment()


                self.state = 162 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==13):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SegmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def segPiece(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UrlParser.SegPieceContext)
            else:
                return self.getTypedRuleContext(UrlParser.SegPieceContext,i)


        def fileExt(self):
            return self.getTypedRuleContext(UrlParser.FileExtContext,0)


        def getRuleIndex(self):
            return UrlParser.RULE_segment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSegment" ):
                listener.enterSegment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSegment" ):
                listener.exitSegment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSegment" ):
                return visitor.visitSegment(self)
            else:
                return visitor.visitChildren(self)




    def segment(self):

        localctx = UrlParser.SegmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_segment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 165 
            self._errHandler.sync(self)
            _alt = 1+1
            while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1+1:
                    self.state = 164
                    self.segPiece()

                else:
                    raise NoViableAltException(self)
                self.state = 167 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,20,self._ctx)

            self.state = 170
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 169
                self.fileExt()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FileExtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOT(self):
            return self.getToken(UrlParser.DOT, 0)

        def EXT(self):
            return self.getToken(UrlParser.EXT, 0)

        def getRuleIndex(self):
            return UrlParser.RULE_fileExt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFileExt" ):
                listener.enterFileExt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFileExt" ):
                listener.exitFileExt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFileExt" ):
                return visitor.visitFileExt(self)
            else:
                return visitor.visitChildren(self)




    def fileExt(self):

        localctx = UrlParser.FileExtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_fileExt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 172
            self.match(UrlParser.DOT)
            self.state = 173
            self.match(UrlParser.EXT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SegPieceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEG_TEXT(self):
            return self.getToken(UrlParser.SEG_TEXT, 0)

        def PCT(self):
            return self.getToken(UrlParser.PCT, 0)

        def STRAY_PCT(self):
            return self.getToken(UrlParser.STRAY_PCT, 0)

        def DOT(self):
            return self.getToken(UrlParser.DOT, 0)

        def EXT(self):
            return self.getToken(UrlParser.EXT, 0)

        def EMAIL(self):
            return self.getToken(UrlParser.EMAIL, 0)

        def getRuleIndex(self):
            return UrlParser.RULE_segPiece

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSegPiece" ):
                listener.enterSegPiece(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSegPiece" ):
                listener.exitSegPiece(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSegPiece" ):
                return visitor.visitSegPiece(self)
            else:
                return visitor.visitChildren(self)




    def segPiece(self):

        localctx = UrlParser.SegPieceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_segPiece)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 34476544) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QueryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QMARK(self):
            return self.getToken(UrlParser.QMARK, 0)

        def pair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UrlParser.PairContext)
            else:
                return self.getTypedRuleContext(UrlParser.PairContext,i)


        def AMP(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.AMP)
            else:
                return self.getToken(UrlParser.AMP, i)

        def AMP_ESC(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.AMP_ESC)
            else:
                return self.getToken(UrlParser.AMP_ESC, i)

        def getRuleIndex(self):
            return UrlParser.RULE_query

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery" ):
                listener.enterQuery(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery" ):
                listener.exitQuery(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuery" ):
                return visitor.visitQuery(self)
            else:
                return visitor.visitChildren(self)




    def query(self):

        localctx = UrlParser.QueryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_query)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 177
            self.match(UrlParser.QMARK)
            self.state = 178
            self.pair()
            self.state = 183
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==20 or _la==21:
                self.state = 179
                _la = self._input.LA(1)
                if not(_la==20 or _la==21):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 180
                self.pair()
                self.state = 185
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def key(self):
            return self.getTypedRuleContext(UrlParser.KeyContext,0)


        def EQ(self):
            return self.getToken(UrlParser.EQ, 0)

        def value(self):
            return self.getTypedRuleContext(UrlParser.ValueContext,0)


        def getRuleIndex(self):
            return UrlParser.RULE_pair

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPair" ):
                listener.enterPair(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPair" ):
                listener.exitPair(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPair" ):
                return visitor.visitPair(self)
            else:
                return visitor.visitChildren(self)




    def pair(self):

        localctx = UrlParser.PairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_pair)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.key()
            self.state = 189
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==22:
                self.state = 187
                self.match(UrlParser.EQ)
                self.state = 188
                self.value()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def qPiece(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UrlParser.QPieceContext)
            else:
                return self.getTypedRuleContext(UrlParser.QPieceContext,i)


        def getRuleIndex(self):
            return UrlParser.RULE_key

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKey" ):
                listener.enterKey(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKey" ):
                listener.exitKey(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKey" ):
                return visitor.visitKey(self)
            else:
                return visitor.visitChildren(self)




    def key(self):

        localctx = UrlParser.KeyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_key)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 59248640) != 0):
                self.state = 191
                self.qPiece()
                self.state = 196
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def qPiece(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(UrlParser.QPieceContext)
            else:
                return self.getTypedRuleContext(UrlParser.QPieceContext,i)


        def EQ(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.EQ)
            else:
                return self.getToken(UrlParser.EQ, i)

        def getRuleIndex(self):
            return UrlParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = UrlParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_value)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 201
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 63442944) != 0):
                self.state = 199
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [12, 19, 23, 24, 25]:
                    self.state = 197
                    self.qPiece()
                    pass
                elif token in [22]:
                    self.state = 198
                    self.match(UrlParser.EQ)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 203
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QPieceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUERY_TEXT(self):
            return self.getToken(UrlParser.QUERY_TEXT, 0)

        def PCT(self):
            return self.getToken(UrlParser.PCT, 0)

        def STRAY_PCT(self):
            return self.getToken(UrlParser.STRAY_PCT, 0)

        def EMAIL(self):
            return self.getToken(UrlParser.EMAIL, 0)

        def NESTED_URL(self):
            return self.getToken(UrlParser.NESTED_URL, 0)

        def getRuleIndex(self):
            return UrlParser.RULE_qPiece

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQPiece" ):
                listener.enterQPiece(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQPiece" ):
                listener.exitQPiece(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQPiece" ):
                return visitor.visitQPiece(self)
            else:
                return visitor.visitChildren(self)




    def qPiece(self):

        localctx = UrlParser.QPieceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_qPiece)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 204
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 59248640) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FragmentPartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def HASH(self):
            return self.getToken(UrlParser.HASH, 0)

        def FRAG_TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.FRAG_TEXT)
            else:
                return self.getToken(UrlParser.FRAG_TEXT, i)

        def PCT(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.PCT)
            else:
                return self.getToken(UrlParser.PCT, i)

        def STRAY_PCT(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.STRAY_PCT)
            else:
                return self.getToken(UrlParser.STRAY_PCT, i)

        def EMAIL(self, i:int=None):
            if i is None:
                return self.getTokens(UrlParser.EMAIL)
            else:
                return self.getToken(UrlParser.EMAIL, i)

        def getRuleIndex(self):
            return UrlParser.RULE_fragmentPart

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFragmentPart" ):
                listener.enterFragmentPart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFragmentPart" ):
                listener.exitFragmentPart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFragmentPart" ):
                return visitor.visitFragmentPart(self)
            else:
                return visitor.visitChildren(self)




    def fragmentPart(self):

        localctx = UrlParser.FragmentPartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_fragmentPart)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            self.match(UrlParser.HASH)
            self.state = 210
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 101191680) != 0):
                self.state = 207
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 101191680) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 212
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





