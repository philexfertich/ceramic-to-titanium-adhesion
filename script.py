import os
import re
import io

import pandas as pd

from seleniumbase import SB

from bs4 import BeautifulSoup


# TODO implement saving to file
# TODO add CLI
# TODO implement --use-selenium command for CLI to not to bypass seleniumbase
# TODO implement --url command for CLI
# TODO implement --pattern command for CLI
# TODO implement --headless command for CLI
# TODO separate code into modules: Downloader, TableExtractor, DataFormatter


URL = "https://academic.oup.com/ooms/article/3/1/itad011/7211653"
RAW_DATA_PATH = './var/prep/tables.html'
FORMAT_DATA_PATH = './var/tables/adhesion.xlsx'

def scrape():
    with SB(uc=True, browser='chrome', locale='en', headless=False) as sb:
        sb.activate_cdp_mode(URL)
        sb.sleep(2)
        print(sb.get_title())
        sb.uc_gui_click_captcha()
        sb.sleep(1.1)
        return sb.get_html()


def extract(html) -> list:
    soup = BeautifulSoup(html, 'html.parser')

    def has_id(id):
        return id and re.compile(r"itad011-T\d").fullmatch(id)
    titles = set(soup.find_all(id=has_id))
    
    def to_table(t):
        table = t.find_next_sibling('div', class_=['table-overflow']).table
        table.attrs['id'] = t['id']
        return table

    return [to_table(t) for t in titles]


def dir_exist_or_create(path):
    """False when dir doesnt exists, othervise returns True"""

    directory, _ = os.path.split(path)
    
    if not os.path.isdir(directory):
        os.makedirs(directory)
        # TODO create saving filename and directory to state or top-level
        return False
    
    return True

def load_file(path) -> str:
    if not dir_exist_or_create(path):
        return None
    
    with open(path) as f:
        return f.read()


def save(string, path):
    with open(path, 'w') as ts:
        ts.write(string)


def main():
    html = load_file(RAW_DATA_PATH)
    
    if not html:
        html = scrape()
        save(html, RAW_DATA_PATH)
    
    tables = extract(html)

    dfs = pd.read_html(io.StringIO(str(tables)))
    
    dir_exist_or_create(FORMAT_DATA_PATH)
    with pd.ExcelWriter(FORMAT_DATA_PATH, engine='openpyxl') as writer:
        for name, df in zip([str(t.attrs['id']) for t in tables], dfs):
            print(name, df)
            df.to_excel(writer, sheet_name=name)

if __name__ == "__main__":
    main()