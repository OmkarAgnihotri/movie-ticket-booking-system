from Booking import Booking
from Seat import Seat
from Show import Show
from Theatre import Theatre
from User import User
from datetime import datetime, time, date

USERS = []

NAMES = ['Omkar Agnihotri', 'John Doe', 'Dummy User']

SHOWS = [
    (datetime(2021, 5,30,8,15), datetime(2021, 5,30,10,30)),
    (datetime(2021, 5,30,10,30), datetime(2021, 5,30,12, 45)),
    (datetime(2021, 5,30,12,0), datetime(2021, 5,30,14,0)),
    (datetime(2021, 5,30,13,25), datetime(2021, 5,30,16,0)),
    (datetime(2021, 5,30,15,35), datetime(2021, 5,30,17,30)),
    (datetime(2021, 5,30,18,45), datetime(2021, 5,30,20,45))
]

numberOfSeats = 30
while True:
    try:
        numberOfSeats = int(input('\n Enter number of seats per show to start with :'))
        break
    except Exception:
        print('\n INVALID INPUT !\n')
        
THEATRE = Theatre(numberOfSeats, SHOWS)

for firstName, lastName in [name.split() for name in NAMES]:
    USERS.append(User(firstName, lastName, THEATRE))
    
def isValidChoice(choice, available_choices):
    if choice > 0 and choice <= available_choices:
        return True
    False

LOGGED_IN_USER = None
def login():
    print('\n=========== PLEASE SELECT USER PROFILE ============\n')
    
    flag = False
    while not flag:
        for index, user in enumerate(USERS):
            print('{}. {} {}'.format(index + 1, user.firstName, user.lastName))
        try:
            choice = int(input('\nSelect User Profile : '))
            
            if isValidChoice(choice, 3):
                LOGGED_IN_USER = USERS[choice - 1]
                
                print('\n======== WELCOME {} ==============\n'.format(LOGGED_IN_USER.firstName))
                break
            else :
                print('\nINVALID CHOICE! PLEASE TRY AGAIN !!\n')
        except Exception:
            print('\nINVALID CHOICE! PLEASE TRY AGAIN !!\n')
        
            
    return LOGGED_IN_USER
            
def logout():
    LOGGED_IN_USER = None
    return LOGGED_IN_USER

def list_available_shows():
    print('\n=========FOLLOWING ARE AVAILABLE SHOWS ============\n')
    AVAILABLE_SHOWS = THEATRE.available_shows()
    print(AVAILABLE_SHOWS.iloc[:, 1:])
    return AVAILABLE_SHOWS
    
def book_ticket():
    
    while True:
        AVAILABLE_SHOWS=list_available_shows()
        choice = int(input('\nSelect a show : '))
        
        if isValidChoice(choice, AVAILABLE_SHOWS['showID'].shape[0]):
            SELECTED_SHOW = AVAILABLE_SHOWS.iloc[choice - 1]['showID']
            SEATS = THEATRE.seatSelector(SELECTED_SHOW)
            print(SEATS.applymap(lambda seat : int(seat.is_booked)))
            
            try:
                choice = int(input('\n ENTER NUMBER OF SEATS : '))
                SELECTED_SEATS = []
                chosen_seats = 0
                while chosen_seats < choice:
                    chosenSeat = input(' SELECT {} SEAT : '.format(chosen_seats + 1))
                    if chosenSeat in SELECTED_SEATS:
                        print('\n SEAT ALREADY SELECTED !! CHOOSE ANOTHER ONE!\n')
                    else:
                        SELECTED_SEATS.append(chosenSeat)
                        chosen_seats+=1
                
                LOGGED_IN_USER.bookTicket(SELECTED_SHOW, SELECTED_SEATS)
                break
            except Exception:
                print("\n INVALID OPTION\n")
        else :
            print('\nINVALID CHOICE! PLEASE TRY AGAIN !!\n')
            
def cancel_booking():
    while True:
        if len(LOGGED_IN_USER.bookings.values()) == 0:
            print('\n YOU HAVE NO BOOKED SHOWS\n')
            break
        
        print('\n=========FOLLOWING ARE YOUR BOOKED SHOWS ============\n')
        BOOKED_SHOWS = LOGGED_IN_USER.bookedShows()
        print(BOOKED_SHOWS.iloc[:, 1:])
        choice = int(input('\nSelect a Booking to cancel : '))
        
        if isValidChoice(choice, BOOKED_SHOWS['bookingID'].shape[0]):
            SELECTED_BOOKING = BOOKED_SHOWS.iloc[choice - 1]['bookingID']
            
            LOGGED_IN_USER.cancelBooking(SELECTED_BOOKING)
            break
        else :
            print('\nINVALID CHOICE! PLEASE TRY AGAIN !!\n')
            
def cancel_seats():
        while True:
            if len(LOGGED_IN_USER.bookings.values()) == 0:
                print('\n YOU HAVE NO BOOKED SHOWS\n')
                break
            
            print('\n=========FOLLOWING ARE YOUR BOOKED SHOWS ============\n')
            BOOKED_SHOWS = LOGGED_IN_USER.bookedShows()
            print(BOOKED_SHOWS.iloc[:, 1:])
            choice = int(input('\nSelect a Booking to proceed : '))
            
            if isValidChoice(choice, BOOKED_SHOWS['bookingID'].shape[0]):
                SELECTED_BOOKING = BOOKED_SHOWS.iloc[choice - 1]['bookingID']
                
                print('\n=========FOLLOWING ARE YOUR BOOKED SEATS ============\n')
                BOOKED_SEATS = BOOKED_SHOWS.iloc[choice - 1]['seat Numbers']
                
                print(BOOKED_SEATS)
                
                seat_choice = input('\n Enter Seat Number to be cancelled : ')
                LOGGED_IN_USER.cancelSeat(SELECTED_BOOKING, seat_choice)
                break
            else :
                print('\nINVALID CHOICE! PLEASE TRY AGAIN !!\n')
    
while True:
    print('\n==============================================\n')
    print("WELCOME TO MOVIE TICKET BOOKING SYSTEM")
    print('\n==============================================\n')
    LOGGED_IN_USER = login()
    
    quit = False
    while True:
        print('\n WHAT WHOULD YOU LIKE TO DO ?\n')
        print(' 1. View Available shows')
        print(' 2. Book a Ticket.')
        print(' 3. Cancel a Booking.')
        print(' 4. Cancel seats from a booking')
        print(' 5. View Booked Tickets')
        print(' 6. Log Out')
        print(' 7. Quit')
        
        
        try:
            choice = int(input('\nPlease select an option : '))
            if isValidChoice(choice, 7):
                if choice == 1:
                    list_available_shows()
                elif choice == 2:
                    book_ticket()
                elif choice == 3:
                    cancel_booking()
                elif choice == 4:
                    cancel_seats()
                elif choice == 5:
                    BOOKED_SHOWS = LOGGED_IN_USER.bookedShows()
                    if BOOKED_SHOWS.shape[0] == 0:
                        print('\n NO BOOKINGS PRESENT\n')
                    else :
                        print('\n=========FOLLOWING ARE YOUR BOOKED SHOWS ============\n')
                        print(BOOKED_SHOWS.iloc[:, 1:])
                elif choice == 6:
                    break
                elif choice == 7:
                    quit = True
                    break
            else :
                print('\nINVALID CHOICE! PLEASE TRY AGAIN !!\n')
        except Exception:
            print('\nINVALID CHOICE! PLEASE TRY AGAIN !!\n')
        
    print('\n========== GOODBYE ===============\n')
    if quit:
        break