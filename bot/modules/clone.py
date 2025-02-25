from telegram.ext import CommandHandler
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import new_thread
from bot import dispatcher


@new_thread
def cloneNode(update,context):
    args = update.message.text.split(" ",maxsplit=1)
    if update.message.from_user.username:
        uname = f"@{update.message.from_user.username}"
    else:
        uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
    if uname is not None:
            cc = f'\n\n<b>👤𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚛 :</b> {uname}'
    if len(args) > 1:
        link = args[1]
        msg = sendMessage(f"🌈𝙲𝚕𝚘𝚗𝚒𝚗𝚐🌈: <code>{link}</code>",context.bot,update)
        gd = GoogleDriveHelper()
        result, button = gd.clone(link)
        deleteMessage(context.bot,msg)
        if button == "":
            sendMessage(result,context.bot,update)
        else:
            sendMarkup(result + cc,context.bot,update,button)
    else:
        sendMessage("𝙿𝚛𝚘𝚟𝚒𝚍𝚎 𝙶-𝙳𝚛𝚒𝚟𝚎 𝚂𝚑𝚊𝚛𝚎𝚊𝚋𝚕𝚎 𝙻𝚒𝚗𝚔 𝚝𝚘 𝙲𝚕𝚘𝚗𝚎😏.",context.bot,update)

clone_handler = CommandHandler(BotCommands.CloneCommand,cloneNode,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(clone_handler)
