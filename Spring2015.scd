
#All feilds are cap and space sensitive

#List all course which will apprear in every schedule
Courses:
MATH, 267, None
COM S, 309, None
CPR E, 288, None
E E, 201, None
;

#Scheules will be listed in order of priority
#A section must be listed
Schedule: 0
MATH, 267, 11
COM S, 309, 1
CPR E, 288, C
E E, 201, D
;

Schedule: 1
MATH, 267, 12
COM S, 309, 1
CPR E, 288, C
E E, 201, D
;

Schedule: 2
MATH, 267, 11
COM S, 309, 2
CPR E, 288, C
E E, 201, D
;

Schedule: 3
MATH, 267, 12
COM S, 309, 2
CPR E, 288, C
E E, 201, D
;

Schedule: 4
MATH, 267, 11
COM S, 309, 2
CPR E, 288, D
E E, 201, E
;

Schedule: 5
MATH, 267, 12
COM S, 309, 2
CPR E, 288, D
E E, 201, E
;


#Last Schedule is always your current schedule
Schedule: 6
MATH, 267, 5
COM S, 309, 1
CPR E, 288, C
E E, 201, D
;