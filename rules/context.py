from imports import *
from dragonfly import ActionError, Pause
from castervoice.lib.merge.state.async import AsyncState, AsyncItem

from castervoice.lib.clipboard import Clipboard
from castervoice.lib import utilities, settings
import time
import win32clipboard, win32ui, win32con, win32api, win32gui

class BracketCompare(object):
    EQUAL = 0
    GREATEREQUAL = 1
    LESSEREQUAL = 2
    
class BracketClamp(object):
    NONE = 0
    POSITIVE = 1
    NEGATIVE = 2
    
class NavigationState:
    def __init__(self):
        self.selection_size = 0
    
        self.context = ""
        self.index = -1
        self.target_index = -1
        self.target_token = ""
        
        self.bracket_count = 0
        self.target_bracket_count = 0
        self.target_bracket_compare = BracketCompare.EQUAL
        self.target_bracket_clamp = BracketClamp.POSITIVE
        self.arg_count = 0
     
    def reset_context(self):
        self.context = ""
        self.index = -1
        self.target_index = -1
        self.target_token = ""
    
    def reset_bracket_count(self, count=0, factor=1, offset=0, compare = BracketCompare.EQUAL, clamp = BracketClamp.POSITIVE):
        #print("arg: {} factor: {} offset: {}".format(count, factor, offset))
        self.bracket_count = 0
        self.target_bracket_count = count * factor + offset
        self.target_bracket_compare = compare
        self.target_bracket_clamp = clamp
        print("setting bracket_count target:{} compare:{} clamp:{}".format(self.target_bracket_count, compare, clamp))
        
    def brackets_match_target(self, bracket_count):
        return _compare_bracket_state(bracket_count, self.target_bracket_count, self.target_bracket_compare)
     
class NavigationAction(AsyncItem):
    def __init__(self, action):
        AsyncItem.__init__(self)
        self._action = action
        self._nav_state = NavigationState()
        
    def execute(self, data=None):
        async_state = data["async_state"]
        if async_state.iteration == 0:
            self._nav_state = NavigationState()
            
        data["nav_state"] = self._nav_state
        return self._action.execute(data)
            
def select_more(nav_state, look_left, keep_selection=False):
    
    # make sure nothing is highlighted to boot
    if not keep_selection:
        if len(nav_state.context) > 0:
            Key("left" if look_left else "right").execute()
        else:
            Key("left, right" if look_left else "right, left").execute()
        nav_state.reset_context()
          
    # select progressively more lines to amortize cost
    nav_state.selection_size = (1 if nav_state.selection_size == 0 else min(nav_state.selection_size * 2, 8))
    #nav_state.selection_size = 1    
    for i in range(0, nav_state.selection_size):
        if look_left:
            Key("s-home, cs-left, s-left").execute()
        else:
            Key("s-end, s-right").execute()
    
    new_context = read_nmax_tries(5, .01, same_is_okay=True)
    if new_context is None:
        raise ActionError("select_more")
        
    # initialize index on fresh selection
    if nav_state.index == -1:
        nav_state.index = len(new_context)-1 if look_left else 0
    
    # offset indices to new context on expanded selection
    elif keep_selection and look_left:
        extra_length = len(new_context) - len(nav_state.context)
        nav_state.index += extra_length
        if nav_state.target_index != -1:
            nav_state.target_index += extra_length
        
    nav_state.context = new_context
    
    
    print("select _index: {} _context: {}".format(nav_state.index, nav_state.context))
    return True
    
def reach_target(async_state, nav_state, direction, move_over=False, select=False):
    
    # cache these before we reset context
    look_left = str(direction) == "left"
    index = nav_state.target_index
    length = len(nav_state.target_token)
    context_before = (nav_state.context[index+length:] if look_left else nav_state.context[:index])
    print("reaching index:{} length:{}".format(index, length))
    print("context_before:'{}'".format(context_before))
    
    # deselect context
    Key("right" if look_left else "left").execute()
    nav_state.reset_context()
    
    # move up to the target
    context_before = context_before.replace("\r\n", "\n")
    Key(("left:" if look_left else "right:") + str(len(context_before))).execute()
    
    if move_over:
        Key(("left:" if look_left else "right:") + str(length)).execute()
    elif select:
        Key(("s-left:" if look_left else "s-right:") + str(length)).execute()
           
    async_state.complete = True

def read_nmax_tries(n, slp=0.1, same_is_okay=False):
    tries = 0
    while True:
        tries += 1
        results = read_selected_without_altering_clipboard(same_is_okay)
        error_code = results[0]
        if error_code == 0:
            return results[1]
        if tries > n:
            return None
        time.sleep(slp)

def paste():
    win32clipboard.OpenClipboard(0)
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data
    
class ClipRecord(object):
    def __init__(self):
        self.hPrev = 0
        self.first = True
        self.win = win32ui.CreateFrame()
        self.win.CreateWindow(None,'',win32con.WS_OVERLAPPEDWINDOW)
        self.win.HookMessage(self.OnDrawClipboard,win32con.WM_DRAWCLIPBOARD)
        self.win.HookMessage(self.OnChangeCBChain,win32con.WM_CHANGECBCHAIN)
        self.win.HookMessage(self.OnDestroy,win32con.WM_DESTROY)
        self.StartListen()
        
    def StartListen(self):
        
        self.first = True
        self.text = None
        self.change = True
        try:
            self.hPrev=win32clipboard.SetClipboardViewer(self.win.GetSafeHwnd())
        except win32api.error, err:
            if win32api.GetLastError () == 0:
                # information that there is no other window in chain
                pass
            else:
                raise
                
    def StopListen(self):
        if self.hPrev:
            win32clipboard.ChangeClipboardChain(self.win.GetSafeHwnd(),self.hPrev)
        else:
            win32clipboard.ChangeClipboardChain(self.win.GetSafeHwnd(),0)
            
    def Reset(self):
        win32gui.PumpWaitingMessages()
        self.change = False
        
    def Update(self):
        win32gui.PumpWaitingMessages()
        return cr.change
        
    def OnChangeCBChain(self, *args):
        msg, wParam, lParam = args[-1][1:4]
        if self.hPrev == wParam:
            # repair the chain
            self.hPrev = lParam
        if self.hPrev:
            # pass the message to the next window in chain
            win32api.SendMessage (self.hPrev, msg, wParam, lParam)

    def OnDrawClipboard(self, *args):
        msg, wParam, lParam = args[-1][1:4]
        if self.first:
            self.first = False
            print("CLIPBOARD FIRST")
        else:
            self.change = True
            print("CLIPBOARD")
        if self.hPrev:
            # pass the message to the next window in chain
            win32api.SendMessage (self.hPrev, msg, wParam, lParam)
    
    def OnDestroy(self):
        self.StopListen()
        
cr = ClipRecord()

def GetClipboard():
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return text
    
def SetClipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_TEXT)
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    
def read_selected_without_altering_clipboard(same_is_okay=False, pause_time="0"):
    '''Returns a tuple:
    (0, "text from system") - indicates success
    (1, None) - indicates no change
    (2, None) - indicates clipboard error
    '''

    temporary = None
    prior_content = None
    max_tries = 20
    error_code = 0
    
    try:
        prior_content = GetClipboard()
    except Exception:
        print("ERROR: failed to obtain clipboard")
        pass
        
    cr.Reset()
    Key("c-c").execute()
                       
    for i in range(0, max_tries):
        failure = True
        time.sleep(0.1)
        if cr.Update():
        #if True:
            try:
                temporary = GetClipboard()
                failure = False
            except Exception:
                print("clipboard exception")
                utilities.simple_log(False)
        
        if not failure:
            break
        print("Clipboard Read Attempts " + str(i))  # Debugging
        if i is max_tries:
            temporary = None
            error_code = 2
    
    if not prior_content is None:    
        try:
            SetClipboard(prior_content)
        except Exception:
            print("ERROR: failed to restore clipboard")
            pass
        
    if prior_content == temporary and not same_is_okay:
        return 1, None
        
    return error_code, temporary