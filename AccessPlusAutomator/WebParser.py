from selenium import webdriver
from Course import Course
from bs4 import BeautifulSoup


class WebParser():
	
	def __init__(self, browser):
		self.browser = browser



	#takes a web page and returns a list of ALL visible courses and their avaiability
	def parsePageCourses(self):
		pageText = self.browser.page_source.encode('utf-8')
		soup = BeautifulSoup(str(pageText))
		
		#find all course entries
		odds = soup.find_all(class_="odd")
		evens = soup.find_all(class_="even")
		#clean up entries
		entries = []
		for i in range(0,len(evens)):
			if i % 2 == 0:
				entries.append(odds[i])
				entries.append(evens[i])

		#convert HTML to Course Object
		courseResults = []
		for entry in entries:
			courseResults.append(self.processEntry(entry))

		return courseResults

	#takes an entry in HTML and converts it to a course
	def processEntry(self, entry):



		#split  up entry data into columns
		columns = entry.find_all('td')

		info = columns[1].find_all('input')
		status = columns[2]

		#parse course info
		department = info[3]['value']
		department = department.strip()
		

		courseNum = info[1]['value']
		courseNum = courseNum.strip()

		section = info[2]['value']
		section = section.strip()
		

		#parse availability
		availability = next(status.children)

		availability = availability.replace('Seats', '').strip()	
		

		crs = Course(department,courseNum,section,availability)
		return crs






