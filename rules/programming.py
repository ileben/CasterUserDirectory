from imports import *

class SymbolSpecs(object):
    IF = "iffae"
    ELSE = "shells"

    SWITCH = "switch"
    CASE = "case of"
    BREAK = "breaker"
    DEFAULT = "default"

    DO_LOOP = "do loop"
    WHILE_LOOP = "while loop"
    FOR_LOOP = "for loop"
    FOR_EACH_LOOP = "for each"

    TO_INTEGER = "convert to integer"
    TO_FLOAT = "convert to floating point"
    TO_STRING = "convert to string"

    AND = "lodge and"
    OR = "lodge or"
    NOT = "lodge not"

    SYSOUT = "print to console"

    IMPORT = "import"

    FUNCTION = "function"
    CLASS = "class"

    COMMENT = "add comment"
    LONG_COMMENT = "long comment"
    COMMENT_OUT = "comment out"
    REMOVE_COMMENT = "remove comment"

    NULL = "value not"

    RETURN = "return"

    TRUE = "value true"
    FALSE = "value false"

    # not part of the programming standard:
    CANCEL = "(terminate | escape | exit | cancel)"
    
    
alphabet_dict = {
            "alfa"   : "a",
            "ulfa"   : "a",
            "bravo"    : "b",
            "Charlie"    : "c",
            "delta"   : "d",
            "echo"    : "e",
            "foxy"    : "f",
            "goof"    : "g",
            "hotel"   : "h",
            "India"   : "i",
            "endia"   : "i",
            "julia"   : "j",
            "kilo"    : "k",
            "Lima"    : "l",
            "Mike"    : "m",
            "November": "n",
            "oscar"   : "o",
            "prime"   : "p",
            #"Quebec"  : "q", #too much like "go back"
            "quantum"  : "q",
            "Romeo"   : "r",
            "Sierra"  : "s",
            "tango"   : "t",
            "uniform" : "u",
            "victor"  : "v",
            "whiskey" : "w",
            "x-ray"   : "x",
            "yankee"  : "y",
            "Zulu"    : "z",
        }
        
double_punctuation_dict = {
    "quotes":                              "\"\"",
    "thin quotes":                         "''",
    #"tickris":                             "``",
    #"prekris":                             "()",
    "parens":                               "()",
    "brax":                                "[]",
    "curly":                               "{}",
    "angle":                               "<>",
}

inv_dp = {v: k for k, v in double_punctuation_dict.iteritems()}

punctuation_dict = {
    "space":                                              " ",
    "period":                                             ".",
    "comma":                                              ",",
    "bam":                                                ". ",
    "boom":                                               ", ",
    "questo":                                             "?",
    "clamor":                                             "!",
    "deckle":                                             ":",
    "semper":                                             ";",
    "underscore":                                         "_",
    "apostrophe":                                         "'",
    "ticky":                                              "`",
    "starling":                                           "*",
    "plus":                                               "+",
    "minus":                                              "-",
    "slash":                                              "/",
    "backslash":                                          "\\",
    "less than | open " + inv_dp["<>"]:                   "<",
    "less [than] [or] equal [to]":                        "<=",
    "greater than | close " + inv_dp["<>"]:               ">",
    "greater [than] [or] equal [to]":                     ">=",
    "equals":                                             "=",
    "equal to":                                           "==",
    "not equal to":                                       "!=",
    "hashy":                                              "#",
    "Dolly":                                              "$",
    "modulo":                                             "%",
    "ampersand":                                          "&",
    "pipe":                                               "|",
    "tilde":                                              "~",
    "carrot":                                             "^",
    "(atty | at symbol)":                                 "@",
    "(open|close) " + inv_dp["''"]:                       "'",
    "(open|close) " + inv_dp['""']:                       '"',
    "open " + inv_dp["[]"]:                               "[",
    "close " + inv_dp["[]"]:                              "]",
    "open " + inv_dp["()"]:                               "(",
    "close " + inv_dp["()"]:                              ")",
    "open " + inv_dp["{}"]:                               "{",
    "close " + inv_dp["{}"]:                              "}",
}

class Punctuation(MappingRule):
    exported = False
    
    mapping = {
        "[<long>] <punctuation> [<npunc>]":
            R(Text("%(long)s" + "%(punctuation)s" + "%(long)s"))*Repeat(extra="npunc"),
        "<double_punctuation> [<npunc>]":
            R(Text("%(double_punctuation)s") + Key("left"))*Repeat(extra="npunc"),
    }

    extras = [
        IntegerRefST("npunc", 0, 10),
        Choice(
            "long", {
                "long": " ",
            }),
        Choice(
            "punctuation", punctuation_dict),
        Choice(
            "double_punctuation", double_punctuation_dict)
    ]
    defaults = {
        "npunc": 1,
        "long": "",
    }
        
def letters2(big, letter):
    if big:
        Key(letter.capitalize()).execute()
    else:
        Key(letter).execute()
        


format_dict = {
    "yell":  (1, 3),
    "title": (2, 1),
    "camel": (3, 1),
    "snake": (5, 3),
    "sing":  (4, 0),
    "say":   (5, 0)
}

def format_text(format, text):
    textformat.master_format_text(capitalization=format[0], spacing=format[1], textnv=text)
    

# By default process_recognition Is only called on the top level rule in the recognition.
# This rule recursively calls process_recognition on all of the nested rules
class RecursiveRule(CompoundRule):
        
    def process_recognition(self, node):
        self.process_node(node)
        
    def process_node(self, node):
        if isinstance(node.actor, RuleRef):
            rule = node.children[0].actor
            print("Found Rule: {} Children: {}".format(str(rule), str(node)))
            rule.process_recognition(node.children[0])
        else:
            for child in node.children:
                self.process_node(child)
        
class Alphabet(MappingRule):
    exported = False
    
    mapping = {
        "[<big>] <letter>":
            R(Function(letters2, extra={"big", "letter"})),
    }
    extras = [
        Choice("letter", alphabet_dict),
        Choice("big", {
            "big": True,
        }),
    ]
    defaults = {
        "big": False,
    }
    
class TextFormatting(MappingRule):
    exported = False

    mapping = {
        "<format> <text>":
            R(Function(format_text, extra={"text"})),
        #"<format>":
            #R(Text("Formatting")),
    }
    extras = [
        Choice("format", format_dict),
        Dictation("text"),
    ]
    
class Spelling(RecursiveRule):
    exported = False
    
    spec = "spell <letters>"
    extras = [
        Repetition(RuleRef(Alphabet()), max=20, name="letters"),
    ]
    
class ProgrammingOptions(RecursiveRule):
    exported = False
    
    spec = "<TextFormatting> | <Spelling> | <Punctuation>"
    #spec = "<TextFormatting> | <Spelling>"
    extras = [
        RuleRef(TextFormatting(), name="TextFormatting"),
        RuleRef(Spelling(), name="Spelling"), 
        RuleRef(Punctuation(), name="Punctuation")
    ]
    
class CustomProgramming(MappingRule):
    
    mapping = {
        "<ProgrammingOptions>": ActionBase()
    }
    extras = [
        Repetition(RuleRef(ProgrammingOptions()), name="ProgrammingOptions", max=20),
    ]
    
    def process_recognition(self, node):
        self.process_node(node)
        
    def process_node(self, node):
        #print("BLAH_BLAH_BLAH\n")
        if isinstance(node.actor, RuleRef):
            rule = node.children[0].actor
            print("Found Rule: {} Children: {}\n".format(str(rule), str(node)))
            rule.process_recognition(node.children[0])
        else:
            for child in node.children:
                self.process_node(child)
                
                
# This is for when you really want to make sure that everything is recognized as a literal word
class JustDictation(MappingRule):
    mapping = {
        "dictate <text>":
            R(Text("%(text)s")),
    }
    extras = [
        Dictation("text"),
    ]

def get_rule():
    #return JustDictation, RuleDetails(name="JustDictation")
    return CustomProgramming, RuleDetails(name="CustomProgramming")