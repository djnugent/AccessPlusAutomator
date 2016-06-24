from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from Course import Course



class Navigator():

	def __init__(self, driver):
		self.browser = driver
		self.RAN = None

	#Login to accessplus
	def login(self, userID, password):
		#Login page
		self.browser.get('https://accessplus.iastate.edu/frontdoor/login.jsp')
		print 'Login page'


		username = self.browser.find_element_by_id('loginid') 
		pinPass = self.browser.find_element_by_id('pinpass')
		username.send_keys(userID)
		pinPass.send_keys(password + Keys.RETURN)

		print 'login successful!'
		print 'Login Cookie: ' + str(self.browser.get_cookies())
		print 'Home page'

		#navigate to student tab
		studentTab = self.browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a[3]/img')
		studentTab.click()
		print 'Student page'

	#attempt to bypass login with previous session cookie
	def bypassLogin(self, userID, password, sessionValue):

		#Login page
		self.browser.get('https://accessplus.iastate.edu/frontdoor/login.jsp')
		print 'Login Page'


		#resume previous session
		self.browser.add_cookie({'domain':'.iastate.edu', 'name': 'APLUSID', 'value': sessionValue, 'expiry': None, 'path': '/', 'secure': True})
		self.browser.get('https://accessplus.iastate.edu/servlet/adp.A_Plus?A_Plus_action=/home.jsp')

		#previous session expired so we have to login again
		if(self.browser.title == 'AccessPlus Session Expired'):
			print 'FAILED TO RESUME SESSION PLEASE REFRESH COOKIES'
			self.login(userID,password)

		else:
			print 'Bypass successful: Logged in'

			#navigate to student tab
			studentTab = self.browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a[3]/img')
			studentTab.click()
			print 'Student page'

	def gotoClassRegistration(self, ranNumber = None):
		#save RAN Number for later use
		if(ranNumber is not None):
			self.RAN = ranNumber

		if(self.RAN is None):
			print 'No RAN number present, please enter as Arguement'
			return
		
		#already Entered RAN number
		if(self.browser.title == 'Class Registration'):
			#navigate to add/drop page
			add_drop = WebDriverWait(self.browser, 10).until(
			        EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr/td[1]/table/tbody/tr[2]/td/a[1]/span')))
			add_drop.click()
			print 'Add/Drop page'

		else:
			#navigate to class registration
			classReg = self.browser.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/table/tbody/tr[2]/td/a[7]/b')
			classReg.click()
			print 'Class Registration page'

			#contine to ran
			cont2Ran = WebDriverWait(self.browser, 10).until(
			        EC.presence_of_element_located((By.NAME, "Continue")))
			cont2Ran.click()
			print 'RAN Entry Page'

			#enter ran
			ranNum = WebDriverWait(self.browser, 10).until(
			        EC.presence_of_element_located((By.NAME, "Raccessnum")))

			ranNum.send_keys(self.RAN + Keys.RETURN)
			print 'Entered RAN'

			#end up at add/drop page
			print 'Add/Drop page'

	def gotoCourseAvailability(self, course):

		if(self.browser.title != 'Class Registration'):
			self.gotoClassRegistration()

		departmentOpt =  Select(WebDriverWait(self.browser, 10).until(
			        EC.presence_of_element_located((By.NAME, "DeptInfo"))))
		courseBox = WebDriverWait(self.browser, 10).until(
			        EC.presence_of_element_located((By.NAME, "R2193_CRSE")))
		
		#enter deprartment
		departmentOpt.select_by_value(course.department)

		#enter course
		courseBox.clear()
		courseBox.send_keys(course.course)

		#enter section if available
		if(course.section is not None):
			sectionBox = WebDriverWait(self.browser, 10).until(
			        EC.presence_of_element_located((By.NAME, "R2193_SECT")))
			sectionBox.clear()
			sectionBox.send_keys(course.section + Keys.RETURN)
			print "Displaying Course Availability for " + course.department + ' ' + course.course + ' section ' + course.section

		else:
			courseBox.send_keys(Keys.RETURN)
			print "Displaying Course Availability for " + course.department + ' ' + course.course + ' all sections'

	def showNext20(self):

		self.browser.execute_script("document.searchDeptCrse.R2193_FNCTN_CD.value='NS';document.searchDeptCrse.submit()")
		print 'Next 20'

	def addCourse(self,course):
		#Navigate to add/drop page
		self.gotoClassRegistration()

		#TODO
