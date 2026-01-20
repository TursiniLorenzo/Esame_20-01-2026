import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self._map_artisti = {}
        self._map_connessioni = {}
        self.load_all_artists()

        self._nodes = []
        self._edges = []
        self._artisti_filtrati = []

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        for artist in self._artists_list:
            self._map_artisti [artist.id] = artist
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        id_artisti_filtrati = DAO.get_artists_filtrati(min_albums)
        self._nodes = []
        for id_artista in id_artisti_filtrati:
            self._nodes.append (id_artista)
        return self._nodes

    def load_artists_durata_min (self, min_albums, durata_min):
        id_artisti_filtrati = DAO.get_artists_per_durata(min_albums, durata_min)
        for id_artisti_filtrato in id_artisti_filtrati :
            self._artisti_filtrati.append (self._map_artisti[id_artisti_filtrato])

        return self._artisti_filtrati


    def load_connessioni (self, min_albums) :
        connessioni = DAO.get_connessione(min_albums)
        self._edges = []
        for connessione in connessioni :
            self._edges.append ((connessione.artist_id_A, connessione.artist_id_B, connessione.num_generi))
            self._map_connessioni [(connessione.artist_id_A, connessione.artist_id_B)] = connessione.num_generi
            self._map_connessioni [(connessione.artist_id_B, connessione.artist_id_A)] = connessione.num_generi
        return self._edges

    def build_graph(self):
        self._graph.clear()
        for node in self._nodes :
            self._graph.add_node (self._map_artisti [node['artist_id']])

        for u, v, peso in self._edges :
            self._graph.add_edge (self._map_artisti [u], self._map_artisti [v], peso=peso)

        return self._graph

    def get_num_nodes (self) :
        return self._graph.number_of_nodes()

    def get_num_edges (self) :
        return self._graph.number_of_edges()

    def get_connected (self, node) :
        connected = []
        for nodo in self._graph.neighbors(self._map_artisti[int (node)]) :
            connected.append ((nodo, self._map_connessioni [(int(node), nodo.id)] ))
            connected.sort(key = lambda x : x[0].id)

        return connected

    def find_best_path (self, start_node, len_max, durata_min) :
        self.best_path = []
        self.best_weight = -1

        self._ricorsione (start_node, len_max, [start_node], 0, durata_min)
        return self.best_path, self.best_weight

    def _ricorsione (self, corrente, len_max, parziale, peso_parziale, durata_min) :
        if len (parziale) == int(len_max) + 1 :
            if peso_parziale > self.best_weight :
                self.best_weight = peso_parziale
                self.best_path = list (parziale)
            return

        for neighbor in self._graph.neighbors (corrente) :
            if neighbor not in parziale :
                peso_arco = self._graph [corrente][neighbor]["peso"]
                parziale.append (neighbor)
                self._ricorsione (neighbor, len_max, parziale, peso_parziale + peso_arco, durata_min)
                parziale.pop()

