from PyQt6 import QtWidgets, QtGui, QtCore
import json
from confluent_kafka import Consumer, KafkaError
from threading import Thread
import requests

class Ui_MainWindow(object):

    def init(self):

        # make a get request on the api 127.0.0.1:8000/api/news
        response = requests.get("http://127.0.0.1:8000/api/news")

        # get the json response
        json_response = response.json()

        # iterate over the json response
        for news in json_response:
            # get the news title
            title = news['title']
            message = news['message']

            # update the ui with the news title
            self.update_ui_with_message(title, message)
        

    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(789, 440)
        MainWindow.setWindowTitle("Kafka Consumer")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 10, 201, 51))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(16)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(60, 60, 681, 311))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setKerning(True)
        self.listWidget.setFont(font)
        self.listWidget.setFlow(QtWidgets.QListView.Flow.TopToBottom)
        self.listWidget.setResizeMode(QtWidgets.QListView.ResizeMode.Fixed)
        self.listWidget.setViewMode(QtWidgets.QListView.ViewMode.ListMode)
        self.listWidget.setObjectName("listWidget")

        # ADd padding to the list widget
        self.listWidget.setContentsMargins(10, 10, 10, 10)

        # Inicie um loop de leitura Kafka em uma thread separada
        self.read_kafka_thread = Thread(target=self.read_kafka)
        self.read_kafka_thread.daemon = True
        self.read_kafka_thread.start()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 27))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(parent=self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuAbout = QtWidgets.QMenu(parent=self.menubar)
        self.menuAbout.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.menuAbout.setToolTipsVisible(True)
        self.menuAbout.setObjectName("menuAbout")

        self.init()

        # On click on about menu
        def menuAboutClicked():
            print("About clicked")
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("About")
            msg.setText("Kafka Consumer")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg.exec()

        about_action = self.menuAbout.addAction("About")
        about_action.triggered.connect(menuAboutClicked)

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "Últimas Notícias"))
        self.listWidget.setSortingEnabled(False)
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

    def read_kafka(self):
        # Configurações do consumidor Kafka
        consumer_config = {
            'bootstrap.servers': 'localhost:9092',  # Endereço do cluster Kafka
            'group.id': 'my-consumer-group',       # Identificador do grupo de consumidores
            'auto.offset.reset': 'earliest'        # Configuração de reset do offset para ler desde o início
        }

        # Crie um consumidor Kafka
        consumer = Consumer(consumer_config)

        # Inscreva-se no tópico desejado
        consumer.subscribe(['testTopic'])  # Subscreva-se ao tópico desejado

        while True:
            msg = consumer.poll(1.0)  # Aguarde por mensagens por até 1 segundo

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"Reached end of partition {msg.partition()}")
                else:
                    print(f"Error while consuming message: {msg.error()}")
            else:
                # Atualize a interface do PyQt com a mensagem Kafka
                json_string = msg.value().decode('utf-8')

                # Converta a string JSON em um objeto Python
                news = json.loads(json_string)

                # Obtenha o título e a mensagem da notícia
                title = news['title']
                message_text = news['message']

                # Atualize a interface do PyQt com a mensagem Kafka
                self.update_ui_with_message(title, message_text)

        # Feche o consumidor Kafka quando você terminar de usá-lo
        consumer.close()

    def update_ui_with_message(self, title, message):
        # Create a item on the list with a big bold title and a small italic message
        item = QtWidgets.QListWidgetItem()
        
        # Set the title as text and message 
        item.setText(f"{title}\n{message}")

        # Set the item size
        item.setSizeHint(QtCore.QSize(100, 100))    

        # Add the item to the top of the list
        self.listWidget.insertItem(0, item)

        # Select the created item
        self.listWidget.setCurrentItem(item)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
