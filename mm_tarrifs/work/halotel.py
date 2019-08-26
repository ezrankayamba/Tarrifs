from bs4 import BeautifulSoup
import requests
import csv
from collections import OrderedDict

url = 'http://halotel.co.tz/en/service/halopesa/halopesa'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
tbody = soup.table.tbody
field_names = ['amount_from', 'amount_to', 'fee_p2p_onnet', 'fee_p2p_xnet', 'fee_cashout', 'fee_otf']
with open('data/halotel_fees.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    for index, tr in enumerate(tbody.find_all('tr')):
        if index < 2:
            continue
        cols = tr.find_all('td')
        if len(cols) < 5:
            break
        reg = cols[2].p.text.replace(',', '').strip()
        co = cols[3].p.text.replace(',', '').strip()
        unreg = cols[4].p.text.replace(',', '').strip()
        row = {
            'amount_from': cols[0].p.text.replace(',', '').strip(),
            'amount_to': cols[1].p.text.replace(',', '').strip(),
            'fee_p2p_onnet': reg,
            'fee_p2p_xnet': reg,
            'fee_cashout': co,
            'fee_otf': unreg,
        }
        dict = OrderedDict(row.items())
        writer.writerow(dict)
