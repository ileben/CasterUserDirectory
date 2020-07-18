from imports import *

direction_dict = {
    "duck|doc|dog": "down",
    "neck|Nick": "up",
    "lease": "left",
    "ross": "right",
}
        
class CustomNavigationGlobal(MergeRule):

    mapping = {
    
        '(escape|cancel)':
            R(Key("escape"), rspec="cancel"),
        '(shock|Shaw|show) [<nn50>]':
            R(Key("enter"), rspec="shock")*Repeat(extra="nn50"),
        'becky [<nn50>]':
            R(Key("backspace/5:%(nn50)d"), rspec="back"),
        "deli [<nn50>]":
            R(Key("del/5"), rspec="deli")*Repeat(extra="nn50"),
        "tabby [<nn10>]":
            R(Key("tab"))*Repeat(extra="nn10"),
        "shin tabby [<nn10>]":
            R(Key("s-tab"))*Repeat(extra="nn10"),
            
         "<direction> [<nn50>]":
            R(Key("%(direction)s")*Repeat(extra='nn50'), rdescript="arrow keys"),
         "home [<nn10>]":
            R(Key("home:%(nn10)s")),
        "(end | and) [<nn10>]":
            R(Key("end:%(nn10)s")),
        "back to top":
            R(Key("c-home")),
        "down to bottom":
            R(Key("c-end")),
            
        "leash [<nn50>]":
            R(Key("c-left:%(nn50)s")),
        "rush [<nn50>]":
            R(Key("c-right:%(nn50)s")),
        "(lick | leak) [<nn50>]":
            R(Key("cs-left:%(nn50)s")),
        "rock [<nn50>]":
            R(Key("cs-right:%(nn50)s")),
        "chain":
            R(Key("c-left, cs-right"), rspec="chain"),
        "shackle":
            R(Key("end, s-home"), rspec="shackle"),
        "whoops [<nn50>]":
            R(Key("s-home, s-home, s-up:%(nn50)s")),
        "dupes [<nn50>]":
            R(Key("s-end, s-down:%(nn50)s, s-end")),
        "multi down (<nn50>)":
            R(Key("sa-down:%(nn50)s")),
        "multi up (<nn50>)":
            R(Key("sa-up:%(nn50)s")),
            
        "copy":
            R(Key("c-c"), rspec="copy"),
        "cut":
            R(Key("c-x"), rspec="copy"),
        "paste":
            R(Key("c-v"), rspec="paste"),
            
        "copy line":
            R(Key("end, s-home/5, c-c/5")),
        "cut line":
            R(Key("end, s-home/5, c-x/5, s-home/5, backspace, backspace")),
        "paste above":
            R(Key("left, right, end, home, enter, up, end, c-v"), rspec="paste above"),
        "paste below [<below_left>]":
            R(Key("right, left, end, enter, s-tab:%(below_left)d, c-v"), rspec="paste below"),
        "blank above [<nn50>]":
            R(Key("left, right, end, home") + Key("enter, up")*Repeat(extra="nn50"), rspec="blank above"),
        "blank below [<nn50>]":
            R(Key("right, left, end, enter:%(nn50)d"), rspec="blank above"),
            
        "slap [<splatdir>] [<nn50>]":
            R(Key("c-%(splatdir)s"), rspec="splat")*Repeat(extra="nn50"),
        "nuke line [<nn50>]":
            R(Key("end, s-home/5, s-home/5, del, del"))*Repeat(extra="nn50"),
        "nuke above [<nn50>]":
            R(Key("up, end, s-home/5, s-home/5, del, del, home"))*Repeat(extra="nn50"),
        "nuke below [<nn50>]":
            R(Key("down, end, s-home/5, s-home/5, backspace, backspace, home"))*Repeat(extra="nn50"),
        "nuke empty [<nn50>]":
            R(Key("s-home/5, del, del, end"))*Repeat(extra="nn50"),
        "nuke empty above [<nn50>]":
            R(Key("end, up, s-home/5, del, del, home"))*Repeat(extra="nn50"),
        "nuke empty below [<nn50>]":
            R(Key("end, down, s-home/5, backspace, backspace, home"))*Repeat(extra="nn50"),
        
    }
    extras = [
        IntegerRefST("nn10", 1, 11),
        IntegerRefST("nn50", 1, 50),
        Choice("direction", direction_dict),
        Choice("splatdir", {
            "left": "backspace",
            "right": "delete",
        }),
        Choice("below_left", {
            "left": 1,
        })
    ]
    defaults = {
        "nn10": 1,
        "nn50": 1,
        "splatdir": "backspace",
        "below_left": 0,
    }
    
def get_rule():
    return CustomNavigationGlobal, RuleDetails(ccrtype=CCRType.GLOBAL)