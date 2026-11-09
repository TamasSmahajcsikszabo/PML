# Generated from UrlParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .UrlParser import UrlParser
else:
    from UrlParser import UrlParser

# This class defines a complete generic visitor for a parse tree produced by UrlParser.

class UrlParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by UrlParser#url.
    def visitUrl(self, ctx:UrlParser.UrlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#authority.
    def visitAuthority(self, ctx:UrlParser.AuthorityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#userinfo.
    def visitUserinfo(self, ctx:UrlParser.UserinfoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#port.
    def visitPort(self, ctx:UrlParser.PortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#host.
    def visitHost(self, ctx:UrlParser.HostContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#ipv4.
    def visitIpv4(self, ctx:UrlParser.Ipv4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#domain.
    def visitDomain(self, ctx:UrlParser.DomainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#subdomain.
    def visitSubdomain(self, ctx:UrlParser.SubdomainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#registrable.
    def visitRegistrable(self, ctx:UrlParser.RegistrableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#publicSuffix.
    def visitPublicSuffix(self, ctx:UrlParser.PublicSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#tld.
    def visitTld(self, ctx:UrlParser.TldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#platformHost.
    def visitPlatformHost(self, ctx:UrlParser.PlatformHostContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#otherHost.
    def visitOtherHost(self, ctx:UrlParser.OtherHostContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#hostLabel.
    def visitHostLabel(self, ctx:UrlParser.HostLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#labelTok.
    def visitLabelTok(self, ctx:UrlParser.LabelTokContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#authTok.
    def visitAuthTok(self, ctx:UrlParser.AuthTokContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#path.
    def visitPath(self, ctx:UrlParser.PathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#segment.
    def visitSegment(self, ctx:UrlParser.SegmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#fileExt.
    def visitFileExt(self, ctx:UrlParser.FileExtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#segPiece.
    def visitSegPiece(self, ctx:UrlParser.SegPieceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#query.
    def visitQuery(self, ctx:UrlParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#pair.
    def visitPair(self, ctx:UrlParser.PairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#key.
    def visitKey(self, ctx:UrlParser.KeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#value.
    def visitValue(self, ctx:UrlParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#qPiece.
    def visitQPiece(self, ctx:UrlParser.QPieceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UrlParser#fragmentPart.
    def visitFragmentPart(self, ctx:UrlParser.FragmentPartContext):
        return self.visitChildren(ctx)



del UrlParser