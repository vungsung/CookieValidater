import json
import requests
import tldextract

file_name = 'cookiebro-cookies.json' # the cookies exported by CookieBro Chrome extension
keywords = ('vungsung', 'vung.sung') # the keywords that can only be found in the logged-in response (e.g. your nickname)
timeout_sec = 5 # max seconds to wait before a connetion is considered timeout

def search_keyword(response):
	for keyword in keywords:
		if keyword.lower() in response.lower():
			return keyword
	return False

def load_cookies(cookies):
	domains = {}
	for cookie in cookies:
		domain_key = '.'.join(tldextract.extract( cookie['domain'].strip('.') )[1:])
		if domain_key not in domains:
			domains[domain_key] = {}
		domains[domain_key][cookie['name']] = cookie['value']
	return domains

def main():
	cookies = json.load(open(file_name))
	domains = load_cookies(cookies)
	print('Cookies loaded.')

	domain_lens = len(domains)
	i = 1

	for domain_name in domains:
		scheme = 'https://' # disabled http:// since sending session cookies over it is insecure anyway
		try:
			print(f'[*] Testing[{i}/{domain_lens}] {scheme + domain_name} ...', end='')
			r = requests.get(scheme + domain_name, cookies = domains[domain_name], allow_redirects = True, timeout = timeout_sec)
			found = search_keyword(r.text)
			if found:
				print(f'\n\033[6;30;42m[+] Valid session found:\033[1;33;40m {domain_name} ({found})\033[0m')
			else:
				print('') # Nothing interesting found
		except KeyboardInterrupt:
			print('')
			return
		except Exception as e:
			print(f'\033[1;31;40m failed\033[0m') # mostly caused by connetion errors
		i += 1

if __name__ == '__main__':
	main()