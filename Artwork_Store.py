import sqlite3

db = 'Artwork_Catalog.db'

class Artwork:





#class Artwork:

    """ Represent one artwork in the program.
    Before artworks are saved, create without ID then call save() method to DB and create an ID.
    Future calls to save() will update the database item for the artwork catalog with this id
    """

    def __init__(self, artist, name, price, available = True, sold = False, id=None):
        self.artist = artist
        self.name = name
        self.price = price
        self.available = available,
        self.sold = sold
        self.id = id

        self.artworkStore = ArtworkStore()

    def save(self):
         if self.id:
             self.artworkStore._update_Artwork(self)
         else:
             self.artworkStore._add_Artwork(self)

    def __str__(self):
         available_status = 'available' if self.available else 'sold'
         return f'ID {self.id},Artist: {self.artist},Name: {self.name}, Price: {self.price}. Is {available_status}'

    def __repr__(self):
          return f'ID {self.id} Artist: {self.artist} Name: {self.name} Price:{self.price} Availability: {self.availability}'

    def __eq__(self, other):
          """ Overrides the Python == operator so one artwork can be tested for equality to another artwork based on attribute values """
          if isinstance(self,other._class_):
             return self.id == other.id and self.artist == other.artist and self.artwork == other.artwork and self.price == other.price and self.availability == other.availabilty
          return False
    def __ne__(self, other):
         """ Overrides the != operator """
         if not isinstance(self, other.__class__):
            return True
         return self.id != other.id or self.artist != other.artist or self.artwork != other.artwork or self.price != other.price or self.availability != other.availability

    def __hash__(self):
         """ And Python makes us implement __hash__ if __eq__ is overridden """
         return hash((self.id, self.artist, self.artwork, self.price, self.availability))


    class ArtworkStore:
         """ Singleton class to hold and manage a list of artworks. All Artwork objects created are the same object.
             Provides operations to add, update, delete, and query the store. """
         instance = None

         class __ArtworkStore:

             def __init__(self):
                 create_table_sql = 'CREATE TABLE IF NOT EXISTS artworks(artist TEXT, name TEXT, price FLOAT, availability BOOLEAN, UNIQUE(artist COLLATE NOCASE, name COLLATE NOCASE))'


                 con = sqlite3.connect(db)

                 with con:
                     con.execute(create_table_sql)

                 con.close()

             create_table_sql = 'CREATE TABLE IF NOT EXISTS artists(name TEXT, email TEXT, UNIQUE(email COLLATE NOCASE))'

             con = sqlite3.connect(db)

             with con:
                 con.execute(create_table_sql)
                 #con.close()

    def add_artist(self, artist):
        """ Adds artists to store.
            Raises ArtistError if an artist with exact name and artwork (not case sensitive) is already in the store.
            :param artist the Artist to add """

        insert_sql = 'INSERT INTO artists (name, email) VALUES (?, ?)'

        try:
            with sqlite3.connect(db) as con:
             res = con.execute(insert_sql, (artist.name, artist.email))

             new_id = res.lastrowid # Get the ID of the new row in the table
             artist.id = new_id # Set this artist's ID
        except sqlite3.IntegrityError as e:
            raise ArtistError(f'Error - this artist is already in the database. {artist}') from e
        finally:
             con.close()

    def  add_artwork(self, artwork):
        """ Adds artworks to store.
        :param artwork the artwork to add
        """

        insert_sql = 'INSERT INTO artworks (artist, name, price, availability) VALUES (?, ?, ?, ?)'

        try:
            with sqlite3.connect(db) as con:
                res = con.execute(insert_sql, (artwork.artist, artwork.name,artwork.price,artwork.availability))


                new_id = res.lastrowid # Get the ID of the new row in the table
                artwork.id = new_id # Set this artist's ID
        except sqlite3.IntegrityError as e:
            raise ArtworkError(f'Error - this artwork is already in the database. {artwork}') from e
        finally:
            con.close()

    def delete_artwork(self, artwork):

        """ Removes artwork from store. Raises ArtworkError if book not in store.
        :param artwork the artwork to delete """

        delete_sql = 'DELETE FROM artworks WHERE rowid = ?'

        with sqlite3.connect(db) as con:
             deleted = con.execute(delete_sql, (artwork.id,))
             deleted_count = deleted.rowcount  # rowcount = how many rows affected by the query
        con.close()

        if deleted_count == 0:
            raise ArtworkError(f'Artwork {artwork} not found in store.')

    def _update_artwork(self, artwork):
        """ Updates the information for an artwork. Assumes id has not changed and updates artist, name and available values
        Raises ArtworkError if artwork does not have id
        :param artwork the Artwork to update
        """

        if not artwork.id:
            raise ArtworkError('Artwork does not have ID, can\'t update')

        update_available_sql = 'UPDATE artworks SET artist = ?, name= ?, price = ?, available = ? WHERE rowid = ?'

        with sqlite3.connect(db) as con:
            updated = con.execute(update_available_sql, (artwork.artist, artwork.name, artwork.price, artwork.available, artwork.id))

            rows_modified = updated.rowcount

        con.close()

        # Raise ArtworkError if artwork not found
        if rows_modified == 0:
         raise ArtworkError(f'Artwork with id {artwork.id} not found')

    def _update_artist(self, artistError):
        """ Updates the information for an artist. Assumes id has not changed and updates name, email and available values
        Raises ArtistError if artist does not have id
        :param artist the Artist to update
            """

        if not artist.id:
           raise artistError('Artist does not have ID, can\'t update')

        update_available_sql = 'UPDATE artists SET name = ?, email = ? WHERE rowid = ?'

        with sqlite3.connect(db) as con:
            updated = con.execute(update_available_sql, (artist.name, artist.email,  artist.id))
            rows_modfied = updated.rowcount

        con.close()


            #  Raise ArtistError if name not found.
        if rows_modfied == 0:
                raise artistError(f'Artist with id {artist.id} not found')

    def get_artist_by_id(self, id):
                """ Searches list for Artist with given ID,
                :param id the ID to search for
                :returns the artist, if found, or None if artist not found.
                """

                get_artist_by_id_sql = 'SELECT rowid, * FROM artists WHERE rowid = ?'

                con = sqlite3.connect(db)
                con.row_factory = sqlite3.Row  # This row_factory allows access to data by row name
                rows = con.execute(get_artist_by_id_sql, (id,))
                artist_data = rows.fetchone()  # Get first result

                if artist_data:
                    artist = Artist(artist_data['name'], artist_data['email'], artist_data['available'], artist_data['rowid'])

                con.close()

                return artist

    def artist_search(self, term):
                """ Searches the store for artists whose name or email contain a search term. Case insensitive.
                Makes partial matches, so a search for 'row' will match an artist with name='Longue Longue' and an artist with email='longue@yahoo.com'
                :param term the search term
                :returns a list of artists with name or email that match the search term. The list will be empty if there are no matches.
                """

                search_sql = 'SELECT rowid, * FROM artists WHERE UPPER(name) like UPPER(?) OR UPPER(email) like UPPER(?)'

                search = f'%{term}%'  # Example - if searching for text with 'bOb' in then use '%bOb%' in SQL

                con = sqlite3.connect(db)
                con.row_factory = sqlite3.Row
                rows = con.execute(search_sql, (search, search))
                artists = []
                for r in rows:
                    artist = artist(r['name'], r['email'], r['availability'], r['rowid'])
                    artists.append(artist)

                con.close()

                return artist

    def artwork_search(self, term):
        """ Searches the store for artworks whose artist or name contain a search term. Case insensitive.
        Makes partial matches, so a search for 'row' will match an artwork with artist='Longue Longue' and an artwork with name='Dialogue National'
        :param term the search term
        :returns a list of artworks with artist or name that match the search term. The list will be empty if there are no matches.
        """

        search_sql = 'SELECT rowid, * FROM artworks WHERE UPPER(artist) like UPPER(?) OR UPPER(name) like UPPER(?)'

        search = f'%{term}%'  # Example - if searching for text with 'bOb' in then use '%bOb%' in SQL

        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        rows = con.execute(search_sql, (search, search))
        artworks = []
        for r in rows:
            artwork = artwork(r['artist'], r['name'],r['price'], r['available'], r['rowid'])
            artworks.append(artwork)

        con.close()

        return artworks

    def artist_count(self):
        """ :returns the number of artists in the store """

        count_artists_sql = 'SELECT COUNT(*) FROM artists'

        con = sqlite3.connect(db)
        count = con.execute(count_artists_sql)
        total = count.fetchone()[
            0]  # fetchone() returns the first row of the results. This is a tuple with one element - the count
        con.close()

        return total

    def artwork_count(self):
        """ :returns the number of artworks in the store """

        count_artworks_sql = 'SELECT COUNT(*) FROM artworks'

        con = sqlite3.connect(db)
        count = con.execute(count_artworks_sql)
        total = count.fetchone()[
            0]  # fetchone() returns the first row of the results. This is a tuple with one element - the count
        con.close()

        return total


    def __new__(cls, artist, name, price, available = True, sold = False, id=None):
        """  Method that  handles object creation. (Compare to __init__ which initializes an object.)
        If there's already a ArtworkStore instance, return that. If not, then create a new one
        This way, there can only ever be one __ArtworkStore, which uses the same database. """

        if not ArtworkStore.instance:
            ArtworkStore.instance = ArtworkStore.__ArtworkkStore()
        return ArtworkStore.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

class ArtworkError(Exception):
        """ For ArtworkStore errors. """
        pass
































