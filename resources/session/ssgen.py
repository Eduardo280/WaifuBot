#!/usr/bin/env bash
# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev

import os
from time import sleep

a = r"""
===========================================
|             VERSION v1.0.1              |
|              By: @fnixdev               |
|          (C) 2021 - WaifuBot            |
===========================================
"""


def spinner(x):
    if x == "tele":
        print("Checking if Telethon is installed...")
    else:
        print("Checking if Pyrogram is installed...")
    for _ in range(3):
        for frame in r"-\|/-\|/":
            print("\b", frame, sep="", end="", flush=True)
            sleep(0.1)


def clear_screen():
    # https://www.tutorialspoint.com/how-to-clear-screen-in-python#:~:text=In%20Python%20sometimes%20we%20have,screen%20by%20pressing%20Control%20%2B%20l%20.
    if os.name == "posix":
        os.system("clear")
    else:
        # for windows platfrom
        os.system("cls")


def get_api_id_and_hash():
    print(
        "Get your API ID and API HASH from my.telegram.org or @ScrapperRoBot to proceed.\n\n",
    )
    try:
        API_ID = int(input("Please enter your API ID: "))
    except ValueError:
        print("APP ID must be an integer.\nQuitting...")
        exit(0)
    API_HASH = input("Please enter your API HASH: ")
    return API_ID, API_HASH


def telethon_session():
    try:
        spinner("tele")

        x = "\bFound an existing installation of Telethon...\nSuccessfully Imported.\n\n"
    except BaseException:
        print("Installing Telethon...")
        os.system("pip install telethon")

        x = "\bDone. Installed and imported Telethon."
    clear_screen()
    print(a)
    print(x)

    # the imports

    from telethon.errors.rpcerrorlist import ApiIdInvalidError, PhoneNumberInvalidError
    from telethon.sessions import StringSession
    from telethon.sync import TelegramClient

    API_ID, API_HASH = get_api_id_and_hash()

    # logging in
    try:
        with TelegramClient(StringSession(), API_ID, API_HASH) as ultroid:
            print("Gerando uma sess�o de usu�rio para KanaBot...")
            ult = ultroid.send_message(
                "me",
                f"**WAIFU** `SESSION`:\n\n`{ultroid.session.save()}`\n\n**N�o compartilhe isso em nenhum lugar!**",
            )
            print(
                "Sua SESSION foi gerada. Verifique suas mensagens salvas do telegrama!"
            )
            exit(0)
    except ApiIdInvalidError:
        print(
            "Sua combina��o API ID / API HASH � inv�lida. Verifique novamente.\nSaindo..."
        )
        exit(0)
    except ValueError:
        print("O HASH da API n�o deve estar vazio! \nSaindo...")
        exit(0)
    except PhoneNumberInvalidError:
        print("O n�mero de telefone � inv�lido!\nSaindo...")
        exit(0)


def pyro_session():
    try:
        spinner("pyro")
        from pyrogram import Client

        x = "\bFound an existing installation of Pyrogram...\nSuccessfully Imported.\n\n"
    except BaseException:
        print("Installing Pyrogram...")
        os.system("pip install pyrogram tgcrypto")
        x = "\bDone. Installed and imported Pyrogram."
    clear_screen()
    print(a)
    print(x)

    # generate a session
    API_ID, API_HASH = get_api_id_and_hash()
    print("Digite o n�mero de telefone quando solicitado.\n\n")
    with Client(":memory:", api_id=API_ID, api_hash=API_HASH) as pyro:
        ss = pyro.export_session_string()
        pyro.send_message(
            "me",
            f"`{ss}`\n\nAcima est� o seu Pyrogram Session String para o bot de m�sica. **N�O COMPARTILHE.**",
        )
        print("A sess�o foi enviada para suas mensagens salvas!")
        exit(0)


def main():
    clear_screen()
    print(a)
    try:
        type_of_ss = int(
            input(
                "\nQual sess�o voc� deseja gerar?\n1. User Session.\n2. Music Session.\n\nDigite a escolha:  "
            )
        )
    except Exception as e:
        print(e)
        exit(0)
    if type_of_ss == 1:
        telethon_session()
    elif type_of_ss == 2:
        pyro_session()
    else:
        print("Lean English.")
        x = input("Run again? (y/n")
        if x == "y":
            main()
        else:
            exit(0)


main()
