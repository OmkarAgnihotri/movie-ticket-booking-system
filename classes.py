import uuid
import numpy as np
import pandas as pd

class Show:
    ROWS = 5
    def __init__(self,startTime, endTime, numberOfSeats):
        self.ID = uuid.uuid4().hex
        self.__startTime = startTime
        self.__endTime = endTime

        self.seatsPerRow = numberOfSeats//self.ROWS
        
        self.seats = {}
        for row in range(self.ROWS):
            for seatNumber in range(1,self.seatsPerRow + 1):
                seat = Seat(chr(row + ord('A')), seatNumber)
                self.seats[seat.ID] = seat

    
    def bookTicket(self, userID, seats):
        # seats = ['A1', 'A2', 'A3',..]
        
        selectedSeats = []
        for seatNumber in seats:
            currentSeat = self.getSeat(seatNumber)
            if currentSeat is None:
                raise Exception('Invalid seat Number!!\n')
            elif not currentSeat.is_available:
                raise Exception('Some of the selected seats are already booked!! Try again !\n')
            else :
                selectedSeats.append(currentSeat)
                
        total_available_seats = len(self.available_seats())
        
        if 10*len(selectedSeats) > total_available_seats:
            raise Exception('You cannot book more than {} seats in one booking !!\n'.format(int(0.1*total_available_seats)))
        
        return Booking(
            showID=self.ID,
            userID=userID,
            selectedSeats=selectedSeats
        )
    
    def available_seats(self):
        vacant_seats = [seat for seat in self.seats.values() if seat.is_available]
        return vacant_seats
            
    def seatSelector(self):
        vacant_seats = self.available_seats()
        print('{} seats are available for booking \n'.format(len(vacant_seats)))
       
        seat_view = np.array(list(self.seats.values())).reshape(self.ROWS, self.seatsPerRow)
        
        seat_view = pd.DataFrame(
            seat_view,
            index = [chr(row + ord('A')) for row in range(self.ROWS)],
            columns = [i+1 for i in range(self.seatsPerRow)]
        )
        
        return seat_view
            
    # Utility methods
    def getSeat(self, seatNumber):
        return next((seat for seat in self.seats.values() if seat.seatNo == seatNumber), None)
    
    @property
    def date(self):
        return self.__startTime.strftime("%m/%d/%Y")
    @property
    def duration(self):
        interval = self.__endTime - self.__startTime
        seconds = interval.total_seconds()
        hours = int(seconds//3600)
        minutes = int((seconds%3600)//60)
        return "{}:{}".format(hours, minutes)
        
    @property
    def start(self):
        return "{}:{}".format(self.__startTime.hour, self.__startTime.minute)


class Booking:
    def __init__(self, showID, userID, selectedSeats):
        self.ID = uuid.uuid4().hex
        self.showID = showID
        self.userID = userID
        
        self.bookedSeats = {}
        for seat in selectedSeats:
            seat.bookSeat(self.ID)
            self.bookedSeats[seat.ID] = seat
       
        
    def cancelSeat(self,userID, seatNumber):
        if userID != self.userID:
            raise Exception('You are not the owner of this seat !!\n')
            
        bookedSeat = next((seat for seat in self.bookedSeats.values() if seat.seatNo == seatNumber), None)
        if bookedSeat is not None:
            self.bookedSeats[bookedSeat.ID].cancelSeat()
            self.bookedSeats.pop(bookedSeat.ID, None)
        else:
            raise Exception("Seat {} is not booked in this booking !!\n".format(seatNumber))
    
    def cancelBooking(self, userID):
        if userID != self.userID:
            raise Exception('You are not the owner of this booking !!\n')
            
        for seat in self.bookedSeats.values():
            seat.cancelSeat()
    
    def printBookingDetails(self):
        pass
 

class Seat:
    def __init__(self, row, number):
        self.ID = uuid.uuid4().hex
        self.row = row
        self.number = number
        self.is_booked = False
        self.bookingID = None
        
    @property
    def seatNo(self):
        return self.row + str(self.number)
        
    def bookSeat(self, bookingID):
        self.is_booked = True
        self.bookingID = bookingID
        
    def cancelSeat(self):
        self.is_booked = False
        self.bookingID = None
        
    @property
    def is_available(self):
        return not self.is_booked

class Theatre:
    
    def __init__(self, numberOfSeats, numberOfShows):
        self.bookings = {}
        # numberOfShows is a list of tuples representing start, end times
        
        self.shows = {}
        for startTime,endTime in numberOfShows:
            createdShow = Show(startTime, endTime, numberOfSeats)
            self.shows[createdShow.ID] = createdShow
        
    def available_shows(self):
        
        timetable = pd.DataFrame({
            'showID' : [show.ID for show in self.shows.values()],
            'Date' : [show.date for show in self.shows.values()],
            'Start Time' : [show.start for show in self.shows.values()],
            'Duration' : [show.duration for show in self.shows.values()],
            'Available seats' : [len(show.available_seats()) for show in self.shows.values()]
        }, index = [i+1 for i in range(len(self.shows.values()))])
        
        return timetable
        
    def available_seats(self, showID):
        try:
            show = self.shows[showID]
            return show.available_seats()
        except KeyError:
            print("Invalid show!")
        
    def bookTicket(self, userID, showID, seats):
        try:
            show = self.shows[showID]
            booking = show.bookTicket(userID, seats)
            if booking is not None :
                self.bookings[booking.ID] = booking
                
            return booking                
            
        except KeyError:
            print("Not a valid show!!")
        except Exception as err:
            print(err)
        
    def cancelBooking(self, userID, bookingID):
        self.bookings[bookingID].cancelBooking(userID)
        self.bookings.pop(bookingID, None)    
        
    def seatSelector(self, showID):
        try:
            return self.shows[showID].seatSelector()
        except KeyError:
            print('\nINVALID SHOW !!\n')
        
    def cancelSeat(self,userID, bookingID, seatNumber):
        self.bookings[bookingID].cancelSeat(userID, seatNumber)
        
    def getBookedShows(self, bookings):
        try:
            return pd.DataFrame({
                'bookingID':[booking.ID for booking in bookings],
                'Start Time':[self.shows[booking.showID].start for booking in bookings],
                'Booked Seats' : [len(booking.bookedSeats.values()) for booking in bookings],
                'seat Numbers' : [' '.join([seat.seatNo for seat in booking.bookedSeats.values()]) for booking in bookings ]
            }, index = [i+1 for i in range(len(bookings))])
            
        except KeyError:
            pass
            
 

class User:

    def __init__(self, firstName, lastName, theatre):
        self.ID = uuid.uuid4().hex
        self.firstName = firstName
        self.lastName = lastName
        self.theatre = theatre
        self.bookings = {}
        
    def bookTicket(self, showID, seats):
        if len(seats) == 0:
            print("Must select atleast One seat !! \n")
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
            print("Booking Failed\n")
                    
        
    def cancelBooking(self, bookingID):
        self.theatre.cancelBooking(self.ID, bookingID)
        try:
            self.bookings.pop(bookingID, None)
            print('Succesfully cancelled the booking !!\n')
        except KeyError:
            print('Invalid Booking ID !!\n')
        except Exception as err:
            print(err)
        
    def cancelSeat(self, bookingID, seatNumber):
        
        try:
            if len(self.bookings[bookingID].bookedSeats) == 1:
                self.cancelBooking(bookingID)
                return
                
            self.theatre.cancelSeat(self.ID, bookingID, seatNumber)
            print('Successfully cancelled seat {}'.format(seatNumber))
        except KeyError:
            print('Invalid Booking ID !!\n')
        except Exception as err:
            print(err)
            
    def bookedShows(self):
        return self.theatre.getBookedShows(self.bookings.values())
        
    def getBookedTickets(self):
        return self.bookings.items()

class Interval:
    def __init__(self, *args, **kwargs):
        # TODO : initialize with start and endtime
        pass
           
    @property
    def duration(self):
        # TODO : return interval duration
        pass
