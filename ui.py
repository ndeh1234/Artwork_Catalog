from Artwork_Store import Artwork


def display_menu_get_choice(menu):
    """ Displays all of the menu options, checks that the user enters a valid choice and returns the choice.
        :param menu: the menu to display
        :returns: the user's choice """
    while True:
        print(menu)
        choice = input('Enter choice? ')
        if menu.is_valid(choice):
            return choice
        else:
            print('Not a valid choice, try again.')
def message(msg):
    """ Prints a message for the user
     :param msg: the message to print"""
    print(msg)

def get_artwork_info():
    """ Create a new artwork from artist and name provided by user
     :returns: an artwork created by the artist and name. """
    artist= input('Enter  artist: ')
    name = input('Enter name of artwork: ')
    return Artwork(artist, name, )


def get_artist_id():
    """ Ask for ID, validate to ensure is positive integer
    :returns: the ID value """
    while True:
        try:
            id = int(input('Enter artist ID: '))
            if id > 0:
                return id
            else:
                print('Please enter a positive number.')

        except ValueError:
            print('Please enter a number.')


def get_artwork_id():
    """ Ask for ID, validate to ensure is positive integer
    :returns: the ID value """
    while True:
        try:
            id = int(input('Enter artwork ID: '))
            if id > 0:
                return id
            else:
                print('Please enter a positive number.')

        except ValueError:
            print('Please enter a number.')



def get_available_value():
    """ Ask user to enter 'available' or 'sold'
     :returns: True if user enters 'available' or False if user enters 'sold' """
    while True:
        response = input('Enter \'available\' if artwork is available or \'sold\' if  artwork is sold: ')
        if response.lower() in ['available', 'sold']:
            return response.lower() == 'available'
        else:
            print('Type \'available\' or \'sold\'')