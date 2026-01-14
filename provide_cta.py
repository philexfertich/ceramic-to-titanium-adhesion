import os
import re
import io
import argparse

import pandas as pd

from seleniumbase import SB

from bs4 import BeautifulSoup


def scrape(url, headless):
    """Fetches raw html of the page."""
    with SB(uc=True, browser='chrome', locale='en', headless=headless) as sb:
        sb.activate_cdp_mode(url)
        sb.sleep(2)
        print(sb.get_title())
        sb.uc_gui_click_captcha()
        sb.sleep(1.1)
        return sb.get_html()


def extract(html):
    """Extracts tables from html."""
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
    """Checks if dir exists or creates new one."""
    directory, _ = os.path.split(path)
    
    if not os.path.isdir(directory):
        os.makedirs(directory)
        return False
    
    return True


def load_file(path):
    """Loads file if exists othervise just creates a new dir."""
    if not dir_exist_or_create(path):
        return None
    
    with open(path) as f:
        return f.read()


def save(string, path):
    """Saves data into a new file."""
    with open(path, 'w') as ts:
        ts.write(string)


def main(
    url, 
    raw_data_path, 
    formatted_data_path,
    headless,
    use_selenium
):
    html = load_file(raw_data_path)
    
    if not html or use_selenium:
        html = scrape(url, headless)
        save(html, raw_data_path)
    
    tables = extract(html)

    dfs = pd.read_html(io.StringIO(str(tables)))
    
    dir_exist_or_create(formatted_data_path)
    
    with pd.ExcelWriter(formatted_data_path, engine='openpyxl') as writer:
        for name, df in zip([str(t.attrs['id']) for t in tables], dfs):
            df.to_excel(writer, sheet_name=name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="provideCTA",
        description="Collects data from open scientific sources."
    )
    parser.add_argument('-u', '--url')
    parser.add_argument(
        '-r', 
        '--raw',
        default='./var/prep/tables.html'
    )
    parser.add_argument(
        '-f', 
        '--formatted', 
        default='./var/tables/adhesion.xlsx'
    )
    parser.add_argument(
        '-H',
        '--headless',
        action='store_true'
    )

    parser.add_argument(
        '-s',
        '--use-selenium',
        action='store_true'
    )

    args = parser.parse_args()
    main(
        url=args.url,
        raw_data_path=args.raw,
        formatted_data_path=args.formatted,
        headless=args.headless,
        use_selenium=args.use_selenium
    )