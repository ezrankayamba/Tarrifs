from bs4 import BeautifulSoup
import requests
import csv
from collections import OrderedDict

url = 'https://www.airtel.co.tz/cms/webpage/dataTable?opco=TZ&tableType=myairtel_social_packs&tableSubType=one'
r = requests.get(url)
data = r.json()
field_names = ['amount_from', 'amount_to', 'fee_p2p_onnet', 'fee_p2p_xnet', 'fee_cashout', 'fee_otf']
with open('data/airtel_fees.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    for row in data:
        p2p_onnet = row['c3'].strip().replace(',', '')
        if p2p_onnet == 'BURE':
            p2p_onnet = 0
        p2p_xnet = row['c4'].strip().replace(',', '')
        if p2p_xnet == '-':
            p2p_xnet = 'N/A'
        co = row['c5'].strip().replace(',', '')
        if co == '-':
            co = 'N/A'
        row = {
            'amount_from': row['c1'].strip().replace(',', ''),
            'amount_to': row['c2'].strip().replace(',', ''),
            'fee_p2p_onnet': p2p_onnet,
            'fee_p2p_xnet': p2p_xnet,
            'fee_cashout': co,
            'fee_otf': 'N/A'
        }
        dict = OrderedDict(row.items())
        writer.writerow(dict)
