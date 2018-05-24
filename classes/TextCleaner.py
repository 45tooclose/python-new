
import io
import re

class TextCleaner:

    text = ""
    #test
    f_name = ""
    links_list =[]
    special_chars = []
    dates_list = []

    #TODO adding one list of removed chars, add deleted matches position(low priority)
    def open_file(self):
        try:
            f = io.open(self.f_name, "r", encoding="utf-8")
            self.text = f.read()
        except FileNotFoundError:
            print("File Not Found")
        else:
            f.close()

    # Clears  binded wrods
    def clear_binded_words(self):

        # Function for detecting binded words 'XXYy' splitting them

        def clean_XXYy():
            re_pattern_split = '(([A-Z]+([a-z])))'
            re_matches_split = re.findall(re_pattern_split, self.text)
            for match in re_matches_split:
                if match[0].__len__() > 2:
                    #  print(match[0])
                    fixed_match = match[0][:-2] + " " + match[0][-2:]
                    self.text = self.text.replace(match[0], fixed_match)

        # pattern for detecting binded words 'xxYy' splitting them

        def clean_xxYy():
            re_pattern_split = '(([a-z])+([A-Z]))'
            re_matches_split = re.findall(re_pattern_split, self.text)
            for match in re_matches_split:
                fixed_match = match[0][:-1] + " " + match[0][-1]
                self.text = self.text.replace(match[0], fixed_match)

        clean_XXYy()
        clean_xxYy()

    # Clears links
    def clear_links(self):
        # pattern for main site names
        re_pattern = '(http|ftp|https)\:\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
        re_match = re.findall(re_pattern, self.text)
        for match in re_match:
            # print(match[0],match[1],match[2])
            match_str = ''.join(match[0]) + '://'
            match_str += ''.join(match[1])
            match_str += ''.join(match[2])
            self.text = self.text.replace(match_str, " ")
            self.links_list.append(match_str)

    # Clears special chars

    def find_special_chars(self):

        # Finding special characters

        for char in self.text:
            if not char.isalnum() and not char.isspace():
                # print(char, char.isalnum(), char.isspace())
                if not char in self.special_chars:
                    self.special_chars.append(char)
                else:
                    pass

    # Find dates using regex

    def clear_dates(self):

        re_pattern_date = '(([0-9]{2,4})(\/|\-|\s)([0-9]{1,2})(\/|\-|\s)([0-9]{1,4}))'
        re_match = re.findall(re_pattern_date, self.text)

        for match in re_match:
            self.dates_list.append(match[0])
            self.text = self.text.replace(match[0], " ")

    # Clears special characters

    def clear_special_char(self):
        for char in self.text:
            if char in self.special_chars:
                self.text = self.text.replace(char, " ")

    # Clears digitis

    def clear_digits(self):
        for char in self.text:
            if char.isdigit():
                self.text = self.text.replace(char, " ")

    # Clears multispace

    def clear_multispace(self):
        self.text = ' '.join(self.text.split())

    # text words to list
    # return words_list

    def text_to_list(self):
        words= self.text.split()
        return words

    def lower_text(self):
        self.text = self.text.lower()

    def clear_text(self):
        self.clear_binded_words()
        self.clear_links()
        self.find_special_chars()
        self.clear_dates()
        self.clear_special_char()
        self.clear_digits()
        self.clear_multispace()
        self.lower_text()

    def get_text(self):
        return self.text

    def __init__(self, file_name=None,txt=None):

        if file_name is not None:
            self.f_name=file_name

        if txt is None:
            self.open_file()
        else:
            self.text =txt

def main():
    pass

if __name__=="__main__":
    main()