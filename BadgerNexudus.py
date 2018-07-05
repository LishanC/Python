# file name -BadgerNexudus.py

import pprint   #pretty printer for displaying JSON nicely
import requests #for making server calls
from requests.auth import HTTPBasicAuth #for server call authentication
from users import User   # call users class
from booking import Booking # call Booking class
from machine import Machine # call Machine class
import datetime

#for display setting
pp = pprint.PrettyPrinter(indent=4)

#perform HTTP GET call to Nexudus server, and returns list of user objects

response_users = requests.get("https://spaces.nexudus.com/api/sys/users",
         auth=HTTPBasicAuth("spacebadgerstest@gmail.com", "Badger123"))

#perform HTTP GET call to Nexudus server and return list of booking objects
response_booking = requests.get("https://spaces.nexudus.com/api/spaces/bookings",
         auth=HTTPBasicAuth("spacebadgerstest@gmail.com", "Badger123"))

#perform HTTP GET call to Nexudus server and return list of machine objects
response_machines = requests.get("https://spaces.nexudus.com/api/spaces/resources",
         auth=HTTPBasicAuth("spacebadgerstest@gmail.com", "Badger123"))
     	

#extract results as JSON
users = response_users.json()
bookings = response_booking.json()
machines = response_machines.json()

    # 1. Check for valid username.
    # 2. Check for user authorizations.
    # 3. check for machine authorization requirements.
    # 4. Check that authorizations match.
    # 5. Check for reservation.

def validateAction(badgerAction, user):
    #print(badgerAction)
    result = BadgerResponseType.ERROR_UNKNOWN
    if not user:
       user = badgerAction['user']
       machine = badgerAction['machine']
       action = badgerAction['action']
  
	
	# 2.check for user authorizations
    userAuth = _getUserAuthorizations(user)
    if not userAuth:
        result = BadgerResponseType.NOT_RECOGNIZED
    else:
	    # 3.check for machine authorization requirements
        machineAuth = _getMachineAuthorizationRequirement(machine)
		
		# 4. check user and machine authorizations match
        match = _checkAuthorizationsMatch(userAuth, machineAuth)
        if not match:
            result = BadgerResponseType.NOT_AUTHORIZED
        else:
		    # 5. check for reservation
            now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            eventId = _checkMachineReservation(user, machine, now)
            if not eventId :
                result = BadgerResponseType.NOT_AVAILABLE
            else:
                _updateMachineReservation(eventId, action, user, machine, dateTime)
                
    if result == BadgerResponseType.OK:
        _updateMachineStateCache(user, machine, action)
        
    return result

def _getUserAuthorizations(user):
#print all the user objects with fields FullName, Id , UniqueId, AccessToken
   list_user = []
   result=true
   for i in range(len(users)):
       fullname = users["Records"][i]["FullName"]
       id = users["Records"][i]["Id"]
       uniqueId = users["Records"][i]["UniqueId"]
       accesstoken = users["Records"][i]["AccessToken"]

       user = User(fullname, id, UniqueId,accesstoken)
       #testing purposes to check if I can get the data
       #user = {"Name": fullname , "id" : id , "UniqueId" : uniqueId , "AccessToken" : accesstoken}
       list_user.append(user)
  
    if user in list_user:
	   return result;
   
 
 def _getMachineAuthorizationRequirement(machine):
   #get all resource (machine objects)
   list_machine = []
   for i in range(len(machines["Records"])):
       machineName = machines["Records"][i]["Name"]
       groupName = machines["Records"][i]["GroupName"]
       resourceTypeId = machines["Records"][i]["ResourceTypeId"]
       businessId = machines["Records"][i]["BusinessId"]

       #using the above fields to create a machine object
       new_machine = Machines(machineName, groupName, resourceTypeId, businessId)
       list_machine.append(new_machine)
  
    # check if the require machine in the database
    if machine in list_machine:
      return true
	 else:
	   return false
 	
#get data from resources -> accessrule and check if the user have access authorization to the machine
# https://spaces.nexudus.com/api/spaces/resourceaccessrules can get all the access rules
# https://spaces.nexudus.com/api/spaces/resourceaccessrules/{id} can get the Members of the machine
def _checkAuthorizationsMatch(userAuthorizations, machineRequirements):
	memberlist=[]
	
	# perform HTTP GET call to Nexudus server and return list of machine objects and it's members
	resource_request=requests.get("https://spaces.nexudus.com/api/spaces/resourceaccessrules/",
	      auth=HTTPBasicAuth("spacebadgerstest@gmail.com", "Badger123"))
	
	# resourceID is the machineID
	resource=resource_request.json()
    for i in range(len(resource["Records"])):
	   if machineRequirements==resource["Records"][i]["ResourceId"]: 
	      ruleid=resource["Records"][i]["Id"] 
		
     # perform HTTP GET call to Nexudus server and return list of member of that ruleID 		
    rules_request=requests.get("https://spaces.nexudus.com/api/spaces/resourceaccessrules/{ruleid}",
          auth=HTTPBasicAuth("spacebadgerstest@gmail.com", "Badger123"))
		  
   accessrules=rules_request.json()
   
     memberlist=accessrules["Members"]
    if userAuthorizations in memberlist:
       return true
    else :
      return false
    
    
#get data from booking calendar and check user and machine and dateTime match, return eventID
def _checkMachineReservation(user, machine, dateTime):
  
  # set the time format to UTC time
   now = datetime.utcnow().isoformat() + 'Z'
   list_calendar = []
   for i in range(len(bookings["Records"])):
       bookid = bookings["Records"][i]["ResourceId"]
       bookname = bookings["Records"][i]["ResourceName"]
       userid = bookings["Records"][i]["CoworkerId"]
       userfullname = bookings["Records"][i]["CoworkerFullName"]
       bookfromtime = bookings["Records"][i]["FromTime"]
       booktotime = bookings["Records"][i]["ToTime"]
       
	   #create a Booking object
       book=Booking(bookid, bookname, usererid, userfullname,bookfromtime, booktotime)
       
	   #add the Booking object to the list
       list_calendar.append(booking)
  
   # compare the user, machine and dateTime with the Booking object
   for i in range(len(list_calendar)):
       book1=list_calendar[i]
       if book1.bookname==machine && book1.userfullname==user && now >book1.bookfromtime && now <booktotime:
	      return book1.resourceid
	    else:
		  return false
  
# method when user bagerin , log information feedback to Nexudus server and automatically create a checkin event
def _checkinReservation(user,dateTime):
    now=datetime.datetime.now()
	url='https://ccsf.spaces.nexudus.com/api/public/checkin'
    username = "spacebadgerstest@gmail.com"
    password = "Badger123"
    query = {
     'BusinessId': '572455884',
     'FromTime':  now,
    }

    response = requests.post(url,auth=(username, password),data=query,verify=True)
    content = json.loads(response.content)
	print(content)
	 
    return True
     	 




 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 

