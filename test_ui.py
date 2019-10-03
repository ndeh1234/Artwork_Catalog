from unittest import TestCase
from unittest.mock import patch

import Artwork_Store
from Artwork_Store import Artwork

import ui
from menu import Menu

class TestUI(TestCase):

    @classmethod
    def setUpClass(cls):
        Artwork_Store.db = 'database/test_artworks.db'
        Artwork_Store.instance =None

    @patch('builtins.input', side_effect=['a'])
    @patch('builtins.print')
    def test_display_menu_get_choice(self, mock_print, mock_input):
        menu = Menu()
        menu.add_option('a', 'aaa', lambda: None)
        menu.add_option('b', 'bbb', lambda: None)

        self.assertEqual('a', ui.display_menu_get_choice(menu))

        mock_print.assert_any_call(menu)

    @patch('builtins.print')
    def test_message(self, mock_print):
        ui.message('hello')
        mock_print.assert_called_with('hello')

    @patch('builtins.print')
    def test_show_artworks_empty(self, mock_print):
        artworks = []
        ui.show_artworks(artworks)
        mock_print.assert_called_with('No artworks to display')

    @patch('builtins.print')
    def test_show_artworks_list(self, mock_print):
        ak1 = Artwork('1', '111', )
        ak2 = Artwork('2', '222', )
        artworks = [ak1, ak2]
        ui.show_artworks(artworks)

        mock_print.assert_any_call(ak1)
        mock_print.assert_any_call(ak2)

    @patch('builtins.input', side_effect=['artist', 'name'])
    def test_get_artwork_info(self, mock_input):
        artwork = ui.get_artwork_info()
        self.assertEqual('artist', artwork.artist)
        self.assertEqual('name', artwork.name)

    @patch('builtins.input', side_effect=['42'])
    def test_get_artwork_id(self, mock_input):
        self.assertEqual(42, ui.get_artwork_id())

    @patch('builtins.input', side_effect=['no', '-4', '0', 'sdfdf', 'makossa makossa makossa', '99 99 99', '9'])
    def test_get_artwork_id_rejects_non_positive_integer(self, mock_input):
        self.assertEqual(9, ui.get_book_id())

    @patch('builtins.input', side_effect=['available'])
    def test_get_available_value_available(self, mock_input):
        self.assertTrue(ui.get_available_value())

    @patch('builtins.input', side_effect=['sold'])
    def test_get__value_sold(self, mock_input):
        self.assertFalse(ui.get_available_value())

    @patch('builtins.input', side_effect=['not one of the options', 'makossa', '1234', 'Not', 'rea', 'available'])
    def test_get_available_value_validates(self, mock_input):
        self.assertTrue(ui.get_available_value())

    @patch('builtins.input', side_effect=['makossa'])
    @patch('builtins.print')
    def ask_question(self, mock_print, mock_input):
        self.assertEqual('makossa', ui.ask_question('What is your favorite artwork?'))
        mock_print.assert_called_with('What is your favorite artwork?')