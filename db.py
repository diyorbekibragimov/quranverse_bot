import sqlite3

class BotDB:
    def __init__(self, db_file):
        """Initializing the connection with the database"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Checking whether the user exists"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))
    
    def get_user_id(self, user_id):
        """Getting the database user id from user_id in Telegram"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id),)
        return result.fetchone()[0]

    def get_user_language(self, user_id):
        """Getting the language of the user"""
        result = self.cursor.execute("SELECT `language` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, language):
        """Adding user to the database"""
        self.cursor.execute("INSERT INTO `users` (`user_id`, `language`) VALUES (?, ?)", (user_id, language))
        return self.conn.commit()

    def edit_language(self, user_id, language):
        """Editing the language"""
        self.cursor.execute("UPDATE `users` SET language = ? WHERE user_id = ?", (language, user_id))
        return self.conn.commit()

    def close(self):
        """Closing the connection () -> None"""
        self.conn.close()