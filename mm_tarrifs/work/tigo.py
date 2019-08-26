from bs4 import BeautifulSoup
import requests
import csv
from collections import OrderedDict

url = 'https://www.tigo.co.tz/tigo-pesa-tariffs'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
tbody = soup.table.tbody
field_names = ['amount_from', 'amount_to', 'fee_p2p_onnet', 'fee_p2p_xnet', 'fee_cashout', 'fee_otf']
with open('data/tigo_fees.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    for index, tr in enumerate(tbody.find_all('tr')):
        if index < 2:
            continue
        cols = tr.find_all('td')
        if len(cols) < 4:
            break
        reg = cols[2].text.replace(',', '')
        co = cols[3].text.replace(',', '')
        row = {
            'amount_from': cols[0].text.replace(',', ''),
            'amount_to': cols[1].text.replace(',', ''),
            'fee_p2p_onnet': reg,
            'fee_p2p_xnet': reg,
            'fee_cashout': co,
            'fee_otf': 'N/A' if co == 'N/A' else int(reg) + int(co)
        }
        dict = OrderedDict(row.items())
        writer.writerow(dict)
