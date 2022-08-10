import requests
import json
from config import keys


class ConvertException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise ConvertException('Указаны одинаковые наименования валют!\nПомощь /help\nДоступные валюты /values')
        if base not in keys.keys() or quote not in keys.keys():
            raise ConvertException('Неверный формат!\nПомощь /help\nДоступные валюты /values')
        try:
            float(amount)
        except ValueError:
            raise ConvertException('Неверно указано количество!')
        r = requests.get(f'https://api.exchangerate.host/convert?from={keys[base]}&to={keys[quote]}')
        count = float(json.loads(r.content)['result']) * float(amount)
        return count
