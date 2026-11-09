# Generated from UrlParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .UrlParser import UrlParser
else:
    from UrlParser import UrlParser

# This class defines a complete listener for a parse tree produced by UrlParser.
class UrlParserListener(ParseTreeListener):

    # Enter a parse tree produced by UrlParser#url.
    def enterUrl(self, ctx:UrlParser.UrlContext):
        pass

    # Exit a parse tree produced by UrlParser#url.
    def exitUrl(self, ctx:UrlParser.UrlContext):
        pass


    # Enter a parse tree produced by UrlParser#authority.
    def enterAuthority(self, ctx:UrlParser.AuthorityContext):
        pass

    # Exit a parse tree produced by UrlParser#authority.
    def exitAuthority(self, ctx:UrlParser.AuthorityContext):
        pass


    # Enter a parse tree produced by UrlParser#userinfo.
    def enterUserinfo(self, ctx:UrlParser.UserinfoContext):
        pass

    # Exit a parse tree produced by UrlParser#userinfo.
    def exitUserinfo(self, ctx:UrlParser.UserinfoContext):
        pass


    # Enter a parse tree produced by UrlParser#port.
    def enterPort(self, ctx:UrlParser.PortContext):
        pass

    # Exit a parse tree produced by UrlParser#port.
    def exitPort(self, ctx:UrlParser.PortContext):
        pass


    # Enter a parse tree produced by UrlParser#host.
    def enterHost(self, ctx:UrlParser.HostContext):
        pass

    # Exit a parse tree produced by UrlParser#host.
    def exitHost(self, ctx:UrlParser.HostContext):
        pass


    # Enter a parse tree produced by UrlParser#ipv4.
    def enterIpv4(self, ctx:UrlParser.Ipv4Context):
        pass

    # Exit a parse tree produced by UrlParser#ipv4.
    def exitIpv4(self, ctx:UrlParser.Ipv4Context):
        pass


    # Enter a parse tree produced by UrlParser#domain.
    def enterDomain(self, ctx:UrlParser.DomainContext):
        pass

    # Exit a parse tree produced by UrlParser#domain.
    def exitDomain(self, ctx:UrlParser.DomainContext):
        pass


    # Enter a parse tree produced by UrlParser#subdomain.
    def enterSubdomain(self, ctx:UrlParser.SubdomainContext):
        pass

    # Exit a parse tree produced by UrlParser#subdomain.
    def exitSubdomain(self, ctx:UrlParser.SubdomainContext):
        pass


    # Enter a parse tree produced by UrlParser#registrable.
    def enterRegistrable(self, ctx:UrlParser.RegistrableContext):
        pass

    # Exit a parse tree produced by UrlParser#registrable.
    def exitRegistrable(self, ctx:UrlParser.RegistrableContext):
        pass


    # Enter a parse tree produced by UrlParser#publicSuffix.
    def enterPublicSuffix(self, ctx:UrlParser.PublicSuffixContext):
        pass

    # Exit a parse tree produced by UrlParser#publicSuffix.
    def exitPublicSuffix(self, ctx:UrlParser.PublicSuffixContext):
        pass


    # Enter a parse tree produced by UrlParser#tld.
    def enterTld(self, ctx:UrlParser.TldContext):
        pass

    # Exit a parse tree produced by UrlParser#tld.
    def exitTld(self, ctx:UrlParser.TldContext):
        pass


    # Enter a parse tree produced by UrlParser#platformHost.
    def enterPlatformHost(self, ctx:UrlParser.PlatformHostContext):
        pass

    # Exit a parse tree produced by UrlParser#platformHost.
    def exitPlatformHost(self, ctx:UrlParser.PlatformHostContext):
        pass


    # Enter a parse tree produced by UrlParser#otherHost.
    def enterOtherHost(self, ctx:UrlParser.OtherHostContext):
        pass

    # Exit a parse tree produced by UrlParser#otherHost.
    def exitOtherHost(self, ctx:UrlParser.OtherHostContext):
        pass


    # Enter a parse tree produced by UrlParser#hostLabel.
    def enterHostLabel(self, ctx:UrlParser.HostLabelContext):
        pass

    # Exit a parse tree produced by UrlParser#hostLabel.
    def exitHostLabel(self, ctx:UrlParser.HostLabelContext):
        pass


    # Enter a parse tree produced by UrlParser#labelTok.
    def enterLabelTok(self, ctx:UrlParser.LabelTokContext):
        pass

    # Exit a parse tree produced by UrlParser#labelTok.
    def exitLabelTok(self, ctx:UrlParser.LabelTokContext):
        pass


    # Enter a parse tree produced by UrlParser#authTok.
    def enterAuthTok(self, ctx:UrlParser.AuthTokContext):
        pass

    # Exit a parse tree produced by UrlParser#authTok.
    def exitAuthTok(self, ctx:UrlParser.AuthTokContext):
        pass


    # Enter a parse tree produced by UrlParser#path.
    def enterPath(self, ctx:UrlParser.PathContext):
        pass

    # Exit a parse tree produced by UrlParser#path.
    def exitPath(self, ctx:UrlParser.PathContext):
        pass


    # Enter a parse tree produced by UrlParser#segment.
    def enterSegment(self, ctx:UrlParser.SegmentContext):
        pass

    # Exit a parse tree produced by UrlParser#segment.
    def exitSegment(self, ctx:UrlParser.SegmentContext):
        pass


    # Enter a parse tree produced by UrlParser#fileExt.
    def enterFileExt(self, ctx:UrlParser.FileExtContext):
        pass

    # Exit a parse tree produced by UrlParser#fileExt.
    def exitFileExt(self, ctx:UrlParser.FileExtContext):
        pass


    # Enter a parse tree produced by UrlParser#segPiece.
    def enterSegPiece(self, ctx:UrlParser.SegPieceContext):
        pass

    # Exit a parse tree produced by UrlParser#segPiece.
    def exitSegPiece(self, ctx:UrlParser.SegPieceContext):
        pass


    # Enter a parse tree produced by UrlParser#query.
    def enterQuery(self, ctx:UrlParser.QueryContext):
        pass

    # Exit a parse tree produced by UrlParser#query.
    def exitQuery(self, ctx:UrlParser.QueryContext):
        pass


    # Enter a parse tree produced by UrlParser#pair.
    def enterPair(self, ctx:UrlParser.PairContext):
        pass

    # Exit a parse tree produced by UrlParser#pair.
    def exitPair(self, ctx:UrlParser.PairContext):
        pass


    # Enter a parse tree produced by UrlParser#key.
    def enterKey(self, ctx:UrlParser.KeyContext):
        pass

    # Exit a parse tree produced by UrlParser#key.
    def exitKey(self, ctx:UrlParser.KeyContext):
        pass


    # Enter a parse tree produced by UrlParser#value.
    def enterValue(self, ctx:UrlParser.ValueContext):
        pass

    # Exit a parse tree produced by UrlParser#value.
    def exitValue(self, ctx:UrlParser.ValueContext):
        pass


    # Enter a parse tree produced by UrlParser#qPiece.
    def enterQPiece(self, ctx:UrlParser.QPieceContext):
        pass

    # Exit a parse tree produced by UrlParser#qPiece.
    def exitQPiece(self, ctx:UrlParser.QPieceContext):
        pass


    # Enter a parse tree produced by UrlParser#fragmentPart.
    def enterFragmentPart(self, ctx:UrlParser.FragmentPartContext):
        pass

    # Exit a parse tree produced by UrlParser#fragmentPart.
    def exitFragmentPart(self, ctx:UrlParser.FragmentPartContext):
        pass



del UrlParser