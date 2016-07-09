# -*- coding: utf-8 -*-
import requests
import json
from provider import send

URL  					= 'http://domains.yougetsignal.com/domains.php'
KEY_REMOTE_ADDR 		= 'remoteAddress'
KEY_RESERVE_KEY 		= 'key'
KEY_RESERVE_UNDERLINE 	= '_'
KEY_DOMAIN_ARRAY 		= 'domainArray'

def retrieve(target, ip):
	retval = []
	try:
		result = send(URL,
			payload = {
				KEY_REMOTE_ADDR 		: target,
				KEY_RESERVE_KEY			: '',
				KEY_RESERVE_UNDERLINE	: ''
			},
			headers = {
				'Referer' : 'http://www.yougetsignal.com/tools/web-sites-on-web-server'
			})
		if result:
			data = json.loads(result)
			domainList = data.get(KEY_DOMAIN_ARRAY)

			if domainList:
				for domain in domainList:
					# Construct as ['example.com', '']
					retval.append(domain[0])

	except Exception as e:
		print e

	return retval
