import sys
import requests
import urllib.request
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import DataFrame
import re

#set timeout after each request to prevent overloading the website or getting blacklisted, in seconds
timeout = 1

percentage = 0
counter = 1
df = pd.read_excel('CVEs.xlsx')
CVEs = df['CVE-ID'].tolist()

for CVE in CVEs:

	html = "https://www.cvedetails.com/cve-details.php?cve_id={}".format(CVE)
	
#progress bar
	percentage = counter/(len(CVEs))*100
	counter +=1
	# sys.stdout.write('\r')
	# sys.stdout.write('Collecting: ' + html + ' - ' + str(int(percentage)) + ' %')
	# sys.stdout.flush()
		
	try:
	#request page

		page = requests.post(html)

		soup = bs(page.text, "html.parser")	
		meta_tag = soup.find('meta', attrs={'name': 'keywords'})
		
		# Format:
		# <meta name="keywords" content="CVE-2013-2035, 201300002035, CWE-94, CVSS 4.4" />
		print(meta_tag)
		# print(CWE_ID)


	except:
		print("Error")
		
	finally:
		time.sleep(timeout)
	
