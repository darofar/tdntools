# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from hashlib import md5


class Activity(scrapy.Item):
    """
    A single activity from http://jornadas-tdn.org/
    """
    id = scrapy.Field()
    event_name = scrapy.Field()
    game = scrapy.Field()
    category = scrapy.Field()
    director = scrapy.Field()
    organization = scrapy.Field()
    description = scrapy.Field()
    complementary = scrapy.Field()
    when = scrapy.Field()
    where = scrapy.Field()
    starts_at = scrapy.Field()
    ends_at = scrapy.Field()
    schedule = scrapy.Field()

    def set_time_schedule(self, date):
        self['when'] = date.split("\n")[0]
        self['where'] = date.split("\n")[2].strip() if len(date.split("\n")) > 2 else ""
        m = re.match(r".*de (.*) a (.*).*", date)
        self['starts_at'] = "" if m.lastindex < 1 else m.group(1)
        self['ends_at'] = "" if m.lastindex < 2 else m.group(2)
        print(self)
        self['schedule'] = ""
        if self['starts_at']:
            start_as_int = int(str(self['starts_at']).replace(":", ""))
            if start_as_int < 1300:
                self['schedule'] = "mañana"
            elif start_as_int < 2000:
                self['schedule'] = "tarde"
            else:
                self['schedule'] = "noche"

    def set_id(self, date, tdn_id):
        str_id = str(date + tdn_id).encode('utf-8')
        md5_id = md5()
        md5_id.update(str_id)
        self['id'] = md5_id.hexdigest()


