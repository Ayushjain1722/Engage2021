import json

def getStatus(beneficiary_id):
  with open('./CoWinDB.json') as json_file:
    vaccinationData = json.load(json_file)
  for entry in vaccinationData:
    if entry['beneficiary_id'] == beneficiary_id:
      return entry['status']
  return "Record not found"


def priority(beneficiary_id):
  current_status = getStatus(beneficiary_id)
  if "Fully" in current_status:
    priority = 2
  elif "Partially" in current_status:
    priority = 1
  else:
    priority = 0
  return priority