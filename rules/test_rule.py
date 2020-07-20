from imports import *
import context
import lex

class TestRule(MappingRule):
    mapping = {
        "leaf [<nn10>]":
            AsynchronousAction([L(S(["cancel"], NavigationAction(
                               AsyncFunction(lex.next_expression, {"nn10":"count"}, direction="left") +
                               AsyncFunction(context.reach_target, direction="left", select=True)
                               )))], time_in_seconds=0, repetitions=10),
        "reef [<nn10>]":
            AsynchronousAction([L(S(["cancel"], NavigationAction(
                               AsyncFunction(lex.next_expression, {"nn10":"count"}, direction="right") +
                               AsyncFunction(context.reach_target, direction="right", select=True)
                               )))], time_in_seconds=0, repetitions=10),
    }
    
    extras = [
        IntegerRefST("nn10", 1, 11),
        IntegerRefST("nn50", 1, 50),
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
    return TestRule, RuleDetails(name="TestRule")
    