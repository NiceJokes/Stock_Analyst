from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
import numpy as np
import matplotlib

import requests
import pandas as pd
from datetime import datetime, timedelta
from .models import Items_table,Indicators




API_KEY='EEtfS6RiT-wyA-4Bpu7_'



def days_frequency(freq,type):
    if type==0:
        if freq=='daily': result=1
        elif freq=='weekly': result=7
        elif freq=='monthly': result=30
        elif freq=='quarterly': result=90
        else: result=365
    elif type==1:
        if int(freq)==1: result='daily'
        elif int(freq)==7: result='weekly'
        elif int(freq)==30: result='monthly'
        elif int(freq)==90: result='quarterly'
        else: result='annual'
    else:
        if freq=='daily': result='days'
        elif freq=='weekly': result='weeks'
        elif freq=='monthly': result='months'
        elif freq=='quarterly': result='quarters'
        else: result='years'
    return result


def quandl_data(title, dataset, default_item, col_index, sorting, ctype):

    start_date = (datetime.now() - timedelta(4 * 365)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    items = Items_table.objects.filter(dataset=dataset).order_by(sorting)

    url = 'https://www.quandl.com/api/v3/datasets/{}/{}' \
          + '.json?&api_key={}&start_date={}&end_date={}&order=asc&collapse=none&transform=none&column_index={}'
    dataurl = url.format(dataset, default_item, API_KEY, start_date, end_date, col_index)
    print(dataurl)
    result = requests.get(dataurl).json()
    freq = result['dataset']['frequency']
    lower_limit = result['dataset']['oldest_available_date']
    upper_limit = result['dataset']['newest_available_date']

    freq_days = days_frequency(freq, 0)
    freq_unit = days_frequency(freq, 2)


    context = {'title': title, 'dataset': dataset, 'items': items,
               'default_item': default_item, 'default_title': result['dataset']['name'], 'col_index': col_index,
               'ctype': ctype,
               'min': lower_limit, 'max': upper_limit, 'start_date': start_date, 'end_date': end_date,
               'freq_days': freq_days, 'freq_unit': freq_unit}
    return context


def stock(request):
    dataset = 'WSE'
    default_item = 'WIG20'
    title = 'Stock Markets'
    col_index = '15'
    ctype = 'line'
    sorting = 'description'
    context = quandl_data(title, dataset, default_item, col_index, sorting, ctype)

    return render(request, 'stocks_chart/chart.html', context)
