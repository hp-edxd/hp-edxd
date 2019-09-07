# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hpMCA.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_hpMCA(object):
    def setupUi(self, hpMCA):
        hpMCA.setObjectName("hpMCA")
        hpMCA.resize(1236, 715)
        self.centralwidget = QtWidgets.QWidget(hpMCA)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self._Layout = QtWidgets.QHBoxLayout()
        self._Layout.setObjectName("_Layout")
        self.ControlsLayout = QtWidgets.QVBoxLayout()
        self.ControlsLayout.setObjectName("ControlsLayout")
        self.groupBoxAcq = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxAcq.sizePolicy().hasHeightForWidth())
        self.groupBoxAcq.setSizePolicy(sizePolicy)
        self.groupBoxAcq.setMinimumSize(QtCore.QSize(180, 90))
        self.groupBoxAcq.setMaximumSize(QtCore.QSize(180, 16777215))
        self.groupBoxAcq.setObjectName("groupBoxAcq")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBoxAcq)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.acqBtnLayout = QtWidgets.QGridLayout()
        self.acqBtnLayout.setObjectName("acqBtnLayout")
        self.btnOn = QtWidgets.QPushButton(self.groupBoxAcq)
        self.btnOn.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOn.sizePolicy().hasHeightForWidth())
        self.btnOn.setSizePolicy(sizePolicy)
        self.btnOn.setMinimumSize(QtCore.QSize(75, 0))
        self.btnOn.setCheckable(True)
        self.btnOn.setObjectName("btnOn")
        self.acqBtnLayout.addWidget(self.btnOn, 0, 0, 1, 1)
        self.btnOff = QtWidgets.QPushButton(self.groupBoxAcq)
        self.btnOff.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOff.sizePolicy().hasHeightForWidth())
        self.btnOff.setSizePolicy(sizePolicy)
        self.btnOff.setMinimumSize(QtCore.QSize(75, 0))
        self.btnOff.setObjectName("btnOff")
        self.acqBtnLayout.addWidget(self.btnOff, 0, 1, 1, 1)
        self.btnErase = QtWidgets.QPushButton(self.groupBoxAcq)
        self.btnErase.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnErase.sizePolicy().hasHeightForWidth())
        self.btnErase.setSizePolicy(sizePolicy)
        self.btnErase.setMinimumSize(QtCore.QSize(75, 0))
        self.btnErase.setObjectName("btnErase")
        self.acqBtnLayout.addWidget(self.btnErase, 1, 0, 1, 1)
        self.verticalLayout_10.addLayout(self.acqBtnLayout)
        self.ControlsLayout.addWidget(self.groupBoxAcq)
        self.groupBoxElapsed = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxElapsed.sizePolicy().hasHeightForWidth())
        self.groupBoxElapsed.setSizePolicy(sizePolicy)
        self.groupBoxElapsed.setMinimumSize(QtCore.QSize(170, 70))
        self.groupBoxElapsed.setMaximumSize(QtCore.QSize(180, 70))
        self.groupBoxElapsed.setObjectName("groupBoxElapsed")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBoxElapsed)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.ElapsedHLayout = QtWidgets.QHBoxLayout()
        self.ElapsedHLayout.setObjectName("ElapsedHLayout")
        self.ElapsedlLblVLayout = QtWidgets.QVBoxLayout()
        self.ElapsedlLblVLayout.setObjectName("ElapsedlLblVLayout")
        self.label = QtWidgets.QLabel(self.groupBoxElapsed)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(50, 0))
        self.label.setObjectName("label")
        self.ElapsedlLblVLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.groupBoxElapsed)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(50, 0))
        self.label_2.setObjectName("label_2")
        self.ElapsedlLblVLayout.addWidget(self.label_2)
        self.ElapsedHLayout.addLayout(self.ElapsedlLblVLayout)
        self.ElapsedIndicatorVlayout = QtWidgets.QVBoxLayout()
        self.ElapsedIndicatorVlayout.setObjectName("ElapsedIndicatorVlayout")
        self.lblLiveTime = QtWidgets.QLabel(self.groupBoxElapsed)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblLiveTime.sizePolicy().hasHeightForWidth())
        self.lblLiveTime.setSizePolicy(sizePolicy)
        self.lblLiveTime.setMinimumSize(QtCore.QSize(60, 0))
        self.lblLiveTime.setMidLineWidth(2)
        self.lblLiveTime.setObjectName("lblLiveTime")
        self.ElapsedIndicatorVlayout.addWidget(self.lblLiveTime)
        self.lblRealTime = QtWidgets.QLabel(self.groupBoxElapsed)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRealTime.sizePolicy().hasHeightForWidth())
        self.lblRealTime.setSizePolicy(sizePolicy)
        self.lblRealTime.setMinimumSize(QtCore.QSize(60, 0))
        self.lblRealTime.setObjectName("lblRealTime")
        self.ElapsedIndicatorVlayout.addWidget(self.lblRealTime)
        self.ElapsedHLayout.addLayout(self.ElapsedIndicatorVlayout)
        self.verticalLayout_11.addLayout(self.ElapsedHLayout)
        self.ControlsLayout.addWidget(self.groupBoxElapsed)
        self.groupBoxROIs = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxROIs.sizePolicy().hasHeightForWidth())
        self.groupBoxROIs.setSizePolicy(sizePolicy)
        self.groupBoxROIs.setMinimumSize(QtCore.QSize(180, 0))
        self.groupBoxROIs.setMaximumSize(QtCore.QSize(180, 120))
        self.groupBoxROIs.setObjectName("groupBoxROIs")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBoxROIs)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.ROIBtnsLayout = QtWidgets.QGridLayout()
        self.ROIBtnsLayout.setObjectName("ROIBtnsLayout")
        self.btnROIadd = QtWidgets.QPushButton(self.groupBoxROIs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnROIadd.sizePolicy().hasHeightForWidth())
        self.btnROIadd.setSizePolicy(sizePolicy)
        self.btnROIadd.setMinimumSize(QtCore.QSize(75, 0))
        self.btnROIadd.setCheckable(True)
        self.btnROIadd.setObjectName("btnROIadd")
        self.ROIBtnsLayout.addWidget(self.btnROIadd, 0, 0, 1, 1)
        self.btnROIdelete = QtWidgets.QPushButton(self.groupBoxROIs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnROIdelete.sizePolicy().hasHeightForWidth())
        self.btnROIdelete.setSizePolicy(sizePolicy)
        self.btnROIdelete.setMinimumSize(QtCore.QSize(75, 0))
        self.btnROIdelete.setObjectName("btnROIdelete")
        self.ROIBtnsLayout.addWidget(self.btnROIdelete, 0, 1, 1, 1)
        self.btnROIclear = QtWidgets.QPushButton(self.groupBoxROIs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnROIclear.sizePolicy().hasHeightForWidth())
        self.btnROIclear.setSizePolicy(sizePolicy)
        self.btnROIclear.setMinimumSize(QtCore.QSize(75, 0))
        self.btnROIclear.setObjectName("btnROIclear")
        self.ROIBtnsLayout.addWidget(self.btnROIclear, 1, 0, 1, 1)
        self.verticalLayout_8.addLayout(self.ROIBtnsLayout)
        self.ROIPrevNextLayout = QtWidgets.QHBoxLayout()
        self.ROIPrevNextLayout.setObjectName("ROIPrevNextLayout")
        self.btnROIprev = QtWidgets.QPushButton(self.groupBoxROIs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnROIprev.sizePolicy().hasHeightForWidth())
        self.btnROIprev.setSizePolicy(sizePolicy)
        self.btnROIprev.setMaximumSize(QtCore.QSize(30, 23))
        self.btnROIprev.setObjectName("btnROIprev")
        self.ROIPrevNextLayout.addWidget(self.btnROIprev)
        self.lineROI = QtWidgets.QLineEdit(self.groupBoxROIs)
        self.lineROI.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineROI.setObjectName("lineROI")
        self.ROIPrevNextLayout.addWidget(self.lineROI)
        self.btnROInext = QtWidgets.QPushButton(self.groupBoxROIs)
        self.btnROInext.setMaximumSize(QtCore.QSize(30, 23))
        self.btnROInext.setObjectName("btnROInext")
        self.ROIPrevNextLayout.addWidget(self.btnROInext)
        self.verticalLayout_8.addLayout(self.ROIPrevNextLayout)
        self.ControlsLayout.addWidget(self.groupBoxROIs)
        self.groupBoxXRF = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxXRF.sizePolicy().hasHeightForWidth())
        self.groupBoxXRF.setSizePolicy(sizePolicy)
        self.groupBoxXRF.setMinimumSize(QtCore.QSize(180, 0))
        self.groupBoxXRF.setMaximumSize(QtCore.QSize(180, 16777215))
        self.groupBoxXRF.setObjectName("groupBoxXRF")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBoxXRF)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.XRFPrevNextLayout = QtWidgets.QHBoxLayout()
        self.XRFPrevNextLayout.setObjectName("XRFPrevNextLayout")
        self.btnKLMprev = QtWidgets.QPushButton(self.groupBoxXRF)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnKLMprev.sizePolicy().hasHeightForWidth())
        self.btnKLMprev.setSizePolicy(sizePolicy)
        self.btnKLMprev.setMaximumSize(QtCore.QSize(30, 23))
        self.btnKLMprev.setObjectName("btnKLMprev")
        self.XRFPrevNextLayout.addWidget(self.btnKLMprev)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBoxXRF)
        self.lineEdit_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.XRFPrevNextLayout.addWidget(self.lineEdit_2)
        self.btnKLMnext = QtWidgets.QPushButton(self.groupBoxXRF)
        self.btnKLMnext.setMaximumSize(QtCore.QSize(30, 23))
        self.btnKLMnext.setObjectName("btnKLMnext")
        self.XRFPrevNextLayout.addWidget(self.btnKLMnext)
        self.verticalLayout_6.addLayout(self.XRFPrevNextLayout)
        self.ControlsLayout.addWidget(self.groupBoxXRF)
        self.groupBoxVerticalScale = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxVerticalScale.sizePolicy().hasHeightForWidth())
        self.groupBoxVerticalScale.setSizePolicy(sizePolicy)
        self.groupBoxVerticalScale.setMinimumSize(QtCore.QSize(180, 0))
        self.groupBoxVerticalScale.setMaximumSize(QtCore.QSize(180, 16777215))
        self.groupBoxVerticalScale.setObjectName("groupBoxVerticalScale")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBoxVerticalScale)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.LogScaleLayout = QtWidgets.QHBoxLayout()
        self.LogScaleLayout.setObjectName("LogScaleLayout")
        self.radioLog = QtWidgets.QRadioButton(self.groupBoxVerticalScale)
        self.radioLog.setMaximumSize(QtCore.QSize(50, 16777215))
        self.radioLog.setChecked(True)
        self.radioLog.setObjectName("radioLog")
        self.LogScaleLayout.addWidget(self.radioLog)
        self.radioLin = QtWidgets.QRadioButton(self.groupBoxVerticalScale)
        self.radioLin.setChecked(False)
        self.radioLin.setObjectName("radioLin")
        self.LogScaleLayout.addWidget(self.radioLin)
        self.verticalLayout_7.addLayout(self.LogScaleLayout)
        self.ControlsLayout.addWidget(self.groupBoxVerticalScale)
        self.groupBoxHorizontalScale = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxHorizontalScale.sizePolicy().hasHeightForWidth())
        self.groupBoxHorizontalScale.setSizePolicy(sizePolicy)
        self.groupBoxHorizontalScale.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBoxHorizontalScale.setMaximumSize(QtCore.QSize(180, 16777215))
        self.groupBoxHorizontalScale.setObjectName("groupBoxHorizontalScale")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBoxHorizontalScale)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.HorizontalScaleLayout = QtWidgets.QGridLayout()
        self.HorizontalScaleLayout.setSpacing(5)
        self.HorizontalScaleLayout.setObjectName("HorizontalScaleLayout")
        self.radioE = QtWidgets.QRadioButton(self.groupBoxHorizontalScale)
        self.radioE.setMinimumSize(QtCore.QSize(35, 0))
        self.radioE.setChecked(True)
        self.radioE.setObjectName("radioE")
        self.HorizontalScaleLayout.addWidget(self.radioE, 0,0)
        self.radioq = QtWidgets.QRadioButton(self.groupBoxHorizontalScale)
        self.radioq.setMinimumSize(QtCore.QSize(35, 0))
        self.radioq.setObjectName("radioq")
        self.HorizontalScaleLayout.addWidget(self.radioq, 0,1)
        self.radioChannel = QtWidgets.QRadioButton(self.groupBoxHorizontalScale)
        self.radioChannel.setObjectName("radioChannel")
        self.HorizontalScaleLayout.addWidget(self.radioChannel, 1,0)
        self.radiod = QtWidgets.QRadioButton(self.groupBoxHorizontalScale)
        self.radiod.setObjectName("radiod")
        self.HorizontalScaleLayout.addWidget(self.radiod, 1,1)
        self.horizontalLayout_8.addLayout(self.HorizontalScaleLayout)
        self.ControlsLayout.addWidget(self.groupBoxHorizontalScale)
        spacerItem = QtWidgets.QSpacerItem(20, 1000, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ControlsLayout.addItem(spacerItem)
        self._Layout.addLayout(self.ControlsLayout)
        self.DisplayLayout = QtWidgets.QVBoxLayout()
        self.DisplayLayout.setObjectName("DisplayLayout")
        self.pg = PltWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pg.sizePolicy().hasHeightForWidth())
        self.pg.setSizePolicy(sizePolicy)
        self.pg.setMinimumSize(QtCore.QSize(200, 0))
        self.pg.setInteractive(True)
        self.pg.setObjectName("pg")
        self.DisplayLayout.addWidget(self.pg)
        self.CursorsLayout = QtWidgets.QHBoxLayout()
        self.CursorsLayout.setObjectName("CursorsLayout")
        self.indexLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.indexLabel.sizePolicy().hasHeightForWidth())
        self.indexLabel.setSizePolicy(sizePolicy)
        self.indexLabel.setMinimumSize(QtCore.QSize(150, 0))
        self.indexLabel.setMaximumSize(QtCore.QSize(250, 16777215))
        self.indexLabel.setText("")
        self.indexLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.indexLabel.setObjectName("indexLabel")
        self.CursorsLayout.addWidget(self.indexLabel)
        self.cursorLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cursorLabel.sizePolicy().hasHeightForWidth())
        self.cursorLabel.setSizePolicy(sizePolicy)
        self.cursorLabel.setMinimumSize(QtCore.QSize(150, 0))
        self.cursorLabel.setMaximumSize(QtCore.QSize(250, 16777215))
        self.cursorLabel.setText("")
        self.cursorLabel.setObjectName("cursorLabel")
        self.CursorsLayout.addWidget(self.cursorLabel)
        self.DisplayLayout.addLayout(self.CursorsLayout)
        self._Layout.addLayout(self.DisplayLayout)
        self.verticalLayout_4.addLayout(self._Layout)
        hpMCA.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(hpMCA)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1236, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuControl = QtWidgets.QMenu(self.menubar)
        self.menuControl.setObjectName("menuControl")
        self.menuDisplay = QtWidgets.QMenu(self.menubar)
        self.menuDisplay.setObjectName("menuDisplay")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        hpMCA.setMenuBar(self.menubar)
        self.actionBackground = QtWidgets.QAction(hpMCA)
        self.actionBackground.setObjectName("actionBackground")
        self.actionSave_As = QtWidgets.QAction(hpMCA)
        self.actionSave_As.setEnabled(False)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionPrint = QtWidgets.QAction(hpMCA)
        self.actionPrint.setObjectName("actionPrint")
        self.actionPreferences = QtWidgets.QAction(hpMCA)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionExit = QtWidgets.QAction(hpMCA)
        self.actionExit.setObjectName("actionExit")
        self.actionPresets = QtWidgets.QAction(hpMCA)
        self.actionPresets.setObjectName("actionPresets")
        self.actionCalibrate_energy = QtWidgets.QAction(hpMCA)
        self.actionCalibrate_energy.setEnabled(False)
        self.actionCalibrate_energy.setObjectName("actionCalibrate_energy")
        self.actionPreferences_2 = QtWidgets.QAction(hpMCA)
        self.actionPreferences_2.setObjectName("actionPreferences_2")
        self.actionJCPDS = QtWidgets.QAction(hpMCA)
        self.actionJCPDS.setEnabled(False)
        self.actionJCPDS.setObjectName("actionJCPDS")
        self.actionFit_peaks = QtWidgets.QAction(hpMCA)
        self.actionFit_peaks.setObjectName("actionFit_peaks")
        self.actionAbout = QtWidgets.QAction(hpMCA)
        self.actionAbout.setObjectName("actionAbout")
        self.actionOpen_detector = QtWidgets.QAction(hpMCA)
        self.actionOpen_detector.setObjectName("actionOpen_detector")
        self.actionOpen_file = QtWidgets.QAction(hpMCA)
        self.actionOpen_file.setObjectName("actionOpen_file")
        self.actionCalibrate_2theta = QtWidgets.QAction(hpMCA)
        self.actionCalibrate_2theta.setEnabled(False)
        self.actionCalibrate_2theta.setObjectName("actionCalibrate_2theta")
        self.actionFluor = QtWidgets.QAction(hpMCA)
        self.actionFluor.setEnabled(False)
        self.actionFluor.setObjectName("actionFluor")
        self.actionROIs = QtWidgets.QAction(hpMCA)
        self.actionROIs.setEnabled(False)
        self.actionROIs.setObjectName("actionROIs")
        self.actionOverlay = QtWidgets.QAction(hpMCA)
        self.actionOverlay.setEnabled(False)
        self.actionOverlay.setObjectName("actionOverlay")
        self.actionExport_pattern = QtWidgets.QAction(hpMCA)
        self.actionExport_pattern.setEnabled(False)
        self.actionExport_pattern.setObjectName("actionExport_pattern")
        self.actionSave_next = QtWidgets.QAction(hpMCA)
        self.actionSave_next.setEnabled(False)
        self.actionSave_next.setObjectName("actionSave_next")
        self.actionPressure = QtWidgets.QAction(hpMCA)
        self.actionPressure.setEnabled(False)
        self.actionPressure.setObjectName("actionPressure")
        self.actionDisplayPrefs = QtWidgets.QAction(hpMCA)
        self.actionDisplayPrefs.setObjectName("actionDisplayPrefs")
        self.menuFile.addAction(self.actionOpen_file)
        self.menuFile.addAction(self.actionOpen_detector)
        self.menuFile.addAction(self.actionOverlay)
        self.menuFile.addAction(self.actionSave_next)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionExport_pattern)
        self.menuFile.addAction(self.actionPreferences)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuControl.addAction(self.actionCalibrate_energy)
        self.menuControl.addAction(self.actionCalibrate_2theta)
        self.menuDisplay.addAction(self.actionJCPDS)
        self.menuDisplay.addAction(self.actionFluor)
        self.menuDisplay.addAction(self.actionROIs)
        self.menuDisplay.addAction(self.actionPressure)
        self.menuDisplay.addAction(self.actionDisplayPrefs)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuControl.menuAction())
        self.menubar.addAction(self.menuDisplay.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(hpMCA)
        QtCore.QMetaObject.connectSlotsByName(hpMCA)

    def retranslateUi(self, hpMCA):
        _translate = QtCore.QCoreApplication.translate
        hpMCA.setWindowTitle(_translate("hpMCA", "hpMCA"))
        self.groupBoxAcq.setTitle(_translate("hpMCA", "Aquisition"))
        self.btnOn.setText(_translate("hpMCA", "On"))
        self.btnOff.setText(_translate("hpMCA", "Off"))
        self.btnErase.setText(_translate("hpMCA", "Erase"))
        self.groupBoxElapsed.setTitle(_translate("hpMCA", "Elapsed Time"))
        self.label.setText(_translate("hpMCA", "Live"))
        self.label_2.setText(_translate("hpMCA", "Real"))
        self.lblLiveTime.setText(_translate("hpMCA", "0"))
        self.lblRealTime.setText(_translate("hpMCA", "0"))
        self.groupBoxROIs.setTitle(_translate("hpMCA", "ROIs"))
        self.btnROIadd.setText(_translate("hpMCA", "Add"))
        self.btnROIdelete.setText(_translate("hpMCA", "Delete"))
        self.btnROIclear.setText(_translate("hpMCA", "Clear All"))
        self.btnROIprev.setText(_translate("hpMCA", "<"))
        self.btnROInext.setText(_translate("hpMCA", ">"))
        self.groupBoxXRF.setTitle(_translate("hpMCA", "Fluorescence markers"))
        self.btnKLMprev.setText(_translate("hpMCA", "<"))
        self.btnKLMnext.setText(_translate("hpMCA", ">"))
        self.groupBoxVerticalScale.setTitle(_translate("hpMCA", "Vertical scale"))
        self.radioLog.setText(_translate("hpMCA", "Log"))
        self.radioLin.setText(_translate("hpMCA", "Linear"))
        self.groupBoxHorizontalScale.setTitle(_translate("hpMCA", "Horizontal scale"))
        self.radioE.setText(_translate("hpMCA", "E"))
        self.radioq.setText(_translate("hpMCA", "q"))
        self.radioChannel.setText(_translate("hpMCA", "Channel"))
        self.radiod.setText(_translate("hpMCA", "d"))
        self.menuFile.setTitle(_translate("hpMCA", "File"))
        self.menuControl.setTitle(_translate("hpMCA", "Control"))
        self.menuDisplay.setTitle(_translate("hpMCA", "Display"))
        self.menuHelp.setTitle(_translate("hpMCA", "Help"))
        self.actionBackground.setText(_translate("hpMCA", "Background"))
        self.actionSave_As.setText(_translate("hpMCA", "Save As"))
        self.actionPrint.setText(_translate("hpMCA", "Print"))
        self.actionPreferences.setText(_translate("hpMCA", "Preferences"))
        self.actionExit.setText(_translate("hpMCA", "Exit"))
        self.actionPresets.setText(_translate("hpMCA", "Presets..."))
        self.actionCalibrate_energy.setText(_translate("hpMCA", "Calibrate energy..."))
        self.actionPreferences_2.setText(_translate("hpMCA", "Preferences..."))
        self.actionJCPDS.setText(_translate("hpMCA", "Phase"))
        self.actionFit_peaks.setText(_translate("hpMCA", "Fit peaks..."))
        self.actionAbout.setText(_translate("hpMCA", "About"))
        self.actionOpen_detector.setText(_translate("hpMCA", "Open detector..."))
        self.actionOpen_file.setText(_translate("hpMCA", "Open file..."))
        self.actionCalibrate_2theta.setText(_translate("hpMCA", "Calibrate 2theta..."))
        self.actionFluor.setText(_translate("hpMCA", "Fluorescence"))
        self.actionROIs.setText(_translate("hpMCA", "ROIs"))
        self.actionOverlay.setText(_translate("hpMCA", "Overlay"))
        self.actionExport_pattern.setText(_translate("hpMCA", "Export pattern"))
        self.actionSave_next.setText(_translate("hpMCA", "Save next"))
        self.actionPressure.setText(_translate("hpMCA", "Pressure"))
        self.actionDisplayPrefs.setText(_translate("hpMCA", "Colors options"))

from hpMCA.widgets.PltWidget import PltWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    hpMCA = QtWidgets.QMainWindow()
    ui = Ui_hpMCA()
    ui.setupUi(hpMCA)
    hpMCA.show()
    sys.exit(app.exec_())

