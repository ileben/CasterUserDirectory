from imports import *

def numbers2(wnKK):
    Text(str(wnKK)).execute()
    
class CustomNumbers(MergeRule):
    
    mapping = {
        "numb [<multiplier>] <wnKK>":
            R(Function(numbers2, extra="wnKK"), rspec="Number")*Repeat(extra="multiplier"),
        "hexa":
            R(Text("0x"))
    }
    
    extras = [
        IntegerRefST("wn", 0, 10),
        IntegerRefST("wnKK", 0, 1000000),
        Choice("multiplier", {
            "single": 1,
            "double": 2,
            "triple": 3,
            "Quadra": 4
        }),
    ]
    defaults = {
        "multiplier": 1,
    }

def get_rule():
    return CustomNumbers, RuleDetails(ccrtype=CCRType.GLOBAL)
