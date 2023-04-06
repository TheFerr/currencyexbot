import requests
import json

class BrokerAPI:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> str:
        from config import tokenCu
        from config import currs
        if type(amount) != float and type(amount) != int:
            raise ValueError(f'Invalid amount parameter: {str(amount)}')
        if amount <= 0:
            raise ValueError(f'Amount parameter should not be less or equal 0:')
        baseISO = currs[base]
        quoteISO = currs[quote]
        baseURL = 'https://min-api.cryptocompare.com'
        try:
            r = requests.get(f'{baseURL}/data/pricemulti?fsyms={baseISO}&tsyms={quoteISO}&api_key={tokenCu}').content
            texts = json.loads(r)
            result = float(texts[baseISO][quoteISO]) * amount
            # print(texts)
            # print(result)

        except requests.exceptions.ConnectionError:
            raise ValueError(f'API can not connect to server {baseURL}')
        except KeyError:
            raise ValueError(f'API do not found pair {baseISO} > {quoteISO}')


        else:
            return str(result)

    @staticmethod
    def get_synonym(curr: str) -> str:
        from config import synon
        synonymKeyList = [_ for _ in synon.keys()]
        if curr in synonymKeyList: # if currency name specified correctly
            return curr
        else:
            for i in synonymKeyList:  # try to find in synonym dictionary
                if synon[i].find(curr) > -1:
                    return i
        raise ValueError(f'Currency name did not find in our DB: {curr}')

    @staticmethod
    def check_input(intext: str) -> list:
        tlist = intext.lower().split(' ')
        if len(tlist)<3:
            raise ValueError('Invalid request format - less than 3 parameters space separated')
        if len(tlist) > 3:
            raise ValueError('Invalid request format - greater than 3 parameters space separated')
        if tlist[2].find(',')>-1:
            tlist[2] = tlist[2].replace(',','.')
        tlist[2]=float(tlist[2])
        return tuple(tlist)