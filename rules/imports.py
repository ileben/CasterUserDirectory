from dragonfly import MappingRule, CompoundRule, Dictation, Choice, Repetition, RuleRef, Key, Function, ActionBase, Repeat
from castervoice.lib.merge.state.short import S, L, R
from castervoice.lib.actions import Text
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.const import CCRType
from castervoice.lib import textformat