# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from MyLabel import MyLabel
from PersonInfo import PersonInfo
import sys
import re

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class InputDlg(QDialog):
    def __init__(self, parent = None):
        super(InputDlg,self).__init__(parent)
        self.setWindowTitle("家族信息表")
        self.setWindowIcon(QIcon("./icon/dialog.png"))
        self.personInfo = PersonInfo()
        self.CreateWidgets()
        self.Layout()
        self.connect(self.birthdayEditLabel, SIGNAL("mouseDoubleClicked()"), self.ShowBirthCalendar)
        self.connect(self.birthCalendar, SIGNAL("selectionChanged()"), self.ShowBirthday)
        self.connect(self.deadCheckBox, SIGNAL("stateChanged(int)"), self.SetDeath)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def CreateWidgets(self):
        self.nameLabel = QLabel("姓名:")
        self.birthdayLabel = QLabel("出生年月:")
        self.birthdayEditLabel = MyLabel("1900-01-01")
        self.birthdayEditLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.addressLabel = QLabel("地址:")
        self.deathdayLabel = QLabel("去世年月:")
        self.deathdayEditLabel = MyLabel("- - - ")
        self.deathdayEditLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)

        self.nameEdit = QLineEdit()
        self.addressEdit = QLineEdit()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        self.confirmButton = QPushButton("确定")
        self.cancelButton = QPushButton("取消")

        self.birthCalendar = QCalendarWidget()
        self.birthCalendar.setWindowTitle("出生年月")
        self.birthCalendar.setWindowIcon(QIcon("./icon/calendar1.png"))
        self.birthCalendar.hide()
        self.deathCalendar = QCalendarWidget()
        self.deathCalendar.setWindowTitle("去世年月")
        self.deathCalendar.setWindowIcon(QIcon("./icon/calendar2.png"))
        self.deathCalendar.hide()

        self.deadCheckBox = QCheckBox("去世")  # 默认未去世
        self.marryCheckBox = QCheckBox("结婚")
        self.marryCheckBox.toggle()  # 默认结婚


    def Layout(self):
        self.UpLayout()
        mainLayout = QGridLayout(self)
        mainLayout.addLayout(self.upLayout, 0, 0)

    def UpLayout(self):
        self.upLayout = QGridLayout()
        self.upLayout.addWidget(self.nameLabel, 0, 0)
        self.upLayout.addWidget(self.nameEdit, 0, 1)
        self.upLayout.addWidget(self.birthdayLabel, 1, 0)
        self.upLayout.addWidget(self.birthdayEditLabel, 1, 1)
        self.upLayout.addWidget(self.addressLabel, 2, 0)
        self.upLayout.addWidget(self.addressEdit, 2, 1)
        self.upLayout.addWidget(self.deadCheckBox, 3, 0)
        self.upLayout.addWidget(self.marryCheckBox, 3, 1)
        self.upLayout.addWidget(self.deathdayLabel, 4, 0)
        self.upLayout.addWidget(self.deathdayEditLabel, 4, 1)
        self.upLayout.addWidget(self.buttons, 5, 1)

    def ShowBirthCalendar(self):
        self.birthCalendar.show()

    def ShowDeathCalendar(self):
        self.deathCalendar.show()

    def SetDeath(self, state):
        # state为2时，表示复选框选中
        if state == 2:
            self.connect(self.deathdayEditLabel, SIGNAL("mouseDoubleClicked()"), self.ShowDeathCalendar)
            self.connect(self.deathCalendar, SIGNAL("selectionChanged()"), self.ShowDeathday)
        # 否则将之前建立的连接断开
        else:
            self.disconnect(self.deathdayEditLabel, SIGNAL("mouseDoubleClicked()"), self.ShowDeathCalendar)
            self.disconnect(self.deathCalendar, SIGNAL("selectionChanged()"), self.ShowDeathday)    


    def ShowBirthday(self):
        birthday = self.birthCalendar.selectedDate()
        birthdayString = birthday.toString()
        pattern = re.compile(r"\d+")  # 匹配月、日、年
        birthdayList = re.findall(pattern, birthdayString)
        self.birthdayEditLabel.setText(str(birthdayList[2])+"-"+str(birthdayList[0])+"-"+str(birthdayList[1]))

    def ShowDeathday(self):
        deathday = self.deathCalendar.selectedDate()
        deathdayString = deathday.toString()
        pattern = re.compile(r"\d+")  # 匹配月、日、年
        deathdayList = re.findall(pattern, deathdayString)
        self.deathdayEditLabel.setText(str(deathdayList[2])+"-"+str(deathdayList[0])+"-"+str(deathdayList[1]))

    # 获取对话框中的数据
    def GetData(self):
        personInfo = PersonInfo()
        personInfo.name = self.nameEdit.text()
        personInfo.birthday = self.birthdayEditLabel.text()
        personInfo.address = self.addressEdit.text()
        if self.marryCheckBox.checkState() == 2:
            personInfo.marry = "是"
        else:
            personInfo.marry = "否"
        if self.deadCheckBox.checkState() == 2:
            personInfo.alive = "否"
            personInfo.deathday = self.deathdayEditLabel.text()
        else:
            personInfo.alive = "是"
            personInfo.deathday = "- - -"
        return personInfo

def main():
    app = QApplication(sys.argv)
    inputDialog = InputDlg()
    inputDialog.show()
    app.exec_()

if __name__ == '__main__':
    main()