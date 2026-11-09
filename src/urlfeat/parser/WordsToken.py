# Generated from /var/home/tamas/repos/phishing_ML/src/grammar/WordsToken.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,2,12,6,-1,2,0,7,0,2,1,7,1,1,0,4,0,7,8,0,11,0,12,0,8,1,1,1,1,
        0,0,2,1,1,3,2,1,0,1,2,0,48,57,97,122,12,0,1,1,0,0,0,0,3,1,0,0,0,
        1,6,1,0,0,0,3,10,1,0,0,0,5,7,7,0,0,0,6,5,1,0,0,0,7,8,1,0,0,0,8,6,
        1,0,0,0,8,9,1,0,0,0,9,2,1,0,0,0,10,11,9,0,0,0,11,4,1,0,0,0,2,0,8,
        0
    ]

class WordsToken(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    WORD = 1
    ANY = 2

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
 ]

    symbolicNames = [ "<INVALID>",
            "WORD", "ANY" ]

    ruleNames = [ "WORD", "ANY" ]

    grammarFileName = "WordsToken.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


