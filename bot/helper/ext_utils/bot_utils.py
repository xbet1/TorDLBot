import logging
import re
import threading
import time

from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import download_dict, download_dict_lock

LOGGER = logging.getLogger(__name__)

MAGNET_REGEX = r"magnet:\?xt=urn:btih:[a-zA-Z0-9]*"

URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"


class MirrorStatus:
    STATUS_UPLOADING = "𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐...📤"
    STATUS_DOWNLOADING = "𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐...📥"
    STATUS_WAITING = "𝚀𝚞𝚎𝚞𝚎𝚍...📝"
    STATUS_FAILED = "𝙵𝚊𝚒𝚕𝚎𝚍 🚫. 𝙲𝚕𝚎𝚊𝚗𝚒𝚗𝚐 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍..."
    STATUS_CANCELLED = "𝙲𝚊𝚗𝚌𝚎𝚕𝚕𝚎𝚍 ❌. 𝙲𝚕𝚎𝚊𝚗𝚒𝚗𝚐 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍..."
    STATUS_ARCHIVING = "𝙰𝚛𝚌𝚑𝚒𝚟𝚒𝚗𝚐...🔐"
    STATUS_EXTRACTING = "𝙴𝚡𝚝𝚛𝚊𝚌𝚝𝚒𝚗𝚐...📂"


PROGRESS_MAX_SIZE = 100 // 8
PROGRESS_INCOMPLETE = ['█', '█', '█', '█', '█', '█', '█']

SIZE_UNITS = ['𝙱', '𝙺𝙱', '𝙼𝙱', '𝙶𝙱', '𝚃𝙱', '𝙿𝙱']


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'


def getDownloadByGid(gid):
    with download_dict_lock:
        for dl in download_dict.values():
            status = dl.status()
            if status != MirrorStatus.STATUS_UPLOADING and status != MirrorStatus.STATUS_ARCHIVING \
                    and status != MirrorStatus.STATUS_EXTRACTING:
                if dl.gid() == gid:
                    return dl
    return None


def get_progress_bar_string(status):
    completed = status.processed_bytes() / 8
    total = status.size_raw() / 8
    if total == 0:
        p = 0
    else:
        p = round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 8
    cPart = p % 8 - 1
    p_str = '█' * cFull
    if cPart >= 0:
        p_str += PROGRESS_INCOMPLETE[cPart]
    p_str += '░' * (PROGRESS_MAX_SIZE - cFull)
    p_str = f"[{p_str}]"
    return p_str


def get_readable_message():
    with download_dict_lock:
        msg = ""
        for download in list(download_dict.values()):
            msg += f"<b>📂𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎:</b> <code>{download.name()}</code>"
            msg += f"\n<b>🥏𝚂𝚝𝚊𝚝𝚞𝚜:</b> <i>{download.status()}</i>"
            if download.status() != MirrorStatus.STATUS_ARCHIVING and download.status() != MirrorStatus.STATUS_EXTRACTING:
                msg += f"\n<code>{get_progress_bar_string(download)} {download.progress()}</code>"
                if download.status() == MirrorStatus.STATUS_DOWNLOADING:
                    msg += f"\n<b>🔻𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚍:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
                else:
                    msg += f"\n<b>🔺𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚍:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
                msg += f"\n<b>🚀𝚂𝚙𝚎𝚎𝚍:</b> {download.speed()} | <b>⏳𝙴T𝙰:</b> {download.eta()} "
                # if hasattr(download, 'is_torrent'):
                try:
                    msg += f"\n<b>🧲𝚂𝚎𝚎𝚍𝚎𝚛𝚜:</b> {download.aria_download().num_seeders}" \
                        f" | <b>🛰𝙿𝚎𝚎𝚛𝚜:</b> {download.aria_download().connections}"
                except:
                    pass
            if download.status() == MirrorStatus.STATUS_DOWNLOADING:
                msg += f"\n<b>💥T𝚘 𝚂𝚝𝚘𝚙👉:</b> <code>/{BotCommands.CancelMirror} {download.gid()}</code>"
            msg += "\n\n"
        return msg


def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}𝚍'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}𝚑'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}𝚖'
    seconds = int(seconds)
    result += f'{seconds}𝚜'
    return result


def is_url(url: str):
    url = re.findall(URL_REGEX, url)
    if url:
        return True
    return False


def is_mega_link(url: str):
    return "mega.nz" in url

def get_mega_link_type(url: str):
    if "folder" in url:
        return "folder"
    elif "file" in url:
        return "file"
    elif "/#F!" in url:
        return "folder"
    return "file"

def is_magnet(url: str):
    magnet = re.findall(MAGNET_REGEX, url)
    if magnet:
        return True
    return False

def new_thread(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
