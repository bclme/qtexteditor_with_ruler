from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QStatusBar, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QFont, QFontMetrics, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
mouse_pos = None
class TextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.parent().Ruler_V.update()
        self.parent().Ruler_H.update()
class Square(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the widget
 
        self.setFixedHeight(20)
        self.setFixedWidth(20)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.blue)
        
class Ruler_H(QWidget):
    def __init__(self, text_edit):
        super().__init__()

        # Set up the widget
 
        self.setFixedHeight(20)
  
        self.font = QFont('Arial', 5)
        self.font_metrics = QFontMetrics(self.font)
        self.text_edit = text_edit
        self.text_edit.mouseMoveEvent = self.mouseMoveEvent
        #self.mouse_pos = None
        #self.orientation = orientation

    def paintEvent(self, event):
        global mouse_pos
        if not self.text_edit:
           return

        painter = QPainter(self)

        # Set up the white background
        painter.fillRect(self.rect(), Qt.white)

        # Get the metrics for the font
        painter.setFont(self.font)
        font_metrics = self.font_metrics

        # Draw the tick marks and text labels
  
        x_pos = self.text_edit.horizontalScrollBar().value()
        width = self.width()
        step = font_metrics.width(' ') * 5

        for x in range(x_pos % step, width, step):
             if x % 100 == 0:
                 painter.drawLine(x, 0, x, 5)

                 # Center the text labels to the lines
                 label_width = font_metrics.width(str(x))
                 label_x_pos = x - label_width / 2
                 label_y_pos = 15
                 painter.drawText(int(label_x_pos), int(label_y_pos), str(x))
             elif x % 50 == 0:
                 painter.drawLine(x, 0, x, 3)
             elif x % 10 == 0:
                    painter.drawLine(x, 0, x, 1)
            #painter.setPen(QPen(Qt.red, 1))
            #try:
            #  painter.drawLine(mouse_pos.x(), 0, mouse_pos.x(), 20)
              
            #except Exception as err:
            #    print(str(err))
        

        # Draw the red line at the current mouse position
        painter.setPen(QPen(Qt.red, 1))
        try:
   
                painter.drawLine(mouse_pos.x(), 0, mouse_pos.x(), self.height())
  
                
        except Exception as err:
                print(str(err))
        #ruler_v.update()        

    def mouseMoveEvent(self, event):
        global mouse_pos
        mouse_pos = event.pos()
        self.update()
        
class Ruler_V(QWidget):
    def __init__(self, text_edit):
        super().__init__()

        # Set up the widget

        self.setFixedWidth(20)
        self.font = QFont('Arial', 5)
        self.font_metrics = QFontMetrics(self.font)
        self.text_edit = text_edit
        self.text_edit.mouseMoveEvent = self.mouseMoveEvent
        #self.mouse_pos = None
        #self.orientation = orientation

    def paintEvent(self, event):
        global mouse_pos
        if not self.text_edit:
            return

        painter = QPainter(self)

        # Set up the white background
        painter.fillRect(self.rect(), Qt.white)

        # Get the metrics for the font
        painter.setFont(self.font)
        font_metrics = self.font_metrics

        # Draw the tick marks and text labels
 
        y_pos = self.text_edit.verticalScrollBar().value()
        height = self.height()
        step = font_metrics.height() * 1

        for y in range(y_pos % step, height, step):
                if y % 100 == 0:
                    painter.drawLine(0, y, 5, y)

                    # Center the text labels to the lines
                    label_height = font_metrics.height()
                    label_y_pos = y - label_height / 2.2
                    label_x_pos = 15
                    painter.save()
                    painter.translate(label_x_pos, label_y_pos)
                    painter.rotate(-90)
                    painter.drawText(-label_height, 0, str(y))
                    painter.restore()
                    painter.resetTransform() # reset translation and rotation
                elif y % 50 == 0:
                    painter.drawLine(0, y, 3, y)
                elif y % 10 == 0:
                    painter.drawLine(0, y, 1, y)

        # Draw the red line at the current mouse position
        painter.setPen(QPen(Qt.red, 1))
        try:
 
                painter.drawLine(0, mouse_pos.y(), self.width(), mouse_pos.y())
                
        except Exception as err:
                print(str(err))

    def mouseMoveEvent(self, event):
        global mouse_pos
        mouse_pos = event.pos()
        self.update()        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up main window
        self.setWindowTitle("Ruler Example")
        self.setGeometry(100, 100, 800, 600)

        # Set up text editor
        self.text_edit = TextEdit()
        self.setCentralWidget(self.text_edit)

        # Set up vertical ruler
        self.v_ruler = Ruler_V(self.text_edit)
        #self.v_ruler.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # Set up horizontal ruler
        self.h_ruler = Ruler_H(self.text_edit)
        #self.h_ruler.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.square = Square()

        # Set up layout
        ruler_vlayout = QVBoxLayout()
        ruler_vlayout.addWidget(self.square)
        ruler_vlayout.addWidget(self.v_ruler)
        ruler_layout = QHBoxLayout()
        ruler_layout.addLayout(ruler_vlayout)
        editor_layout = QVBoxLayout()
        editor_layout.addWidget(self.h_ruler)
        editor_layout.addWidget(self.text_edit)
        main_layout = QHBoxLayout()
        main_layout.addLayout(ruler_layout)
        main_layout.addLayout(editor_layout)

        # Set the layout for the main window
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        #self.text_edit.mouseMoveEvent = self.mouseMoveEvent
        # Add status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.mouse_pos_label = QLabel()
        self.statusBar.addPermanentWidget(self.mouse_pos_label)
        
    def paintEvent(self, event):
        global mouse_pos
        # Get the mouse position
        #mouse_pos = event.pos()
        try:
          #print(mouse_pos.x())
          x = mouse_pos.x()
          y = mouse_pos.y()
          self.v_ruler.update()
          #self.h_ruler.painter.drawLine(mouse_pos.x(), 0, mouse_pos.x(), 20)
          # Update the mouse position label in the status bar
          self.mouse_pos_label.setText(f'x: {x}, y: {y}')
          
          # Call the base class implementation of mouseMoveEvent
        except Exception as err:
            print(str(err))
        #super().mouseMoveEvent(event)
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
        
