import uuid
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from Booking import Booking
from Seat import Seat

class Show:
    '''
        Each show/Cinema hall shall have fixed number of rows
    '''
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
        selectedSeats = []
        for seatNumber in seats:
            currentSeat = self.getSeat(seatNumber)
            if currentSeat is None:
                raise Exception('\nInvalid seat Number!!\n')
            elif not currentSeat.is_available:
                raise Exception('\nSome of the selected seats are already booked!! Try again !\n')
            else :
                selectedSeats.append(currentSeat)
                
        total_available_seats = len(self.available_seats())
        
        if 10*len(selectedSeats) > total_available_seats:
            raise Exception('\nYou cannot book more than {} seats in one booking !!\n'.format(int(0.1*total_available_seats)))
        
        return Booking(
            showID=self.ID,
            userID=userID,
            selectedSeats=selectedSeats
        )
        
    '''
        returns all unoccupied seats
    '''
    def available_seats(self):
        vacant_seats = [seat for seat in self.seats.values() if seat.is_available]
        return vacant_seats
    
    '''
        Displays the seat selector matrix as a pandas DataFrame
    '''     
    def seatSelector(self):
        vacant_seats = self.available_seats()
        print('\n{} seats are available for booking \n'.format(len(vacant_seats)))
       
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
