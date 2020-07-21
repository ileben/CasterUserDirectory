from imports import *

class TortoiseMerge(MappingRule):
    pronunciation = "merge"
    weight = 2

    mapping = {
        "nexxy [<n>]":
            R(Key("c-down"))*Repeat(extra="n"),
        "proxy [<n>]":
            R(Key("c-up"))*Repeat(extra="n"),
        "next conflict [<n>]":
            R(Key("f8"))*Repeat(extra="n"),
        "prior conflict [<n>]":
            R(Key("s-f8"))*Repeat(extra="n"),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 100),
    ]
    defaults = {"n": 1}


def get_rule():
    return TortoiseMerge, RuleDetails(name="TortoiseMerge", executable="TortoiseMerge")