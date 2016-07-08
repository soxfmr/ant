# -*- coding: utf-8 -*-
import threading
import Queue
import dns.resolver
from colorama import init
from colorama import Fore

'''
Check the accuracy of the result

Callback function:

def callback(domains):
	// do something
'''
class DomainFilter():

	def __init__(self, target, callback):
		init(autoreset = True)

		self.target = target
		self.callback = callback

		self.thread_max = 8
		self.confirm_list = []
		self.thread_pool = []

		self.queue = Queue.Queue()
		self.lock = threading.Semaphore()

	def filter(self, domains):
		if not domains:
			self.callback([])
			return

		self.confirm_list = []
		self.thread_pool = []
		self.queue.queue.clear()

		for domain in domains:
			self.queue.put(domain)

		for i in range(self.thread_max):
			worker = threading.Thread(target=self.query)
			worker.setDaemon(True)
			worker.start()

			self.thread_pool.append(worker)

		for thread in self.thread_pool:
			thread.join()
		
		self.callback(self.confirm_list)

	def query(self):
		while True:
			if self.queue.empty():
				break

			domain = self.queue.get()
			# Retrieve the A records
			answer = dns.resolver.query(domain, 'A')
			if not answer: continue

			for record in answer:
				if self.target == record:
					try:
						self.lock.acquire()
						if not domain in self.confirm_list:
							self.confirm_list.append(domain)
							print Fore.GREEN + ('[+] %s confirmed' % domain)
					finally:
						self.lock.release()
					# jump out
					break

			self.queue.task_done()