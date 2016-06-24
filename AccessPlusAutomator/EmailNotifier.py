from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
import datetime
import time

class EmailNotifier():

	def __init__(self,username,password):

		self.username = username  
		self.password = password 


		
		self.msg = MIMEMultipart()
		self.msg['From'] = self.username




	def sendEmail(self,toaddr):
		self.msg['To'] = toaddr

		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		try :
		    server = smtplib.SMTP("smtp.mail.yahoo.com",587)#465
		    
		    server.ehlo()
		    server.starttls()
		    server.ehlo()

		    server.login(self.username, self.password)
		    server.sendmail(self.username, toaddr, self.msg.as_string())
		    server.quit()
		    

		    

		    print 'Email has been sent with subject line "' + self.msg['Subject'] + '"  to ' +  toaddr + ' at: ' + str(timestamp)
		except:
			print 'Unable to send email with subject line "' + self.msg['Subject'] + '"  to ' +  toaddr + ' at: ' + str(timestamp)

	#program did not run properly
	def notifyTermination(self, terminationMsg):
		self.msg['Subject'] = "APlusNotifier: Program Terminated"
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		body = 'Program terminated at: ' + str(timestamp)

		body += '\n\nUnexpected Error: \n'

		body += terminationMsg

		self.msg.attach(MIMEText(body, 'plain'))

	#a better schedule is available but the user must take action
	def notifyAvailableSchedule(self,baseSchedule,desiredSchedule):
		self.msg['Subject'] = "APlusNotifier: Schedule Updated Available"
		body = 'There is a better schedule Available. User action Required'
		body = self.createMsg(body, baseSchedule, desiredSchedule)


		self.msg.attach(MIMEText(body, 'plain'))


	#classes added successfully
	def notifySuccesfulUpdate(self,baseSchedule,desiredSchedule,currentSchedule):
		self.msg['Subject'] = "APlusNotifier: Schedule Changed"
		body = 'Schdedule was successfully Updated!'
		body = self.createMsg(body, baseSchedule,desiredSchedule,currentSchedule)

		self.msg.attach(MIMEText(body, 'plain'))
		

	#class update failed
	def notifyFailedUpdate(self,baseSchedule,desiredSchedule,currentSchedule):
		self.msg['Subject'] = "APlusNotifier: Schedule Update Failed"
		body = 'There was a failure with course update. Reverted to original Schdedule.'
		body = self.createMsg(body, baseSchedule,desiredSchedule,currentSchedule)

		self.msg.attach(MIMEText(body, 'plain'))		


	#was unable to revert schedule
	def notifyRevertFailed(self,baseSchedule,desiredSchedule,currentSchedule):
		self.msg['Subject'] = "APlusNotifier: UNABLE TO REVERT ORGINIAL SCHEDULE!"
		body = 'There was a failure and was unable to revert to original schedule, User action required'
		body = self.createMsg(body, baseSchedule,desiredSchedule,currentSchedule)

		self.msg.attach(MIMEText(body, 'plain'))


	#creates message body
	def createMsg(self, text, baseSchedule, desiredSchedule, currentSchedule = None):
		text += '\n'

		text += 'The original schedule BEFORE action was taken: \n'
		text += str(baseSchedule) + '\n\n\n'

		text += 'The desired schedule: \n'
		text += str(desiredSchedule) + '\n\n\n' 


		if currentSchedule is not None:
			text += 'The current schedule AFTER action was taken: \n'
			text += str(currentSchedule) + '\n\n\n' 

		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		text += "Message created at:  " + str(timestamp)



		return text

	def notifyHeartBeat(self, text):
		self.msg['Subject'] = "APlusNotifier: Heartbeat"
		body = 'Program is running properly\n'
		body += text + '\n'

		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		body += "Message created at:  " + str(timestamp)
		self.msg.attach(MIMEText(body, 'plain'))

