from imports import *

def numbers2(wnKK, digits):
    Text(str(wnKK)).execute()
    if not digits is None:
        Text(".").execute()
        for d in digits:
            Text(str(d)).execute()
    
def digit(digits):
    for d in digits:
        Text(str(d)).execute()
    
class CustomNumbers(MergeRule):
    
    mapping = {
        "numb [<multiplier>] <wnKK> [point <digits>]":
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
