import pandas as pd
import json

#Class for smallest unit of time table which stores the teacher emailID, class code and class name
class slot_info:
  def __init__(self):
    self.slot = {
        "teacher_email" : None,
        "class_code" : None,
        "class_name" : None,
        "timeSlot": None
    }

#Class for storing the complete time-table for a particular group(group+batchNumber)
class time_table:
  def __init__(self):
    self.schedule = {
        "monday" : [],
        "tuesday" : [],
        "wednesday" : [],
        "thursday" : [],
        "friday" : [],
        "saturday" : []
    }

#Class for storing all the information for a particular group
class class_unit:
  def __init__(self):
    self.classes = {
        "batchNumber": None,
        "branch": None,
        "timeTable": None
    }

class timeTableMain:
  def __init__(self):
    self.timeTable = {
        "degree": None,
        "year": None,
        "time_table_data": []
    }

def getSlotInfo(string, time):
  if not str(string) == "nan":
    strList = string.split(' ')
    slotObj = slot_info()
    slotObj.slot['teacher_email'] = strList[0]
    slotObj.slot['class_code'] = strList[2]
    slotObj.slot['class_name'] = " ".join(strList[1].split("-"))
    slotObj.slot['timeSlot'] = time
    return slotObj.slot
  return None


timeSlots = [8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
def getTimeTable(col):
  timeTableObj = time_table()
  for i in range(0,len(col)):
    day = int(i/11)
    timeSlot = i%11
    slotObj = getSlotInfo(str(col[i]), timeSlots[timeSlot])
    if slotObj is None:
      continue
    if day == 0:
      timeTableObj.schedule['monday'].append(slotObj)
    elif day == 1:
      timeTableObj.schedule['tuesday'].append(slotObj)
    elif day == 2:
      timeTableObj.schedule['wednesday'].append(slotObj)
    elif day == 3:
      timeTableObj.schedule['thursday'].append(slotObj)
    elif day == 4:
      timeTableObj.schedule['friday'].append(slotObj)
    elif day == 5:
      timeTableObj.schedule['saturday'].append(slotObj)
  return timeTableObj.schedule
# print(getTimeTable(df.iloc[:,0]).schedule['monday'][0].slot['class_name'])

def getClassDetail(col):
  classObj = class_unit()
  group = str(col.name)
  for i in range(0, len(group)):
    if group[i].isdigit():
      classObj.classes['branch'] = group[:i]
      classObj.classes['batchNumber'] = group[i:]
      break
  classObj.classes['timeTable'] = getTimeTable(col)

  # print(classObj.classes['batchNumber'])
  return classObj.classes

def makeTimeTableDB(path):
  timetable = []
  xl = pd.ExcelFile(path)
  for sheet in xl.sheet_names:
    df = pd.read_excel(path, sheet_name=sheet, index_col=0)
    timetableMainObj = timeTableMain()
    sheetNameList = sheet.split("_")
    timetableMainObj.timeTable['degree'] = sheetNameList[0]
    timetableMainObj.timeTable['year'] = sheetNameList[1]
    for i in range(df.shape[1]):
      groupTimeTable = getClassDetail(df.iloc[:,i])
      json.dumps(groupTimeTable)
      # print(groupTimeTable.classes['batchNumber'])
      timetableMainObj.timeTable['time_table_data'].append(groupTimeTable)
    timetable.append(timetableMainObj.timeTable)
  return timetable

def converter(path):
    tt = makeTimeTableDB(path)
    jsonObj = json.dumps(tt)
    with open("scheduler/TimeTableDB.json", "w") as outfile:
        outfile.write(jsonObj)