from termcolor import colored

def warn(s):
    print(colored("*** " + s,"red"))

def info(s):
    print(colored("... " + s,"green"))
