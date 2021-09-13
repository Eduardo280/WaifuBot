# /usr/bin/python3
# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev

# Standalone file for facilitating local deploys.

import os

a = r"""
===========================================
|             VERSION v1.0.1              |
|              By: @fnixdev               |
|          (C) 2021 - WaifuBot            |
===========================================
"""


def start():

    clear_screen()
    check_for_py()

    print(f"{a}\n\n")
    print("Welcome to Waifu, lets start setting up!\n\n")
    print("Cloning the repository...\n\n")
    try:
        os.system("rm -rf WaifuBot")
    except BaseException:
        pass
    os.system("git clone https://github.com/fnixdev/WaifuBot")
    print("\n\nDone")
    os.chdir("WaifuBot")
    clear_screen()
    print(a)
    print("\n\nLet's start!\n")

    # generate session if needed.
    sessionisneeded = input(
        "Do you want to generate a new session, or have an old session string? [generate/skip]",
    )
    if sessionisneeded == "generate":
        gen_session()
    elif sessionisneeded == "skip":
        pass
    else:
        print(
            'Please choose "generate" to generate a session string, or "skip" to pass on.\n\nPlease run the script again!',
        )
        exit(0)

    # start bleck megik
    print("\n\nLets start entering the variables.\n\n")
    varrs = [
        "API_ID",
        "API_HASH",
        "SESSION",
        "REDIS_URI",
        "REDIS_PASSWORD",
    ]
    all_done = "# WaifuBot Environment Variables.\n# Do not delete this file.\n\n"
    for i in varrs:
        all_done += do_input(i)
    clear_screen()
    print(a)
    print("\n\nHere are the things you've entered.\nKindly check.")
    print(all_done)
    isitdone = input("\n\nIs it all correct? [y/n]")
    if isitdone == "y":
        # https://github.com/fnixdev/WaifuBot/blob/31b9eb1f4f8059e0ae66adb74cb6e8174df12eac/resources/startup/locals.py#L35
        f = open(".env", "w")
        f.write(all_done)
        f.close
    elif isitdone == "n":
        print("Oh, let's redo these then -_-")
        start()
    else:
        # https://github.com/fnixdev/WaifuBot/blob/31b9eb1f4f8059e0ae66adb74cb6e8174df12eac/resources/startup/locals.py#L35
        f = open(".env", "w")
        f.write(all_done)
        f.close
    clear_screen()
    print("\nCongrats. All done!\nTime to start the bot!")
    print("\nInstalling requirements... This might take a while...")
    os.system("pip3 install -r requirements.txt")
    os.system("pip3 install -r resources/extras/local-requirements.txt")
    clear_screen()
    print(a)
    print("\nStarting Waifu...")
    os.system("python3 -m pyUltroid")


def do_input(var):
    val = input(f"Enter your {var}: ")
    to_write = f"{var}={val}\n"
    return to_write


def clear_screen():
    # clear screen
    if os.name == "posix":
        _ = os.system("clear")
    else:
        # for windows platfrom
        _ = os.system("cls")


def check_for_py():
    print(
        "Please make sure you have python installed. \nGet it from http://python.org/\n\n",
    )
    try:
        ch = int(
            input(
                "Enter Choice:\n1. Continue, python is installed.\n2. Exit and install python.\n",
            ),
        )
    except BaseException:
        print("Please run the script again, and enter the choice as a number!!")
        exit(0)
    if ch == 1:
        pass
    elif ch == 2:
        print("Please install python and continue!")
        exit(0)
    else:
        print("Weren't you taught how to read? Enter a choice!!")
        return


def gen_session():
    print("\nProcessing...")
    # https://github.com/fnixdev/WaifuBot/blob/31b9eb1f4f8059e0ae66adb74cb6e8174df12eac/resources/startup/locals.py#L35
    os.system("python3 resources/session/ssgen.py")
    return


start()
