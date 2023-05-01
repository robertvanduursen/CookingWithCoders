from database import manager

m = manager.Manager()
print(m.recipes)

from viewer import graph

import sys

pos_ending = '*PyQt5.QtCore.QPointF(0.0,0.0)'

dummy_data = ['']
for recipe in m.recipes:
    dummy_data += [recipe.name+pos_ending]
    dummy_data += [i.name+pos_ending for i in recipe.ingredients]

dummy_data += ['']

for i in m.recipes[1].ingredients:
    dummy_data += [f"{i.name}*{m.recipes[1].name}"]

dummy_data = '\n'.join(dummy_data)
print(dummy_data)

# dummy_data = """
# verycool*PyQt5.QtCore.QPointF(64.23599999999998, 44.23799999999999)
# it*PyQt5.QtCore.QPointF(391.476, 58.782)
# get*PyQt5.QtCore.QPointF(288.45599999999996, 158.16600000000003)
# but*PyQt5.QtCore.QPointF(277.548, 253.914)
# i*PyQt5.QtCore.QPointF(18.786, 199.98)
# dont*PyQt5.QtCore.QPointF(135.75400000000002, 156.964)
# haha*PyQt5.QtCore.QPointF(224.22000000000003, 15.756)
# its*PyQt5.QtCore.QPointF(410.86800000000005, 252.702)
# cool*PyQt5.QtCore.QPointF(452.07599999999996, 159.378)
#
# get*but
# it*get
# dont*it
# dont*get
# verycool*dont
# i*dont
# haha*dont
# but*its
# its*cool
# """


graph.c.load_graph(load_from_data=dummy_data)
sys.exit(graph.app.exec())
