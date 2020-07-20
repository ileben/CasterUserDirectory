from imports import *

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
    "ace":                                                " ",
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
    "arrow":                                              "->",
    "fat arrow":                                          "=>",
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

class CustomPunctuation(MergeRule):
    
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
    
def get_rule():
    return CustomPunctuation, RuleDetails(ccrtype=CCRType.GLOBAL)