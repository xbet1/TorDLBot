import math

import requests
import heroku3

from bot import dispatcher, HEROKU_APP_NAME, HEROKU_API_KEY
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage
from telegram import update
from telegram.ext import run_async, CommandHandler


@run_async
def dyno_usage(update, context):
    heroku_api = "https://api.heroku.com"
    if HEROKU_API_KEY is not None and HEROKU_APP_NAME is not None:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        sendMessage(
            "Please insert your HEROKU_APP_NAME and HEROKU_API_KEY in Vars",
            context.bot,
            update
        )
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/81.0.4044.117 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    session = requests.Session()
    with session as ses:
        with ses.get(heroku_api + path, headers=headers) as r:
            result = r.json()
            """Account Quota."""
            quota = result["account_quota"]
            quota_used = result["quota_used"]
            quota_remain = quota - quota_used
            quota_percent = math.floor(quota_remain / quota * 100)
            minutes_remain = quota_remain / 60
            hours = math.floor(minutes_remain / 60)
            minutes = math.floor(minutes_remain % 60)
            day = math.floor(hours / 24)

            """App Quota."""
            Apps = result["apps"]
            for apps in Apps:
                if apps.get("app_uuid") == app.id:
                    AppQuotaUsed = apps.get("quota_used") / 60
                    AppPercent = math.floor(apps.get("quota_used") * 100 / quota)
                    break
            else:
                AppQuotaUsed = 0
                AppPercent = 0

            AppHours = math.floor(AppQuotaUsed / 60)
            AppMinutes = math.floor(AppQuotaUsed % 60)
            
            sendMessage(
                f"<b>📊𝗗𝘆𝗻𝗼 𝗨𝘀𝗮𝗴𝗲 for</b> <code>{app.name}</code>:\n"
                f"• <code>{AppHours}</code> <b>Hours and</b> <code>{AppMinutes}</code> <b>Minutes - {AppPercent}%</b>\n\n"
                "<b>⌛𝙳𝚢𝚗𝚘 𝚁𝚎𝚖𝚊𝚒𝚗𝚒𝚗𝚐 𝚝𝚑𝚒𝚜 𝚖𝚘𝚗𝚝𝚑:</b>\n"
                f"• <code>{hours}</code> <b>Hours and</b> <code>{minutes}</code> <b>Minutes - {quota_percent}%</b>\n\n"
                "<b>🔋 𝙳𝚢𝚗𝚘 𝙴𝚡𝚙𝚒𝚛𝚎𝚍:</b>\n"
                f"• <code>{day}</code> <b>Days</b>",
                context.bot,
                update
            )
            return True


dyno_usage_handler = CommandHandler(command=BotCommands.UsageCommand, callback=dyno_usage,
                                    filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
                                    
dispatcher.add_handler(dyno_usage_handler)
