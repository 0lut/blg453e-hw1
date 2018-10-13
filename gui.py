
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QAction, QDesktopWidget, QFileDialog, QMainWindow,
                             QSizePolicy)

import utils
from hist_match import calculate_hist, match_histogram


class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.init_menu()
        self.init_size_name()

    def load_input(self):
        filename = QFileDialog.getOpenFileName(self, 'Open Input', '.')
        self.input = utils.load_im(filename[0])
        m = PlotCanvas(self, width=4, height=4,
                       img=self.input, title='Input Image')
        m.move(50, 50)
        m2 = PlotCanvas(self, width=5, height=5, img=self.input, hist=True)
        m2.move(0, 450)

    def load_target(self):
        filename = QFileDialog.getOpenFileName(self, 'Open Target', '.')
        self.target = utils.load_im(filename[0])
        m = PlotCanvas(self, width=4, height=4,
                       img=self.target, title='Target Image')
        m.move(650, 50)
        m2 = PlotCanvas(self, width=5, height=5, img=self.target, hist=True)
        m2.move(600, 450)

    def match_hist(self):
        matched = match_histogram(self.input, self.target)
        m = PlotCanvas(self, width=4, height=4,
                       img=matched, title='Matched Image')
        m.move(1250, 50)
        m2 = PlotCanvas(self, width=5, height=5, img=matched, hist=True)
        m2.move(1200, 450)

    def init_menu(self):
        menubar = self.menuBar()
        file = menubar.addMenu('File Operations')
        imageProcessing = menubar.addMenu('Image Processing')

        self.open_input = QAction('Open Input Image', self)
        self.open_target = QAction('Open Target Image', self)
        self.match = QAction('Match Histograms', self)

        self.open_input.triggered.connect(self.load_input)
        self.open_target.triggered.connect(self.load_target)
        self.match.triggered.connect(self.match_hist)

        file.addAction(self.open_input)
        file.addAction(self.open_target)
        imageProcessing.addAction(self.match)

    def init_size_name(self):
        self.resize(1600, 1600)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Histogram Matching')


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5,
                 height=4, dpi=100,
                 img=None, hist=False, title=''):
        fig = plt.figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        if hist is not False:
            ay = self.figure.add_subplot(311)
            az = self.figure.add_subplot(312)
            aq = self.figure.add_subplot(313)
            hists = [calculate_hist(img[..., i]) for i in range(3)]
            ay.bar(range(256), hists[0], color='r')
            az.bar(range(256), hists[1], color='g')
            aq.bar(range(256), hists[2], color='b')
        else:
            ax = self.figure.add_subplot(111)
            ax.imshow(img)
            ax.set_title(title)
        self.draw()
        self.show()
