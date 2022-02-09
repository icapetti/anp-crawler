# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface

from re import findall

# Pipeline helper functions
def to_float(value):
    """
    Receives a string that contains a numeric value and converts it to an 
    international standard (. to decimals) and to a float type.
    """

    if value.isdigit():
        return float(value)

    if findall("^[,.]", value):
        return float("0" + value.replace(",", "."))

    cleaned_value = "".join(
        findall("[\d]+\,*\.*[\d]*\,*\.*[\d]+", value.strip())
    )

    if cleaned_value:
        try:
            return float(cleaned_value)
        except ValueError:
            return float(cleaned_value.replace(".", "").replace(",", "."))

    return value

def standardize_field(item, key):
    field_pattern_mapping = {
        'município': string_pattern,
        'estado': string_pattern,
        'combustível': string_pattern,
        'nº de postos': int_pattern,
        'preço médio': decimal_pattern,
        'desvio padrão': decimal_pattern,
        'preço mínimo': decimal_pattern,
        'preço máximo': decimal_pattern,
    }

    chosen_pattern = field_pattern_mapping.get(key)

    return chosen_pattern(item, key)

def string_pattern(item, key) -> str:
    return item.get(key).upper().strip().replace('@', ' ')

def int_pattern(item, key) -> int:
    return int(item.get(key)) if item.get(key).isdigit() else item.get(key)

def decimal_pattern(item, key) -> float:
    return to_float(item.get(key))

class AnpCrawlerPipeline:
    def process_item(self, item, spider):
        for key in item.keys():
            if item.get(key):
                item[key] = standardize_field(item, key)

        return item
