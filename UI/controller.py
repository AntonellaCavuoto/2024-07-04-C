import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._selectedShape = None
        self._selectedYear = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        year = self._selectedYear
        shape = self._selectedShape

        if year is None or shape is None:
            self._view.create_alert("Per favore inserire anno e forma")

        numNodi, numArchi = self._model.buildGraph(year, shape)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {numNodi}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {numArchi}"))
        self._view.txt_result1.controls.append(ft.Text(f"I 5 archi di peso maggiore sono: "))
        for e in self._model.getOutEdges():
            self._view.txt_result1.controls.append(ft.Text(f"{e[0]} -> {e[1]} | weight = {e[2]}"))

        self._view.update_page()
    def handle_path(self, e):
        pass

    def fillDDYear(self):
        years = self._model.getYears()
        yearsDD = []
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(data=year, text=year, on_click=self.readDDYear))
        self._view.update_page()

    def fillDDShape(self):
        year = self._selectedYear
        shapes = self._model.getShapes(year)
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(data=shape, text=shape, on_click=self.readDDShape))
        self._view.update_page()

    def readDDYear(self, e):
        if e.control.data is None:
            self._selectedYear = None
        else:
            self._selectedYear = e.control.data
            self.fillDDShape()

        print(f"readDDTeams -- {self._selectedYear}")

    def readDDShape(self, e):
        if e.control.data is None:
            self._selectedShape = None
        else:
            self._selectedShape = e.control.data

        print(f"readDDTeams -- {self._selectedShape}")
