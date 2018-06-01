import json
import io

"""
Taken from https://api.coinmarketcap.com/v2/listings/

straszne gowno
"""

class coins_list:
    """
    json_data struct:
    data:
          [i]
              id:
              name:
              symbol:
              website_slug:
    """
    json_data = {}

    # symbol_dict
    #   name    :   symbol
    symbol_dict = {}

    def open_file(self, f_name):

        with io.open(f_name, "r", encoding="utf-8") as f:
            self.json_data = json.load(f)

    """ For test only"""
    def get_website_slug(self):
        # print(json_data['data'][0]['symbol'])
        json_data = self.json_data
        for i, x in enumerate(json_data['data']):
            print(i)
            json_data['data'][i]['name'] = json_data['data'][i]['name'].lower()
            #json_data['data'][i]['name'] = json_data['data'][i]['name'].replace(" ", "-")

            if not json_data['data'][i]['name'] == json_data['data'][i]['website_slug']:
                print(json_data['data'][i]['name'], json_data['data'][i]['website_slug'])

    def create_symbol_dict(self):
        json_data = self.json_data
        symbol_dict = {}
        for i, x in enumerate(json_data['data']):
            name = json_data['data'][i]['name']
            symbol = json_data['data'][i]['symbol']
            website_slug = json_data['data'][i]['website_slug']
            symbol_dict[name] = [symbol,name,website_slug]
        symbol_dict["length"]=str(len(symbol_dict))
        self.symbol_dict = symbol_dict

    def write_file(self,f_name):
        with io.open(f_name,'w',encoding="utf-8") as f:
            json.dump(self.symbol_dict,f,indent=4,separators=(',', ': '), ensure_ascii=False)

def main():
    PATH_COIN_SOURCE = "../res/txt_corp/listings.json"
    PATH_COIN_LIST = "../res/txt_corp/coin_list.json"

    cl = coins_list()
    cl.open_file(PATH_COIN_SOURCE)
    cl.create_symbol_dict()
    cl.write_file(PATH_COIN_LIST)


if __name__ == "__main__":
    main()
