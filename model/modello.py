import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self._bestScore = 0
        self._bestPath = []
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getYears(self):
        return DAO.getYears()

    def getShapes(self, year):
        return DAO.getShapes(year)

    def buildGraph(self, year, shape):
        nodes = DAO.getSitingsYear(year, shape)
        for n in nodes:
            self._idMap[n.id] = n

        self._graph.add_nodes_from(nodes)

        edges = DAO.getEdges(year, shape, year, shape, self._idMap)
        for e in edges:
            self._graph.add_edge(e[0], e[1], weight = e[2])

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getOutEdges(self):
        outEdges = []
        for n in self._graph.nodes:
            edges = self._graph.out_edges(n)

            for e in edges:
                tot = self.calcolaTot(e[0], e[1])
                outEdges.append((e[0], e[1], tot))

        outEdges_sorted = sorted(outEdges, key=lambda x: x[2], reverse=True)

        return outEdges_sorted[:5]

    def calcolaTot(self, nodo1, nodo2 ):
        tot = 0
        tot += self._graph[nodo1][nodo2]["weight"]
        print(list(self._graph.successors(nodo1)), len(list(self._graph.successors(nodo1))))
        return tot

    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

        for nodo in self._graph.nodes:
            self._occorrenze_mese[nodo.datetime.month] += 1
            successivi_durata_crescente = self._calcola_successivi(nodo)
            self._calcola_cammino_ricorsivo([nodo], successivi_durata_crescente)
            self._occorrenze_mese[nodo.datetime.month] -= 1
        return self._cammino_ottimo, self._score_ottimo

    def _calcola_cammino_ricorsivo(self, parziale: list[Sighting], successivi: list[Sighting]):
        if len(successivi) == 0:
            score = Model._calcola_score(parziale)
            if score > self._score_ottimo:
                self._score_ottimo = score
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                # aggiungo il nodo in parziale ed aggiorno le occorrenze del mese corrispondente
                parziale.append(nodo)
                self._occorrenze_mese[nodo.datetime.month] += 1
                # nuovi successivi
                nuovi_successivi = self._calcola_successivi(nodo)
                # ricorsione
                self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                # backtracking: visto che sto usando un dizionario nella classe per le occorrenze, quando faccio il
                # backtracking vado anche a togliere una visita dalle occorrenze del mese corrispondente al nodo che
                # vado a sottrarre
                self._occorrenze_mese[parziale[-1].datetime.month] -= 1
                parziale.pop()

    def _calcola_successivi(self, nodo: Sighting) -> list[Sighting]:
        """
        Calcola il sottoinsieme dei successivi ad un nodo che hanno durata superiore a quella del nodo, senza eccedere
        il numero ammissibile di occorrenze per un dato mese
        """
        successivi = self._graph.successors(nodo)
        successivi_ammissibili = []
        for s in successivi:
            if s.duration > nodo.duration and self._occorrenze_mese[s.datetime.month] < 3:
                successivi_ammissibili.append(s)
        return successivi_ammissibili

    @staticmethod
    def _calcola_score(cammino: list[Sighting]) -> int:
        """
        Funzione che calcola il punteggio di un cammino.
        :param cammino: il cammino che si vuole valutare.
        :return: il punteggio
        """
        # parte del punteggio legata al numero di tappe
        score = 100 * len(cammino)
        # parte del punteggio legata al mese
        for i in range(1, len(cammino)):
            if cammino[i].datetime.month == cammino[i - 1].datetime.month:
                score += 200
        return score




