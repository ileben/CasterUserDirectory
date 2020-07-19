from imports import *
from programming import SymbolSpecs

class CustomPython(MergeRule):
    pronunciation = "Python"

    mapping = {
    
        SymbolSpecs.IF:
            R(Key("i,f,space,colon,left")),
        SymbolSpecs.ELSE:
            R(Text("else:") + Key("enter")),
        # (no switch in Python)
        SymbolSpecs.BREAK:
            R(Text("break")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for  in TOKEN:") + Key("left:10")),
        SymbolSpecs.FOR_LOOP:
            R(Text("for  in range(0, TOKEN):") + Key("left:20")),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while :") + Key("left")),
        # (no do-while in Python)
        #SymbolSpecs.TO_INTEGER:
        #    R(Store() + Text("int()") + Key("left") + Retrieve(action_if_text="right")),
        #SymbolSpecs.TO_FLOAT:
        #    R(Store() + Text("float()") + Key("left") + Retrieve(action_if_text="right")),
        #SymbolSpecs.TO_STRING:
        #    R(Store() + Text("str()") + Key("left") + Retrieve(action_if_text="right")),
        SymbolSpecs.AND:
            R(Text(" and ")),
        SymbolSpecs.OR:
            R(Text(" or ")),
        SymbolSpecs.NOT:
            R(Text("not ")),
        SymbolSpecs.IMPORT:
            R(Text("import ")),
        SymbolSpecs.FUNCTION:
            R(Text("def ():") + Key("left:3")),
        SymbolSpecs.CLASS:
            R(Text("class :") + Key("left")),
        SymbolSpecs.COMMENT:
            R(Text("#") + Key("space")),
        SymbolSpecs.LONG_COMMENT:
            R(Text("''''''") + Key("left:3")),
        (SymbolSpecs.COMMENT_OUT + " [<nnavi50>]"):
            R((Key("end") + Key("home") + Text("#") + Key("down"))*Repeat(extra="nnavi50"), rspec="comment out"),
        (SymbolSpecs.REMOVE_COMMENT + " [<nnavi50>]"):
            R((Key("end") + Key("home, delete") + Key("down"))*Repeat(extra="nnavi50"), rspec="remove comment"),
        "alter line":
            R(Mimic("duple") + Key("up, home") + Text("#") + Key("down, home")),
        
        SymbolSpecs.NULL:
            R(Text("None")),
        SymbolSpecs.RETURN:
            R(Text("return ")),
        SymbolSpecs.TRUE:
            R(Text("True")),
        SymbolSpecs.FALSE:
            R(Text("False")),
        
        "ternary":
            R(Text(" if TOKEN else TOKEN")),

        # Python specific
        "sue iffae":
            R(Text("if ")),
        "sue shells":
            R(Text("else ")),
        "from":
            R(Text("from ")),
        "self":
            R(Text("self")),
        "long not":
            R(Text(" not ")),
        "it are in":
            R(Text(" in ")),
        "shell iffae | LFA":
            R(Key("e,l,i,f,space,colon,left")),
        "convert to character":
            R(Text("chr()") + Key("left")),
        "length of":
            R(Text("len()") + Key("left")),
        "global":
            R(Text("global ")),
        "list (comprehension | comp)":
            R(Text("[x for x in TOKEN if TOKEN]")),
        "identity is":
            R(Text(" is ")),
        "yield":
            R(Text("yield ")),

        # Essentially an improved version of the try catch command above
        # probably a better option than this is to use snippets with tab stops
        # VS code has the extension Python-snippets. these are activated by
        # going into the command pallet (cs-p) and typing in "insert snippet"
        # then press enter and then you have choices of snippets show up in the drop-down list.
        # you can also make your own snippets.
        "try [<exception>]":
            R(
                Text("try : ") + Pause("10") + Key("enter/2") +
                Text("except %(exception)s:") + Pause("10") + Key("enter/2")),
        "try [<exception>] as":
            R(
                Text("try :") + Pause("10") + Key("enter/2") +
                Text("except %(exception)s as :") + Pause("10") + Key("enter/2")),

        # class and class methods
        #"dunder":
        #    R(Store() + Text("____()") + Key("left:4") +
        #      Retrieve(action_if_text="right:4")),
        "init":
            R(Text("__init__()") + Key("left")),
        "meth [<binary_meth>]":
            R(Text("__%(binary_meth)s__(self, other):")),
        "meth [<unary_meth>]":
            R(Text("__%(unary_meth)s__(self):")),
    }

    extras = [
        Dictation("text"),
        IntegerRefST("nnavi50", 1, 50),
        Choice("unary_meth", {
            "reper": "reper",
            "stir": "str",
            "len": "len",
        }),
        Choice("binary_meth", {
            "add": "add",
            "subtract": "sub",
        }),
        Choice(
            "exception", {
                "exception": "Exception",
                "stop iteration": "StopIteration",
                "system exit": "SystemExit",
                "standard": "StandardError",
                "arithmetic": "ArithmeticError",
                "overflow": "OverflowError",
                "floating point": "FloatingPointError",
                "zero division": "ZeroDivisionError",
                "assertion": "AssertionError",
                "EOF": "EOFError",
                "import": "ImportError",
                "keyboard interrupt": "KeyboardInterrupt",
                "lookup": "LookupError",
                "index": "IndexError",
                "key": "KeyError",
                "name": "NameError",
                "unbound local": "UnboundLocalError",
                "environment": "EnvironmentError",
                "IO": "IOError",
                "OS": "OSError",
                "syntax": "SyntaxError",
                "system exit": "SystemExit",
                "type": "TypeError",
                "value": "ValueError",
                "run time": "RuntimeError",
                "not implemented": "NotImplementedError",
            })
    ]
    defaults = {"nnavi50": 1, "unary_meth": "", "binary_meth": "", "exception": ""}


def get_rule():
    return CustomPython, RuleDetails(ccrtype=CCRType.GLOBAL)
