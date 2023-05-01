from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys, os, math


nodeColours = {
    0: QtGui.QColor(0, 0, 220, 255),
    1: QtGui.QColor(220, 128, 0, 255),
    2: QtGui.QColor(220, 0, 220, 255),
    3: QtGui.QColor(220, 220, 0, 255),
    4: QtGui.QColor(100, 0, 0, 255),
    5: QtGui.QColor(100, 0, 100, 255),
    6: QtGui.QColor(100, 100, 0, 255),
    7: QtGui.QColor(100, 0, 255, 255),
    8: QtGui.QColor(100, 255, 0, 255),

}


def node_colour(nr):
    if nr in nodeColours.keys():
        return nodeColours[nr]
    return nodeColours[0]


class Node(QtWidgets.QGraphicsItem):
    connections = False
    _size = 20

    def __init__(self, name=False):
        super(Node, self).__init__()

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.rectF = QtCore.QRectF(0, 0, 50, 50)

        self._center = QtCore.QPoint(0, 0)
        self.name = name if name else 'test'

        self._brush = QtGui.QBrush()
        self._brush.setStyle(QtCore.Qt.SolidPattern)
        self._brush.setColor(QtGui.QColor(0, 0, 220, 255))

        self._pen = QtGui.QPen()
        self._pen.setStyle(QtCore.Qt.SolidLine)
        self._pen.setWidth(0.1)
        self._pen.setColor(QtCore.Qt.black)

        self._textPen = QtGui.QPen()
        self._textPen.setStyle(QtCore.Qt.SolidLine)
        self._textPen.setColor(QtCore.Qt.white)

        self._nodeTextFont = QtGui.QFont("Arial", 10, QtGui.QFont.Bold)

        self.connections = []

    def update_node(self):
        if self.isSelected():
            self._brush.setColor(QtGui.QColor(0, 220, 0, 255))
        else:
            self._brush.setColor(node_colour(len(self.connections)))

    @property
    def center(self):
        return self.pos() + self._center

    def boundingRect(self):
        return self.rectF

    def my_size(self):
        return self._size

    def paint(self, painter=None, style=None, widget=None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen)

        painter.setFont(self._nodeTextFont)
        metrics = QtGui.QFontMetrics(painter.font())
        text_width = metrics.boundingRect(self.name).width()  # + 14
        text_height = metrics.boundingRect(self.name).height()  # + 14

        padding = 15
        circleSize = max(text_width, 25) + padding

        painter.drawEllipse(0, 0, circleSize, circleSize)
        self.rectF = QtCore.QRectF(0, 0, circleSize, circleSize)

        self._center.setX(circleSize * 0.5)
        self._center.setY(circleSize * 0.5)
        self._size = circleSize * 0.5

        painter.setPen(self._textPen)

        margin = circleSize * 0.5  # (text_width - 50) * 0.5
        text_rect = QtCore.QRect(padding * 0.5,
                                margin - (text_height * 0.5),
                                max(text_width, 25),
                                text_height)

        painter.drawText(text_rect,
                         QtCore.Qt.AlignCenter,
                         self.name)

