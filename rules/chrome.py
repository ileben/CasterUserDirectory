from imports import *


class CustomChrome(MappingRule):
    pronunciation = "custom chrome"

    mapping = {
        "go back [<n>]":
            R(Key("a-left/20")) * Repeat(extra="n"),
        "go forward [<n>]":
            R(Key("a-right/20")) * Repeat(extra="n"),
        "zoom in [<n>]":
            R(Key("c-plus/20")) * Repeat(extra="n"),
        "zoom out [<n>]":
            R(Key("c-minus/20")) * Repeat(extra="n"),
        "zoom reset [<n>]":
            R(Key("c-0")),
        #browser.TOGGLE_BOOKMARK_TOOLBAR:
            #R(Key("cs-b")),
        #"switch user":
            #R(Key("cs-m")),
        #"focus notification":
            #R(Key("a-n")),
        #"allow notification":
            #R(Key("as-a")),
        #"deny notification":
            #R(Key("as-a")),
        #"google that":
            #R(Store(remove_cr=True) + Key("c-t") + Retrieve() + Key("enter")),
        #"wikipedia that":
            #R(Store(space="+", remove_cr=True) + Key("c-t") + Text(
                #"https://en.wikipedia.org/w/index.php?search=") + Retrieve() + Key("enter")),
    }
    defaults = {"n": 1}
    extras = [
        IntegerRefST("n", 1, 50),
    ]

def get_rule():
    return CustomChrome, RuleDetails(name="CustomChrome", executable="chrome")