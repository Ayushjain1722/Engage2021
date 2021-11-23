import csv
from scheduler.config import threshold

def getDetails(studentEmail, UserList):
    for student in UserList:
        if studentEmail == student.email:
            return student
    return None

#The list of preferences is sorted according to the vaccination status of the students and then according to the timestamps.
def studentSelection(UserList, PhysicalClassList):
    studentList = []
    teacherList = []
    batchCount = {}
    studentsThreshold = threshold
    for entry in PhysicalClassList:
        entryFound = False
        student_details = getDetails(entry.email, UserList)
        #Check the number of students of particular batch and then decide if the students are less than the threshold or not..
        groupName = student_details.branch + student_details.groupNumber
        if groupName in list(batchCount.keys()) and batchCount['groupName'] >= studentsThreshold:
            continue
        for student_email in studentList:
            #If this student had a class earlier as well, then add this class in the list as well..
            if entry.email == student_email['email']:
                student_email['classes'].append({
                    "class_name": entry.className,
                    "class_code": entry.classCode,
                    "timeSlot": entry.timeSlot
                })
                entryFound = True
        if entryFound == False:
            studentList.append({"email": entry.email, 
                                "rollNo": student_details.rollNumber,
                                "classes": [{
                                                "class_name": entry.className,
                                                "class_code": entry.classCode,
                                                "timeSlot": entry.timeSlot,
                                            }]
                                })
        #Check if teacher had a class schedule initialized earlier or not, if not, intialize it, otherwise add it to the list    
        entryFound = False
        for teacher_email in teacherList:
            if entry.teacherEmail == teacher_email['email']:
                teacher_email['classes'].append({
                    "rollNo": student_details.rollNumber,
                    "groupNo": student_details.branch + student_details.groupNumber,
                    "class_name": entry.className,
                    "class_code": entry.classCode,
                    "timeSlot": entry.timeSlot
                })    
                entryFound = True
        if entryFound == False:
            teacherList.append({"email": entry.teacherEmail,
                                "classes": [{
                                                "rollNo": student_details.rollNumber,
                                                "groupNo": student_details.branch + student_details.groupNumber,
                                                "class_name": entry.className,
                                                "class_code": entry.classCode,
                                                "timeSlot": entry.timeSlot
                                            }]
                                })  
        
    #Saving the contents in a csv file that is to be sent in the email to the student
    csv_columns = ["class_name", "class_code", "timeSlot"]
    for student in studentList:
        fileName = student['email'] + ".csv"
        with open('scheduler/mails/'+fileName, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for classDetails in student['classes']:
                writer.writerow(classDetails)
    #Saving the contents in a csv file that is to be sent in the email to the teacher
    csv_columns = ["rollNo", "groupNo", "class_name", "class_code", "timeSlot"]
    for teacher in teacherList:
        fileName = teacher['email']
        with open('scheduler/mails/'+f'{fileName}.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            for data in teacher['classes']:
                writer.writerow(data)

    return studentList, teacherList