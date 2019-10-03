""" Program to create and manage a list of artworks and artists available in a store. """


from Artwork_Store import Artwork, ArtworkStore
from menu import Menu
import ui

store = ArtworkStore()

def main():

    menu = create_menu()

    while True:
        choice = ui.display_menu_get_choice(menu)
        action = menu.get_action(choice)
        action()
        if choice == 'Q':
            break

def create_menu():



    menu = Menu()
    menu.add_option('1', 'Add Artist', add_artist)
    menu.add_option('2', 'Add Artwork', add_artwork)
    menu.add_option('3', 'Search For An Artist', search_for_an_artist)
    menu.add_option('4', 'Search For All Artworks', search_for_all_artworks)
    menu.add_option('5', 'Delete An Artwork', delete_an_artwork)
    menu.add_option('6', 'Change Status For An Artwork', change_status_for_an_artwork)
    menu.add_option('Q', 'Quit', quit_program)

    return menu


def add_artist():
    new_artist = ui.get_artist_info()
    all_artists = store.get_all_artists()
    if new_artist in all_artists:
        ui.message('The artist already exists')
    else:
        store.add_artist(new_artist)
    new_artist = ui.get_artist_info()
    new_artist.save()

def add_artwork():
    new_artwork = ui.get_artwork_info()
    all_artworks = store.get_all_artworks()
    if new_artwork in all_artworks:
        ui.message('The artwork already exists')
    else:
        store.add_artwork(new_artwork)
    new_artwork = ui.get_artwork_info()
    new_artwork.save()

def search_for_an_artist():
    search_term = ui.ask_question('Enter search term, will match partial names or emails.')
    matches = store.artist_search(search_term)
    ui.show_artists(matches)


def search_for_all_artworks():
    artworks = store.get_all_artworks()
    ui.show_artworks(artworks)

def delete_an_artwork():
    artwork_id = ui.get_artwork_id()
    artwork = store.get_artwork_by_id(artwork_id)
    store.delete_artwork(artwork)
    ui.message('Artwork Deleted')

def change_status_for_an_artwork():
    try:
        artwork_id = ui.get_artwork_id()
        artwork = store.get_artworkk_by_id(artwork_id)
        new_available = ui.get_available_value()
        artwork.read = new_available
        artwork.save()
    except:
        ui.message('Artwork not available')


def show_available_artworks():
    available_artworks = store.get_artworks_by_available_value(True)
    ui.show_arworks(available_artworks)


def show_sold_artworks():
    sold_artworks = store.get_artworks_by_available_value(False)
    ui.show_artworks(sold_artworks)


def show_all_artworks():
    artworks = store.get_all_artworks()
    ui.show_artworks(artworks)




def change_status():
    try:
        artwork_id = ui.get_artwork_id()
        artwork = store.get_artwork_by_id(artwork_id)
        new_status = ui.get_status_value()
        artwork.status = new_status
        artwork.save()
    except:
        ui.message('Artwork not available')


def quit_program():
    quit_program = input("enter q or Q to quit")


if quit_program == 'q' or 'Q':
    ui.message('Thanks and bye!')

if __name__ == '__main__':
    main()
