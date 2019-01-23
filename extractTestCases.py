import sys
import urllib.request
from bs4 import BeautifulSoup

def extractTestCases(urlOfQuestion):
	#get Markup
	try:
		pg = urllib.request.urlopen(urlOfQuestion)
	except Exception as e:
		fh = open(sys.__stdout__,'w')
		fh.write("An error occured while fetching the specified URL\n",e)
		fh.flush()
		fh.close()

	#convert to BeautifulSoup
	pg = BeautifulSoup(pg,'lxml')

	allTests = pg.find('div', class_ = 'sample-tests')
	tcases = allTests.findAll('pre')

	#the number of testcases
	T = len(tcases)//2

	#lists for input and output
	ip = []
	op = []

	for i in range(T):
		ip.append(tcases[2*i].string)
		op.append(tcases[(2*i)+1].string)

	#clean input output
	ip = [i.strip() for i in ip if i is not None]
	op = [i.strip() for i in op if i is not None]

	#get question name
	name = pg.find('div',class_ = 'header')
	name = name.find('div',class_ = 'title')
	name = name.string
	name = name.split()			#remove spaces from in between
	name = ''.join(name)


	#write to file

	sys.stdout = open(name + '.input','w')

	print(T)		#total number of testcases
	print(*ip,sep = '\n')

	#now write expected output
	sys.stdout = open(name + '.expectedOutput', 'w')

	print(*op,sep = '\n')


def getQuestionsList(urlOfContest):
	#get Markup
	try:
		pg = urllib.request.urlopen(urlOfContest)
	except Exception as e:
		fh = open(sys.__stdout__,'w')
		fh.write("An error occured while fetching the specified URL\n",e)
		fh.flush()
		fh.close()

	#convert to BeautifulSoup
	pg = BeautifulSoup(pg,'lxml')

	tbl = pg.find('table', class_ = 'problems')

	listOfUrls = []

	for row in tbl.findAll('tr'):
		if(row.find('td')):
			listOfUrls.append('http://codeforces.com'+ row.a['href'])

	return listOfUrls
		

urlOfContest = input('Enter the link of the CodeForces contest whose testcases you want to fetch:\n')

listOfQurls = getQuestionsList(urlOfContest)

for url in listOfQurls:
	extractTestCases(url)


#restore stdout
sys.stdout = sys.__stdout__

print('Completed Successfully')