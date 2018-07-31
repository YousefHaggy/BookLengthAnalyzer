from bs4 import BeautifulSoup
import lxml
import requests
import time
import operator;
titleList=[]
bookList=[]
class Book:
	def __init__(self,title,hours,mins):
		self.title=title
		self.hours=hours
		self.mins=mins
		self.total=int(hours)+(int(mins)/60)
def pullTitlesFromFile():
	with open('books.txt') as f:
		for line in f:
			titleList.append(line)
	f.close()
def scrape(list):
	for title in list:
		url='https://www.howlongtoreadthis.com/search-redirect.php?search_keyword='
		titleParsed=title.split(" ");
		for i in range(len(titleParsed)):
			if i != len(titleParsed)-1:
				url+=titleParsed[i]+"+"
			else:
				url+=titleParsed[i]

		request=requests.get(url);
		requestText=request.text;
		time.sleep(1)
		locationOfNewUrl=requestText.find("book_details")
		endOfNewUrl=requestText.find(";")
		newUrl='https://www.howlongtoreadthis.com/'+requestText[locationOfNewUrl:endOfNewUrl];
		request=requests.get(newUrl);
		print(url);
		time.sleep(1)
		soup= BeautifulSoup(request.content,"lxml")
		if soup.find("span",{"id":"reading-desc"}) != None:
			times=soup.find("span",{"id":"reading-desc"}).find_all("span")
			book=Book(title,times[0].text[0:2].strip(),times[1].text[0:2].strip())
			if book.total > 0:	
				global bookList
				bookList.append(book)
				list.remove(title);
		printAll()
	if len(list)>0:
		scrape(list)
def printAll():
	global bookList
	bookList=sorted(bookList,key=operator.attrgetter('total'))
	with open("results.txt","w") as f:
		for book in bookList:
			f.write(book.title+" "+str(book.total)+"\n")
	f.close();
pullTitlesFromFile()
scrape(titleList)


