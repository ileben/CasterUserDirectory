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
        "zoom (and) hold":
            R(Function(et.zoom, hold=True)),
        "zoom out":
            R(Function(et.unzoom)) +
            R(Function(et.disable_follow_gaze)),
        "(click|kick|punch) <textnv>":
            R(Function(et.click_text)),
        "touch <textnv>":
            R(Function(et.touch_text)),
        "debug O C R":
            R(Function(et.debug_character_recognition)),
        "curse":
            R(Function(et.enable_follow_gaze)),
        "uncurse":
            R(Function(et.disable_follow_gaze)),
        "drag":
            R(Function(et.unzoom))+
            Mouse("left:down")+
            R(Function(et.begin_drag)),
        "fly kick [<nn10>]":
            R(Function(et.teleport_cursor))+
            Mouse("left")*Repeat(extra="nn10"),
        "push [<nn10>]":
            R(Function(et.stop_zoom_unless_holding))+
            Mouse("left")*Repeat(extra="nn10"),
        "psychic":
            R(Function(et.stop_zoom_unless_holding))+
            Mouse("right"),
        "double kick":
            R(Function(et.stop_zoom_unless_holding))+
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