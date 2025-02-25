from telegram.ext import CommandHandler, run_async
import threading
from telegram import Update
from bot import dispatcher, LOGGER
from bot.helper.telegram_helper.message_utils import auto_delete_message, sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.mirror_utils.upload_utils import gdriveTools

@run_async
def deletefile(update, context):
	msg_args = update.message.text.split(None, 1)
	msg = ''
	try:
		link = msg_args[1]
		LOGGER.info(msg_args[1])
	except IndexError:
		msg = '𝚂𝚎𝚗𝚍 𝚊 𝚕𝚒𝚗𝚔 𝚊𝚕𝚘𝚗𝚐 𝚠𝚒𝚝𝚑 𝚌𝚘𝚖𝚖𝚊𝚗𝚍😏'

	if msg == '' : 
		drive = gdriveTools.GoogleDriveHelper()
		msg = drive.deletefile(link)
	LOGGER.info(f"DeleteFileCmd : {msg}")
	reply_message = sendMessage(msg, context.bot, update)

	threading.Thread(target=auto_delete_message, args=(context.bot, update.message, reply_message)).start()

delete_handler = CommandHandler(command=BotCommands.DeleteCommand, callback=deletefile, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
dispatcher.add_handler(delete_handler)
