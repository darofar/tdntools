import sqlite3
from .. import config


class ActivityRepo(object):

    def __init__(self):
        self.conn = sqlite3.connect(config.DATABASE_URI)
        self.check_schema()
        self.batch = {}

    def create_activity(self):
        pass

    def read_activity(self):
        pass

    def start_batch(self):
        self.batch = {}
        return self

    def add_to_batch(self, single_activity):
        if single_activity['id'] not in self.batch:
            self.batch[single_activity['id']] = single_activity
            return True
        return False

    def save_batch(self):
        pass

    def read_batch(self):
        pass

    def check_schema(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS activities (
        id TEXT PRIMARY KEY,
        event_name TEXT,
        game TEXT,
        category TEXT,
        director TEXT,
        organization TEXT,
        description TEXT,
        complementary TEXT,
        when TEXT,
        where TEXT,
        starts_at TEXT,
        ends_at TEXT,
        schedule TEXT
        )""")
