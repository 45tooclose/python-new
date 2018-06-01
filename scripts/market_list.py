from requests import get
from lxml import html
import io
import json

def create_symbol_dict():
    PATH_COINCAP_SITE="https://coinmarketcap.com/exchanges/volume/24-hour/all"
    result = get(PATH_COINCAP_SITE)
    market_list = []

    root = html.fromstring(result.content)
    markets = root.xpath('//td/h3/a')


    for market in markets:
        print(market.text_content())
        market_list.append(market.text_content())

    json_dict = {'Amount':(str(len(markets))),'markets': market_list}

    with io.open("../res/txt_corp/market_list.json", "w", encoding="utf-8") as f:
        json.dump(json_dict,f,indent=4,separators=(',', ': '),ensure_ascii=False)

def main():
    create_symbol_dict()

if __name__ == '__main__':
    main()