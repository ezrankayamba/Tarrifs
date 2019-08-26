from django.shortcuts import render
import csv


def index(request):
    if request.method == 'POST':
        mno = request.POST['mno']
    else:
        mno = 'vodacom'
    context = {
        'mnos': MNO_DICT_LIST,
        'selected_mno': mno
    }
    csv_path = f"mm_tarrifs/work/data/{mno}_fees.csv"
    with open(csv_path, 'r') as f:
        csv_reader = csv.DictReader(f)
        context['headers'] = ['From', 'To', 'P2P ONNET', 'P2P XNET', 'CASHOUT', 'OTF']
        context['tarrifs'] = [row for row in csv_reader]
        context['fieldnames'] = csv_reader.fieldnames
    return render(request, 'mm_tarrifs/index.html', context=context)


# Dict list of MNOs
MNO_DICT_LIST = [{
    'code': 'vodacom',
            'name': 'M-Pesa'
}, {
    'code': 'tigo',
            'name': 'Tigo Pesa'
}, {
    'code': 'zantel',
            'name': 'Ezy Pesa'
}, {
    'code': 'halotel',
            'name': 'Halo Pesa'
}, {
    'code': 'ttcl',
            'name': 'T-Pesa'
}]
