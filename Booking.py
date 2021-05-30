import uuid

'''
    This class represents a Booking of a Movie Ticket
'''

class Booking:
    def __init__(self, showID, userID, selectedSeats):
        self.ID = uuid.uuid4().hex
        self.showID = showID
        self.userID = userID
        
        self.bookedSeats = {}
        for seat in selectedSeats:
            seat.bookSeat(self.ID)
            self.bookedSeats[seat.ID] = seat
       
    '''
        Cancels a particular seat
        throws error if either the user is not the owner of this seat
        or if the seat is not present in the booking
    '''   
    def cancelSeat(self,userID, seatNumber):
        if userID != self.userID:
            raise Exception('\nYou are not the owner of this seat !!\n')
            
        bookedSeat = next((seat for seat in self.bookedSeats.values() if seat.seatNo == seatNumber), None)
        if bookedSeat is not None:
            self.bookedSeats[bookedSeat.ID].cancelSeat()
            self.bookedSeats.pop(bookedSeat.ID, None)
        else:
            raise Exception("\nSeat {} is not booked in this booking !!\n".format(seatNumber))
        
    '''
        Cancels a particular booking
        throws error if either the user is not the owner of this booking
        and then frees up all the seats that are associated with this booking
    '''   
    def cancelBooking(self, userID):
        if userID != self.userID:
            raise Exception('\nYou are not the owner of this booking !!\n')
            
        for seat in self.bookedSeats.values():
            seat.cancelSeat()