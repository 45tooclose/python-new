from requests import get
from lxml import html
import io
import json


def main():
    result = get("https://coinmarketcap.com/exchanges/volume/24-hour/all")
    print("before get")
    root = html.fromstring(result.content)
    print("after get")
    markets = root.xpath('//td/h3/a')

    market_list=[]

    for market in markets:
        print(market.text_content())
        market_list.append(market.text_content())

    json_dict = {'Amount':(len(markets)),'markets': market_list}

    with io.open("../res/txt_corp/market_list.json", "w", encoding="utf-8") as f:
        json.dump(json_dict,f,indent=4,separators=(',', ': '),ensure_ascii=False)

if __name__ == '__main__':
    main()