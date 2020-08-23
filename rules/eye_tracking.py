import ctypes
import traceback
import os
import subprocess

try:
    #d = ctypes.CDLL(r"I:\Projects\Code\Source\EyeTrackingHooks\Release\EyeTrackingCLR.dll")
    d = ctypes.CDLL(r"D:\MobileDevelopment\third_party\EyeTrackingHooks\x64\Release\EyeTrackingCLR.dll")
    d.GetCurrentFile.restype = ctypes.c_char_p
    d.GetCurrentFolder.restype = ctypes.c_char_p

    print("Initializing eye tracking...")
    d.Initialize()
    i = d.Test()
    d.Connect()
    x = d.GetX()
    y = d.GetY()
    print("x:{} y:{}".format(x, y))
    
    print("Initializing character recognition...")
    d.InitCharacterRecognition()
    print("Done.")
    
except Exception as e:
    print("Exception: {}".format(e))
    track = traceback.format_exc()
    print(track)
    
def get_gaze_position():
    global d
    x = d.GetX()
    y = d.GetY()
    return x, y
    
def follow_gaze(enable):
    global d
    if enable:
        d.EnableFollowGaze()
    else:
        d.DisableFollowGaze()
        
def enable_follow_gaze():
    global d
    d.EnableFollowGaze()
        
def disable_follow_gaze():
    global d
    d.DisableFollowGaze()
    
def begin_drag():
    global d
    d.BeginDrag()
    
def teleport_cursor():
    global d
    d.TeleportCursor()
    
def zoom(hold=False):
    global d
    global zoomHold
    zoomHold = hold
    autoClick = (not zoomHold)
    d.Zoom(autoClick)
    
def unzoom():
    global d
    d.Unzoom()
    
def stop_zoom_unless_holding():
    global d
    global zoomHold
    if not zoomHold:
        d.DisableFollowGaze()
        d.Unzoom()
    
def click_text(textnv):
    global d
    d.ClickText(ctypes.c_char_p(str(textnv)))
    
def touch_text(textnv):
    global d
    d.TouchText(ctypes.c_char_p(str(textnv)))
    
def debug_character_recognition():
    global d
    d.DebugCharacterRecognition()
    
def get_current_file():
    global d
    text = d.GetCurrentFile()
    print("Current file: {}".format(text))
    return text
    
def get_current_folder():
    global d
    text = d.GetCurrentFolder()
    print("Current folder: {}".format(text))
    return text
    
def current_file_command(command, folder=False):
    file = get_current_folder() if folder else get_current_file()
    if len(file) > 0:
        run_detached_process(command.format(file))
        
def current_folder_command(command):
    file = get_current_folder()
    if len(file) > 0:
        run_detached_process(command.format(file))
        
def run_detached_process(command):
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    DETACHED_PROCESS = 0x00000008
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS)