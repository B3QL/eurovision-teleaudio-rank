#!/usr/bin/env python3
#-*-coding: utf-8-*-

from collections import defaultdict
from lxml import html
import requests

url = "http://www.eurovision.tv/page/results"
event_id = 1893  # Eurovision Song Contest 2014 Grand Final
xpaths = {"country_name": '//*[@id="content-wrap"]/div[2]/div/div/div[6]/div/table/tbody/tr[*]/td[1]/text()',
          "televoting_rank": '//*[@id="content-wrap"]/div[2]/div/div/div[6]/div/table/tbody/tr[*]/td[9]/text()'
          }

points = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]
results = defaultdict(int)
countries = {"AL": "Albania", "AM": "Armenia", "AT": "Austria", "AZ": "Azerbaijan", "BY": "Belarus",
             "BE": "Belgium", "DK": "Denmark", "EE": "Estonia", "MK": "F.Y.R. Macedonia",
             "FI": "Finland", "FR": "France", "GE": "Georgia", "DE": "Germany", "GR": "Greece",
             "HU": "Hungary", "IS": "Iceland", "IE": "Ireland", "IL": "Israel", "IT": "Italy",
             "LV": "Latvia", "LT": "Lithuania", "MT": "Malta", "MD": "Moldova", "ME": "Montenegro",
             "NO": "Norway", "PL": "Poland", "PT": "Portugal", "RO": "Romania", "RU": "Russia",
             "SM": "San Marino", "SI": "Slovenia", "ES": "Spain", "SE": "Sweden", "CH": "Switzerland",
             "NL": "The Netherlands", "UA": "Ukraine", "GB": "United Kingdom"
             }

for country_code in countries.keys():
    page = requests.get(url, params={"event": event_id, "voter": country_code})
    print("[FETCH]", countries[country_code], page.url)

    tree = html.fromstring(page.text)
    for country, rank in zip(tree.xpath(xpaths['country_name']), tree.xpath(xpaths['televoting_rank'])):
        country_code = list(countries.keys())[list(countries.values()).index(str(country).strip())]
        try:
            results[country_code] += points[int(rank) - 1]  # ranks starts from 1 to n
        except IndexError as e:
            pass  # Country don't get any points

for i, country_code in enumerate(sorted(results, key=results.get, reverse=True)):
    print(i + 1, countries[country_code], "-", results[country_code])