import uuid

class Seat{
    def __init__(self, row, number):
        self.ID = uuid.uuid4().hex
        self.row = row
        self.number = number
        self.is_booked = False
        self.bookingID = None
        
        
    def bookSeat(self, bookingID):
        self.is_booked = True
        self.bookingID = bookingID
        
    def cancelSeat(self):
        self.is_booked = False
        self.bookingID = None
}

class Show{
    def __init__(self, numberOfSeats):
        self.ID = uuid.uuid4().hex
        self.seats = {}
        
        for row in range(rows):
            for seatNumber in range(seatsPerRow):
                seat = Seat()
            
        
    
    def availabe_seats(self):
        # TODO : fetch available seats
        pass
    
}

class Booking{
    def __init__(self, showID, userID, seats):
        self.ID = uuid.uuid4().hex
        self.showID = showID
        self.userID = userID
        
        self.bookedSeats = {}
        for seat in seats:
            self.bookedSeats[seat.ID] = seat
            
        pass
        
    def cancelSeat(self, seatID):
        try:
            self.bookedSeats[seatID].cancelSeat()
            self.bookedSeats.pop(seatID)
        except KeyError:
            print("You have not booked this seat!")
    
    def cancelBooking(self):
        for seat in self.bookedSeats.values():
            seat.cancelSeat()
        
}



class Theatre{
    
    def __init__(self, *args, **kwargs):
        # TODO : init system with predefined shows
        pass
        
    def available_shows(self):
        # TODO : return available shows with times
        pass
        
    def available_seats(self, showID):
        # TODO : call shows[showID].availabe_shows()
        pass
        
    def bookTicket(self, userID, showID, seats):
        # TODO : call shows[showID].bookTicket(userID, seats)
        pass
        
    def cancelBooking(self, bookingID):
        # TODO : call shows[showID].cancelBooking(bookingID)
        pass
        
    def cancelSeat(self,userID, bookingID, seatID):
        # TODO : call bookings[bookingID].cancelSeat(userID, seatID)
        pass
        
}


class User{

    def __init__(self, *args, **kwargs):
        # TODO : init user
        pass
        
    def bookTicket(self, showID, seats):
        # TODO : input showID and seats
        pass
        
    def cancelBooking(self, bookingID):
        pass
        
    def cancelSeat(self, bookingID, seatID):
        pass
}