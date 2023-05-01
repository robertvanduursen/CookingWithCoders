from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys, os, math

from viewer.nodes import Node

app = QtWidgets.QApplication(sys.argv)
# app.setStyle('Fusion')
root = os.path.dirname(__file__)
save_file = None


class Link(QtWidgets.QGraphicsPathItem):
    """ the concept of a relationship """

    # https://stackoverflow.com/questions/32345714/qgraphicspathitem-different-colors
    # https://stackoverflow.com/questions/50347595/mouse-hover-over-a-pyside-qgraphicspathitem

    def __init__(self, source, target):
        super().__init__()
        self.source = source
        self.target = target

        self.setAcceptHoverEvents(True)
        self.setZValue(-1)

        self._pen = QtGui.QPen(QtGui.QColor(200, 200, 200, 255))
        self._pen.setStyle(QtCore.Qt.DashLine)
        self._pen.setWidth(3)

    def hoverEnterEvent(self, event):
        QtWidgets.QGraphicsPathItem.hoverEnterEvent(self, event)
        print('hovering over link')

        #self.update()

    def shape(self):
        s = QtGui.QPainterPathStroker()
        s.setWidth(30)
        s.setCapStyle(QtCore.Qt.RoundCap)
        path = s.createStroke(self.path())
        return path

    def boundingRect(self):
        return self.shape().boundingRect()


    def mouseDoubleClickEvent(self, event):
        QtWidgets.QGraphicsPathItem.mouseDoubleClickEvent(self, event)
        print(self)
        print(event)



        #super().mouseDoubleClickEvent(self, event)
        #print('lol')
        #self.update()



    def update_path(self):
        self.setPen(self._pen)

        direction = (self.source.pos() - self.target.pos())
        mag = math.sqrt((pow(direction.x(), 2) + pow(direction.y(), 2)))
        norm = direction / mag
        direction = norm

        size = 10

        at = self.target.center + (direction * self.target._size)
        side = QtGui.QVector3D.crossProduct(QtGui.QVector3D(0, 1.0, 0),
                                            QtGui.QVector3D(direction.x(), 0, direction.y())).normalized()
        point_side = QtCore.QPointF(side.x(), side.z()) * size

        path = QtGui.QPainterPath()
        path.moveTo(self.source.center)
        dx = (self.target.pos().x() - self.source.pos().x()) * 0.5
        dy = self.target.pos().y() - self.source.pos().y()
        path.cubicTo(self.source.center, at + (direction * size), at + (direction * size))  # self.target.center)

        self._pen.setStyle(QtCore.Qt.SolidLine)
        my_polygon = QtGui.QPolygonF()

        my_polygon << at
        my_polygon << at + (direction * size) + point_side
        my_polygon << at + (direction * size) - point_side
        my_polygon << at

        path.addPolygon(my_polygon)

        self.setPath(path)


class _view(QtWidgets.QGraphicsView):
    signal_NodeMoved = QtCore.pyqtSignal(str, object)

    connecting = False
    editting = False
    dragging = False
    item1 = False

    def __init__(self, parent):
        super().__init__(parent)

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        # self._initRubberband(event.pos())

        self.setRenderHint(QtGui.QPainter.Antialiasing, True)
        # self.setRenderHint(QtGui.QPainter.TextAntialiasing, config['antialiasing'])
        self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)

        # Connect scene node moved signal
        # scene.signal_NodeMoved.connect(self.signal_NodeMoved)

        self.show()

    def mousePressEvent(self, event):
        """
        Initialize tablet zoom, drag canvas and the selection.

        """
        # Tablet zoom
        if (event.button() == QtCore.Qt.RightButton and
                event.modifiers() == QtCore.Qt.AltModifier):

            if not self.connecting:
                self.item1 = self.itemAt(event.pos())
                self.connecting = True
                print('connecting')
            if self.connecting and self.item1 and self.itemAt(event.pos()) != self.item1:
                link = Link(self.item1, self.itemAt(event.pos()))
                link.update_path()
                self.scene().addItem(link)
                self.connecting = False
                self.item1 = False
                print('connected')

            # self.initMouse = QtGui.QCursor.pos()
            # self.setInteractive(False)

        if (event.button() == QtCore.Qt.LeftButton and
                event.modifiers() == QtCore.Qt.ShiftModifier):
            self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
            self.dragging = True

        if not self.itemAt(event.pos()):
            for item in self.scene().items():
                if isinstance(item, Node):
                    item.setSelected(0)
                    item.update_node()

        else:
            node = self.itemAt(event.pos())
            # print(len(node.connections), node.connections)
            node.setSelected(1)
            node.update_node()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.dragging:
            # self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            painterPath = QtGui.QPainterPath()
            rect = self.mapToScene(self.rubberBandRect())
            painterPath.addPolygon(rect)
            self.scene().setSelectionArea(painterPath)  # ,QtCore.Qt.ContainsItemBoundingRect)

            for item in self.scene().items():
                if isinstance(item, Node):
                    item.update_node()

            self.dragging = False

        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        """
        Emit a signal.

        """
        self.item1 = self.itemAt(event.pos())
        self.editting = True
        self.item1.setSelected(True)
        self.item1.name = ''
        self.item1.update()
        print('editting')

        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        if self.editting:
            if event.key() == QtCore.Qt.Key_Return:
                print('im done')
                self.editting = False
            else:
                print(event.text())
                self.item1.name += event.text()
                self.item1.update()

        if event.key() == QtCore.Qt.Key_Delete:
            for item in self.scene().items():
                if isinstance(item, Node) and item.isSelected():
                    print('deleting', item)
                    self.scene().removeItem(item)

        if event.key() == QtCore.Qt.Key_A and QtCore.Qt.ControlModifier:
            for item in self.scene().items():
                if isinstance(item, Node):
                    item.setSelected(1)
            print('select all')

        super().keyPressEvent(event)


class _scene(QtWidgets.QGraphicsScene):
    signal_NodeMoved = QtCore.pyqtSignal(str, object)

    def __init__(self):
        super().__init__()

        self.setSceneRect(0, 0, 2000, 2000)
        _brush = QtGui.QBrush()
        _brush.setStyle(QtCore.Qt.SolidPattern)
        grey = 128
        _brush.setColor(QtGui.QColor(grey, grey, grey, 255))
        self.setBackgroundBrush(_brush)

    # self.graphicsView
    def mouseMoveEvent(self, event):
        for item in self.items():
            if isinstance(item, Link):
                item.update_path()

        '''
        self.rubberband.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())
        '''

        super().mouseMoveEvent(event)


class CanvasModule(QtWidgets.QMainWindow):
    words = {}
    connections = {}

    filePath = False

    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi(root + r"\canvas.ui", self)
        scene = _scene()

        self.ui.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.ui_content.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        view = _view(parent=None)
        view.setScene(scene)

        self.view = view
        self.scene = scene

        layout = QtWidgets.QGridLayout()
        layout.addWidget(view)
        self.viewWidget.setLayout(layout)

        scene.signal_NodeMoved.connect(view.signal_NodeMoved)

        view.fitInView(scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatioByExpanding)


        self.setContentsMargins(10, 10, 10, 10)
        self.show()

        self.zoom = 100.0
        self.make_connections()

    def make_connections(self):
        self.close_btn.pressed.connect(self.quit)
        pass


    def quit(self):
        print('exiting')
        sys.exit()

    def search_scene(self):
        text = self.searchText.text()
        print(text)
        for word in text.split():
            if word in self.words.keys():
                print(word)
                self.words[word].setSelected(1)
                self.words[word].update_node()

    def zoom_to(self):
        """ Zoom in the view with the mouse wheel. """

        new_zoom = float(eval(self.zoomBox.currentText()))
        zoom_factor = (new_zoom / self.zoom)  # * 0.01
        self.zoom = new_zoom
        self.view.scale(zoom_factor, zoom_factor)
        # print(self.zoomBox.currentText())
        # print((new_zoom / self.zoom))

    def untangle(self):
        pass

    def process_text(self):
        words = [item.name for item in self.scene.items() if isinstance(item, Node)]
        print(words)
        text = self.textInput.toPlainText()
        for word in text.split():
            if word not in words:
                test2 = Node(word)
                self.scene.addItem(test2)

    def new_statement(self):
        text = self.logicInput.toPlainText()
        print(text)
        new_words = text.split()
        new_links = []
        for idx, word in enumerate(new_words):
            if idx != len(new_words) - 1:
                if word in self.words.keys() and new_words[idx + 1] in self.words.keys():
                    if (word, new_words[idx + 1]) not in self.connections.keys():
                        link = Link(self.words[word], self.words[new_words[idx + 1]])
                        new_links.append(link)
                        print(word, new_words[idx + 1])

        print('new_links', len(new_links), new_links)
        for new in new_links:
            self.scene.addItem(new)

    def clear_graph(self):
        self.scene.clear()

    def check_filePath(self):
        custom_file = False
        if custom_file:
            print('found custom path')
            self.filePath = custom_file
        else:
            print('found old path')
            self.filePath = save_file
        print(self.filePath)


    def save_graph(self):
        items = [item for item in self.scene.items() if isinstance(item, Node)]
        links = [item for item in self.scene.items() if isinstance(item, Link)]

        if len(set([item.name for item in items])) < len(items):
            print('there are duplicates')

        self.check_filePath()
        with open(self.filePath, 'w') as FH:
            for item in items:
                FH.write('%s*%s\n' % (item.name, item.pos()))

            FH.write('\n')

            for link in links:
                FH.write('%s*%s\n' % (link.source.name, link.target.name))

    def load_graph(self, load_from_memory=False, load_from_data: str = False):
        self.scene.clear()

        if load_from_memory:
            data = [item for item in dummy_data.strip().split('\n')]
        elif load_from_data:
            data = [item for item in load_from_data.strip().split('\n')]
        else:
            self.check_filePath()
            with open(self.filePath, 'r') as FH:
                data = [item[:-1] for item in FH.readlines()]

        parter = data.index('')
        # parter = [idx for idx, x in enumerate(data) if x == ''][0]
        items = data[:parter]
        links = data[parter + 1:]

        self.words = {}

        words = []
        for item in set(items):
            name = item.split('*')[0]
            if name not in words:
                pos = item.split('*')[1][len('PyQt5.'):]
                pos = eval(pos)
                test1 = Node(name)
                test1.setPos(pos)
                self.scene.addItem(test1)
                words.append(name)
                self.words[name] = test1

        self.connections = {}
        draw_links = []
        for link in links:
            source_name, target_name = link.split('*')
            source = [x for x in self.scene.items() if x.name == source_name]
            target = [x for x in self.scene.items() if x.name == target_name]
            link = Link(source[0], target[0])

            if link not in draw_links:
                draw_links.append(link)
                self.connections[(source[0], target[0])] = link

        for idx, k in enumerate(draw_links):
            self.scene.addItem(k)
            k.update_path()
            k.source.connections.append(link)
            k.target.connections.append(link)

        # print('graph loaded')


# if __name__ == '__main__':

c = CanvasModule()

styleSheet = """
QMainWindow {
    background-color: #4e4e4e;
    color: #ffffff;
}

QPushButton {
    background-color: #4e4e4e;
    color: #ffffff;
}

QPushButton#enterStatement{
    background-color: #ffffff;
    color: #4e4e4e;
}
"""

app.setStyleSheet(styleSheet)

# demo
dummy_data = """
amazing*PyQt5.QtCore.QPointF(64.23599999999998, 44.23799999999999)
it*PyQt5.QtCore.QPointF(391.476, 58.782)
get*PyQt5.QtCore.QPointF(288.45599999999996, 158.16600000000003)
but*PyQt5.QtCore.QPointF(277.548, 253.914)
i*PyQt5.QtCore.QPointF(18.786, 199.98)
dont*PyQt5.QtCore.QPointF(135.75400000000002, 156.964)
haha*PyQt5.QtCore.QPointF(224.22000000000003, 15.756)
its*PyQt5.QtCore.QPointF(410.86800000000005, 252.702)
cool*PyQt5.QtCore.QPointF(452.07599999999996, 159.378)

get*but
it*get
dont*it
dont*get
amazing*dont
i*dont
haha*dont
but*its
its*cool
"""

