from selenium import webdriver
from Navigator import Navigator
from Course import Course
from CourseManager import CourseManager
from WebParser import WebParser
from ScheduleParser import ScheduleParser, Schedule
from EmailNotifier import EmailNotifier
import sys
import traceback
import random
import time


'''
TODO:
Build my own Scheduler: not use cronTab
Take in a config file with user info: passwords, receipeint email
refine revert method to be less aggressive: currently bruteforces in original chedule
refine add/drop page navigation: we navigate a lot during addCourse and verfiy add
fix error:
  File "/home/dannuge/Python/AccessPlusAutomator/WebParser.py", line 42, in processEntry
    status = columns[2]
 ***the page isn't done loading at the time of parse
 ***temporary fix in courseManger.checkcourseAvailability

 Sometimes the program thinks the scheduel is of rank 0 when it is not actually
'''

#change course schedule if available
takeAction = False

recipient = 'personalemail@here.com'

#make to scheduling more random
delayStartup = False

#send heartbeat email every time program runs
heartbeat = True

if delayStartup:
	delay = random.randint(60,690) #delay between 1 minute and 16 minutes
	print 'Delaying program: ' + str(delay/60) + '  minutes'
	time.sleep(delay)





browser = webdriver.Firefox()

nav = Navigator(browser)
parser = WebParser(browser)
manager = CourseManager(browser,nav, parser)
schedParser = ScheduleParser()
notify = EmailNotifier(sender,sender_pass)



#if True:
try:
	#parse schedule file
	schedParser.parseFile('Spring2015.scd')

	courseList = schedParser.getCourseList()
	schedules = schedParser.getSchedules()


	#Login to access plus
	nav.bypassLogin('student_id','student_pass', '0001soQW4_NsnMLgyDhE4-RQDsP:14a0b94d8')
	nav.gotoClassRegistration('ran_num')



	#check the status of the current schedule
	baseSchedule = manager.checkCurrentSchedule()
	rank = manager.getScheduleRank(baseSchedule, schedules)

	#if it is already at it's best then we can leave
	if rank == 0:
		print "Schedule is complete!"

		if heartbeat:
			notify.notifyHeartBeat("Schedule is complete, suggest terminating program")
			notify.sendEmail(recipient)

		browser.close()

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

			#TODO: test take action, untested
			#try to update schedule
			if(takeAction):
				#create of list of classes we need to CHANGE
				#then add that list
				coursesToAdd = findUpdatedCourses(baseSchedule,compatible)
				success = True
				for crs in coursesToAdd:
					nav.addCourse(crs)
					added = manager.verfiyAdd(crs)

					#class add failed
					if added == False:
						success = False
						#try to revert schedule
						reverted = manager.revertSchedule(baseSchedule)

						#failed to revert back
						if reverted == False:
							#alert of failed revert critical issue
							currentSchedule = manager.checkCurrentSchedule()
							notify.notifyRevertFailed(baseSchedule,compatibleSchedule,currentSchedule)
							notify.sendEmail(recipient)
							#leave loop
							break

						#we failed to update course and reverted succesfully
						currentSchedule = manager.checkCurrentSchedule()
						#alert of udpate fail
						notify.notifyUpdateFailed(baseSchedule,compatibleSchedule,currentSchedule)
						notify.send(recipient)
						break

				#alert of schedule change
				if(success == True):
					currentSchedule = manager.checkCurrentSchedule()
					notify.notifySuccessfulUpdate(baseSchedule,compatibleSchedule,currentSchedule)

			#dont take action, just notify user
			else:
				notify.notifyAvailableSchedule(baseSchedule,compatibleSchedule)
				notify.sendEmail(recipient)

			#end program
			browser.close


		#the current schedule is th best option
		if(compatibleSchedule.ID >= rank):
			print "The current schedule is the best compatible Schedule"

			if heartbeat:
				notify.notifyHeartBeat("The current schedule is the best compatible Schedule")
				notify.sendEmail(recipient)

			#end program
			browser.close()


except:
	#unable to finish program

	#log error
	_, _, tb = sys.exc_info()
	error = traceback.format_list(traceback.extract_tb(tb)[-1:])[-1]

	print error

	#notify user of issue
	notify.notifyTermination(str(error))
	notify.sendEmail(recipient)

	#close the browser
	browser.close()
