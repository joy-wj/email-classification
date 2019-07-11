from bs4 import BeautifulSoup
import pandas as pd
from tld import get_tld
import requests
import re
import sys
from multiprocessing import Pool


class Scrape:
    def __init__(self, file_path):
        domains = pd.read_csv(file_path)
        self.urls = ['https://www.' + u for u in domains.domain]

    def scrape(self, url):
        tld, l, f, t, y, i = "N", "N", "N", "N", "N", "N"

        try:
            tld = get_tld(url)
        except:
            pass

        try:
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.text, features="lxml")
        except:
            return url, tld, l, f, t, y, i

        try:
            l = soup.find('a', attrs={'href': re.compile("^https://www.linkedin.com")})['href']
            if l != 'N':
                l = 'Y'
        except:
            pass

        try:
            f = soup.find('a', attrs={'href': re.compile("^https://www.facebook.com")})['href']
            if f != 'N':
                f = 'Y'
        except:
            pass

        try:
            t = soup.find('a', attrs={'href': re.compile("^https://twitter.com")})['href']
            if t != 'N':
                t = 'Y'
        except:
            pass

        try:
            y = soup.find('a', attrs={'href': re.compile("^https://www.youtube.com")})['href']
            if y != 'N':
                y = 'Y'
        except:
            pass

        try:
            i = soup.find('a', attrs={'href': re.compile("^https://www.instagram.com")})['href']
            if i != 'N':
                i = 'Y'
        except:
            pass

        return url, tld, l, f, t, y, i

    def parse(self, url):
        return ','.join(self.scrape(url))

    def write(self, output_path):
        with Pool(24) as p:
            records = p.map(self.parse, self.urls)
        with open(output_path, 'w') as f:
            f.write(','.join(['url', 'tld', 'linkedin', 'facebook', 'twitter', 'youtube', 'instagram']) + '\n')
            f.write('\n'.join(records))


if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    data = Scrape(input_path)
    data.write(output_path)


