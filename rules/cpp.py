from imports import *
from programming import SymbolSpecs

class CustomCPP(MergeRule):
    pronunciation = "C plus plus"

    mapping = {
        "new scope":
            R(Key("leftbrace, enter, rightbrace, up, enter")),
        SymbolSpecs.IF:
            #R(Key("i, f, space, lparen, rparen, enter, leftbrace, enter, rightbrace, left, up:3, right:4")),
            R(Key("i, f, space, lparen, rparen, left")),
        SymbolSpecs.ELSE:
            R(Key("e, l, s, e, enter, leftbrace, enter, enter, rightbrace, left, up, tab")),
        #
        SymbolSpecs.SWITCH:
            R(Text("switch(){\ncase : break;\ndefault: break;") + Key("up,up,left,left")),
        SymbolSpecs.CASE:
            R(Text("case :") + Key("left")),
        SymbolSpecs.BREAK:
            R(Text("break;")),
        SymbolSpecs.DEFAULT:
            R(Text("default: ")),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("do {}") + Key("left, enter:2")),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while ()") + Key("left")),
        SymbolSpecs.FOR_LOOP:
			R(Text("for (; TOKEN; TOKEN)") + Key("home, right:5")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for ( : TOKEN);") + Key("home, right:5")),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("(int)")),
        SymbolSpecs.TO_FLOAT:
            R(Text("(double)")),
        SymbolSpecs.TO_STRING:
            R(Text("std::to_string()") + Key("left")),
        #
        SymbolSpecs.AND:
            R(Text(" && ")),
        SymbolSpecs.OR:
            R(Text(" || ")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("cout <<")),
        #
        #SymbolSpecs.IMPORT:
        "include":
            R(Text("#include ")),
        #
        SymbolSpecs.FUNCTION:
            R(Text("TOKEN TOKEN(){}") + Key("left")),
        SymbolSpecs.CLASS:
            R(Text("class TOKEN{}") + Key("left")),
        #
        SymbolSpecs.COMMENT:
            R(Text("// ")),
        SymbolSpecs.LONG_COMMENT:
            R(Text("/*  */") + Key("left, left, left")),
        (SymbolSpecs.COMMENT_OUT + " [<nnavi50>]"):
            R((Key("end") + Key("home") + Text("//") + Key("down"))*Repeat(extra="nnavi50"), rspec="comment out"),
        (SymbolSpecs.REMOVE_COMMENT + " [<nnavi50>]"):
            R((Key("end") + Key("home, delete, delete") + Key("down"))*Repeat(extra="nnavi50"), rspec="remove comment"),
        "alter line":
            R(Mimic("duple") + Key("up, home") + Text("//") + Key("down, home")),
        #
        SymbolSpecs.NULL:
            R(Text("null")),
        #
        SymbolSpecs.RETURN:
            R(Text("return")),
        #
        SymbolSpecs.TRUE:
            R(Text("true")),
        SymbolSpecs.FALSE:
            R(Text("false")),

        # C++ specific
        "public":
            R(Text("public ")),
        "private":
            R(Text("private ")),
        "static":
            R(Text("static ")),
        "final":
            R(Text("final ")),
        "static cast integer":
            R(Text("static_cast<int>()") + Key("left")),
        "static cast double":
            R(Text("static_cast<double>()") + Key("left")),
        "scope":
            R(Text("::")),
        "standard":
            R(Text("std")),
        "constant":
            R(Text("const ")),

        #http://www.learncpp.com/cpp-tutorial/67-introduction-to-pointers/
        "(reference to | address of)":
            R(Text("&")),
        "(pointer | D reference)":
            R(Text("*")),
        "(member | arrow)":
            R(Text("->")),
        "new new":
            R(Text("new ")),
        "void":
            R(Text("void ")),
        "boolean":
            R(Text("bool ")),
        "integer":
            R(Text("int ")),
        "float":
            R(Text("float ")),
        "double float":
            R(Text("double ")),
        "character":
            R(Text("char ")),
        "big integer":
            R(Text("Integer")),
        "string":
            R(Text("string ")),
        "ternary":
            R(Text("() ? TOKEN : TOKEN;") + (Key("left")*17)),
    }

    extras = [
        IntegerRefST("nnavi50", 1, 50),
    ]
    defaults = {"nnavi50": 1}


def get_rule():
    return CustomCPP, RuleDetails(ccrtype=CCRType.GLOBAL)
