import sys
import rsa
import requests
import json
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QPushButton,QTextEdit,QGridLayout, QHBoxLayout,QVBoxLayout,QApplication)


class RegUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.nickname = QLabel('用户名')
        self.email = QLabel('邮箱')
        self.pwd = QLabel('密码')
        self.pwdcheck = QLabel('再次确认密码')
        self.warning = QLabel('')

        self.nicknameEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.pwdEdit = QLineEdit()
        self.pwdEdit.setEchoMode(QLineEdit.Password)
        self.pwdcheckEdit = QLineEdit()
        self.pwdcheckEdit.setEchoMode(QLineEdit.Password)
        regbtn = QPushButton('注册并登录', self)
        regbtn.clicked.connect(self.reg)
        grid = QGridLayout()


        grid.addWidget(self.nickname, 1, 0)
        grid.addWidget(self.nicknameEdit, 1, 1)

        grid.addWidget(self.email, 2, 0)
        grid.addWidget(self.emailEdit, 2, 1)

        grid.addWidget(self.pwd, 3, 0)
        grid.addWidget(self.pwdEdit, 3, 1)

        grid.addWidget(self.pwdcheck, 4, 0)
        grid.addWidget(self.pwdcheckEdit, 4, 1)

        hbox = QHBoxLayout()
        hbox.addLayout(grid)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.warning)
        vbox.addWidget(regbtn)

        self.setLayout(vbox)

        self.setGeometry(900, 400, 350, 180)
        self.setWindowTitle('注册')
        self.show()

    def reg(self):
        if self.validate():
            (pubkey, privkey) = rsa.newkeys(512)  #本地生成公私钥对，RSA算法
            #print(pubkey)
            self.postData(pubkey)

    def validate(self):
        #依次判断输入框是否为空
        if not self.nicknameEdit.text():
            self.warning.setText("用户名不能设置为空")

        elif not self.emailEdit.text():
            self.warning.setText("邮箱不能设置为空")

        elif not self.pwdEdit.text():
            self.warning.setText("密码不能设置为空")

        #判断两次密码输入是否相同，不同则清空密码框
        elif self.pwdcheckEdit.text() != self.pwdEdit.text():
            self.pwdEdit.clear()
            self.pwdcheckEdit.clear()
            self.warning.setText("两次密码输入不同，请重新输入！")

        else:
            return True

    def postData(self,pubkey):
        #print(pubkey)
        reginfo = {'nickname': self.nicknameEdit.text(), 'email': self.emailEdit.text(),'pwd': self.pwdEdit.text(),'pubkey':pubkey}
        #TO_DO:服务器关闭状态就会停止运行
        #contact：Atlas
        r = requests.post("http://127.0.0.1:8888/reg", data=reginfo)
        #print(r.status_code)

        if not r:
            self.warning.setText("服务器维护中...")
        else:

            feedback = json.loads(r.content)

            if feedback['status'] == "ok":
                self.warning.clear()
                # 接收证书
                cert = open("cert.xml", "w")
                cert.write(feedback['cert'])
                cert.close()
                # 验证证书
                cer_tree = ET.parse('cert.xml')
                cer_root = cer_tree.getroot()
                verify = True
                if verify:
                    self.close()
                else:
                    self.warning.setText("服务器证书不可信，请勿继续")
            else:
                self.warning.setText("登录失败，请稍后再试")







