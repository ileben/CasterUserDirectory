from imports import *

class CustomNotepad(MappingRule):

    mapping = {
        "show in explorer":
            R(Key("cas-e")),

        "open":
            R(Key("c-o")),
        "go [to] line <n>":
            R(Key("c-g/10") + Text("%(n)s") + Key("enter")),
        "new (tab|tabby)":
            R(Key("c-n")),
    }
    extras = [
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1}


def get_rule():
    return CustomNotepad, RuleDetails(name="CustomNotepad", executable="notepad++")