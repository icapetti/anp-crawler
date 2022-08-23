"""
TODO: docstring
"""
import scrapy
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from json import load
from datetime import date, datetime


DATE = date.today()
BASE_URI = f's3://da-vinci-raw/crawler-various/anp/run={DATE}/'

MONTH_YEAR = datetime.now().strftime('%m*%Y')

HELPER_FILE = Path(__file__).parents[2] / 'utils' / 'helper_files' / 'anp_states_and_fuels.yaml'
with open(HELPER_FILE) as f:
    HELPER_DATA = yaml.load(f, Loader=SafeLoader)

STATES = HELPER_DATA['states']
FUELS = HELPER_DATA['fuels']

class AnpSpider(scrapy.Spider):
    name = 'anp'
    allowed_domains = ['preco.anp.gov.br']
    start_urls = ['https://preco.anp.gov.br/include/Resumo_Mensal_Index.asp']
    custom_settings = {
        'FEEDS': {
            f'{BASE_URI}%(batch_id)d-{name}-%(batch_time)s.jl.gz': {
                'format': 'jl.gz',
                'encoding': 'utf8',
                'store_empty': False,
            }
        },
    }

    def parse(self, response):
        headers =  {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
            '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,de-DE;q=0.6,de;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'preco.anp.gov.br',
            'Origin': 'https://preco.anp.gov.br',
            'Referer': 'https://preco.anp.gov.br/',
            'Upgrade-Insecure-Requests': '1',
        }

        for state in STATES:
            for fuel in FUELS:
                payload = f'selMes={MONTH_YEAR}&selEstado={state}&selCombustivel={fuel}'

                yield scrapy.Request(
                    url=self.start_urls[0],
                    method='POST',
                    headers=headers,
                    body=payload,
                    dont_filter=True,
                    callback=self.parse_states
                )

    def parse_states(self, response):
        url = 'https://preco.anp.gov.br/include/Resumo_mensal_Municipio.asp'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
            '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,de-DE;q=0.6,de;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host':'preco.anp.gov.br',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = response.request.body.decode('UTF-8')

        yield scrapy.Request(
            url=url,
            method='GET',
            headers=headers,
            body=payload,
            dont_filter=True,
            callback=self.parse_cities
        )

    def parse_cities(self, response):
        state = response.request.body.decode('UTF-8').split('&')[1].split('*')[1]
        fuel = response.request.body.decode('UTF-8').split('&')[2].split('*')[1]
        self.logger.info(f'Parsing cities from {state} state and fuel {fuel}.')

        # Remove unnecessary fields
        trash_keys = ['DADOS MUNICÍPIO', 'pesquisados']
        keys = [i.strip() for i in response.xpath('//*[@id="box"]/table/tr/th/text()').getall() \
            if i.strip() not in trash_keys]

        # Add fields that are not in the website's data structure
        keys.insert(1, 'estado')
        keys.insert(2, 'combustível')

        # Get all cities of the currently state
        cities = [i.strip() for i in response.xpath('//*[@id="box"]/table/tr/td[1]/text()').getall() \
                if 'Preço ao Consumidor' not in i]
        self.logger.info(f'{len(cities)} cities found for state {state}!')

        for city in cities:
            # Get values
            values = response.xpath(f'//td[text()="{city}"]/following-sibling::node()/text()').extract()

            # Add the values of the complementary fields
            values.insert(0, city)
            values.insert(1, state)
            values.insert(2, fuel)

            # Build the final dictionary with the list of keys and the list of values
            data = dict(zip(keys, values))

            yield data
