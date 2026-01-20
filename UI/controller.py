import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        self._view.txt_result.clean()

        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False
        self._view.txtMinDuration.disabled = False
        self._view.txtMaxArtists.disabled = False
        self._view.btnSearchArtists.disabled = False

        numero_minimo_album = self._view.txtNumAlbumMin.value
        if int (numero_minimo_album) == 0:
            self._view.show_alert("Errore: Inserire un numero >= 0")
        else :
            self._model.load_artists_with_min_albums (numero_minimo_album)
            self._model.load_connessioni (numero_minimo_album)

            self._model.build_graph()
            numero_nodi = self._model.get_num_nodes()
            numero_archi = self._model.get_num_edges()

            self._view.txt_result.controls.append (ft.Text(f"Grafo creato: {numero_nodi} nodi (artisti), {numero_archi} archi."))
            for artist in self._model.load_artists_with_min_albums(numero_minimo_album):
                self._view.ddArtist.options.append (ft.dropdown.Option (key=str(artist['artist_id']),
                                                                                text = self._model._map_artisti[artist['artist_id']].name))

            self._view._page.update()


    def handle_connected_artists(self, e):
        self._view.txt_result.clean()

        nodo_scelto = self._view.ddArtist.value
        componenti_connesse = self._model.get_connected(nodo_scelto)
        self._view.txt_result.controls.append (ft.Text(f"Artisti direttamente collegati all'artista {nodo_scelto}"))
        for componente, generi_in_comune in componenti_connesse :
            self._view.txt_result.controls.append (ft.Text (f"{componente} - Numero di generi in comune: {generi_in_comune}"))

        self._view._page.update()


    def handle_best_path (self, e) :
        self._view.txt_result.clean()

        durata_minima = float (self._view.txtMinDuration.value)
        len_max = self._view.txtMaxArtists.value
        nodo_scelto = self._view.ddArtist.value

        best_path, best_weight = self._model.find_best_path(self._model._map_artisti [int(nodo_scelto)], len_max, durata_minima)
        self._view.txt_result.controls.append (ft.Text(f"Cammino di peso massimo dall'artista {nodo_scelto}"))
        for nodo in best_path :
            self._view.txt_result.controls.append (ft.Text (f"{nodo}"))

        self._view.txt_result.controls.append (ft.Text (f"Peso massimo: {best_weight}"))

        self._view._page.update()
