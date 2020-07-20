from imports import *

def numbers2(wnKK):
    Text(str(wnKK)).execute()
    
def digit(digits):
    for d in digits:
        Text(str(d)).execute()
    
class CustomNumbers(MergeRule):
    
    mapping = {
        "numb [<multiplier>] <wnKK>":
            R(Function(numbers2, extra="wnKK"), rspec="Number")*Repeat(extra="multiplier"),
        "digit <digits>":
            R(Function(digit, extra="digits"), rspec="Digit"),
        "hexa":
            R(Text("0x"))
    }
    
    extras = [
        IntegerRefST("wn", 0, 10),
        IntegerRefST("wnKK", 0, 1000000),
        Repetition(IntegerRefST("wn", 0, 10), max=10, name="digits"),
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
