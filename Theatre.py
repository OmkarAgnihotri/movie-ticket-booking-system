import numpy as np
import pandas as pd
from Show import Show
from Seat import Seat


'''
    This Class represents the original ticket booking system
'''
class Theatre:
    
    def __init__(self, numberOfSeats, numberOfShows):
        self.bookings = {}
        # numberOfShows is a list of tuples representing start, end times
        
        self.shows = {}
        for startTime,endTime in numberOfShows:
            createdShow = Show(startTime, endTime, numberOfSeats)
            self.shows[createdShow.ID] = createdShow
            
    ''' 
        returns all available shows as a pandas dataFrame
        columns include - date, start time, duration, vacant/available seats
    '''
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