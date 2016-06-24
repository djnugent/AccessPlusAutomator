from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()

#home page
browser.get('https://accessplus.iastate.edu/frontdoor/login.jsp')

#resume previous session
sessionValue = '00015nkpAHD9RrsJ5Jh3bsPsyhB:14a0b94d8'
browser.add_cookie({'domain':'.iastate.edu', 'name': 'APLUSID', 'value': sessionValue, 'expiry': None, 'path': '/', 'secure': True})
browser.get('https://accessplus.iastate.edu/servlet/adp.A_Plus?A_Plus_action=/home.jsp')

#previous session expired so we have to login again
if(browser.title == 'AccessPlus Session Expired'):

	print 'FAILED TO RESUME SESSION PLEASE REFRESH COOKIES'

	#home page
	browser.get('https://accessplus.iastate.edu/frontdoor/login.jsp')

	#login
	username = browser.find_element_by_id('loginid')  # Find the search box
	password = browser.find_element_by_id('pinpass')
	username.send_keys(student_id)
	password.send_keys('student_pass' + Keys.RETURN)

	print browser.get_cookies()

#navigate to student tab
studentTab = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a[3]/img')
studentTab.click()

#navigate to class registration
classReg = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/table/tbody/tr[2]/td/a[7]/b')
classReg.click()

#contine to ran
cont2Ran = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "Continue")))

cont2Ran.click()

#enter ran
ranNum = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "Raccessnum")))

ranNum.send_keys('ran_num' + Keys.RETURN)


#browser.quit()
