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
        4,1,25,206,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,1,0,3,0,52,8,0,1,0,
        1,0,3,0,56,8,0,1,0,3,0,59,8,0,1,0,3,0,62,8,0,1,0,1,0,1,1,1,1,1,1,
        3,1,69,8,1,1,1,1,1,1,1,3,1,74,8,1,3,1,76,8,1,1,2,1,2,5,2,80,8,2,
        10,2,12,2,83,9,2,1,3,1,3,1,4,1,4,1,4,3,4,90,8,4,1,5,1,5,1,5,1,5,
        1,5,1,5,1,5,1,5,1,6,1,6,1,6,5,6,103,8,6,10,6,12,6,106,9,6,1,6,1,
        6,1,6,1,6,3,6,112,8,6,1,7,1,7,1,8,1,8,1,9,1,9,1,9,1,9,3,9,122,8,
        9,1,10,1,10,1,11,1,11,1,11,5,11,129,8,11,10,11,12,11,132,9,11,1,
        11,3,11,135,8,11,1,12,4,12,138,8,12,11,12,12,12,139,1,13,1,13,1,
        14,1,14,1,14,3,14,147,8,14,1,15,1,15,3,15,151,8,15,4,15,153,8,15,
        11,15,12,15,154,1,16,4,16,158,8,16,11,16,12,16,159,1,16,3,16,163,
        8,16,1,17,1,17,1,17,1,18,1,18,1,19,1,19,1,19,1,19,5,19,174,8,19,
        10,19,12,19,177,9,19,1,20,1,20,1,20,3,20,182,8,20,1,21,5,21,185,
        8,21,10,21,12,21,188,9,21,1,22,1,22,5,22,192,8,22,10,22,12,22,195,
        9,22,1,23,1,23,1,24,1,24,5,24,201,8,24,10,24,12,24,204,9,24,1,24,
        2,104,159,0,25,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,
        36,38,40,42,44,46,48,0,6,1,0,2,3,3,0,1,7,11,11,15,15,4,0,8,8,11,
        11,16,18,24,24,1,0,19,20,3,0,11,11,18,18,22,24,3,0,11,11,18,18,24,
        25,209,0,51,1,0,0,0,2,68,1,0,0,0,4,81,1,0,0,0,6,84,1,0,0,0,8,89,
        1,0,0,0,10,91,1,0,0,0,12,104,1,0,0,0,14,113,1,0,0,0,16,115,1,0,0,
        0,18,121,1,0,0,0,20,123,1,0,0,0,22,125,1,0,0,0,24,137,1,0,0,0,26,
        141,1,0,0,0,28,146,1,0,0,0,30,152,1,0,0,0,32,157,1,0,0,0,34,164,
        1,0,0,0,36,167,1,0,0,0,38,169,1,0,0,0,40,178,1,0,0,0,42,186,1,0,
        0,0,44,193,1,0,0,0,46,196,1,0,0,0,48,198,1,0,0,0,50,52,5,1,0,0,51,
        50,1,0,0,0,51,52,1,0,0,0,52,53,1,0,0,0,53,55,3,2,1,0,54,56,3,30,
        15,0,55,54,1,0,0,0,55,56,1,0,0,0,56,58,1,0,0,0,57,59,3,38,19,0,58,
        57,1,0,0,0,58,59,1,0,0,0,59,61,1,0,0,0,60,62,3,48,24,0,61,60,1,0,
        0,0,61,62,1,0,0,0,62,63,1,0,0,0,63,64,5,0,0,1,64,1,1,0,0,0,65,66,
        3,4,2,0,66,67,5,10,0,0,67,69,1,0,0,0,68,65,1,0,0,0,68,69,1,0,0,0,
        69,70,1,0,0,0,70,75,3,8,4,0,71,73,5,9,0,0,72,74,3,6,3,0,73,72,1,
        0,0,0,73,74,1,0,0,0,74,76,1,0,0,0,75,71,1,0,0,0,75,76,1,0,0,0,76,
        3,1,0,0,0,77,80,3,28,14,0,78,80,5,10,0,0,79,77,1,0,0,0,79,78,1,0,
        0,0,80,83,1,0,0,0,81,79,1,0,0,0,81,82,1,0,0,0,82,5,1,0,0,0,83,81,
        1,0,0,0,84,85,5,6,0,0,85,7,1,0,0,0,86,90,3,10,5,0,87,90,3,12,6,0,
        88,90,3,22,11,0,89,86,1,0,0,0,89,87,1,0,0,0,89,88,1,0,0,0,90,9,1,
        0,0,0,91,92,5,6,0,0,92,93,5,8,0,0,93,94,5,6,0,0,94,95,5,8,0,0,95,
        96,5,6,0,0,96,97,5,8,0,0,97,98,5,6,0,0,98,11,1,0,0,0,99,100,3,14,
        7,0,100,101,5,8,0,0,101,103,1,0,0,0,102,99,1,0,0,0,103,106,1,0,0,
        0,104,105,1,0,0,0,104,102,1,0,0,0,105,107,1,0,0,0,106,104,1,0,0,
        0,107,108,3,16,8,0,108,109,5,8,0,0,109,111,3,18,9,0,110,112,5,8,
        0,0,111,110,1,0,0,0,111,112,1,0,0,0,112,13,1,0,0,0,113,114,3,24,
        12,0,114,15,1,0,0,0,115,116,3,24,12,0,116,17,1,0,0,0,117,118,5,2,
        0,0,118,119,5,8,0,0,119,122,3,20,10,0,120,122,3,20,10,0,121,117,
        1,0,0,0,121,120,1,0,0,0,122,19,1,0,0,0,123,124,7,0,0,0,124,21,1,
        0,0,0,125,130,3,24,12,0,126,127,5,8,0,0,127,129,3,24,12,0,128,126,
        1,0,0,0,129,132,1,0,0,0,130,128,1,0,0,0,130,131,1,0,0,0,131,134,
        1,0,0,0,132,130,1,0,0,0,133,135,5,8,0,0,134,133,1,0,0,0,134,135,
        1,0,0,0,135,23,1,0,0,0,136,138,3,26,13,0,137,136,1,0,0,0,138,139,
        1,0,0,0,139,137,1,0,0,0,139,140,1,0,0,0,140,25,1,0,0,0,141,142,7,
        1,0,0,142,27,1,0,0,0,143,147,3,26,13,0,144,147,5,8,0,0,145,147,5,
        9,0,0,146,143,1,0,0,0,146,144,1,0,0,0,146,145,1,0,0,0,147,29,1,0,
        0,0,148,150,5,12,0,0,149,151,3,32,16,0,150,149,1,0,0,0,150,151,1,
        0,0,0,151,153,1,0,0,0,152,148,1,0,0,0,153,154,1,0,0,0,154,152,1,
        0,0,0,154,155,1,0,0,0,155,31,1,0,0,0,156,158,3,36,18,0,157,156,1,
        0,0,0,158,159,1,0,0,0,159,160,1,0,0,0,159,157,1,0,0,0,160,162,1,
        0,0,0,161,163,3,34,17,0,162,161,1,0,0,0,162,163,1,0,0,0,163,33,1,
        0,0,0,164,165,5,8,0,0,165,166,5,16,0,0,166,35,1,0,0,0,167,168,7,
        2,0,0,168,37,1,0,0,0,169,170,5,13,0,0,170,175,3,40,20,0,171,172,
        7,3,0,0,172,174,3,40,20,0,173,171,1,0,0,0,174,177,1,0,0,0,175,173,
        1,0,0,0,175,176,1,0,0,0,176,39,1,0,0,0,177,175,1,0,0,0,178,181,3,
        42,21,0,179,180,5,21,0,0,180,182,3,44,22,0,181,179,1,0,0,0,181,182,
        1,0,0,0,182,41,1,0,0,0,183,185,3,46,23,0,184,183,1,0,0,0,185,188,
        1,0,0,0,186,184,1,0,0,0,186,187,1,0,0,0,187,43,1,0,0,0,188,186,1,
        0,0,0,189,192,3,46,23,0,190,192,5,21,0,0,191,189,1,0,0,0,191,190,
        1,0,0,0,192,195,1,0,0,0,193,191,1,0,0,0,193,194,1,0,0,0,194,45,1,
        0,0,0,195,193,1,0,0,0,196,197,7,4,0,0,197,47,1,0,0,0,198,202,5,14,
        0,0,199,201,7,5,0,0,200,199,1,0,0,0,201,204,1,0,0,0,202,200,1,0,
        0,0,202,203,1,0,0,0,203,49,1,0,0,0,204,202,1,0,0,0,27,51,55,58,61,
        68,73,75,79,81,89,104,111,121,130,134,139,146,150,154,159,162,175,
        181,186,191,193,202
    ]

class UrlParser ( Parser ):

    grammarFileName = "UrlParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'www'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "':'", "'@'", "<INVALID>", "<INVALID>", "'?'", "'#'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'&amp;'", "'&'", "'='" ]

    symbolicNames = [ "<INVALID>", "SCHEME_PREFIX", "SLD", "TLD", "WWW", 
                      "PUNYCODE", "DIGITS", "LABEL", "DOT", "COLON", "AT", 
                      "PCT", "SLASH", "QMARK", "HASH", "AUTH_OTHER", "EXT", 
                      "SEG_TEXT", "STRAY_PCT", "AMP_ESC", "AMP", "EQ", "NESTED_URL", 
                      "QUERY_TEXT", "EMAIL", "FRAG_TEXT" ]

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
    RULE_otherHost = 11
    RULE_hostLabel = 12
    RULE_labelTok = 13
    RULE_authTok = 14
    RULE_path = 15
    RULE_segment = 16
    RULE_fileExt = 17
    RULE_segPiece = 18
    RULE_query = 19
    RULE_pair = 20
    RULE_key = 21
    RULE_value = 22
    RULE_qPiece = 23
    RULE_fragmentPart = 24

    ruleNames =  [ "url", "authority", "userinfo", "port", "host", "ipv4", 
                   "domain", "subdomain", "registrable", "publicSuffix", 
                   "tld", "otherHost", "hostLabel", "labelTok", "authTok", 
                   "path", "segment", "fileExt", "segPiece", "query", "pair", 
                   "key", "value", "qPiece", "fragmentPart" ]

    EOF = Token.EOF
    SCHEME_PREFIX=1
    SLD=2
    TLD=3
    WWW=4
    PUNYCODE=5
    DIGITS=6
    LABEL=7
    DOT=8
    COLON=9
    AT=10
    PCT=11
    SLASH=12
    QMARK=13
    HASH=14
    AUTH_OTHER=15
    EXT=16
    SEG_TEXT=17
    STRAY_PCT=18
    AMP_ESC=19
    AMP=20
    EQ=21
    NESTED_URL=22
    QUERY_TEXT=23
    EMAIL=24
    FRAG_TEXT=25

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
            self.state = 51
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 50
                self.match(UrlParser.SCHEME_PREFIX)


            self.state = 53
            self.authority()
            self.state = 55
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 54
                self.path()


            self.state = 58
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 57
                self.query()


            self.state = 61
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 60
                self.fragmentPart()


            self.state = 63
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
            self.state = 68
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.state = 65
                self.userinfo()
                self.state = 66
                self.match(UrlParser.AT)


            self.state = 70
            self.host()
            self.state = 75
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 71
                self.match(UrlParser.COLON)
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 72
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
            self.state = 81
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 79
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 15]:
                        self.state = 77
                        self.authTok()
                        pass
                    elif token in [10]:
                        self.state = 78
                        self.match(UrlParser.AT)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 83
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
            self.state = 84
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
            self.state = 89
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 86
                self.ipv4()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 87
                self.domain()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 88
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
            self.state = 91
            self.match(UrlParser.DIGITS)
            self.state = 92
            self.match(UrlParser.DOT)
            self.state = 93
            self.match(UrlParser.DIGITS)
            self.state = 94
            self.match(UrlParser.DOT)
            self.state = 95
            self.match(UrlParser.DIGITS)
            self.state = 96
            self.match(UrlParser.DOT)
            self.state = 97
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
            self.state = 104
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1+1:
                    self.state = 99
                    self.subdomain()
                    self.state = 100
                    self.match(UrlParser.DOT) 
                self.state = 106
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

            self.state = 107
            self.registrable()
            self.state = 108
            self.match(UrlParser.DOT)
            self.state = 109
            self.publicSuffix()
            self.state = 111
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 110
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
            self.state = 113
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
            self.state = 115
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
            self.state = 121
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 117
                self.match(UrlParser.SLD)
                self.state = 118
                self.match(UrlParser.DOT)
                self.state = 119
                self.tld()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 120
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
            self.state = 123
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
        self.enterRule(localctx, 22, self.RULE_otherHost)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 125
            self.hostLabel()
            self.state = 130
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,13,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 126
                    self.match(UrlParser.DOT)
                    self.state = 127
                    self.hostLabel() 
                self.state = 132
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,13,self._ctx)

            self.state = 134
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 133
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
        self.enterRule(localctx, 24, self.RULE_hostLabel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 136
                self.labelTok()
                self.state = 139 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 35070) != 0)):
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
        self.enterRule(localctx, 26, self.RULE_labelTok)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 141
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 35070) != 0)):
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
        self.enterRule(localctx, 28, self.RULE_authTok)
        try:
            self.state = 146
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 5, 6, 7, 11, 15]:
                self.enterOuterAlt(localctx, 1)
                self.state = 143
                self.labelTok()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 144
                self.match(UrlParser.DOT)
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 3)
                self.state = 145
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
        self.enterRule(localctx, 30, self.RULE_path)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 148
                self.match(UrlParser.SLASH)
                self.state = 150
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17238272) != 0):
                    self.state = 149
                    self.segment()


                self.state = 154 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==12):
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
        self.enterRule(localctx, 32, self.RULE_segment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 157 
            self._errHandler.sync(self)
            _alt = 1+1
            while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1+1:
                    self.state = 156
                    self.segPiece()

                else:
                    raise NoViableAltException(self)
                self.state = 159 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,19,self._ctx)

            self.state = 162
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 161
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
        self.enterRule(localctx, 34, self.RULE_fileExt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self.match(UrlParser.DOT)
            self.state = 165
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
        self.enterRule(localctx, 36, self.RULE_segPiece)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 167
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 17238272) != 0)):
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
        self.enterRule(localctx, 38, self.RULE_query)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 169
            self.match(UrlParser.QMARK)
            self.state = 170
            self.pair()
            self.state = 175
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19 or _la==20:
                self.state = 171
                _la = self._input.LA(1)
                if not(_la==19 or _la==20):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 172
                self.pair()
                self.state = 177
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
        self.enterRule(localctx, 40, self.RULE_pair)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.key()
            self.state = 181
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21:
                self.state = 179
                self.match(UrlParser.EQ)
                self.state = 180
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
        self.enterRule(localctx, 42, self.RULE_key)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 29624320) != 0):
                self.state = 183
                self.qPiece()
                self.state = 188
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
        self.enterRule(localctx, 44, self.RULE_value)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 193
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 31721472) != 0):
                self.state = 191
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [11, 18, 22, 23, 24]:
                    self.state = 189
                    self.qPiece()
                    pass
                elif token in [21]:
                    self.state = 190
                    self.match(UrlParser.EQ)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 195
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
        self.enterRule(localctx, 46, self.RULE_qPiece)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 29624320) != 0)):
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
        self.enterRule(localctx, 48, self.RULE_fragmentPart)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            self.match(UrlParser.HASH)
            self.state = 202
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 50595840) != 0):
                self.state = 199
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 50595840) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 204
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





