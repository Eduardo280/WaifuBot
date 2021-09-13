# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev

import re
import urllib
from glob import glob
from os import remove
from random import choices

from telegraph import Telegraph
from telegraph import upload_file as upl

from . import *

# --------------------------------------------------------------------#
telegraph = Telegraph()
r = telegraph.create_account(short_name="Waifu")
auth_url = r["auth_url"]
# --------------------------------------------------------------------#


TOKEN_FILE = "resources/auths/auth_token.txt"


@callback(
    re.compile(
        "ebk_(.*)",
    ),
)
async def eupload(event):
    match = event.pattern_match.group(1).decode("utf-8")
    await event.answer("Uploading..")
    try:
        await event.edit(
            file=f"https://www.gutenberg.org/files/{match}/{match}-pdf.pdf"
        )
    except BaseException:
        book = "Waifu-Book.epub"
        urllib.request.urlretrieve(
            "https://www.gutenberg.org/ebooks/132.epub.images", book
        )
        fn, media, _ = await asst._file_to_media(
            book, thumb="resources/extras/ultroid.jpg"
        )
        await event.edit(file=media)
        remove(book)


@callback(
    re.compile(
        "sndplug_(.*)",
    ),
)
async def send(eve):
    name = (eve.data_match.group(1)).decode("UTF-8")
    thumb = ""
    for m in choices(sorted(glob("resources/extras/*.jpg"))):
        thumb += m
    if name.startswith("def"):
        plug_name = name.replace(f"def_plugin_", "")
        plugin = f"plugins/{plug_name}.py"
        buttons = [
            [
                Button.inline(
                    "« ᴄᴏʟᴀʀ »",
                    data=f"pasta-{plugin}",
                )
            ],
            [
                Button.inline("« ᴠᴏʟᴛᴀʀ", data="back"),
                Button.inline("ꜰᴇᴄʜᴀʀ", data="close"),
            ],
        ]
    else:
        plug_name = name.replace(f"add_plugin_", "")
        plugin = f"addons/{plug_name}.py"
        buttons = [
            [
                Button.inline(
                    "« ᴄᴏʟᴀʀ »",
                    data=f"pasta-{plugin}",
                )
            ],
            [
                Button.inline("« ᴠᴏʟᴛᴀʀ", data="buck"),
                Button.inline("ꜰᴇᴄʜᴀʀ", data="close"),
            ],
        ]
    await eve.edit(file=plugin, thumb=thumb, buttons=buttons)


@callback("updatenow")
@owner
async def update(eve):
    repo = Repo()
    ac_br = repo.active_branch
    ups_rem = repo.remote("upstream")
    if Var.HEROKU_API:
        import heroku3

        try:
            heroku = heroku3.from_key(Var.HEROKU_API)
            heroku_app = None
            heroku_applications = heroku.apps()
        except BaseException:
            return await eve.edit("`HEROKU_API errado.`")
        for app in heroku_applications:
            if app.name == Var.HEROKU_APP_NAME:
                heroku_app = app
        if not heroku_app:
            await eve.edit("`HEROKU_APP_NAME errado.`")
            repo.__del__()
            return
        await eve.edit(
            "`Atualização em andamento, por favor aguarde.`"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + Var.HEROKU_API + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
        except GitCommandError as error:
            await eve.edit(f"`Aqui está o log de erros:\n{error}`")
            repo.__del__()
            return
        await eve.edit("`Atualizado com sucesso!\nReiniciando, aguarde...`")
    else:
        await eve.edit(
            "`Atualização em andamento, por favor aguarde.`"
        )
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await updateme_requirements()
        await eve.edit(
            "`Atualizado com sucesso!\nReiniciando, aguarde...`"
        )
        execl(sys.executable, sys.executable, "-m", "pyUltroid")


@callback("changes")
@owner
async def changes(okk):
    repo = Repo.init()
    ac_br = repo.active_branch
    changelog, tl_chnglog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    changelog_str = changelog + f"\n\nClique no botão abaixo para atualizar!"
    if len(changelog_str) > 1024:
        await okk.edit(get_string("upd_4"))
        await asyncio.sleep(2)
        with open(f"waifu_updates.txt", "w+") as file:
            file.write(tl_chnglog)
        await okk.edit(
            get_string("upd_5"),
            file="waifu_updates.txt",
            buttons=Button.inline("Atualizar Agora", data="updatenow"),
        )
        remove(f"waifu_updates.txt")
        return
    else:
        await okk.edit(
            changelog_str,
            buttons=Button.inline("Atualizar Agora", data="updatenow"),
            parse_mode="html",
        )


@callback(
    re.compile(
        "pasta-(.*)",
    ),
)
@owner
async def _(e):
    ok = (e.data_match.group(1)).decode("UTF-8")
    with open(ok, "r") as hmm:
        _, key = get_paste(hmm.read())
    if _ == "dog":
        link = "https://del.dog/" + key
        raw = "https://del.dog/raw/" + key
    else:
        link = "https://nekobin.com/" + key
        raw = "https://nekobin.com/raw/" + key
    if ok.startswith("plugins"):
        buttons = [
            Button.inline("« ᴠᴏʟᴛᴀʀ", data="back"),
            Button.inline("ꜰᴇᴄʜᴀʀ", data="close"),
        ]
    else:
        buttons = [
            Button.inline("« ᴠᴏʟᴛᴀʀ", data="buck"),
            Button.inline("ꜰᴇᴄʜᴀʀ", data="close"),
        ]
    await e.edit(
        f"<strong>Pasted\n     👉<a href={link}>[Link]</a>\n     👉<a href={raw}>[Raw Link]</a></strong>",
        buttons=buttons,
        link_preview=False,
        parse_mode="html",
    )


@callback("authorise")
@owner
async def _(e):
    if not e.is_private:
        return
    if not udB.get("GDRIVE_CLIENT_ID"):
        return await e.edit(
            "O ID do client e o secret estão vazios.\nPreencha primeiro.",
            buttons=Button.inline("Back", data="gdrive"),
        )
    storage = await create_token_file(TOKEN_FILE, e)
    authorize(TOKEN_FILE, storage)
    f = open(TOKEN_FILE)
    token_file_data = f.read()
    udB.set("GDRIVE_TOKEN", token_file_data)
    await e.reply(
        "`Successo!\nVocê está pronto para usar o Google Drive com Waifu Userbot.`",
        buttons=Button.inline("ᴍᴇɴᴜ ɪɴɪᴄɪᴀʟ", data="setter"),
    )


@callback("folderid")
@owner
async def _(e):
    if not e.is_private:
        return
    await e.edit(
        "Envie sua FOLDER ID\n\n"
        + "Para FOLDER ID:\n"
        + "1. Abra Google Drive.\n"
        + "2. Crie uma pasta.\n"
        + "3. Altere essa pasta para publica.\n"
        + "4. Copie o link da pasta.\n"
        + "5. Envia todos as letras depois de id= .",
    )
    async with asst.conversation(e.sender_id) as conv:
        reply = conv.wait_event(events.NewMessage(from_users=e.sender_id))
        repl = await reply
        udB.set("GDRIVE_FOLDER_ID", repl.text)
        await repl.reply(
            "Sucesso, agora você pode autorizar.",
            buttons=get_back_button("gdrive"),
        )


@callback("clientsec")
@owner
async def _(e):
    if not e.is_private:
        return
    await e.edit("Send your CLIENT SECRET")
    async with asst.conversation(e.sender_id) as conv:
        reply = conv.wait_event(events.NewMessage(from_users=e.sender_id))
        repl = await reply
        udB.set("GDRIVE_CLIENT_SECRET", repl.text)
        await repl.reply(
            "Successo!\nAgora você pode autorizar ou adicionar FOLDER ID.",
            buttons=get_back_button("gdrive"),
        )


@callback("clientid")
@owner
async def _(e):
    if not e.is_private:
        return
    await e.edit("Envie sua ID CLIENTE que termina com .com")
    async with asst.conversation(e.sender_id) as conv:
        reply = conv.wait_event(events.NewMessage(from_users=e.sender_id))
        repl = await reply
        if not repl.text.endswith(".com"):
            return await repl.reply("`CLIENT ID errado`")
        udB.set("GDRIVE_CLIENT_ID", repl.text)
        await repl.reply(
            "Sucesso, agora defina CLIENT SECRET",
            buttons=get_back_button("gdrive"),
        )


@callback("gdrive")
@owner
async def _(e):
    if not e.is_private:
        return
    await e.edit(
        "[Clique aqui](https://console.developers.google.com/flows/enableapi?apiid=drive) e obtenha CLIENT ID e CLIENT SECRET",
        buttons=[
            [
                Button.inline("Cʟɪᴇɴᴛ Iᴅ", data="clientid"),
                Button.inline("Cʟɪᴇɴᴛ Sᴇᴄʀᴇᴛ", data="clientsec"),
            ],
            [
                Button.inline("Fᴏʟᴅᴇʀ Iᴅ", data="folderid"),
                Button.inline("Aᴜᴛʜᴏʀɪsᴇ", data="authorise"),
            ],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="otvars")],
        ],
        link_preview=False,
    )


@callback("otvars")
@owner
async def otvaar(event):
    await event.edit(
        "Outras variáveis para definir para WaifuBot:",
        buttons=[
            [
                Button.inline("Tᴀɢ Lᴏɢɢᴇʀ", data="taglog"),
                Button.inline("SᴜᴘᴇʀFʙᴀɴ", data="sfban"),
            ],
            [
                Button.inline("Sᴜᴅᴏ Mᴏᴅᴇ", data="sudo"),
                Button.inline("Hᴀɴᴅʟᴇʀ", data="hhndlr"),
            ],
            [
                Button.inline("Exᴛʀᴀ Pʟᴜɢɪɴs", data="plg"),
                Button.inline("Aᴅᴅᴏɴs", data="eaddon"),
            ],
            [
                Button.inline("Eᴍᴏᴊɪ ɪɴ Hᴇʟᴘ", data="emoj"),
                Button.inline("Sᴇᴛ ɢDʀɪᴠᴇ", data="gdrive"),
            ],
            [Button.inline("Inline Pic", data="inli_pic")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="setter")],
        ],
    )


@callback("emoj")
@owner
async def emoji(event):
    await event.delete()
    pru = event.sender_id
    var = "EMOJI_IN_HELP"
    name = f"Emoji em `{HNDLR}help` menu"
    async with event.client.conversation(pru) as conv:
        await conv.send_message("Enviar emoji que você deseja definir 🙃.\n\nUse /cancel para cancelar.")
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("otvars"),
            )
        elif themssg.startswith(("/", HNDLR)):
            return await conv.send_message(
                "Emoji Incorreta",
                buttons=get_back_button("otvars"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} alterado para {themssg}\n",
                buttons=get_back_button("otvars"),
            )


@callback("plg")
@owner
async def pluginch(event):
    await event.delete()
    pru = event.sender_id
    var = "PLUGIN_CHANNEL"
    name = "Plugin Channel"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "Enviar id ou nome de usuário de um canal de onde você deseja instalar todos os plugins\n\nNosso Canal~ @ultroidplugins\n\nUse /cancel para.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("otvars"),
            )
        elif themssg.startswith(("/", HNDLR)):
            return await conv.send_message(
                "Canal Incorreto",
                buttons=get_back_button("otvars"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                "{} mudado para {}\n Depois de definir todas as coisas, reinicie".format(
                    name,
                    themssg,
                ),
                buttons=get_back_button("otvars"),
            )


@callback("hhndlr")
@owner
async def hndlrr(event):
    await event.delete()
    pru = event.sender_id
    var = "HNDLR"
    name = "Handler/ Trigger"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"Envie o símbolo que você deseja como Handler/Trigger para usar bot\nSeu Handler atual é [ `{HNDLR}` ]\n\n use /cancel cancelar.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("otvars"),
            )
        elif len(themssg) > 1:
            return await conv.send_message(
                "Handler Incorreto",
                buttons=get_back_button("otvars"),
            )
        elif themssg.startswith(("/", "#", "@")):
            return await conv.send_message(
                "Isso não pode ser usado como Handler",
                buttons=get_back_button("otvars"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} mudado para {themssg}",
                buttons=get_back_button("otvars"),
            )


@callback("taglog")
@owner
async def tagloggrr(e):
    await e.edit(
        "Escolha uma opção",
        buttons=[
            [Button.inline("SET TAG LOG", data="settag")],
            [Button.inline("DELETE TAG LOG", data="deltag")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="otvars")],
        ],
    )


@callback("deltag")
@owner
async def delfuk(e):
    udB.delete("TAG_LOG")
    await e.answer("Done!!! TAG lOG Off")


@callback("settag")
@owner
async def taglogerr(event):
    await event.delete()
    pru = event.sender_id
    var = "TAG_LOG"
    name = "Tag Log Group"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"Faça um grupo, adicione seu assistente e torne-o administrador.\nPegue o `{hndlr}id` desse grupo e enviá-lo aqui para logs de tag.\n\nUse /cancel para cancelar.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("taglog"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} mudado para {themssg}",
                buttons=get_back_button("taglog"),
            )


@callback("eaddon")
@owner
async def pmset(event):
    await event.edit(
        "ADDONS~ Extra Plugins:",
        buttons=[
            [Button.inline("Aᴅᴅᴏɴs  Oɴ", data="edon")],
            [Button.inline("Aᴅᴅᴏɴs  Oғғ", data="edof")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="otvars")],
        ],
    )


@callback("edon")
@owner
async def eddon(event):
    var = "ADDONS"
    await setit(event, var, "True")
    await event.edit(
        "Feito! ADDONS foi ativado!!\n\n Depois de definir todas as coisas, reinicie",
        buttons=get_back_button("eaddon"),
    )


@callback("edof")
@owner
async def eddof(event):
    var = "ADDONS"
    await setit(event, var, "False")
    await event.edit(
        "Feito! ADDONS foi desativado!! Depois de definir todas as coisas, reinicie",
        buttons=get_back_button("eaddon"),
    )


@callback("sudo")
@owner
async def pmset(event):
    await event.edit(
        f"SUDO MODE ~ Some peoples can use ur Bot which u selected. To know More use `{HNDLR}help sudo`",
        buttons=[
            [Button.inline("Sᴜᴅᴏ Mᴏᴅᴇ  Oɴ", data="onsudo")],
            [Button.inline("Sᴜᴅᴏ Mᴏᴅᴇ  Oғғ", data="ofsudo")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="otvars")],
        ],
    )


@callback("onsudo")
@owner
async def eddon(event):
    var = "SUDO"
    await setit(event, var, "True")
    await event.edit(
        "Feito! SUDO MODE foi ligado!!\n\n Depois de definir todas as coisas, reinicie",
        buttons=get_back_button("sudo"),
    )


@callback("ofsudo")
@owner
async def eddof(event):
    var = "SUDO"
    await setit(event, var, "False")
    await event.edit(
        "Feito! SUDO MODE foi desligado!! Depois de definir todas as coisas, reinicie",
        buttons=get_back_button("sudo"),
    )


@callback("sfban")
@owner
async def sfban(event):
    await event.edit(
        "SuperFban Config:",
        buttons=[
            [Button.inline("ɢʀᴜᴘᴏ ꜰʙᴀɴ", data="sfgrp")],
            [Button.inline("ᴇxᴄʟᴜɪʀ ꜰᴇᴅs", data="sfexf")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="otvars")],
        ],
    )


@callback("sfgrp")
@owner
async def sfgrp(event):
    await event.delete()
    name = "FBan Group ID"
    var = "FBAN_GROUP_ID"
    pru = event.sender_id
    async with asst.conversation(pru) as conv:
        await conv.send_message(
            f"Faça um grupo, adicione @MissRose_Bot, envie `{hndlr}id`, copie e envie aqui.\nUse /cancel para voltar.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("sfban"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} changed to {themssg}",
                buttons=get_back_button("sfban"),
            )


@callback("sfexf")
@owner
async def sfexf(event):
    await event.delete()
    name = "Excluded Feds"
    var = "EXCLUDE_FED"
    pru = event.sender_id
    async with asst.conversation(pru) as conv:
        await conv.send_message(
            f"Envie os IDs do Fed que você deseja excluir do banimento. Dividido por um espaço.\nex`id1 id2 id3`\nDefinir como `None` se você não quiser.\nUse /cancel para voltar.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("sfban"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} mudado para {themssg}",
                buttons=get_back_button("sfban"),
            )


@callback("alvcstm")
@owner
async def alvcs(event):
    await event.edit(
        f"Customize seu {HNDLR}alive. Escolha uma das opções abaixo -",
        buttons=[
            [Button.inline("Aʟɪᴠᴇ Tᴇxᴛ", data="alvtx")],
            [Button.inline("Aʟɪᴠᴇ ᴍᴇᴅɪᴀ", data="alvmed")],
            [Button.inline("Dᴇʟᴇᴛᴇ Aʟɪᴠᴇ Mᴇᴅɪᴀ", data="delmed")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="setter")],
        ],
    )


@callback("alvtx")
@owner
async def name(event):
    await event.delete()
    pru = event.sender_id
    var = "ALIVE_TEXT"
    name = "ᴛᴇxᴛᴏ ᴀʟɪᴠᴇ"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Texto Alive**\nInsira o novo texto para seu alive.\n\nUse /cancel para cancelar.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("alvcstm"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                "{} mudado para {}\n\nDepois de definir todas as coisas, reinicie".format(
                    name,
                    themssg,
                ),
                buttons=get_back_button("alvcstm"),
            )


@callback("alvmed")
@owner
async def media(event):
    await event.delete()
    pru = event.sender_id
    var = "ALIVE_PIC"
    name = "Alive Media"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Alive Midia**\nEnvie-me uma imagem/gif/código de API de bot do sicker para definir como mídia ativa.\n\nUse /cancel para cancelar.",
        )
        response = await conv.get_response()
        try:
            themssg = response.message.message
            if themssg == "/cancel":
                return await conv.send_message(
                    "Operação cancelada!!",
                    buttons=get_back_button("alvcstm"),
                )
        except BaseException:
            pass
        media = await event.client.download_media(response, "alvpc")
        if (
            not (response.text).startswith("/")
            and not response.text == ""
            and not response.media
        ):
            url = response.text
        else:
            try:
                x = upl(media)
                url = f"https://telegra.ph/{x[0]}"
                remove(media)
            except BaseException:
                return await conv.send_message(
                    "Terminado.",
                    buttons=get_back_button("alvcstm"),
                )
        await setit(event, var, url)
        await conv.send_message(
            f"{name} foi definido.",
            buttons=get_back_button("alvcstm"),
        )


@callback("delmed")
@owner
async def dell(event):
    try:
        udB.delete("ALIVE_PIC")
        return await event.edit("Done!", buttons=get_back_button("alvcstm"))
    except BaseException:
        return await event.edit(
            "Algo deu errado...",
            buttons=get_back_button("alvcstm"),
        )


@callback("pmcstm")
@owner
async def alvcs(event):
    await event.edit(
        "Customise suas configs de PMPERMIT -",
        buttons=[
            [
                Button.inline("ᴛᴇxᴛᴏ ᴘᴍ", data="pmtxt"),
                Button.inline("ᴘᴍ ᴍɪᴅɪᴀ", data="pmmed"),
            ],
            [
                Button.inline("ᴀᴜᴛᴏ ᴀᴘʀᴏᴠᴀʀ", data="apauto"),
                Button.inline("ʟᴏɢ ᴘᴍ", data="pml"),
            ],
            [
                Button.inline("ᴅᴇꜰɪɴɪʀ ᴀᴠɪsᴏs", data="swarn"),
                Button.inline("ᴅᴇʟᴇᴛᴇ ᴘᴍ ᴍɪᴅɪᴀ", data="delpmmed"),
            ],
            [Button.inline("ᴛɪᴘᴏ ᴅᴇ ᴘᴍᴘᴇʀᴍɪᴛ", data="pmtype")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="ppmset")],
        ],
    )


@callback("pmtype")
@owner
async def pmtyp(event):
    await event.edit(
        "Selecione o tipo de PMPermit.",
        buttons=[
            [Button.inline("ɪɴʟɪɴᴇ", data="inpm_in")],
            [Button.inline("ɴᴏʀᴍᴀʟ", data="inpm_no")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="pmcstm")],
        ],
    )


@callback("inpm_in")
@owner
async def inl_on(event):
    var = "INLINE_PM"
    await setit(event, var, "True")
    await event.edit(
        f"Feito!! O tipo de PMPermit foi definido como inline!",
        buttons=[[Button.inline("« ᴠᴏʟᴛᴀʀ", data="pmtype")]],
    )


@callback("inpm_no")
@owner
async def inl_on(event):
    var = "INLINE_PM"
    await setit(event, var, "False")
    await event.edit(
        f"Feito!! O tipo de PMPermit foi definido como normal!",
        buttons=[[Button.inline("« ᴠᴏʟᴛᴀʀ", data="pmtype")]],
    )


@callback("pmtxt")
@owner
async def name(event):
    await event.delete()
    pru = event.sender_id
    var = "PM_TEXT"
    name = "PM Text"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Texto PM**\nInsira o novo texto para o pmpermit.\n\nVocê pode usar `{name}` `{fullname}` `{count}` `{mention}` `{username}` para obter isso do usuário também\n\nUse /cancel para cancelar.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("pmcstm"),
            )
        else:
            if len(themssg) > 4090:
                return await conv.send_message(
                    "Mensagem muito longa!\nEmvie uma mensagem mais curta!!",
                    buttons=get_back_button("pmcstm"),
                )
            await setit(event, var, themssg)
            await conv.send_message(
                "{} mudado para {}\n\nDepois de definir todas as coisas, reinicie".format(
                    name,
                    themssg,
                ),
                buttons=get_back_button("pmcstm"),
            )


@callback("swarn")
@owner
async def name(event):
    m = range(1, 10)
    tultd = [Button.inline(f"{x}", data=f"wrns_{x}") for x in m]
    lst = list(zip(tultd[::3], tultd[1::3], tultd[2::3]))
    lst.append([Button.inline("« ᴠᴏʟᴛᴀʀ", data="pmcstm")])
    await event.edit(
        "Selecione o número de avisos para um usuário antes de ser bloqueado em PMs.",
        buttons=lst,
    )


@callback(re.compile(b"wrns_(.*)"))
@owner
async def set_wrns(event):
    value = int(event.data_match.group(1).decode("UTF-8"))
    dn = udB.set("PMWARNS", value)
    if dn:
        await event.edit(
            f"PM Avisos definido para {value}.\nNovos usuarios tem {value} chances em PMs antes de ser banido.",
            buttons=get_back_button("pmcstm"),
        )
    else:
        await event.edit(
            f"Algo deu errado, por favor, verifique seu {hndlr}logs!",
            buttons=get_back_button("pmcstm"),
        )


@callback("pmmed")
@owner
async def media(event):
    await event.delete()
    pru = event.sender_id
    var = "PMPIC"
    name = "PM Media"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**PM Midia**\nEnvie-me uma foto/gif/link para definir como mídia de pmpermit.\n\nUse /cancel para cancelar.",
        )
        response = await conv.get_response()
        try:
            themssg = response.message.message
            if themssg == "/cancel":
                return await conv.send_message(
                    "Operação cancelada!!",
                    buttons=get_back_button("pmcstm"),
                )
        except BaseException:
            pass
        media = await event.client.download_media(response, "pmpc")
        if (
            not (response.text).startswith("/")
            and not response.text == ""
            and not response.media
        ):
            url = response.text
        else:
            try:
                x = upl(media)
                url = f"https://telegra.ph/{x[0]}"
                remove(media)
            except BaseException:
                return await conv.send_message(
                    "Terminado.",
                    buttons=get_back_button("pmcstm"),
                )
        await setit(event, var, url)
        await conv.send_message(
            f"{name} foi definido.",
            buttons=get_back_button("pmcstm"),
        )


@callback("delpmmed")
@owner
async def dell(event):
    try:
        udB.delete("PMPIC")
        return await event.edit("Done!", buttons=get_back_button("pmcstm"))
    except BaseException:
        return await event.edit(
            "Something went wrong...",
            buttons=[[Button.inline("« Sᴇᴛᴛɪɴɢs", data="setter")]],
        )


@callback("apauto")
@owner
async def apauto(event):
    await event.edit(
        "Isso vai aprovar automaticamente as mensagens enviadas",
        buttons=[
            [Button.inline("Aᴜᴛᴏ Aᴘᴘʀᴏᴠᴇ ON", data="apon")],
            [Button.inline("Aᴜᴛᴏ Aᴘᴘʀᴏᴠᴇ OFF", data="apof")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="pmcstm")],
        ],
    )


@callback("apon")
@owner
async def apon(event):
    var = "AUTOAPPROVE"
    await setit(event, var, "True")
    await event.edit(
        f"Feito!! AUTOAPROVE  Iniciado!!",
        buttons=[[Button.inline("« ᴠᴏʟᴛᴀʀ", data="apauto")]],
    )


@callback("apof")
@owner
async def apof(event):
    try:
        udB.delete("AUTOAPPROVE")
        return await event.edit(
            "Feito! AUTOAPROVE Desativado!!",
            buttons=[[Button.inline("« ᴠᴏʟᴛᴀʀ", data="apauto")]],
        )
    except BaseException:
        return await event.edit(
            "Algo deu errado...",
            buttons=[[Button.inline("« Sᴇᴛᴛɪɴɢs", data="setter")]],
        )


@callback("pml")
@owner
async def alvcs(event):
    await event.edit(
        "PMLOGGER Isso encaminhará seu PM para seu grupo privado -",
        buttons=[
            [Button.inline("PMLOGGER ON", data="pmlog")],
            [Button.inline("PMLOGGER OFF", data="pmlogof")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="pmcstm")],
        ],
    )


@callback("pmlog")
@owner
async def pmlog(event):
    var = "PMLOG"
    await setit(event, var, "True")
    await event.edit(
        f"Feito!! PMLOGGER  Iniciado!!",
        buttons=[[Button.inline("« ᴠᴏʟᴛᴀʀ", data="pml")]],
    )


@callback("pmlogof")
@owner
async def pmlogof(event):
    try:
        udB.delete("PMLOG")
        return await event.edit(
            "Feito! PMLOGGER Desativado!!",
            buttons=[[Button.inline("« ᴠᴏʟᴛᴀʀ", data="pml")]],
        )
    except BaseException:
        return await event.edit(
            "Something went wrong...",
            buttons=[[Button.inline("« Sᴇᴛᴛɪɴɢs", data="setter")]],
        )


@callback("ppmset")
@owner
async def pmset(event):
    await event.edit(
        "PMPermit config:",
        buttons=[
            [Button.inline("ᴀᴛɪᴠᴀʀ ᴘᴍᴘᴇʀᴍɪᴛ", data="pmon")],
            [Button.inline("ᴅᴇsᴀᴛɪᴠᴀʀ ᴘᴍᴘᴇʀᴍɪᴛ", data="pmoff")],
            [Button.inline("ᴄᴜsᴛᴏᴍɪᴢᴀʀ ᴘᴍᴘᴇʀᴍɪᴛ", data="pmcstm")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="setter")],
        ],
    )


@callback("pmon")
@owner
async def pmonn(event):
    var = "PMSETTING"
    await setit(event, var, "True")
    await event.edit(
        f"Feito! PMPermit foi ativado!!",
        buttons=[[Button.inline("« ᴠᴏʟᴛᴀʀ", data="ppmset")]],
    )


@callback("pmoff")
@owner
async def pmofff(event):
    var = "PMSETTING"
    await setit(event, var, "False")
    await event.edit(
        f"Feito! PMPermit foi desativado!!",
        buttons=[[Button.inline("« ᴠᴏʟᴛᴀʀ", data="ppmset")]],
    )


@callback("chatbot")
@owner
async def chbot(event):
    await event.edit(
        f"Neste recurso, você pode conversar com as pessoas através do seu bot assistente.\n[Mais Informações](https://t.me/UltroidUpdates/2)",
        buttons=[
            [Button.inline("ᴀᴛɪᴠᴀʀ ᴄʜᴀᴛ ʙᴏᴛ", data="onchbot")],
            [Button.inline("ᴅᴇsᴀᴛɪᴠᴀʀ ᴄʜᴀᴛ ʙᴏᴛ", data="ofchbot")],
            [Button.inline("ʙᴏᴀs ᴠɪɴᴅᴀs", data="bwel")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="setter")],
        ],
        link_preview=False,
    )


@callback("bwel")
@owner
async def name(event):
    await event.delete()
    pru = event.sender_id
    var = "STARTMSG"
    name = "Mensagem de boas-vindas do bot:"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Mensagem de Boas-Vindas**\nDigite a mensagem que você deseja mostrar quando alguém iniciar o seu Bot assistente.\nVocê pode usar `{me}` , `{mention}` \nUse /cancel para cancelar.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("chatbot"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                "{} mudado para {}".format(
                    name,
                    themssg,
                ),
                buttons=get_back_button("chatbot"),
            )


@callback("onchbot")
@owner
async def chon(event):
    var = "PMBOT"
    await setit(event, var, "True")
    await event.edit(
        "Feito! Agora você pode conversar com pessoas através deste bot",
        buttons=[Button.inline("« ᴠᴏʟᴛᴀʀ", data="chatbot")],
    )


@callback("ofchbot")
@owner
async def chon(event):
    var = "PMBOT"
    await setit(event, var, "False")
    await event.edit(
        "Feito! Chat Bot foi desativado.",
        buttons=[Button.inline("« ᴠᴏʟᴛᴀʀ", data="chatbot")],
    )


@callback("vcb")
@owner
async def vcb(event):
    await event.edit(
        f"Com este recurso, VOCÊ pode tocar músicas no chat de voz em grupo\n\n[mais informações](https://t.me/UltroidUpdates/4)",
        buttons=[
            [Button.inline("VC Sᴇssɪᴏɴ", data="vcs")],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="setter")],
        ],
        link_preview=False,
    )


@callback("vcs")
@owner
async def name(event):
    await event.delete()
    pru = event.sender_id
    var = "VC_SESSION"
    name = "VC SESSION"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Vc session**\nEnter the New session u generated for vc bot.\n\nUse /cancel to terminate the operation.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("vcb"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                "{} changed to {}\n\nAfter Setting All Things Do restart".format(
                    name,
                    themssg,
                ),
                buttons=get_back_button("vcb"),
            )


@callback("inli_pic")
@owner
async def media(event):
    await event.delete()
    pru = event.sender_id
    var = "INLINE_PIC"
    name = "Inline Media"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Inline Midia**\nEnvie-me uma foto/gif/link para definir como mídia inline.\n\nUse /cancel para cancelar.",
        )
        response = await conv.get_response()
        try:
            themssg = response.message.message
            if themssg == "/cancel":
                return await conv.send_message(
                    "Operação cancelada!!",
                    buttons=get_back_button("setter"),
                )
        except BaseException:
            pass
        media = await event.client.download_media(response, "inlpic")
        if (
            not (response.text).startswith("/")
            and not response.text == ""
            and not response.media
        ):
            url = response.text
        else:
            try:
                x = upl(media)
                url = f"https://telegra.ph/{x[0]}"
                remove(media)
            except BaseException:
                return await conv.send_message(
                    "Terminado.",
                    buttons=get_back_button("setter"),
                )
        await setit(event, var, url)
        await conv.send_message(
            f"{name} foi definido.",
            buttons=get_back_button("setter"),
        )
