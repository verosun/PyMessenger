import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication,QLineEdit,QListWidget,QListWidgetItem)
import socket
import threading
import errno
from socket import error as socket_error

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.isClient = bool()
        self.s = socket.socket()
        self.clientsocket = socket.socket()

    def initUI(self):
        sendButton = QPushButton("Send")
        sendButton.clicked.connect(self.send)
        connectButton = QPushButton("Connect")
        connectButton.clicked.connect(self.connect)
        self.addressBox =QLineEdit()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(sendButton)
        hbox.addWidget(connectButton)
        hbox.addWidget(self.addressBox)
        self.msgBox = QLineEdit()
        self.msgList = QListWidget()
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.msgList)
        vbox.addWidget(self.msgBox)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setGeometry(1000, 100, 500, 250)
        self.setWindowTitle('Cricket Messaging Service')
        self.show()
    def send(self):
        text = "You: "+self.msgBox.text()
        listWidgetItem = QListWidgetItem(text)
        self.msgList.addItem(listWidgetItem)
        if(self.isClient):
            print("client sending")
            self.s.send(bytes(self.msgBox.text(),"utf-8"))
        else:
            print("server sending")
            self.clientsocket.send(bytes(self.msgBox.text(), "utf-8"))
    def recieve(self):
        full_msg = ''
        while True:
            if(self.isClient):
                msg = self.s.recv(1024)
            else:
                msg = self.clientsocket.recv(1024)
            full_msg += msg.decode("utf-8")
            listWidgetItem = QListWidgetItem("recieved: "+full_msg)
            self.msgList.addItem(listWidgetItem)
            full_msg=''
    def connect(self):
        print("connecting")
        try:
            self.isClient = True
            print("is client")
            address = self.addressBox.text()
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((address, 1234))
            rxThread = threading.Thread(target=self.recieve)
            rxThread.start()
        except socket_error as serr:
            self.isClient = False
            print("is Server")
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(("127.0.0.1", 1234))
            self.s.listen(5)
            self.clientsocket, address = self.s.accept()
            rxThread = threading.Thread(target=self.recieve)
            rxThread.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())