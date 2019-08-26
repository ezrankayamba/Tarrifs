from bs4 import BeautifulSoup
import requests
import csv
from collections import OrderedDict
import shutil
from PIL import Image
from pytesseract import image_to_string
import re

url = 'https://www.ttcl.co.tz/newsite/images/ttclpesa_tariffs.jpg'
response = requests.get(url, stream=True)
img_path = 'images/ttcl_fees.jpg'
text_path = 'images/ttcl_fees.txt'
with open('images/ttcl_fees.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response
im = Image.open(img_path)
img_text = image_to_string(im)
with open(text_path, 'w', newline='') as f:
    f.write(img_text)
line_regex = '^\d{1,}[,\d NA/]{0,}\d{0,}$'
lines = []
with open(text_path, 'r') as f:
    for line in f.readlines():
        match = re.search(line_regex, line)
        if match:
            lines.append(match.group())
half = int(len(lines) / 2)
field_names = ['amount_from', 'amount_to', 'fee_p2p_onnet', 'fee_p2p_xnet', 'fee_cashout', 'fee_otf']
with open('data/ttcl_fees.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    for left, right in zip(lines[:half], lines[half:]):
        cols = left.split(' ') + right.split(' ')
        row = {
            'amount_from': cols[0].replace(',', ''),
            'amount_to': cols[1].replace(',', ''),
            'fee_p2p_onnet': cols[2].replace(',', ''),
            'fee_p2p_xnet': cols[3].replace(',', ''),
            'fee_cashout': cols[4].replace(',', ''),
            'fee_otf': 'N/A'
        }
        dict = OrderedDict(row.items())
        writer.writerow(dict)
