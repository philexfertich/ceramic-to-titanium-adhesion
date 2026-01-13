import os

import pandas as pd

from seleniumbase import SB

from bs4 import BeautifulSoup


# TODO replace search with regex
# TODO implement saving to file
# TODO add CLI
# TODO implement --use-selenium command for CLI to not to bypass seleniumbase
# TODO implement --url command for CLI
# TODO implement --pattern command for CLI
# TODO implement --headless command for CLI
# TODO separate code into modules: Downloader, TableExtractor, DataFormatter


table_title_ids = [f'itad011-T{i}' for i in range(1, 4)]

URL = "https://academic.oup.com/ooms/article/3/1/itad011/7211653"


headers = {'user-agent': 'my-app/0.0.1'}

def main():
    
    with SB(uc=True, browser='chrome', locale='en', headless=False) as sb:
        sb.activate_cdp_mode(URL)

        sb.sleep(2)

        print(sb.get_title())

        sb.uc_gui_click_captcha()

        sb.sleep(1.1)

        soup = BeautifulSoup(sb.get_html(), 'html.parser')

        titles = set(soup.find_all(id=table_title_ids))
        
        def to_table(t):
            table = t.find_next_sibling('div', class_=['table-overflow']).table
            table.attrs['id'] = t['id']
            return table
        
        tables = [to_table(t) for t in titles]
        
        for table in tables:
            print(table)
            print()
            

if __name__ == "__main__":
    main()