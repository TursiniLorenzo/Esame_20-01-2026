from database.DB_connect import DBConnect
from model.artist import Artist
from model.connessione import Connessione

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result



    @staticmethod
    def get_artists_filtrati (n_album) :

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select a.artist_id 
                from album a 
                group by a.artist_id 
                having count(a.artist_id) >= %s
                """
        cursor.execute(query, (n_album,))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessione (n_album) :

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select a1.artist_id as artist_id_A, a2.artist_id as artist_id_B, count(distinct(t1.genre_id)) as num_generi
                from album a1, album a2, track t1, track t2
                where a1.id = t1.album_id 
                and a2.id = t2.album_id 
                and a1.artist_id > a2.artist_id
                and t1.genre_id = t2.genre_id 
                and a1.artist_id in (select a3.artist_id
                from album a3
                group by a3.artist_id 
                having count(a3.artist_id)>=%s)
                and a2.artist_id in (select a4.artist_id
                from album a4
                group by a4.artist_id 
                having count(a4.artist_id)>=%s)
                group by a1.artist_id, a2.artist_id 
                """
        cursor.execute(query, (n_album, n_album, ))

        for row in cursor:
            result.append(Connessione (**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_artists_per_durata (durata_min, n_album) :

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select a.artist_id 
                from album a , track t
                where t.milliseconds * 60000 >= %s
                group by a.artist_id 
                having count(a.artist_id) >= %s
                """
        cursor.execute(query, (durata_min, n_album))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result
