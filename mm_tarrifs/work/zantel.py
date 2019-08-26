from bs4 import BeautifulSoup
import requests
import csv
from collections import OrderedDict

url = 'http://www.zantel.co.tz/ezy-pesa-tariffs'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

table = soup.table

tbody = table.tbody
# field_names = ['amount_from', 'amount_to', 'fee_to_registered', 'fee_to_unregistered', 'fee_cashout']
field_names = ['amount_from', 'amount_to', 'fee_p2p_onnet', 'fee_p2p_xnet', 'fee_cashout', 'fee_otf']

with open('data/zantel_fees.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()

    for index, tr in enumerate(tbody.find_all('tr')):
        if index < 2:
            continue
        cols = tr.find_all('td')
        if len(cols) < 4:
            break
        # print(tr.prettify())
        reg = cols[3].text.replace(',', '')
        co = cols[2].text.replace(',', '')
        co = 'N/A' if co == 'none' else co
        row = {
            'amount_from': cols[0].text.replace(',', ''),
            'amount_to': cols[1].text.replace(',', ''),
            'fee_p2p_onnet': reg,
            'fee_p2p_xnet': reg,
            'fee_cashout': co,
            'fee_otf': 'N/A'
        }
        dict = OrderedDict(row.items())
        # print(dict)
        writer.writerow(dict)
