from selenium import webdriver
from Navigator import Navigator
from Course import Course
from WebParser import WebParser



browser = webdriver.Firefox()

nav = Navigator(browser)
parser = WebParser(browser)

nav.bypassLogin('student_id','student_pass', '0001qV1sH8ILGpkqibRr42x47tc:14a0b94d8')
nav.gotoClassRegistration('ran_num')

cpre = Course('CPR E', '288', 'B')
coms = Course('COM S', '309')


nav.gotoCourseAvailability(cpre)
nav.showNext20()
nav.showNext20()
nav.gotoClassRegistration()

cpreStatus = parser.parsePageCourses()

for cr in cpreStatus:
	print cr





