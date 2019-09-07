#!/usr/bin/env python
import os, sys

from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication,  \
                        QPushButton, \
                         QTreeView
from PyQt5.uic import loadUi


class App(QTreeView):
    def __init__(self):
        super().__init__()

        #loadUi('/home/user/yourproject/resource/treeview_nest.ui')

        # row can be 0 even when it's more than 0.
        self._datamodel = QStandardItemModel(0, 2)
        self.setModel(self._datamodel)

        for i in range(4):
            self._add_widget(i + 1)

        self.show()

    def _add_widget(self, n):
        item_toplevel = QStandardItem('{}th item'.format(n))
        self._datamodel.setItem(n, 0, item_toplevel)

        widget_toplevel = QPushButton('{}th button'.format(n))
        qindex_toplevel = self._datamodel.index(n, 1, QModelIndex())
        self.setIndexWidget(qindex_toplevel, widget_toplevel)

        if n == 2:
            item_child_col0 = QStandardItem('child col0')
            item_child_col1 = QStandardItem()
            #item_toplevel.appendRow(item_child_col0)

            item_toplevel.insertRow(0, [item_child_col0, item_child_col1])

            widget_child = QPushButton('child widget')
            qindex_child = item_child_col1.index()
            self.setIndexWidget(qindex_child, widget_child)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())