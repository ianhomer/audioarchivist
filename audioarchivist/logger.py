from termcolor import colored

DEBUG = False

def warn(s):
    print(colored("*** " + s,"red"))

def info(s):
    print(colored("... " + s,"green"))

def debug(s):
    if DEBUG:
        print("DEBUG : " + s)
