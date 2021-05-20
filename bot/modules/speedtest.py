from speedtest import Speedtest
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher, AUTHORIZED_CHATS
from bot.helper.telegram_helper.bot_commands import BotCommands
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext, Filters, run_async, CommandHandler


@run_async
def speedtest(update, context):
    message = update.effective_message
    ed_msg = message.reply_text("🏃‍♂💨𝚁𝚞𝚗𝚗𝚒𝚗𝚐 𝚂𝚙𝚎𝚎𝚍 𝚃𝚎𝚜𝚝 . . . ")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    string_speed = f'''
<b>╭───📟𝕊𝕖𝕣𝕧𝕖𝕣 𝕌𝕤𝕚𝕟𝕘 𝔼𝕟𝕘𝕚𝕟𝕖 𝔸𝕣𝕚𝕒𝟚⚡️</b>
<b>├─📡𝙽𝚊𝚖𝚎:</b> <code>{result['server']['name']}</code>
<b>├─🕹𝙲𝚘𝚞𝚗𝚝𝚛𝚢:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
<b>╰─💶𝚂𝚙𝚘𝚗𝚜𝚘𝚛:</b> <code>{result['server']['sponsor']}</code>
    
<b>╭──────🚀𝕊𝕡𝕖𝕖𝕕𝕋𝕖𝕤𝕥 ℝ𝕖𝕤𝕦𝕝𝕥𝕤💨</b>
<b>├─🔺𝚄𝚙𝚕𝚘𝚊𝚍:</b> <code>{speed_convert(result['upload'] / 8)}</code>
<b>├─🔻𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍:</b>  <code>{speed_convert(result['download'] / 8)}</code>
<b>├─🖲𝙿𝚒𝚗𝚐:</b> <code>{result['ping']} ms</code>
<b>╰─🏬𝙸𝚂𝙿:</b> <code>{result['client']['isp']}</code>
'''
    ed_msg.delete()
    try:
        update.effective_message.reply_photo(path, string_speed, parse_mode=ParseMode.HTML)
    except:
        update.effective_message.reply_text(string_speed, parse_mode=ParseMode.HTML)

def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "MB/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


SPEED_HANDLER = CommandHandler(BotCommands.SpeedCommand, speedtest, 
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)

dispatcher.add_handler(SPEED_HANDLER)
