from bot.helper.telegram_helper.message_utils import sendMessage
from telegram.ext import run_async
from bot import AUTHORIZED_CHATS, SUDO_USERS, dispatcher
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from telegram.ext import Filters
from telegram import Update
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.db_handler import DbManger


@run_async
def authorize(update,context):
    reply_message = None
    message_ = None
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    if len(message_) == 2:
        chat_id = int(message_[1])
        if chat_id not in AUTHORIZED_CHATS:
            msg = DbManger().db_auth(chat_id)
        else:
            msg = '𝚄𝚜𝚎𝚛 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍'
    else:
        if reply_message is None:
            # Trying to authorize a chat
            chat_id = update.effective_chat.id
            if chat_id not in AUTHORIZED_CHATS:
                msg = DbManger().db_auth(chat_id)
            else:
                msg = '𝙰𝚕𝚛𝚎𝚊𝚍𝚢 𝚞𝚗𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚌𝚑𝚊𝚝'

        else:
            # Trying to authorize someone in specific
            user_id = reply_message.from_user.id
            if user_id not in AUTHORIZED_CHATS:
                msg = DbManger().db_auth(user_id)
            else:
                msg = 'User already authorized'
    sendMessage(msg, context.bot, update)


@run_async
def unauthorize(update,context):
    reply_message = None
    message_ = None
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    if len(message_) == 2:
        chat_id = int(message_[1])
        if chat_id in AUTHORIZED_CHATS:
            msg = DbManger().db_unauth(chat_id)
        else:
            msg = 'User already unauthorized'
    else:
        if reply_message is None:
            # Trying to unauthorize a chat
            chat_id = update.effective_chat.id
            if chat_id in AUTHORIZED_CHATS:
                msg = DbManger().db_unauth(chat_id)
            else:
                msg = 'Already unauthorized chat'
        else:
            # Trying to authorize someone in specific
            user_id = reply_message.from_user.id
            if user_id in AUTHORIZED_CHATS:
                msg = DbManger().db_unauth(user_id)
            else:
                msg = '𝚄𝚜𝚎𝚛 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚞𝚗𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍'
    sendMessage(msg, context.bot, update)


@run_async
def addSudo(update,context):
    reply_message = None
    message_ = None
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    if len(message_) == 2:
        chat_id = int(message_[1])
        if chat_id not in SUDO_USERS:
            msg = DbManger().db_addsudo(chat_id)
        else:
            msg = '𝙰𝚕𝚛𝚎𝚊𝚍𝚢 𝚂𝚞𝚍𝚘'
    else:
        if reply_message is None:
            msg = "𝙶𝚒𝚟𝚎 𝙸𝙳 𝚘𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚖𝚎𝚜𝚜𝚊𝚐𝚎 𝚘𝚏 𝚠𝚑𝚘𝚖 𝚢𝚘𝚞 𝚠𝚊𝚗𝚝 𝚝𝚘 𝙿𝚛𝚘𝚖𝚘𝚝𝚎"
        else:
            # Trying to authorize someone in specific
            user_id = reply_message.from_user.id
            if user_id not in SUDO_USERS:
                msg = DbManger().db_addsudo(user_id)
            else:
                msg = '𝙰𝚕𝚛𝚎𝚊𝚍𝚢 𝚂𝚞𝚍𝚘'
    sendMessage(msg, context.bot, update)


@run_async
def removeSudo(update,context):
    reply_message = None
    message_ = None
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ') 
    if len(message_) == 2:
        chat_id = int(message_[1])
        if chat_id in SUDO_USERS:
            msg = DbManger().db_rmsudo(chat_id)
        else:
            msg = 'Not a Sudo'
    else:
        if reply_message is None:
            msg = "𝙶𝚒𝚟𝚎 𝙸𝙳 𝚘𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚖𝚎𝚜𝚜𝚊𝚐𝚎 𝚘𝚏 𝚠𝚑𝚘𝚖 𝚢𝚘𝚞 𝚠𝚊𝚗𝚝 𝚝𝚘 𝚛𝚎𝚖𝚘𝚟𝚎 𝚏𝚛𝚘𝚖 𝚂𝚞𝚍𝚘"
        else:
            user_id = reply_message.from_user.id
            if user_id in SUDO_USERS:
                msg = DbManger().db_rmsudo(user_id)
            else:
                msg = '𝙽𝚘𝚝 𝚊 𝚂𝚞𝚍𝚘'
    sendMessage(msg, context.bot, update)


@run_async
def sendAuthChats(update,context):
    user = sudo = ''
    user += '\n'.join(str(id) for id in AUTHORIZED_CHATS)
    sudo += '\n'.join(str(id) for id in SUDO_USERS)
    sendMessage(f'<b><u>✅𝙰𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝙲𝚑𝚊𝚝𝚜💭</u></b>\n{user}\n<b><u>🥷𝚂𝚞𝚍𝚘 𝚄𝚜𝚎𝚛𝚜🥷</u></b>\n{sudo}', context.bot, update)


send_auth_handler = CommandHandler(command=BotCommands.AuthorizedUsersCommand, callback=sendAuthChats,
                                    filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
authorize_handler = CommandHandler(command=BotCommands.AuthorizeCommand, callback=authorize,
                                    filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
unauthorize_handler = CommandHandler(command=BotCommands.UnAuthorizeCommand, callback=unauthorize,
                                    filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
addsudo_handler = CommandHandler(command=BotCommands.AddSudoCommand, callback=addSudo,
                                    filters=CustomFilters.owner_filter)
removesudo_handler = CommandHandler(command=BotCommands.RmSudoCommand, callback=removeSudo,
                                    filters=CustomFilters.owner_filter)

dispatcher.add_handler(send_auth_handler)
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(unauthorize_handler)
dispatcher.add_handler(addsudo_handler)
dispatcher.add_handler(removesudo_handler)
