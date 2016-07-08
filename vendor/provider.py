# -*- coding: utf-8 -*-
import requests

def send(url, payload, headers=None):
	inner_headers = { 'User-Agent' : 'Ant' }
	# combine the header
	if headers: inner_headers = dict(inner_headers, **headers)

	res = requests.post(url, data = payload, headers = inner_headers)

	if res.status_code != 200:
		raise Exception('The vendor server response wtih status code %d' % res.status_code)

	return res.content