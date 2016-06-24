

class Course():

	def __init__(self, department, course, section = None, status = None):
			self.department = department
			self.course = course
			self.section = section
			self.status = status

	def isEqual(self,other):
		return (self.department == other.department and self.course == other.course and self.section == other.section)

	def __str__(self):
		string = ''
		string += '{' + self.department + ' '
		string += self.course + ' '
		if(self.section is not None):
			string += self.section + ' '
		if(self.status is not None):
			string += self.status + ' '
		string += '}'
		return string