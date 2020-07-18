from imports import *

direction_dict = {
    "duck|doc|dog": "down",
    "neck|Nick": "up",
    "lease": "left",
    "ross": "right",
}
        
class CustomNavigation(MappingRule):

    mapping = {
        "Wendy|windy":
            R(Key("ca-tab")),
        "altar|alter [<nn10>]":
            R(Key("alt:down, tab/20:%(nn10)d, alt:up"), rdescript="Core: switch to most recent Windows"),
        "nexy [<nn50>]":
            R(Key("c-pgdown"))*Repeat(extra="nn50"),
        "proxy [<nn50>]":
            R(Key("c-pgup"))*Repeat(extra="nn50"),
        "close tab [<nn50>]":
            R(Key("c-w/20"))*Repeat(extra="nn50"),
        "close window":
            R(Key("a-f4")),
            
        "context menu":
            R(Key("s-f10")),
            
        'save':
            R(Key("c-s"), rspec="save"),
        "find":
            R(Key("c-f")),
        "find next [<nn50>]":
            R(Key("f3"))*Repeat(extra="nn50"),
        "find prior [<nn50>]":
            R(Key("s-f3"))*Repeat(extra="nn50"),
        "find everywhere":
            R(Key("cs-f")),
        "replace":
            R(Key("c-h")),
    }
    extras = [
        IntegerRefST("nn10", 1, 11),
        IntegerRefST("nn50", 1, 50),
        Choice("direction", direction_dict),
    ]
    defaults = {
        "nn10": 1,
        "nn50": 1,
    }
    
def get_rule():
    return CustomNavigation, RuleDetails(name="CustomNavigation", grammar_name="CustomNavigation")