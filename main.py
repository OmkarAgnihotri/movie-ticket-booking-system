from classes import Theatre, Booking, Show, User, Seat
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
THEATRE = Theatre(30, SHOWS)

for firstName, lastName in [name.split() for name in NAMES]:
    USERS.append(User(firstName, lastName, THEATRE))
    
def isValidChoice(choice, available_choices):
    if choice > 0 and choice <= available_choices:
        return True
    False

LOGGED_IN_USER = None
def login():
    print('\n##########################################\n')
    
    flag = False
    while not flag:
        for index, user in enumerate(USERS):
            print('{}. {} {}'.format(index + 1, user.firstName, user.lastName))
    
        choice = int(input('\nSelect User Profile : '))
        
        if isValidChoice(choice, 3):
            LOGGED_IN_USER = USERS[choice - 1]
            
            print('\n======== WELCOME {} ==============\n'.format(LOGGED_IN_USER.firstName))
            break
        else :
            print('\nINVALID CHOICE! PLEASE TRY AGAIN !!\n')
            
    return LOGGED_IN_USER
            
def logout():
    LOGGED_IN_USER = None
    return LOGGED_IN_USER
    
def book_ticket():
    
    while True:
        print('\n=========FOLLOWING ARE AVAILABLE SHOWS ============\n')
        AVAILABLE_SHOWS = THEATRE.available_shows()
        print(AVAILABLE_SHOWS.iloc[:, 1:])
        choice = int(input('\nSelect a show : '))
        
        if isValidChoice(choice, AVAILABLE_SHOWS['showID'].shape[0]):
            SELECTED_SHOW = AVAILABLE_SHOWS.iloc[choice - 1]['showID']
            SEATS = THEATRE.seatSelector(SELECTED_SHOW)
            print(SEATS.applymap(lambda seat : int(seat.is_booked)))
            
            choice = int(input('\n ENTER NUMBER OF SEATS : '))
            
            SELECTED_SEATS = []
            for i in range(choice):
                chosenSeat = input('SELECT {} SEAT : '.format(i + 1))
                SELECTED_SEATS.append(chosenSeat)
            
            LOGGED_IN_USER.bookTicket(SELECTED_SHOW, SELECTED_SEATS)
            break
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
    LOGGED_IN_USER = login()
    
    quit = False
    while True:
        print('\n WHAT WHOULD YOU LIKE TO DO ?\n')
        print(' 1. Book a Ticket.')
        print(' 2. Cancel a Booking.')
        print(' 3. Cancel seats from a booking')
        print(' 4. View Booked Tickets')
        print(' 5. Log Out')
        print(' 6. Quit')
        
        choice = int(input('\nPlease select an option : '))
        
        if isValidChoice(choice, 6):
            if choice == 1:
                book_ticket()
            elif choice == 2:
                cancel_booking()
            elif choice == 3:
                cancel_seats()
            elif choice == 4:
                BOOKED_SHOWS = LOGGED_IN_USER.bookedShows()
                if BOOKED_SHOWS.shape[0] == 0:
                    print('\n NO BOOKINGS PRESENT\n')
                else :
                    print(BOOKED_SHOWS.iloc[:, 1:])
            elif choice == 6:
                quit = True
                break
            elif choice == 5:
                break
        else :
            print('\nINVALID CHOICE! PLEASE TRY AGAIN !!\n')
    
    
    print('\n========== GOODBYE ===============\n')
    if quit:
        break