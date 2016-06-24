from selenium import webdriver
from Navigator import Navigator
from Course import Course
from WebParser import WebParser
from ScheduleParser import ScheduleParser, Schedule
import time

#handles course availability
#Handles schedule comparison
#handles adding classes
#Verifys class adds


class CourseManager():

	def __init__(self,browser,navigator,parser):
		self.browser = browser
		self.navigator = navigator
		self.parser = parser

	def checkCourseAvailability(self,course, currentSchedule):
		#Navigate to course availability
		self.navigator.gotoCourseAvailability(course)

		#wait for page to load
		#TEMPORARY FIX TO TODO LIST PROBLEM
		time.sleep(2)

		#parse the page
		pageCourses = self.parser.parsePageCourses()

		

		if(len(pageCourses) == 0):
			return pageCourses

		#refine the results to specific course
		lastCourse = pageCourses[len(pageCourses)-1]
		
		#gather more courses if course availability continues onto next page
		while(lastCourse.department == course.department and lastCourse.course == course.course):
			self.navigator.showNext20()
			pageCourses += self.parser.parsePageCourses()
			lastCourse = pageCourses[len(pageCourses)-1]

		#remove extra courses we dont care about
		refinedList = []
		for x in pageCourses:
			if(x.department == course.department and x.course == course.course):
				refinedList.append(x)

		#mark the classes we are currently in as "Open"
		for i in range(0,len(refinedList)):
			x = refinedList[i]
			for y in currentSchedule.courseList:
				if(y.isEqual(x)):
					refinedList[i] = Course(y.department,y.course,y.section, "Open")


		return refinedList

	def checkCurrentSchedule(self):
		#Navigate to add/drop page
		self.navigator.gotoClassRegistration()
		
		#parse the page
		currentCourses = self.parser.parsePageCourses()

		currentSchedule = Schedule()
		currentSchedule.addCourses(currentCourses)
		currentSchedule.ID = 'CR'

		return currentSchedule


	#return the highest rank schedule that is available
	def findCompatibleSchedule(self, scheduleList, availabilityList):

		
		minRank = 100000000
		bestSchedule = None

		for scheduleIndex in range(0,len(scheduleList)):
			#schedule in question
			sch =  scheduleList[scheduleIndex]

			#see if schedule is compatible
			compatible = True
			for courseIndex in range(0,len(sch.courseList)):
				crs = sch.courseList[courseIndex]
				#give up on this schedule if one course doesn't work
				if(self.checkCourseOpening(crs, availabilityList[courseIndex]) == False):
					compatible = False

			#Check for the best schedule
			if(compatible == True):
				if sch.ID < minRank:
					bestSchedule = sch
					minRank = sch.ID

		return bestSchedule


	#returns the current schedules rank on the list of possible schedules
	def getScheduleRank(self, schedule, scheduleList):

		for scd in scheduleList:
			if schedule.isEqual(scd):
				return scd.ID

		#schedule has no rank
		return -1
		



	def verifyCourseAdd(self, courseAdded):

		currentCourses = self.checkCurrentSchedule()

		for crs in currentCourses:
			#check if course exists
			if crs.isEqual(courseAdded):
				return True

		#course was not found in current schedule
		return False


	def revertChanges(self, originalSchedule):
		#add all the original course back to schedule
		for crs in originalSchedule.courseList:
			self.addCourse(crs)

		#capture current schedule and see if revert was successful
		currentCourses = self.checkCurrentSchedule()

		#revert failed
		if(currentCourses.isEqual(originalSchedule) == False):
			#email user
			#TODO
			pass


	#Checks for an opening
	#availability - a list of courses from access plus
	#course - the course to look for
	def checkCourseOpening(self, course, availability):
		for crs in availability:
			#look for class
			if crs.isEqual(course):
				#check its status
				available = False
				try:
					seats = int(crs.status)
					available = (seats > 0 or crs.status == 'Open')
				except:
					available = (crs.status == 'Open')
				if available == True:
					return True
		return False



