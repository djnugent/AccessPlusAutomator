from selenium import webdriver
from Navigator import Navigator
from Course import Course
from CourseManager import CourseManager
from WebParser import WebParser



browser = webdriver.Firefox()

nav = Navigator(browser)
parser = WebParser(browser)
manager = CourseManager(browser,nav, parser)


nav.bypassLogin('student_id','student_pass', '0001qV1sH8ILGpkqibRr42x47tc:14a0b94d8')
nav.gotoClassRegistration('ran_num')

cpre = Course('CPR E', '288', 'B')
math267 = Course('MATH', '267')

crs = manager.checkCourseAvailability(math267)
for x in crs:
	print x

current = manager.checkCurrentSchedule()
for x in current:
	print x