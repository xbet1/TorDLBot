import psycopg2
from psycopg2 import Error
from bot import AUTHORIZED_CHATS, SUDO_USERS, DB_URI, LOGGER

class DbManger:
    def __init__(self):
        self.err = False

    def connect(self):
        try:
            self.conn = psycopg2.connect(DB_URI)
            self.cur = self.conn.cursor()
        except psycopg2.DatabaseError as error :
            LOGGER.error("Error in dbMang : ", error)
            self.err = True

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def db_auth(self,chat_id: int):
        self.connect()
        if self.err :
            return "T𝚑𝚎𝚛𝚎'𝚜 𝚜𝚘𝚖𝚎 𝚎𝚛𝚛𝚘𝚛 𝚌𝚑𝚎𝚌𝚔 𝚕𝚘𝚐 𝚏𝚘𝚛 𝚍𝚎𝚝𝚊𝚒𝚕𝚜"
        else:
            sql = 'INSERT INTO users VALUES ({});'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            AUTHORIZED_CHATS.add(chat_id)
            return '𝙰𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢😉'

    def db_unauth(self,chat_id: int):
        self.connect()
        if self.err :
            return "T𝚑𝚎𝚛𝚎'𝚜 𝚜𝚘𝚖𝚎 𝚎𝚛𝚛𝚘𝚛 𝚌𝚑𝚎𝚌𝚔 𝚕𝚘𝚐 𝚏𝚘𝚛 𝚍𝚎𝚝𝚊𝚒𝚕𝚜"
        else:
            sql = 'DELETE from users where uid = {};'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            AUTHORIZED_CHATS.remove(chat_id)
            if chat_id in SUDO_USERS:
                SUDO_USERS.remove(chat_id)
            return '𝚄𝚗𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢😐'

    def db_addsudo(self,chat_id: int):
        self.connect()
        if self.err :
            return "T𝚑𝚎𝚛𝚎'𝚜 𝚜𝚘𝚖𝚎 𝚎𝚛𝚛𝚘𝚛 𝚌𝚑𝚎𝚌𝚔 𝚕𝚘𝚐 𝚏𝚘𝚛 𝚍𝚎𝚝𝚊𝚒𝚕𝚜"
        else:
            if chat_id in AUTHORIZED_CHATS:
                sql = 'UPDATE users SET sudo = TRUE where uid = {};'.format(chat_id)
                self.cur.execute(sql)
                self.conn.commit()
                self.disconnect()
                SUDO_USERS.add(chat_id)
                return '𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢 𝚙𝚛𝚘𝚖𝚘𝚝𝚎𝚍 𝚊𝚜 𝚜𝚞𝚍𝚘🤗'
            else:
                sql = 'INSERT INTO users VALUES ({},TRUE);'.format(chat_id)
                self.cur.execute(sql)
                self.conn.commit()
                self.disconnect()
                AUTHORIZED_CHATS.add(chat_id)
                SUDO_USERS.add(chat_id)
                return '𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢 𝙰𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚊𝚗𝚍 𝚙𝚛𝚘𝚖𝚘𝚝𝚎𝚍 𝚊𝚜 𝚜𝚞𝚍𝚘🤗'

    def db_rmsudo(self,chat_id: int):
        self.connect()
        if self.err :
            return "T𝚑𝚎𝚛𝚎'𝚜 𝚜𝚘𝚖𝚎 𝚎𝚛𝚛𝚘𝚛 𝚌𝚑𝚎𝚌𝚔 𝚕𝚘𝚐 𝚏𝚘𝚛 𝚍𝚎𝚝𝚊𝚒𝚕𝚜"
        else:
            sql = 'UPDATE users SET sudo = FALSE where uid = {};'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            SUDO_USERS.remove(chat_id)
            return '𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢 𝚛𝚎𝚖𝚘𝚟𝚎𝚍 𝚏𝚛𝚘𝚖 𝚂𝚞𝚍𝚘😐'
