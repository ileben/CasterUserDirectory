from imports import *

class TortoiseGitMerge(MappingRule):
    pronunciation = "gitter merge"
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
    return TortoiseGitMerge, RuleDetails(name="TortoiseGitMerge", executable="TortoiseGitMerge")