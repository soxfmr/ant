import sys
import re
import dns.resolver
import vendors
import domainfilter
from colorama import init
from colorama import Fore
from vendor.yougetsignal import retrieve as yougetsignal_get
from vendor.phpinfome import retrieve as phpinfome_get

banner = '''                                                                                        
_____/\\\\\\\\\____        __/\\\\\_____/\\\_        __/\\\\\\\\\\\\\\\_        
 ___/\\\\\\\\\\\\\__        _\/\\\\\\___\/\\\_        _\///////\\\/////__       
  __/\\\/////////\\\_        _\/\\\/\\\__\/\\\_        _______\/\\\_______      
   _\/\\\_______\/\\\_        _\/\\\//\\\_\/\\\_        _______\/\\\_______     
    _\/\\\\\\\\\\\\\\\_        _\/\\\\//\\\\/\\\_        _______\/\\\_______    
     _\/\\\/////////\\\_        _\/\\\_\//\\\/\\\_        _______\/\\\_______   
      _\/\\\_______\/\\\_        _\/\\\__\//\\\\\\_        _______\/\\\_______  
       _\/\\\_______\/\\\_        _\/\\\___\//\\\\\_        _______\/\\\_______ 
        _\///________\///__        _\///_____\/////__        _______\///________
'''

def show_banner():
	init(autoreset=True)
	print Fore.GREEN + banner

def is_ipaddress(target):
	return True if not re.match(r'\d+\.\d+\.\d+\.\d+', target) else False

def resolve_single_ip(target):
	if not is_ipaddress(target):
		return target

	answer = dns.resolver.query(target, 'A')
	if not answer:
		raise Exception('[-] Cannot resolve target domain %s' % target)

	print Fore.GREEN + '[+] Traget domain resolve to %s' % answer[0]

	# Return first record without determine the real ip which is hidden by CDN
	return answer[0]

def main():
	show_banner()

	if len(sys.argv) < 2:
		print 'Usage: ant.py <domain> or <IP-address>'
		return

	target = sys.argv[1]
	neighbours = []

	print '[-] Starting to retrieve the information of %s' % target

	target_ip = resolve_single_ip(target)

	for vendor_name, func_name in vendors.API_VENDOR.items():
		result = globals()[func_name](target, target_ip)
		# result = method(target)

		print '[-] Retrieve total %d domains from %s' % (len(result), vendor_name)
		neighbours.extend(result)

	def show_result(domains):
		print '\n'
		for domain in domains:
			print domain

		print '\n'
		print 'Totally %d domains were found on the same server.' % (len(domains))

	print '[-] Verify the domain names...'
	dofilter = domainfilter.DomainFilter(target_ip, show_result)
	dofilter.filter(neighbours)

if __name__ == '__main__':
	main()