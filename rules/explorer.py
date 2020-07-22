from imports import *
import eye_tracking as et

class CustomExplorer(MappingRule):
    mapping = {
        "edit address | address bar":
            R(Key("a-d")),
        "copy address":
            R(Key("a-d/20, c-c")),
        "new window":
            R(Key("c-n")),
        "new folder":
            R(Key("cs-n")),
        "(folder up | get up) [<n>]":
            R(Key("a-up/10")*Repeat(extra="n")),
            
        "(navigation | nav | left) pane":
            R(Key("a-d, tab:2")),
        "(center pane | (file | folder) (pane | list))":
            R(Key("a-d, tab:3")),
            
        "(edit in|editing) notepad":
            R(Function(et.current_file_command, command=r"C:\Program Files\Notepad++\notepad++.exe {}")),
            
        "subversion [<folder>] difference":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:diff /path:{}")),
        "subversion [<folder>] log":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:log /path:{}")),
        "subversion [<folder>] blame":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:blame /path:{}")),
        "subversion [<folder>] browser":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:repobrowser /path:{}")),
        "subversion [<folder>] properties":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:properties /path:{}")),
        "subversion [<folder>] commit":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:commit /path:{}")),
        "subversion [<folder>] revert":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:revert /path:{}")),
        "subversion [<folder>] update":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:update /path:{}")),
        "subversion [<folder>] add":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:add /path:{}")),
        "subversion [<folder>] delete":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:remove /path:{}")),
        "subversion [<folder>] rename":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseProc.exe /command:rename /path:{}")),
            
        "gitter [<folder>] difference":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:diff /path:{}")),
        "gitter [<folder>] log":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:log /path:{}")),
        "gitter [<folder>] blame":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:blame /path:{}")),
        "gitter [<folder>] browser":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:repobrowser /path:{}")),
        "gitter [<folder>] properties":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:properties /path:{}")),
        "gitter [<folder>] commit":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:commit /path:{}")),
        "gitter [<folder>] revert":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:revert /path:{}")),
        "gitter [<folder>] (pull|pool)":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:pull /path:{}")),
        "gitter [<folder>] push":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:push /path:{}")),
        "gitter [<folder>] add":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:add /path:{}")),
        "gitter [<folder>] delete":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:remove /path:{}")),
        "gitter [<folder>] rename":
            R(Function(et.current_file_command, extra={"folder"}, command="TortoiseGitProc.exe /command:rename /path:{}")),
            
        "console here":
            R(Function(et.current_file_command, folder=True, command="C:\\Program Files\\ConEmu\\ConEmu64.exe -dir \"{}\"")),
    }
    
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
        Choice("folder", {
            "folder": True,
        }),
    ]
    defaults = {"n": 1}

def get_rule():
    return CustomExplorer, RuleDetails(name="CustomExplorer", executable="explorer")