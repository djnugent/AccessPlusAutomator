from Course import Course

#stores a Schedule / list of courses
class Schedule():

	
	'''
	def __init__(self, courseList = [], ID = -1):
		self.courseList = courseList
		self.ID = ID 
	'''

	def __init__(self):
		self.courseList = []
		self.ID = -1

	def addCourse(self,course):
		self.courseList.append(course)

	def addCourses(self, courses):
		for x in courses:
			self.addCourse(x)


	def isEqual(self,other):
		count = 0
		for x in self.courseList:
			for y in other.courseList:
				if x.isEqual(y):
					count += 1
					break
		return(count == len(self.courseList))

	def __str__(self):
		string = 'Schedule ' + str(self.ID)
		for i in range(0,len(self.courseList)):
			string += '\n' + str(i) + '. ' + str(self.courseList[i])

		return string


class ScheduleParser():



	def __init__(self):
		#list of courses
		self.courses = None

		#different schedules
		self.schedules = [] 

		self.scheduleCount = 0


	def parseFile(self, fileName):
		#open file
		f = open(fileName, 'r')

		lines = f.readlines()

		#remove comments
		lines = self.removeComments(lines)


		#scan in course list
		self.courses = self.scanInCourseList(lines,'Courses:')
		self.courses.ID = 'CL'



		#count the number of schedule in file
		schedNumber = self.countSchedules(lines)

		#Scan in all those schedules and add them to a the list
		for i in range(0,schedNumber):
			header = 'Schedule: ' + str(i)

			tempSchedule = self.scanInCourseList(lines,header)
			tempSchedule.ID = i

			self.schedules.append(tempSchedule)
			self.scheduleCount += 1
		

	#returns a list of classes in a schedule
	def getCourseList(self):
		return self.courses

	def getSchedules(self):

		return self.schedules


	def removeComments(self,lines):
		clean = []
		for line in lines:
			if line.find('#') == -1:
				clean.append(line)
		return clean

	def scanInCourseList(self, lines, header):
		tempCourses = []

		#search for header
		index = 0
		while index < len(lines) and lines[index].find(header) == -1 :
			index += 1

		#header not found
		if(index == len(lines)):
			print "Error parsing course list with header " + header
			return

		index += 1 #move down a line
		while lines[index].find(";") == -1:
			tempCourse = self.scanInCourse(lines[index])

			tempCourses.append(tempCourse)
			index += 1

		#create a schedule from the courses
		tempSchedule = Schedule()
		tempSchedule.addCourses(tempCourses)


		return tempSchedule


	def scanInCourse(self,line):
		data = line.split(',')

		#invalID line, return original line for error handling
		if len(data) != 3:
			print 'Unable to scan in line "' + line + '"'
			return None

		department = data[0].strip()
		courseNum = data[1].strip()
		section = data[2].strip()
		#Null section
		if section == 'None':
			section = None


		return Course(department,courseNum,section)

	def countSchedules(self,lines):
		count = 0
		for line in lines:
			if(line.find(';') != -1):
				count += 1
		return count - 1




if __name__ == "__main__":

	schParser = ScheduleParser()
	schParser.parseFile('Spring2015.scd')

	
	courseList = schParser.getCourseList()

	print courseList

	schedules = schParser.getSchedules()
	for i in schedules:
		print i
