from prepareact.spiders import tdn_activities_config as config
import scrapy
from scrapy.loader import ItemLoader
from prepareact.items import Activity


class TdNActivitiesSpider(scrapy.Spider):
    name = "TdNActivities"
    offset = 0

    def start_requests(self):
        yield scrapy.Request(url=config.url_template, callback=self.parse)

    def parse(self, response):
        # get urls for each activity
        urls = response.css('div.actividad-borde a::attr(href)').extract()
        self.offset = self.offset + len(urls)

        # parse each single activity
        for single_activity in urls:
            yield response.follow(single_activity, self.parse_single_activity)

        yield scrapy.Request(
            url=config.url_template.replace("offset=0", "offset={}".format(self.offset)),
            callback=self.parse
        )

    def get_description(self, html):
        while '>' in html:
            start = html.find("<")
            end = html.find(">") + 1
            html = html[:start] + html[end:]
        return html.strip()

    def parse_single_activity(self, response):

        for date in [date.strip() for date in response.css('span.fecha-actividad::text').extract()]:

            single_activity = Activity()
            single_activity['event_name'] = response.css('div.actividad_datos h3::text').extract_first().strip()
            single_activity['game'] = response.css('div.actividad_datos h4::text').extract_first().strip()
            single_activity['category'] = response.css('div.actividad_datos h5::text').extract_first().strip()
            single_activity['director'] = response.css('div.organizador::text').extract()[1].strip()
            single_activity['organization'] = response.css('h5.organiza strong::text')\
                                                .extract_first().strip()[len("'Organiza: (") - 1:-1]
            single_activity['description'] = self.get_description(response.css('.actividad_descripcion').extract()[0])
            single_activity['complementary'] = self.get_description(response.css('.actividad_descripcion').extract()[1]) \
                if len(response.css('.actividad_descripcion').extract()) > 1 \
                else ""
            single_activity.set_time_schedule(date)
            single_activity.set_id(date, response.url.split("/")[-1])

            from pprint import pprint
            import json
            if single_activity['complementary']:
                pprint(json.dumps(dict(single_activity)))
            yield single_activity
