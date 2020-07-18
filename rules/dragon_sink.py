from imports import *

class DragonSink(MappingRule):
    mapping = {
        "go sleep": ActionBase(), 
        "wake up": ActionBase(), 
    }
    
def get_rule():
    return DragonSink, RuleDetails(name="DragonSink", grammar_name="DragonSink")
    