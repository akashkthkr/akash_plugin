# Reference: https://github.com/longld/peda

import os
import sys
import signal

# set path to absolute path of akash.py
AKASHFILE = os.path.abspath(os.path.expanduser(__file__))
if os.path.islink(AKASHFILE):
    AKASHFILE = os.readlink(AKASHFILE)
sys.path.insert(0, os.path.dirname(AKASHFILE) + "/lib_shell/")

from main_instruction import *
from utils import *
from main_instruction import main_inst

class AkashCmd(object):

    # akash commands intercating with GDB

    commands = []
    def __init__(self):
        # list of all available commands
        self.commands = [c for c in dir(self) if callable(getattr(self, c)) and not c.startswith("_")]

    def _execute(self, gdb_command):
        gdb.execute(gdb_command)
        return

    def _get_helptext(self, *arg):

        """
        Get the help text, for internal use by help command and other aliases
        """
        (cmd,) = normalize_argv(arg, 1)
        helptext = ""
        if cmd is None:
            helptext = get_color("AKASH", "red", "bold") + get_color(" - Python Exploit Development Assistance for GDB", "blue","bold") + "\n"
            helptext += "List of \"akash\" subcommands, type the subcommand to invoke it:\n"
            i = 0
            for cmd in self.commands:
                if cmd.startswith("_"): continue # skip internal use commands
                func = getattr(self, cmd)
                helptext += "%s -- %s\n" % (cmd, get_color(trim(func.__doc__.strip("\n").splitlines()[0]), "green"))
            helptext += "\nType \"help\" followed by subcommand for full documentation."
        else:
            if cmd in self.commands:
                func = getattr(self, cmd)
                lines = trim(func.__doc__).splitlines()
                helptext += get_color(lines[0],"green") + "\n"
                for line in lines[1:]:
                    if "Usage:" in line:
                        helptext += get_color(line,"blue") + "\n"
                    else:
                        helptext += line + "\n"
            else:
                for c in self.commands:
                    if not c.startswith("_") and cmd in c:
                        func = getattr(self, c)
                        helptext += "%s -- %s\n" % (c, get_color(trim(func.__doc__.strip("\n").splitlines()[0]),"green"))


        return helptext

    def help(self, *arg):
        """
        Akash - Print the usage manual for PEDA command

        Usage:
            MYNAME
            MYNAME command
        """
        helptext=self._get_helptext(*arg)
        print(helptext)

        return
    help.options = commands


    def start(self, *arg):
        print("akashCmd::start")
        inst = main_inst()
        inst.check(helptext)
        self._execute("start")
        return


class akashGDBCommand(gdb.Command):
    # akash command's wrapper class
    def __init__(self, cmdname="akash"):
        self.cmdname = cmdname
        self.__doc__ = akashCmd._get_helptext()
        super(akashGDBCommand, self).__init__(self.cmdname, gdb.COMMAND_DATA)

    def invoke(self, arg_string, from_tty): # used by akash help
        print("akash GDB invoke func")
        self.dont_repeat()
        arg = arg_string.split(' ')
        print("arg", arg, arg_string)
        if len(arg) < 1:
            akashCmd.help()
        else:
            cmd = arg[0] if len(arg)==1 else arg[1]
            if cmd in akashCmd.commands:
                func = getattr(akashCmd, cmd)
                func()
            else:
                print("Undefined command: %s. Try \"akash help\"" % cmd)
        return


class Overload(gdb.Command):
    """
    Overload the GDB start command
    """
    def __init__(self, alias, command, shorttext=1):
        (cmd, opt) = (command + " ").split(" ", 1)
        if cmd == "akash":
            cmd = opt.split(" ")[0]
        if not shorttext:
            self.__doc__ = akashCmd._get_helptext(cmd)
        else:
            self.__doc__ = green("Alias for '%s'" % command)
        self._command = command
        self._alias = alias
        super(Overload, self).__init__(alias, gdb.COMMAND_NONE)

    def invoke(self, args, from_tty):
        self.dont_repeat()
        gdb.execute("%s %s" %(self._command, args))


# Driver code for AKASH
akashCmd = AkashCmd()
akashCmd.help.__func__.options = akashCmd.commands # XXX HACK

akashGDBCommand()
print("akashGDBCommand started")

for cmd in akashCmd.commands:
    func = getattr(akashCmd, cmd)
    func.__func__.__doc__ = func.__doc__.replace("MYNAME", cmd)
    #if cmd not in ["help", "show", "set"]:
    #    Overload(cmd, "akash %s" % cmd, 0) ## to override start of GDB

# handle SIGINT / Ctrl-C
def sigint_handler(signal, frame):
    print("ctrl+c interupt recieved")
    warning_msg("SIGINT from keyboard recieved")
    gdb.execute("set logging off")
    raise KeyboardInterrupt
signal.signal(signal.SIGINT, sigint_handler)

# misc gdb settings
akashCmd._execute("set prompt \001%s\002" % get_color("\002gdb-akash$\001", "green")) # custom prompt

