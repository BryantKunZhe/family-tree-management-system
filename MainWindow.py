import sys
import queue
import numpy
import json
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from InputDlg import InputDlg
from PersonInfo import PersonInfo
from FamilyNode import FamilyNode

# 使中文在QT界面中不会乱码
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class MainWindow(QMainWindow, InputDlg):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle("家谱管理系统")
        self.setWindowIcon(QIcon("./icon/family-tree.png"))
        self.CreateFileMenu()
        self.CreateHelpMenu()
        self.CreateContextMenu()
        self.familyTree = QTreeWidget()
        self.familyTree.setColumnCount(6)
        self.familyTree.setHeaderLabels(["姓名", "出生年月", "地址", "婚否", "健在否", "死亡日期"])
        self.setCentralWidget(self.familyTree)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.connect(self.familyTree, SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.pp)
        self.connect(self, SIGNAL("customContextMenuRequested(QPoint)"), self.ShowContextMenu)

    # 创建文件菜单
    def CreateFileMenu(self):
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("&File")
        self.newFile = QAction(QIcon("./icon/new-file.png"), "New File", self)
        self.newFile.setShortcut("Ctrl+N")
        self.connect(self.newFile, SIGNAL("triggered()"), self.ShowInputDlg)
        self.saveFile = QAction(QIcon("./icon/save-file.png"), "Save", self)
        self.saveFile.setShortcut("Ctrl+S")
        self.connect(self.saveFile, SIGNAL("triggered()"), self.SaveFile)
        self.openFile = QAction(QIcon("./icon/open-file.png"), "Open File...", self)
        self.openFile.setShortcut("Ctrl+O")
        self.connect(self.openFile, SIGNAL("triggered()"), self.OpenFile)
        self.fileMenu.addAction(self.newFile)
        self.fileMenu.addAction(self.saveFile)
        self.fileMenu.addAction(self.openFile)

    # 创建右键菜单
    def CreateContextMenu(self):
        self.contextMenu = QMenu(self)
        self.addItem = QAction("增加孩子", self)
        self.connect(self.addItem, SIGNAL("triggered()"), self.AddChildItem)
        self.deleteItem = QAction("删除节点", self)
        self.connect(self.deleteItem, SIGNAL("triggered()"), self.DeleteChildItem)
        self.modifyItem = QAction("修改信息", self) # 修改试试editItem (self, QTreeWidgetItem item, int column = 0)
        self.connect(self.modifyItem, SIGNAL("triggered()"), self.GetJsonData)
        self.contextMenu.addAction(self.addItem)
        self.contextMenu.addAction(self.deleteItem)
        self.contextMenu.addAction(self.modifyItem)

    def CreateHelpMenu(self):
        self.helpMenu = self.menu.addMenu("&Help")
        self.about = QAction("About...", self)
        self.connect(self.about, SIGNAL("triggered()"), self.ShowAboutDlg)
        self.helpMenu.addAction(self.about)

    # 弹出添加祖宗信息的对话框
    def ShowInputDlg(self):
        self.dialog = InputDlg(self)
        self.dialog.setWindowTitle("添加祖宗信息")
        self.dialog.show()
        if self.dialog.exec_():
            info = self.dialog.GetData()
            root = QTreeWidgetItem(self.familyTree)
            root.setText(0, info.name)
            root.setText(1, info.birthday)
            root.setText(2, info.address)
            root.setText(3, info.marry)
            root.setText(4, info.alive)
            root.setText(5, info.deathday)
            self.familyTree.addTopLevelItem(root)  # 将祖宗信息添加到familytree中
        self.dialog.destroy()

    def ShowAboutDlg(self):
        QMessageBox.about(self,"About","PyQt4+python3.6\n"+"author:BryantKunZhe\n"+
            "https://github.com/BryantKunZhe/family-tree-management-system")

    # 增加孩子节点
    def AddChildItem(self):
        self.dialog = InputDlg(self)
        self.dialog.setWindowTitle("添加孩子信息")
        self.dialog.show()
        if self.dialog.exec_():
            info = self.dialog.GetData()
            childItem = QTreeWidgetItem(self.familyTree.currentItem())  # 当前节点的子节点
            childItem.setText(0, info.name)
            childItem.setText(1, info.birthday)
            childItem.setText(2, info.address)
            childItem.setText(3, info.marry)
            childItem.setText(4, info.alive)
            childItem.setText(5, info.deathday)
            self.familyTree.currentItem().addChild(childItem)
        self.dialog.destroy()

    def SaveFile(self):
        filePath =  QFileDialog.getSaveFileName(self, "Save File", "./家谱文件",
            "json file(*.json);;all files(*.*)")
        with open(filePath, "w") as f:
            jsonData = self.GetJsonData()
            f.write(jsonData)

    def DeleteChildItem(self):
        self.familyTree.currentItem().parent().removeChild(self.familyTree.currentItem())

    # 显示右键菜单
    def ShowContextMenu(self, pos):
        currentItem = self.familyTree.currentItem()
        if currentItem == None:
            return
        else:
            self.contextMenu.exec_(QCursor.pos())  # 将菜单显示在鼠标点击处
            self.contextMenu.show()
        self.contextMenu.hide()

    # 递归将QTreeWidgetItem中的数据保存为json
    def GetChildrenJson(self, item):
        childJson = []
        for node in self.nodeList:
            if node.parent() == item:
                childJson.append({"name":node.text(0) ,"birthday":node.text(1),
                    "address":node.text(2), "marry":node.text(3), "alive":node.text(4),
                    "deathday":node.text(5), "children":self.GetChildrenJson(node)})
        return childJson

    def GetJsonData(self):
        self.nodeQueue = queue.Queue()
        self.nodeList = []
        self.root = self.familyTree.currentItem()
        # 获取familytree的根节点
        while self.root.parent() != None:
            self.root = self.root.parent()

        # 层次遍历
        self.nodeQueue.put(self.root)  # 将根节点压入队列
        while self.nodeQueue.empty() == False:
            node = self.nodeQueue.get()
            self.nodeList.append(node)
            for i in range(0, node.childCount()):
                self.nodeQueue.put(node.child(i))

        #print (self.nodeList[1].text(0))
        return json.dumps(self.GetChildrenJson(None))

    # 打开家谱文件，解析json，得到一个FamilyNode的列表
    def OpenFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', './家谱文件', "json file(*.json)")
        with open(filename, "r") as f:
            content = json.load(f)
        jsonData = content[0]
        indentify = 1
        root = FamilyNode()
        root.nodeInfo = PersonInfo()
        root.nodeInfo.name = jsonData["name"]
        root.nodeInfo.birthday = jsonData["birthday"]
        root.nodeInfo.address = jsonData["address"]
        root.nodeInfo.marry = jsonData["marry"]
        root.nodeInfo.alive = jsonData["alive"]
        root.nodeInfo.deathday = jsonData["deathday"]
        root.children = jsonData["children"]
        root.indentify = indentify
        root.parentId = 0

        self.itemList = []
        itemQueue = queue.Queue()
        itemQueue.put(root)

        while itemQueue.empty() == False:
            node = itemQueue.get()
            self.itemList.append(node)
            nodeList = node.children
            for item in nodeList:
                child = FamilyNode()
                child.nodeInfo = PersonInfo()
                indentify = indentify + 1
                child.nodeInfo.name = item["name"]
                child.nodeInfo.birthday = item["birthday"]
                child.nodeInfo.address = item["address"]
                child.nodeInfo.marry = item["marry"]
                child.nodeInfo.alive = item["alive"]
                child.nodeInfo.deathday = item["deathday"]
                child.children = item["children"]
                child.indentify = indentify
                child.parentId = node.indentify
                itemQueue.put(child)
        self.ShowFamilyTree()
        #print (self.itemList)

    def ShowFamilyTree(self):
        root = self.itemList[0]
        self.rootItem = QTreeWidgetItem(self.familyTree)
        self.rootItem.setText(0, root.nodeInfo.name)
        self.rootItem.setText(1, root.nodeInfo.birthday)
        self.rootItem.setText(2, root.nodeInfo.address)
        self.rootItem.setText(3, root.nodeInfo.marry)
        self.rootItem.setText(4, root.nodeInfo.alive)
        self.rootItem.setText(5, root.nodeInfo.deathday)
        self.familyTree.addTopLevelItem(self.rootItem)
        self.InsertTreeItem(root, self.rootItem)

    def InsertTreeItem(self, item, treeItem):
        for node in self.itemList:
            if node.parentId == item.indentify:
                child = QTreeWidgetItem(treeItem)
                child.setText(0, node.nodeInfo.name)
                child.setText(1, node.nodeInfo.birthday)
                child.setText(2, node.nodeInfo.address)
                child.setText(3, node.nodeInfo.marry)
                child.setText(4, node.nodeInfo.alive)
                child.setText(5, node.nodeInfo.deathday)
                treeItem.addChild(self.InsertTreeItem(node, child))

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()