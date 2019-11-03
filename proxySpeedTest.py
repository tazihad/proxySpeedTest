#Contact me http://t.me/biplob_sd
import sys, threading, socket, os
from datetime import datetime
from collections import OrderedDict
from urllib import error
import urllib.request
from tqdm import tqdm, trange
import socks
import sockshandler


def my_hook(t):
    last_b = [0]

    def update_to(b=1, bsize=1, tsize=None):
        if tsize not in (None, -1):
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b

    return update_to


class TqdmUpTo(tqdm):

    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def sec_to_mins(seconds):
	a=str(round((seconds%3600)//60))
	b=str(round((seconds%3600)%60))
	d="{} m {} s".format(a, b)
	return d


def speedTest(ip):
	#mirror = "https://drive.google.com/uc?id=0Bzkrq-7orwGScTAxNkFDaTM0Rkk&authuser=0&export=download"
	mirror = 'http://speedtest.tele2.net/1MB.zip'
	global protocol
	socket.setdefaulttimeout(15)
	filename = '1MB.zip'

	for i in range(3):
		if os.path.exists(f'{filename}{i}'):
			os.remove(f'{filename}{i}')

	timeStart = datetime.now()
	proxy_ip = ip.strip()
	print(f"\n\n\nProxy: {proxy_ip} | Downloading ...")
	def downloadChunk(idx,null):
		try:
			if protocol == 'http':
				proxy_handler = urllib.request.ProxyHandler({'http': proxy_ip,})
			if protocol == 'https':
				proxy_handler = urllib.request.ProxyHandler({'https': proxy_ip,})
			elif protocol == 'sock4':
				ip,port = proxy_ip.split(':')
				proxy_handler = sockshandler.SocksiPyHandler(socks.SOCKS4, ip, int(port))
			elif protocol == 'sock5':
				ip,port = proxy_ip.split(':')
				proxy_handler = sockshandler.SocksiPyHandler(socks.SOCKS5, ip, int(port))

			opener = urllib.request.build_opener(proxy_handler)
			urllib.request.install_opener(opener)
			with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=f'Thread no: {idx}') as t:
						urllib.request.urlretrieve(mirror, filename=f'{filename}{idx}', reporthook=t.update_to,data=None)
		except error.URLError:
			 return print(f"\nThread no: {idx}. Invalid ip or timeout for {proxy_ip}")
		except ConnectionResetError:
			return print(f"\nThread no: {idx}. Could not connect to {proxy_ip}")
		except IndexError:
			return print(f'\nThread no: {idx}. You must provide a testing IP:PORT proxy in the cmd line')
		except socket.timeout:
			return print(f"\nThread no: {idx}. Invalid ip or timeout for {proxy_ip}")
		except KeyboardInterrupt:
			print("\nThread no: {idx}. Exited by User.")

	downloaders = [
		threading.Thread(
			target=downloadChunk,
			args=(idx,null),
		)
		for idx,null in enumerate(range(3))
		]

	for th in downloaders:
		th.start()
	for th in downloaders:
		th.join()

	timeEnd = datetime.now()
	filesize = 0
	for i in range(3):
		try:
			filesize = filesize + os.path.getsize(f'{filename}{i}')
		except FileNotFoundError:
			continue

	filesizeM = round(filesize / pow(1024, 2), 2)
	delta = round(float((timeEnd - timeStart).seconds) + float(str('0.' + str((timeEnd - timeStart).microseconds))), 3)
	speed = round(filesize / 1024) / delta


	for i in range(3):
		if os.path.exists(f'{filename}{i}'):
			os.remove(f'{filename}{i}')

	unsort.append({'ip':f'PROXY: {proxy_ip}  \t\tSIZE: {filesizeM}MB \tTIME: {sec_to_mins(delta)}\t','speed':int(speed)})
	return 'Done'


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def whichProtocol(question, default="http"):
	valid = {"1": 'http', "2": 'https', "3": 'sock4',
 		"4": 'sock5', 'http': 'http'}
	if default is None:
		prompt = "\n\n1. http\n2. https\n3. sock4\n4. sock5 "
	elif default is 'http':
		prompt = f" \n\n1. http\n2. https\n3. sock4\n4. sock5"
	else:
		raise ValueError("\n\ninvalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(prompt + question+f'[default={default}]: ')
		choice = input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			clear()
			sys.stdout.write("\n\nError : Please respond with Number[1/2/3/4] \n")

unsort = []
sort = []
proxyslist = []
banner = """
                             _____                     _ _______        _
                            / ____|                   | |__   __|      | |
  _ __  _ __ _____  ___   _| (___  _ __   ___  ___  __| |  | | ___  ___| |_
 | '_ \| '__/ _ \ \/ / | | |\___ \| '_ \ / _ \/ _ \/ _` |  | |/ _ \/ __| __|
 | |_) | | | (_) >  <| |_| |____) | |_) |  __/  __/ (_| |  | |  __/\__ \ |_
 | .__/|_|  \___/_/\_\\__,  |_____/| .__/ \___|\___|\__,_|  |_|\___||___/\__|
 | |                   __/ |      | |
 |_|                  |___/       |_|                       -dev-by-Alpha4d-
"""

open('proxys.txt', 'a+').close()
handle = open('proxys.txt')
for line in handle:
	if not len(line.strip()) == 0 :
		proxyslist.append(line)
handle.close()

if not len(proxyslist) == 0:
	print(banner)
	protocol = whichProtocol("\n\nWhich's protocol do you want use with ")
	clear()
	print(banner)
	for i in trange(len(proxyslist),unit='A', unit_scale=True, unit_divisor=1024, miniters=1, desc=f'Completed'):
		p = speedTest(proxyslist[i])
		clear()
		print(banner)
		# print(p)
		if not (p[0] == 'C' or p[0] == 'I' or p[0] == 'Y'):
			sort = sorted(
			    unsort,
			    key=lambda x: x['speed'], reverse=True)
		print("\nSort as Speed: (Top 10)")
		count = 0
		for p in sort:
			count += 1
			print(p['ip']+'\t'+str(p['speed'])+' KB/s')
			if count == 10:
				break
		print("\n")
else:
	print("Import some proxys(IP:prot) in proxys.txt file.")
