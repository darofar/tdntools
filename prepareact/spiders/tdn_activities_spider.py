from prepareact.spiders import tdn_activities_config as config
import scrapy


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
        print("\n\n<<<<<< - >>>>>>>")
        print(urls)
        print("<<<<<< - >>>>>>>\n\n")
        for single_activity in urls:
            yield response.follow(single_activity, self.parse_single_activity)

        yield scrapy.Request(
            url=config.url_template.replace("offset=0", "offset={}".format(self.offset)),
            callback=self.parse
        )

    def parse_single_activity(self, response):
        extract_info = {
            'event_name': response.css('div.actividad_datos h3::text').extract_first().strip(),
            'game_rules': response.css('div.actividad_datos h4::text').extract_first().strip(),
            'category': response.css('div.actividad_datos h5::text').extract_first().strip(),
            'organanizer': response.css('div.organizador::text').extract()[1].strip(),
            'organization': response.css('h5.organiza strong::text')
                                .extract_first().strip()[len("'Organiza: (") - 1:-1],
            'description': response.css('.actividad_descripcion').extract()[0].strip(),
            'complementary': response.css('.actividad_descripcion').extract()[1].strip()\
                if len(response.css('.actividad_descripcion').extract()) > 2 else "",
            'dates': [date.strip() for date in response.css('span.fecha-actividad::text').extract()]
        }
        from pprint import pprint
        pprint(extract_info)
        yield extract_info
