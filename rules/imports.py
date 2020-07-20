from dragonfly import MappingRule, CompoundRule, Dictation, Choice, Repetition, RuleRef, Key, Mouse, Function, ActionBase, Repeat, Mimic, Pause
from castervoice.lib.merge.state.short import S, L, R
from castervoice.lib.actions import Text
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.const import CCRType
from castervoice.lib import textformat
from castervoice.lib.merge.state.actions import AsynchronousAction
from castervoice.lib.merge.state.async import AsyncFunction, AsyncRepetition, AsyncRepeat
from context import NavigationAction