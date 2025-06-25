from model.modello import Model

myModel = Model()
print(myModel.buildGraph(1996, "circle"))
print(myModel.getOutEdges())
print(myModel.cammino_ottimo())