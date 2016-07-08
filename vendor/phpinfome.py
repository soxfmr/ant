# -*- coding: utf-8 -*-
import requests
import json
import re
from provider import send
import pdb


URL  					= 'https://phpinfo.me/bing.php'
KEY_IP 					= 'ip'
KEY_ACTION 				= 'action'
KEY_DOMAIN				= 'domain'

def retrieve(target, ip):
	retval = []
	try:
		result = send(URL, { 
				KEY_IP					: ip,
				KEY_ACTION				: 'query'
			})
		if result:
			data = json.loads(result)
			for domainInfo in data:
				# Construct as {title: "Example", domain: "http://example.com/"}
				domain = domainInfo[KEY_DOMAIN]
				# Remove the protocol and suffix
				if domain.find('://'):
					domain = domain[domain.find('://') + 3:domain.rfind('/')]

				retval.append(domain)

	except Exception as e:
		print e

	return retval