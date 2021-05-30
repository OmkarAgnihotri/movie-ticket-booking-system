import uuid

'''
    this class represents a user communicating with
    the ticket booking system
'''
class User:

    def __init__(self, firstName, lastName, theatre):
        self.ID = uuid.uuid4().hex
        self.firstName = firstName
        self.lastName = lastName
        self.theatre = theatre
        self.bookings = {}
        
    def bookTicket(self, showID, seats):
        if len(seats) == 0:
            print("\nMust select atleast One seat !! \n")
            return
        
        booking = self.theatre.bookTicket(
            self.ID,
            showID,
            seats
        )
        
        if booking is not None:
            self.bookings[booking.ID] = booking
            print('\n BOOKING SUCCESSFULL \n')
            print('\n BOOKING ID IS {} FOR FURTHER REFERENCE \n'.format(booking.ID))
        else :
            print("\nBooking Failed\n")
                    
        
    def cancelBooking(self, bookingID):
        self.theatre.cancelBooking(self.ID, bookingID)
        try:
            self.bookings.pop(bookingID, None)
            print('\nSuccesfully cancelled the booking !!\n')
        except KeyError:
            print('\nInvalid Booking ID !!\n')
        except Exception as err:
            print(err)
        
    def cancelSeat(self, bookingID, seatNumber):
        
        try:
            if len(self.bookings[bookingID].bookedSeats) == 1:
                self.cancelBooking(bookingID)
                return
                
            self.theatre.cancelSeat(self.ID, bookingID, seatNumber)
            print('\nSuccessfully cancelled seat {}'.format(seatNumber))
        except KeyError:
            print('\nInvalid Booking ID !!\n')
        except Exception as err:
            print(err)
            
    def bookedShows(self):
        return self.theatre.getBookedShows(self.bookings.values())
        
    def getBookedTickets(self):
        return self.bookings.items()