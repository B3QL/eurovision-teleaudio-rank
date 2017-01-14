#!/usr/bin/env python3
# -*-coding: utf-8-*-
from operator import itemgetter
from collections import defaultdict
import requests
import lxml.html


URL = 'http://www.eurovision.tv/page/results'
EVENT_ID = 1893  # Eurovision Song Contest 2014 Grand Final
COUNTRY_COLUMN = 1
TELEVOTING_COLUMN = 9
XPATH = ('//*[@id="content"]/div[2]/div/div/div[6]/div/'
         'table/tbody/tr[*]/td[{column}]/text()')

COUNTRIES = ('AL', 'AM', 'AT', 'AZ', 'BY', 'BE', 'DK', 'EE', 'MK',
             'FI', 'FR', 'GE', 'DE', 'GR', 'HU', 'IS', 'IE', 'IL',
             'IT', 'LV', 'LT', 'MT', 'MD', 'ME', 'NO', 'PL', 'PT',
             'RO', 'RU', 'SM', 'SI', 'ES', 'SE', 'CH', 'NL', 'UA',
             'GB')


def parse_html(func):
    def wrapper(*args, **kwargs):
        html = func(*args, **kwargs)
        dom_tree = lxml.html.fromstring(html)
        return dom_tree
    return wrapper


@parse_html
def get_country_page(country_code):
    params = {'event': EVENT_ID, 'voter': country_code}
    page = requests.get(URL, params=params)
    return page.text


def get_points(rank, points=(12, 10, 8, 7, 6, 5, 4, 3, 2, 1)):
    rank = int(rank)
    return points[rank] if rank < len(points) else 0


def get_ranks(dom_tree, column):
    return dom_tree.xpath(XPATH.format(column=column))


def pprint_ranking(ranking):
    ranking = sorted(ranking.items(), key=itemgetter(1), reverse=True)
    for position, (country_name, points) in enumerate(ranking, start=1):
        print('{:3} {} ({})'.format(position, country_name,  points))

if __name__ == '__main__':
    results = defaultdict(int)
    for country_code in COUNTRIES:
        print('Fetching {0} ranking'.format(country_code))
        country_page = get_country_page(country_code)
        participiants = get_ranks(country_page, COUNTRY_COLUMN)
        televoting_ranks = get_ranks(country_page, TELEVOTING_COLUMN)
        for country_name, rank in zip(participiants, televoting_ranks):
            results[country_name] += get_points(rank)

    pprint_ranking(results)
