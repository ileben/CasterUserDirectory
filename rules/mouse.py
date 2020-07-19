from imports import *
import eye_tracking as et

def wheel_scroll(direction, nn50):
    wheel = "wheelup" if direction == "up" else "wheeldown"
    for i in range(1, abs(nn50) + 1):
        Mouse("{}:1/5".format(wheel)).execute()

class CustomMouse(MergeRule):

    mapping = {
        "zoom in|zooming|enhance":
            R(Function(et.zoom)),
        "(click|kick) <textnv>":
            R(Function(et.click_text)),
        "touch <textnv>":
            R(Function(et.touch_text)),
        "curse":
            R(Function(et.follow_gaze, enable=True)),
        "uncurse":
            R(Function(et.follow_gaze, enable=False)),
        "push [<nn10>]":
            R(Function(et.follow_gaze, enable=False))+
            Mouse("left")*Repeat(extra="nn10"),
        "fly kick [<nn10>]":
            R(Function(et.teleport_cursor))+
            Mouse("left")*Repeat(extra="nn10"),
        "psychic":
            R(Function(et.follow_gaze, enable=False))+
            Mouse("right"),
        "double kick":
            R(Function(et.follow_gaze, enable=False))+
            Mouse("left")*Repeat(2),
        "squat":
            R(Function(et.unzoom))+
            Mouse("left:down"),
        "bench":
            R(Function(et.disable_follow_gaze))+
            Mouse("left:up"),
        "fly [<nn50>]":
            R(Function(et.disable_follow_gaze)) + 
            R(Function(wheel_scroll, direction="up")),
        "dive [<nn50>]":
            R(Function(et.disable_follow_gaze)) + 
            R(Function(wheel_scroll, direction="down")),
    }
    
    extras = [
        IntegerRefST("nn10", 1, 11),
        IntegerRefST("nn50", 1, 50),
        Dictation("textnv"),
    ]
    
    defaults = {
        "nn10": 1,
        "nn50": 1,
    }

def get_rule():
    return CustomMouse, RuleDetails(ccrtype=CCRType.GLOBAL)