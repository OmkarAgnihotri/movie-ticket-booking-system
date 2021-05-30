import uuid

class Seat:
    def __init__(self, row, number):
        self.ID = uuid.uuid4().hex
        self.row = row
        self.number = number
        self.is_booked = False
        self.bookingID = None
    
    '''
        Returns the Seat Number of the seat instance
    '''
    @property
    def seatNo(self):
        return self.row + str(self.number)
        
    '''
        Books the seat by setting is_booked flag to True
        and bookingID to the booking which the seat belongs to
    '''
    def bookSeat(self, bookingID):
        self.is_booked = True
        self.bookingID = bookingID
        
    '''
        Cancels the seat by setting is_booked flag to False
    '''
    def cancelSeat(self):
        self.is_booked = False
        self.bookingID = None
        
    @property
    def is_available(self):
        return not self.is_booked