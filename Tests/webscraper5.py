from selenium import webdriver
from Navigator import Navigator
from Course import Course
from CourseManager import CourseManager
from WebParser import WebParser
from ScheduleParser import ScheduleParser, Schedule
import sys


browser = webdriver.Firefox()

nav = Navigator(browser)
parser = WebParser(browser)
manager = CourseManager(browser,nav, parser)
schedParser = ScheduleParser()

#parse schedule file
schedParser.parseFile('Spring2015.scd')

courseList = schedParser.getCourseList()
schedules = schedParser.getSchedules()


#Login to access plus
nav.bypassLogin('student_id','student_pass', '0001qV1sH8ILGpkqibRr42x47tc:14a0b94d8')
nav.gotoClassRegistration('ran_num')



#check the status of the current schedule
baseSchedule = manager.checkCurrentSchedule()
rank = manager.getScheduleRank(baseSchedule, schedules)

#if it is already at it's best then we can leave
if rank == 0:
	print "Schedule is complete!"
	#TODO send email

#look for possibly available Schedules
else:
	print "Current schedule is of rank " + str(rank)

	courseAvailability = []

	#check the availability of every class in the course list
	for i in range(0,len(courseList.courseList)):
		courseAvailability.append(manager.checkCourseAvailability(courseList.courseList[i],baseSchedule))


	compatibleSchedule = manager.findCompatibleSchedule(schedules, courseAvailability)

	#we found a better compatible schedule!
	if(compatibleSchedule.ID < rank):
		print "A better schedule is available"
		print compatibleSchedule

		#create of list of classes we need to CHANGE
			#then add that list



	#the current schedule is th best option
	if(compatibleSchedule.ID >= rank):
		print "The current schedule is the best compatible Schedule"
		print compatibleSchedule


