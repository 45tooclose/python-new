import json
import io

"""
Taken from https://api.coinmarketcap.com/v2/listings/
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

    def get_website_slug(self):
        # print(json_data['data'][0]['symbol'])
        json_data = self.json_data
        for i, x in enumerate(json_data['data']):
            print(i)
            json_data['data'][i]['name'] = json_data['data'][i]['name'].lower()
            json_data['data'][i]['name'] = json_data['data'][i]['name'].replace(" ", "-")

            if not json_data['data'][i]['name'] == json_data['data'][i]['website_slug']:
                print(json_data['data'][i]['name'], json_data['data'][i]['website_slug'])

    def initialize_symbol_dict(self):
        json_data = self.json_data
        symbol_dict = {}
        for i, x in enumerate(json_data['data']):
            name = json_data['data'][i]['website_slug']
            symbol = json_data['data'][i]['symbol']
            symbol_dict[name] = symbol
        self.symbol_dict = symbol_dict

    def write_file(self,f_name):
        with io.open(f_name,'w',encoding="utf-8") as f:
            json.dump(self.symbol_dict,f,ensure_ascii=False)

def main():
    file_name = "../res/txt_corp/listings.json"
    cl = coins_list()
    cl.open_file(file_name)
    cl.initialize_symbol_dict()
    file_name ="../res/txt_corp/coin_list.json"
    cl.write_file(file_name)


if __name__ == "__main__":
    main()
