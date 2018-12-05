import records
from sqlalchemy.exc import IntegrityError

class DatabaseHelper:

    def __init__(self):
        self.db = records.Database('sqlite:///crawler_database.db')

    def create_schema(self):
        self.db.query('''CREATE TABLE IF NOT EXISTS links (
            url text PRIMARY KEY,
            created_at datetime,
            visited_at datetime NULL)''')
        self.db.query('''CREATE TABLE IF NOT EXISTS numbers (url text, number integer,
            PRIMARY KEY (url, number))''')

    def store_link(self,url):
        try:
            self.db.query('''INSERT INTO links (url, created_at)
                    VALUES (:url, CURRENT_TIMESTAMP)''', url=url)
        except IntegrityError as ie:
            # This link already exists, do nothing
            pass

    def store_number(self,url, number):
        try:
            self.db.query('''INSERT INTO numbers (url, number)
                    VALUES (:url, :number)''', url=url, number=number)
        except IntegrityError as ie:
            # This number already exists, do nothing
            pass
    def last_visited(self):
        link = self.db.query('''SELECT * FROM links
                        ORDER BY created_at LIMIT 1''').first()
        return None if link is None else link.url


    def mark_visited(self,url):
        self.db.query('''UPDATE links SET visited_at=CURRENT_TIMESTAMP
                WHERE url=:url''', url=url)

    def get_random_unvisited_link(self):
        link = self.db.query('''SELECT * FROM links
                        WHERE visited_at IS NULL
                        ORDER BY RANDOM() LIMIT 1''').first()
        return None if link is None else link.url

    def get_last_visited(self):
        link = self.db.query('''SELECT * FROM links
                        WHERE visited_at IS NULL
                        ORDER BY visited_at LIMIT 1''').first()
        return None if link is None else link.url