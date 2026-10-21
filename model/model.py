import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapA = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def creaGrafo(self, anno1, anno2):
        self._grafo.clear()
        self._idMapA.clear()

        costruttori = DAO.getAllNodes(anno1,anno2)
        for a in  costruttori:
            self._idMapA[a.constructorId] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        for a in costruttori:
           # a.clientiPerArtista = set(DAO.getClientiPerArtista(a.ArtistId))
            a.list_piloti = DAO.getPilotiPerCostr(a.constructorId, anno1, anno2)
           # a.popolarita = DAO.getPopolarita(a.ArtistId)
        print("3 - Informazioni recuperate")

        for costruttore in costruttori:
            costruttore.oldest_driver_dob = DAO.getOldestDriverDob(
                costruttore.constructorId, anno1, anno2
            )

        for i in range(len(costruttori)):
            a1 = costruttori[i]
            for j in range(i + 1, len(costruttori)):
                a2 = costruttori[j]
                pilotiComuni = (set(a1. list_piloti) & set(a2.list_piloti ))
                #ND: & FUNZIONA SOLO CON I SET! SE HAI LE LISTE CONSERVTILE IN SET E POI CONFRONTALE

                if len(  pilotiComuni) > 0:
                    peso = len(pilotiComuni)
                   # if p1 > p2:
                    self._grafo.add_edge(a1, a2, weight=peso)

                   # elif p2 > p1:
                       # self._grafo.add_edge(a2, a1, weight=peso)
                    #else:
                       # self._grafo.add_edge(a1, a2, weight=peso)
                      #  self._grafo.add_edge(a2, a1, weight=peso)
        print("4 - Archi aggiunti")

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getAllNodes(self, anno1, anno2):
        return DAO.getAllNodes(anno1,anno2)

    def getTop3Archi(self):
        # return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:10]
        archi = self._grafo.edges(data=True)
        return sorted(
            archi,
            key=lambda x: x[2]["weight"],
            reverse=True
        )[:3]

    def getConnessaInfo(self):
        # lo trasformo in non orientato pk richiesto di ignorare
        grafo_non_orientato = self._grafo.to_undirected()
        components = list(nx.connected_components(grafo_non_orientato))

        # Se il grafo è vuoto
        if len(components) == 0:
            return 0, set(), []

        # components = list(nx.connected_components(self._grafo))  # TROVO LE COMP CONNESSE e ci faccio una lista
        largest = max(components, key=len)  # trova la + grande

        # b. Film con maggior numero di archi uscenti
        #film_max_out = max(self._grafo.nodes, key=lambda n: self._grafo.out_degree(n))
        # relativo numero archi usenti
        #max_out = self._grafo.out_degree(film_max_out)

        # ORDINO PER  GRADO!!
        ordered_nodes = sorted(largest, key=lambda n: grafo_non_orientato.degree(n), reverse=True)  # ordine decrescente
        details = [(n, len(n.list_piloti)) for n in ordered_nodes]

        return len(components), largest, details

    def getGruppoPiloti(self,  k):
        self._best_path = []
        self._best_score = float("inf")

        self._creaMappaComponenti()

        costruttori = list(self._grafo.nodes)
        self._ricorsione([], costruttori, k, 0)
        # Il percorso parziale parte con il nodo selezionato
       # parziale = [start_node]
       # self._ricorsione(parziale, k)

        return self._best_path, self._best_score

    def _ricorsione(self, parziale,costruttori, k,pos):

        if len(parziale) == k:
            score = self._score(parziale)
           # score = sum(len(a.movies) for a in parziale)

            if score <self._best_score:
                self._best_score = score
                self._best_group = list(parziale)
            return

        # Se non restano abbastanza costruttori, termino
        if len(costruttori) - pos < k - len(parziale):
            return

        # Provo i costruttori a partire dalla posizione pos
        for i in range(pos, len(costruttori)):
            candidato = costruttori[i]


            # Controllo che non ci sia già un costruttore
            # della stessa componente nella soluzione parziale
            stessa_componente = False

            for costruttore in parziale:
                if (self._mappaComponenti[candidato]
                        == self._mappaComponenti[costruttore]):
                    stessa_componente = True
                    break

            if stessa_componente:
                continue

            parziale.append(candidato)
            # Chiamata ricorsiva passando il nuovo arco come riferimento
            self._ricorsione(parziale, costruttori, k, i + 1)
            # BACKTRACKING: annullo l'ultima mossa
            parziale.pop()

    def _score(self, parziale):
        date_nascita = []

        for costruttore in parziale:
            dob = costruttore.oldest_driver_dob
            if dob is None:
                return float("inf")
            date_nascita.append(dob)

        data_piu_vecchia = min(date_nascita)
        data_piu_recente = max(date_nascita)
        scarto = (data_piu_recente - data_piu_vecchia).days

        return scarto

    def _creaMappaComponenti(self):
        self._mappaComponenti = {}

        grafoNonOrientato = self._grafo.to_undirected()
        componenti = list(nx.connected_components(grafoNonOrientato))

        for i, componente in enumerate(componenti):
            for costruttore in componente:
                self._mappaComponenti[costruttore] = i






