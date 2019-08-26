from bs4 import BeautifulSoup
import requests
import csv
from collections import OrderedDict

url = 'https://vodacom.co.tz/en/mpesa_tarriffs/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

table = soup.table

tbody = table.tbody
# field_names = ['amount_from', 'amount_to', 'fee_to_registered', 'fee_to_unregistered', 'fee_cashout']
field_names = ['amount_from', 'amount_to', 'fee_p2p_onnet', 'fee_p2p_xnet', 'fee_cashout', 'fee_otf']

with open('data/vodacom_fees.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()

    for tr in tbody.find_all('tr'):
        cols = tr.find_all('td')
        if len(cols) == 5:
            row = {
                'amount_from': cols[0].text.replace(',', ''),
                'amount_to': cols[1].text.replace(',', ''),
                'fee_p2p_onnet': cols[2].text.replace(',', ''),
                'fee_p2p_xnet': cols[2].text.replace(',', ''),
                'fee_cashout': cols[4].text.replace(',', ''),
                'fee_otf': cols[3].text.replace(',', '')
            }
        else:
            row = {
                'amount_from': cols[0].text.replace('Over Tsh ', '').replace(',', ''),
                'amount_to': 'N/A',
                'fee_p2p_onnet': cols[1].text.replace(',', ''),
                'fee_p2p_xnet': cols[1].text.replace(',', ''),
                'fee_cashout': cols[3].text.replace(',', ''),
                'fee_otf': cols[2].text.replace(',', '')
            }
        dict = OrderedDict(row.items())
        print(dict)
        writer.writerow(dict)
