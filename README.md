# ANP
## The project
The Agência Nacional do Petróleo, Gás Natural e Biocombustíveis is the regulatory body for activities that make up the oil and natural gas and biofuels industries in Brazil. The ANP is responsible for the Levantamento de Preços de Combustíveis (LPC), which is the most comprehensive survey of automotive fuel and LPG prices in Brazil, which provides references for the market, government agencies and civil society in general.[Read more](https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/precos-revenda-e-de-distribuicao-combustiveis/levantamento-de-precos-de-combustiveis)

This project extracts fuel data from ANP website and loads as jl.gz format on AWS s3.

## Architecture


## Resources
This project currently uses:
- Python 3.9
- Scrapy 2.5.1
- Spidermon 1.16.2

## Pipeline
Aqui o item extraído pelo crawler passa por uma camada de padronização como uppercase, strip, conversão de tipos e etc.
Não há validação dos dados aqui, apenas algumas pequenas padronizações.

## Crawler Data validation
Validação dos dados gerados usando json-schema.
Aqui está um gerador de schema baseado numa amostra dos dados "ideais": [jsonschema.net](https://www.jsonschema.net/home)

O schema do gerador é básico, para informar campos obrigatórios e tipos. Com essa base gerada é possível fazer diversas outras validações utilizando até mesmo regex para validar uma url ou formato de cep, por exemplo.

Pra ativar o validador é necessário:
1. Salvar o schema gerado numa pasta do repositório
2. Informar no `settings.py` o path do schema:
```python
SPIDERMON_VALIDATION_SCHEMAS = [
    '../anp_crawler/schemas/anp_default_schema.json',
]
```
3. Ativar o pipeline de validação no `settings.py`
```python
ITEM_PIPELINES = {
    'anp_crawler.pipelines.AnpCrawlerPipeline': 300,
    'spidermon.contrib.scrapy.pipelines.ItemValidationPipeline': 800,
}
```

## Crawler monitoring
Foram implementados dois tipos de monitoramento:
- Durante a execução da spider:


- No encerramento da spider:


## Scrapy deployment
### Scrapyd
Scrapyd is a service for running Scrapy spiders. It allows you to deploy your Scrapy projects and control their spiders using an HTTP JSON API. Created by the same developers that developed Scrapy itself, Scrapyd is a tool for running Scrapy spiders in production on remote servers so you don't need to run them on a local machine.

Scrapyd helps manage multiple Scrapy projects and each project can have multiple versions uploaded, but only the latest one will be used for launching new spiders. 

Scrapyd is an application (typically run as a daemon) that listens to requests for spiders to run and spawns a process for each one, like when we run `scrapy crawl myspider` manually in the terminal. 

[Scrapyd repository](https://github.com/scrapy/scrapyd)
[Scrapyd official docs](https://scrapyd.readthedocs.io/en/stable/overview.html)

To start a spider with `Scrapyd`
```
curl http://52.204.150.228:6800/schedule.json \
-d project=anp_crawler \
-d spider=anp

curl http://localhost:6800/schedule.json \
-d project=anp_crawler \
-d spider=anp
```

### Scrapyd-client

Add your ec2 instane to `scrapy.cfg`:

[deploy:aws_target]
url = http://localhost:6800/
project = anp_crawler

## To run this project in your machine
- Create an `.env` file  on `/home/$USER/.credentials/.env` and add your AWS credentials:
```python
aws_id = "YOUR-ID-HERE"
aws_secret = "YOUR-SECRET-HERE"
```

- Add your URI on `anp.py` file:
`BASE_URI = f's3://da-vinci-raw/crawler-various/anp/run={DATE}/'`
