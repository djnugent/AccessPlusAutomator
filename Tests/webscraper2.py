from selenium import webdriver
from Navigator import Navigator
from Course import Course


browser = webdriver.Firefox()

nav = Navigator(browser)

nav.bypassLogin('student_id','student_pass', '00015nkpAHD9RrsJ5Jh3bsPsyhB:14a0b94d8')
nav.gotoClassRegistration('ran_num')

cpre = Course('CPR E', '288', 'B')
coms = Course('COM S', '309')

nav.gotoCourseAvailability(cpre)
nav.gotoCourseAvailability(coms)
nav.gotoClassRegistration()
nav.gotoCourseAvailability(cpre)





