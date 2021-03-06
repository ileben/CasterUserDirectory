from imports import *
from punctuation import CustomPunctuation
from numeric import CustomNumbers

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
    "sing":  (10, 0),
    "say":   (11, 0)
}

singing = False

def format_text(format, text):
    global singing
    
    # For sing, say, retain the original formatting except for the first letter
    # Afterwards append space to all additional formatting within the same utterance
    style = format[0]
    if style >= 10:
        singing = True
        t = str(text)
        if style == 10:
            t = t[0].upper() + t[1:]
        elif style == 11:
            t = t[0].lower() + t[1:]
        Text(t).execute()
    else:
        textformat.master_format_text(capitalization=format[0], spacing=format[1], textnv=text)
    
    if singing:
        Text(" ").execute()

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
    
class Spelling(RecursiveRule):
    exported = False
    
    spec = "spell <letters>"
    extras = [
        Repetition(RuleRef(Alphabet()), max=20, name="letters"),
    ]
    
# Reduced weight for everything other than text formatting to make it more likely 
# that the first word after text formatting is interpreted verbatim rather than as a command 
W = 0.001
    
class Punctuation(CustomPunctuation):
    weight = W
    exported = False
    
class Numbers(CustomNumbers):
    weight = W
    exported = False
    

class TextFormatting(MappingRule):
    exported = False

    mapping = {
        "<format> <text> [stop]":
            R(Function(format_text, extra={"text"})),
    }
    extras = [
        Choice("format", format_dict),
        Dictation("text"),
    ]

class ProgrammingOptions(RecursiveRule):
    exported = False
    
    spec = "<TextFormatting> | <Spelling> | <Punctuation> | <Numbers>"
    
    extras = [
        RuleRef(TextFormatting(), name="TextFormatting"),
        RuleRef(Spelling(), name="Spelling"), 
        RuleRef(Punctuation(), name="Punctuation"),
        RuleRef(Numbers(), name="Numbers")
    ]
    
class CustomProgramming(MappingRule):
    weight = 3 # Above global and app specific rules
    
    mapping = {
        "<ProgrammingOptions>": ActionBase()
    }
    extras = [
        Repetition(RuleRef(ProgrammingOptions()), name="ProgrammingOptions", max=20),
    ]
    
    def process_recognition(self, node):
        global singing
        singing = False
        self.process_node(node)
        
    def process_node(self, node):
        #print("BLAH_BLAH_BLAH\n")
        if isinstance(node.actor, RuleRef):
            rule = node.children[0].actor
            #print("Found Rule: {} Children: {}\n".format(str(rule), str(node)))
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