class Booking:

    # User class to create a user object 
    def __init__(self, ResourceId, ResourceName, CoworkerId, CoworkerFullName, BookFromTime, BookToTime):
        self.ResourceId = ResourceId
        self.ResourceName = ResourceName
        self.CoworkerId = CoworkerId
        self.CoworkerFullname= CoworkerFullName
	self.BookFromTime=BookFromTime
	self.BookToTime=BookToTime
