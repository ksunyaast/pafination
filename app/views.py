from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
import csv
import urllib.parse


def index(request):
    return redirect(reverse(bus_stations))

with open(settings.BUS_STATION_CSV, encoding = 'cp1251', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	bus_stations_list = []
	for row in reader:
		bus_stations_list.append({'Name': row['Name'], 'Street': row['Street'], 'District': row['District']})
	


def bus_stations(request):
	count = 10
	page_num = int(request.GET.get('page', 1))
	paginator = Paginator(bus_stations_list, count)

	page = paginator.get_page(page_num)
	data = page.object_list

	base_url = f'{reverse(bus_stations)}?'
	if page.has_next():
		params = urllib.parse.urlencode({'page': page_num + 1})
		next_page_url = base_url + params
	else:
		next_page_url = None
	if page.has_previous():
		params = urllib.parse.urlencode({'page': page_num - 1})
		prev_page_url = base_url + params
	else:
		prev_page_url = None

	return render_to_response('index.html', context = {
		'bus_stations': data,
		'current_page': page_num,
		'prev_page_url': prev_page_url,
		'next_page_url': next_page_url,
	})

