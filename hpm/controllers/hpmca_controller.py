# -*- coding: utf8 -*-

# DISCLAIMER
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



import os, os.path, sys, platform, copy

from PyQt5 import uic, QtWidgets,QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox, QErrorMessage
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from epics.clibs import *  # makes sure dlls are included in the exe

from hpm.models.mcaModel import MCA
from hpm.models.epicsMCA import epicsMCA


from hpm.widgets.UtilityWidgets import save_file_dialog, open_file_dialog, open_files_dialog
from hpm.widgets.eCalWidget import mcaCalibrateEnergy
from hpm.widgets.TthCalWidget import mcaCalibrate2theta
from hpm.widgets.xrfWidget import xrfWidget
from hpm.widgets.hpmcaWidget import hpMCAWidget


from hpm.controllers.PhaseController import PhaseController
from hpm.controllers.mcaPlotController import plotController
from hpm.controllers.RoiController import RoiController
from hpm.controllers.OverlayController import OverlayController
from hpm.controllers.LatticeRefinementController import LatticeRefinementController
from hpm.controllers.EnvironmentController import EnvironmentController
from hpm.controllers.MultipleDatasetsController import MultipleDatasetsController

from hpm.controllers.FileSaveController import FileSaveController
from hpm.controllers.DisplayPrefsController import DisplayPreferences
#from hpm.controllers.hklGenController import hklGenController
from hpm.controllers.RoiPrefsController import RoiPreferences


import utilities.hpMCAutilities as mcaUtil
from utilities.HelperModule import increment_filename

from epics import PV

Theme = 1   # app style 0=windows 1=dark 
from .. import style_path

class hpmcaController(QObject):
    key_signal = pyqtSignal(str)
    
    def __init__(self, app):
        super().__init__()
        self.app = app  # app object
        global Theme
        self.Theme = Theme
        self.style_path = style_path
        self.setStyle(self.Theme)
        self.widget = hpMCAWidget(app) 
        
        self.displayPrefs = DisplayPreferences(self.widget.pg)
        

        self.elapsed_time_presets = ['0','2','5','30','60','120'] 
        
        self.zoom_pan = 0        # mouse left button interaction mode 0=rectangle zoom 1=pan
        
        self.create_connections() 
        
        self.working_directories = mcaUtil.restore_folder_settings()
        
        self.defaults_options = mcaUtil.restore_defaults_settings()
        
        self.presets = mcaUtil.mcaDisplay_presets() 
        self.last_saved = ''
        
        # initialize some stuff
        self.mca = None             # mca model

     

        self.epicsMCAholder = None   # holds a epics based MCA reference 
        self.fileMCAholder = None   # holds a file system based MCA reference 

        self.Foreground = None       # str, can be either 'epics' or 'file'
        
        self.plotController = None    
        self.roi_controller = None
        self.phase_controller = None  # phase controller 
        self.fluorescence_controller = None
        self.overlay_controller = None
        self.lattice_refinement_controller = None
        self.controllers_initialized = False

        self.unit = 'E' #default units
        self.dx_type = 'exd'
       

        self.setHorzScaleBtnsEnabled(self.dx_type)

        self.title_name = ''

        #initialize file saving controller
        self.file_save_controller = FileSaveController(self, defaults_options=self.defaults_options)
        self.multiple_datasets_controller = MultipleDatasetsController(self.file_save_controller)
        self.multiple_datasets_controller.file_changed_signal.connect(self.file_changed_signal_callback)
        self.multiple_datasets_controller.channel_changed_signal.connect(self.multispectral_channel_changed_callback)

        self.make_prefs_menu()  # for mac

        #self.initControllers()
        
    def create_connections(self):
        ui = self.widget
        '''ui.btnROIadd.clicked.connect(lambda:self.roi_action('add'))
        ui.btnROIclear.clicked.connect(lambda:self.roi_action('clear'))
        ui.btnROIdelete.clicked.connect(lambda:self.roi_action('delete'))
        ui.btnROIprev.clicked.connect(lambda:self.roi_action('prev'))
        ui.btnROInext.clicked.connect(lambda:self.roi_action('next'))'''
        ui.btnKLMprev.clicked.connect(lambda:self.xrf_action('prev'))
        ui.btnKLMnext.clicked.connect(lambda:self.xrf_action('next'))
        ui.lineEdit_2.editingFinished.connect(lambda:self.xrf_search(ui.lineEdit_2.text()))

        ui.key_signal.connect(self.key_sig_callback)
       
        #epics related buttons:
        self.epicsBtns = [ui.btnOn,ui.btnOff,ui.btnErase]

        
        self.epicsPresets = [ui.PRTM_pv, ui.PLTM_pv]
        self.epicsElapsedTimeBtns_PRTM = [ui.PRTM_0,
                                          ui.PRTM_1,
                                          ui.PRTM_2,
                                          ui.PRTM_3,
                                          ui.PRTM_4,
                                          ui.PRTM_5  ]
        self.epicsElapsedTimeBtns_PLTM = [ui.PLTM_0,
                                          ui.PLTM_1,
                                          ui.PLTM_2,
                                          ui.PLTM_3,
                                          ui.PLTM_4,
                                          ui.PLTM_5  ]
        self.update_elapsed_preset_btn_messages(self.elapsed_time_presets)
        

        ui.radioLog.toggled.connect(self.LogScaleSet)
        ui.radioE.toggled.connect(lambda:self.HorzScaleRadioToggle(self.widget.radioE))
        ui.radioq.toggled.connect(lambda:self.HorzScaleRadioToggle(self.widget.radioq))
        ui.radioChannel.toggled.connect(lambda:self.HorzScaleRadioToggle(self.widget.radioChannel))
        ui.radiod.toggled.connect(lambda:self.HorzScaleRadioToggle(self.widget.radiod))
        ui.radiotth.toggled.connect(lambda:self.HorzScaleRadioToggle(self.widget.radiotth))
        
        ui.actionExit.triggered.connect(self.widget.close)
        
        
        ui.actionJCPDS.triggered.connect(self.jcpds_module)
        ui.actionCalibrate_energy.triggered.connect(self.calibrate_energy_module)
        ui.actionCalibrate_2theta.triggered.connect(self.calibrate_tth_module)
        ui.actionOpen_detector.triggered.connect(self.openDetector)
        ui.actionROIs.triggered.connect(self.roi_module)
        ui.actionOverlay.triggered.connect(self.overlay_module)
        ui.actionFluor.triggered.connect(self.fluorescence_module)
        ui.actionEvironment.triggered.connect(self.environment_module)
        ui.actionMultiSpectra.triggered.connect(self.multi_spectra_module)
        
        ui.actionLatticeRefinement.triggered.connect(self.lattice_refinement_module)
        ui.actionhklGen.triggered.connect(self.hklGen_module)
        ui.actionManualTth.triggered.connect(self.set_Tth)
        ui.actionManualWavelength.triggered.connect(self.set_Wavelength)
        ui.actionDisplayPrefs.triggered.connect(self.display_preferences_module)
        ui.actionRoiPrefs.triggered.connect(self.roi_preferences_module)
        ui.actionPresets.triggered.connect(self.presets_module)
        ui.actionAbout.triggered.connect(self.about_module)

        ui.baseline_subtract.clicked.connect(self.baseline_subtract_callback)

        ui.file_view_btn.pressed.connect(self.file_view_btn_callback)
        ui.live_view_btn.pressed.connect(self.live_view_btn_callback)

        
        
        # file save/read actions moved to self.file_save_controller

    def make_prefs_menu(self):
        _platform = platform.system()
        if _platform == "Darwin":    # macOs has a 'special' way of handling preferences menu
            # TODO upgrade the preferences menu
            pact = QtWidgets.QAction('Preferences', self.app)
            pact.triggered.connect(self.file_save_controller.preferences_module)
            pact.setMenuRole(QtWidgets.QAction.PreferencesRole)
            pmenu = QtWidgets.QMenu('Preferences')
            pmenu.addAction(pact)
            menu = self.widget.menuBar()
            menu.addMenu(pmenu)

    def about_module(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText('This program was written by R. Hrubiak')
        self.msg.setInformativeText('More info to come...')
        self.msg.setWindowTitle('About')
        self.msg.setDetailedText('The details are as follows:')
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()

    '''def file_dragged_in_signal(self, f):
        self.openFile(filename=f)'''

    def key_sig_callback(self, sig):
        if sig == 'right' :
            self.roi_controller. roi_action('next')
        if sig == 'left' :
            self.roi_controller. roi_action('prev')
        if sig == 'delete' :
            self.roi_controller. roi_action('delete')
        if sig == 'shift_press' :
            self.zoomPan(1)
        if sig == 'shift_release' :
            self.zoomPan(0)  
            
    def set_Tth(self):
        mca = self.mca
        calibration = copy.deepcopy(mca.get_calibration()[0])
        tth = calibration.two_theta
        val, ok = QInputDialog.getDouble(self.widget, "Manual 2theta setting", "Current 2theta = "+ '%.4f'%(tth)+"\nEnter new 2theta: \n(Note: calibrated 2theta value will be updated)",tth,0,180,4)
        if ok:
            calibration.two_theta = val
            mca.set_calibration([calibration])

    def set_Wavelength(self):
        mca = self.mca
        calibration = copy.deepcopy(mca.get_calibration()[0])
        wavelength = calibration.wavelength
        val, ok = QInputDialog.getDouble(self.widget, "Manual wavelength setting", "Current wavelength = "+ '%.4f'%(wavelength)+"\nEnter new wavelength: \n(Note: calibrated wavelength value will be updated)",wavelength,0,180,4)
        if ok:
            calibration.wavelength = val
            mca.set_calibration([calibration])
            mca.wavelength = val

           



    def display_preferences_module(self, *args, **kwargs):
        self.displayPrefs.show()

    def roi_preferences_module(self, *args, **kwargs):
        self.roiPrefs.show()
            
    
    def presets_module(self, *args, **kwargs):
        presets = self.mca.get_presets()
        
        [ok, presets] = mcaUtil.mcaControlPresets.showDialog(self.widget,presets) 
        if ok :
            self.presets = presets
            self.mca.set_presets(self.presets)
            #mcaUtil.save_file_settings(file_preferences)
    
    

    def initMCA(self, mcaType, det_or_file):
        if mcaType == 'file':    
            init =    self.initFileMCA(det_or_file)
            if init == 0:
                self.widget.file_view_btn.setEnabled(True)
                self.widget.file_view_btn.setChecked(True)  
        elif mcaType == 'epics': 
            init =    self.initEpicsMCA(det_or_file)
            if init == 0:
                self.widget.live_view_btn.setEnabled(True)
                self.widget.live_view_btn.setChecked(True) 
        if init == 0:
            self.Foreground = mcaType    
            self.refresh_controllers_mca()
        return init

    def refresh_controllers_mca(self):
        self.mca.auto_process_rois = True
        if self.controllers_initialized:
            self.plotController.set_mca(self.mca)
            self.phase_controller.set_mca(self.mca)
            self.roi_controller.set_mca(self.mca)
            self.fluorescence_controller.set_mca(self.mca)
        
    def initFileMCA(self, file):
        mca = None
        if self.Foreground == 'file':
            if self.mca != None:  
                mca = self.mca
        if self.Foreground == 'epics':
            if self.fileMCAholder != None:
                mca = self.fileMCAholder
        if mca == None:
            mca = MCA()
        mca.auto_process_rois = True
        [fileout, success] = mca.read_file(file=file, netcdf=0, detector=0)
        if not success:
            return 1
        self.set_file_mca(mca)
        return 0

    def initEpicsMCA(self, det):
        name = ''
        if self.epicsMCAholder is not None:
            name = self.epicsMCAholder.name
        if name == det : #check if the same epics MCA is already initialized
            mca = self.epicsMCAholder
            mca.toggleEpicsWidgetsEnabled(True)
        else:
            if self.epicsMCAholder != None:
                self.epicsMCAholder.unload()
            mca = epicsMCA(record_name = det, 
                            epics_buttons = self.epicsBtns, 
                            file_options = self.file_save_controller.file_options,
                            environment_file = 'catch1d.env',
                            dead_time_indicator = self.widget.dead_time_indicator
                            )
            if not mca.initOK:
                [live_val, real_val] = self.epicsPresets
                live_val.disconnect()
                real_val.disconnect()
                return 1
        self.set_epics_mca(mca)
        return 0
        

    def set_epics_mca(self, mca):
        if self.Foreground == 'file':
            self.fileMCAholder = self.mca
        self.mca = mca
        [live_val, real_val] = self.epicsPresets
        epicsElapsedTimeBtns_PRTM = self.epicsElapsedTimeBtns_PRTM
        epicsElapsedTimeBtns_PLTM = self.epicsElapsedTimeBtns_PLTM
        record = self.mca.name
        live_val.connect(record + '.PRTM')
        real_val.connect(record + '.PLTM')
        for btn in epicsElapsedTimeBtns_PRTM:
            btn.connect(record + '.PRTM')
        for btn in epicsElapsedTimeBtns_PLTM:
            btn.connect(record + '.PLTM')
        self.widget.dead_time_indicator.re_connect()

    def set_file_mca(self, mca):
        if self.mca != mca:
            if self.Foreground == 'epics':
                [live_val, real_val] = self.epicsPresets
                epicsElapsedTimeBtns_PRTM = self.epicsElapsedTimeBtns_PRTM
                epicsElapsedTimeBtns_PLTM = self.epicsElapsedTimeBtns_PLTM
                self.mca.dataAcquired.disconnect()
                self.mca.acq_stopped.disconnect()
                self.epicsMCAholder = self.mca
                self.blockSignals(True)
                for btn in self.epicsBtns:
                    btn.setEnabled(False)
                    btn.setChecked(False)
                    self.blockSignals(False)
                    live_val.disconnect()
                    real_val.disconnect()
                    for btn in epicsElapsedTimeBtns_PRTM:
                        btn.disconnect()
                    for btn in epicsElapsedTimeBtns_PLTM:
                        btn.disconnect()
                    self.widget.dead_time_indicator.disconnect()
                self.blockSignals(False)
            self.mca = mca
        
            

    def update_elapsed_preset_btn_messages(self, elapsed_presets):
        for i, btn in enumerate(self.epicsElapsedTimeBtns_PLTM):
            btn.setMessage(message = elapsed_presets[i])
        for i, btn in enumerate(self.epicsElapsedTimeBtns_PRTM):
            btn.setMessage(message = elapsed_presets[i])

    def initControllers(self):
        #initialize plot model
        
        self.plotController = plotController(self.widget.pg, self.mca, self, self.unit)
        # updates cursor position labels
        self.plotController.staticCursorMovedSignal.connect(self.mouseCursor)
        self.plotController.fastCursorMovedSignal.connect(self.mouseMoved)  
        self.plotController.selectedRoiChanged.connect(self.roi_selection_updated) 
        self.plotController.envUpdated.connect(self.envs_updated_callback)

        self.environment_controller = EnvironmentController()
        
        #initialize roi controller
        self.roi_controller = self.plotController.roi_controller 
        #self.roi_controller .rois_widget.lock_rois_btn.toggled. connect( self.lock_rois_btn_callback)
        self.roi_controller.roi_updated_signal.connect (self.roi_updated_signal_callback)
        
        # initialize phase controller
        self.phase_controller = PhaseController(self.widget.pg, self.mca, 
                                            self.plotController, self.roi_controller, 
                                            self.working_directories)
        # roiPrefs handles options for automatic ROI adding from the phases module                                   
        self.roiPrefs = RoiPreferences(self.phase_controller)
    
        # initialize overlay controller: not done yet
        self.overlay_controller = OverlayController( self, self.plotController, self.widget)
        #initialize xrf controller
        self.fluorescence_controller = xrfWidget(self.widget.pg, self.plotController, self.roi_controller, self.mca)
        self.fluorescence_controller.xrf_selection_updated_signal.connect(self.xrf_updated)

        self.lattice_refinement_controller = LatticeRefinementController(self.mca,self.widget.pg,self.plotController,self)

        

        #initialize hklGen controller
        #self.hlkgen_controller = hklGenController(self.widget.pg,self.mca,self.plotController,self.roi_controller)
        
        
        self.controllers_initialized = True

        self.widget.menu_items_set_enabled(True)
        
        return 0
        
    def closeEvent(self, QCloseEvent, *event):
        self.app.closeAllWindows()

    ########################################################################################
    ########################################################################################

    

    def openDetector(self, *args, **kwargs):
        text = ''
        ok = False
        if 'detector' in kwargs:
            text = kwargs['detector']
            if len(text):
                ok = True
        else:
            # initialize epics mca
            detector = self.defaults_options.detector
            text, ok = QInputDialog.getText(self.widget, 'EPICS MCA', 'Enter MCA PV name: ', text=detector)
        
        if ok:
            mcaTemp = self.mca 
            status = self.initMCA('epics',text)
            if status == 0:
                if self.controllers_initialized == False:
                    status = self.initControllers()
                if status == 0:
                    self.data_updated()
                    acquiring = self.mca.get_acquire_status()
                    self.mca.dataAcquired.signal.connect(self.dataReceivedEpics)
                    self.mca.acq_stopped.signal.connect(self.file_save_controller.acq_stopped)
                    if acquiring == 1:
                        self.mca.acqOn()
                    elif acquiring == 0:
                        self.mca.acqOff()
                    self.update_titlebar()
                    self.widget.live_view_btn.setEnabled(True)
                    self.widget.live_view_btn.setChecked(True)
                    self.defaults_options.detector = text
                    try:
                        mcaUtil.save_defaults_settings(self.defaults_options)
                    except:
                        pass
            else:
                self.mca = mcaTemp
                mcaUtil.displayErrorMessage( 'init')

    def dataReceivedEpics(self ):
        self.data_updated()

  

    ########################################################################################
    ########################################################################################

    def update_titlebar(self):
        name = self.mca.name
        if name != '':
            name += ' - '
        self.widget.setWindowTitle(name + u'hpMCA')

    def data_updated(self):
        
        self.plotController.update_plot_data() 
        
        self.plotController.roi_controller.data_updated()  #this will in turn trigger updateViews() 
        environment = self.mca.environment
        self.environment_controller.set_environment(environment)
        self.update_titlebar()
        elapsed = self.mca.get_elapsed()[0]
        self.widget.lblLiveTime.setText("%0.2f" %(elapsed.live_time))
        self.widget.lblRealTime.setText("%0.2f" %(elapsed.real_time))
        dx_type = self.mca.dx_type
        if self.dx_type != dx_type:
            self.set_dx_type(dx_type)
        self.phase_controller.pattern_updated()
            

    def set_dx_type(self, dx_type):
        self.dx_type = dx_type
        self.setHorzScaleBtnsEnabled(self.dx_type)
        if dx_type == 'edx':
            self.widget.radioE.setChecked(True)
            self.phase_controller.phase_widget.set_edx()
            self.widget.actionManualWavelength.setEnabled(False)
            self.widget.actionManualTth.setEnabled(True)
            self.widget.actionCalibrate_energy.setEnabled(True)
            self.widget.actionCalibrate_2theta.setEnabled(True)
            #old_tth = self.phase_controller .phase_widget.tth_lbl.text()
        if dx_type == 'adx':
            self.widget.radiotth.setChecked(True)
            self.phase_controller.phase_widget.set_adx()
            self.widget.actionManualWavelength.setEnabled(True)
            self.widget.actionManualTth.setEnabled(False)
            self.widget.actionCalibrate_energy.setEnabled(False)
            self.widget.actionCalibrate_2theta.setEnabled(False)
            self.phase_controller.phase_widget.wavelength_lbl.setValue(self.mca.calibration[0].wavelength)

    def envs_updated_callback(self, envs):
        
        pass

    def xrf_updated(self,text):
        self.blockSignals(True)
        self.widget.lineEdit_2.setText(text)
        self.blockSignals(False)
    
    ########################################################################################
    ########################################################################################

    def file_view_btn_callback(self, *args):
        if self.fileMCAholder != None:
        
            self.set_file_mca(self.fileMCAholder)
            self.refresh_controllers_mca()
            self.data_updated()

        #pass
    def live_view_btn_callback(self, *args):
        detector = self.defaults_options.detector
        if len(detector):
            self.openDetector(detector=detector)
            self.refresh_controllers_mca()
            self.data_updated()
        #pass
        

    def overlay_module(self):
        if self.mca != None:
            self.overlay_controller.showWidget()

    def calibrate_energy_module(self):
        if self.mca != None:
            self.ce = mcaCalibrateEnergy(self.mca)
            if self.ce.nrois < 2:
                mcaUtil.displayErrorMessage( 'calroi')
                self.ce.destroy()
            else:
                self.ce.raise_widget()
    
    def calibrate_tth_module(self):
        if self.mca != None:
            phase=self.working_directories.phase
            data_label = self.plotController.get_data_label()
            self.ctth = mcaCalibrate2theta(self.mca, jcpds_directory=phase, data_label=data_label)
            if self.ctth.nrois < 1:
                mcaUtil.displayErrorMessage( 'calroi')
                self.ctth.destroy()
            else:
                self.ctth.raise_widget()
    
    def jcpds_module(self):
        if self.mca !=None:
            self.phase_controller.show_view()
    
    def roi_module(self):
        if self.mca !=None:
            self.roi_controller.show_view()

    '''def lock_rois_btn_callback(self, locked):
        if locked:
            rois = copy.deepcopy(self.mca.get_rois()[0])
            
        else:
            rois = []
        self.file_save_controller.persistent_rois = rois'''
            
    def fluorescence_module(self):
        if self.mca !=None:
            self.fluorescence_controller.show()

    def roi_updated_signal_callback(self, *args, **kwargs):
        if self.lattice_refinement_controller.active and self.mca !=None:
            
            rois = self.mca.get_rois()[0]
            phases = self.phase_controller.get_phases()
            
            self.lattice_refinement_controller.set_jcpds_directory(self.working_directories.phase)
            self.lattice_refinement_controller.set_mca(self.mca)
            self.lattice_refinement_controller.set_reflections_and_phases(rois,phases)
            autoprocess = self.lattice_refinement_controller.widget.auto_fit.isChecked()
            if autoprocess:
                self.lattice_refinement_controller.update_phases()


    def lattice_refinement_module(self):
        if self.mca !=None:
            rois = self.mca.get_rois()[0]
            phases = self.phase_controller.get_phases()
            
            self.lattice_refinement_controller.set_jcpds_directory(self.working_directories.phase)
            self.lattice_refinement_controller.set_mca(self.mca)
            self.lattice_refinement_controller.set_reflections_and_phases(rois,phases)
            self.lattice_refinement_controller.show_view()

    def environment_module(self):
        if self.mca !=None:
            environment = self.mca.environment
            self.environment_controller.set_environment(environment)
            self.environment_controller.show_view()

    def multi_spectra_module(self):
        self.multiple_datasets_controller.show_view()

    def file_changed_signal_callback(self, fname):
       
        self.file_save_controller.openFile(filename=fname)

    def multispectral_channel_changed_callback(self, channel):
        self.plotController.mouseCursor_non_signalling(channel)

    def hklGen_module(self):
        self.hlkgen_controller.show_view()
        

    ########################################################################################
    ########################################################################################


    def roi_selection_updated(self, text):
        self.widget.lineROI.setText(text)

    def xrf_action(self, action):
        if self.mca != None:
            if action == 'next':
                self.fluorescence_controller.navigate_btn_click_callback('next')
            elif action == 'prev':
                self.fluorescence_controller.navigate_btn_click_callback('prev')
            else: 
                pass

    def xrf_search(self, query):
        if self.mca != None:
            self.fluorescence_controller.search_by_symbol(query)

    ########################################################################################
    ########################################################################################

    def HorzScaleRadioToggle(self,b):
        if b.isChecked() == True:
            if self.widget.radioE.isChecked() == True:
                horzScale = 'E'
            elif self.widget.radioq.isChecked() == True:
                horzScale = 'q'
            elif self.widget.radioChannel.isChecked() == True:
                horzScale = 'Channel'
            elif self.widget.radiod.isChecked() == True:
                horzScale = 'd'
            elif self.widget.radiotth.isChecked() == True:
                horzScale = '2 theta'
            self.set_unit(horzScale)

    def setHorzScaleBtnsEnabled(self, preset = 'edx'):
        scales = ['Channel']
        if preset == 'edx':
            scales =['E','q','d','Channel']   
        elif preset == 'adx':
            scales =['2 theta','q','d','Channel']   
        self.widget.set_scales_enabled_states(scales)
        

    def set_unit(self,unit):
            self.unit = unit
            if self.mca != None:
                self.plotController.set_unit(unit)

    def zoomPan(self, zoom):
        if zoom: setting = 1
        else: setting = 0
        self.setPlotMouseMode(setting)

    def setPlotMouseMode(self, mode):
        pg = self.widget.pg
        pg.setPlotMouseMode(mode)
        
    def setPlotLogMode(self, mode):
        if self.plotController != None:
            self.plotController.setLogMode([False, mode])
            self.overlay_controller.update_log_scale()
        pg = self.widget.pg   
        pg.set_log_mode(False, mode)
        
    def LogScaleSet(self):
        log_scale = self.widget.radioLog.isChecked()
        self.widget.baseline_subtract.setEnabled( log_scale==False)
        if log_scale:
            if self.widget.baseline_subtract.isChecked():
                self.widget.baseline_subtract.setChecked(False)
                self.baseline_subtract_callback()
        self.setPlotLogMode(log_scale)

    def baseline_subtract_callback(self):
        if self.plotController != None:

            baseline_state = self.widget.baseline_subtract.isChecked()
            self.mca.baseline_state = baseline_state
            self.plotController.updated_baseline_state()

        
    ########################################################################################
    ########################################################################################

    def mouseMoved(self, input):
        text =self.format_cursor_label(input)
        self.widget.indexLabel.setText(text)
        

    def mouseCursor(self, input):
        text =self.format_cursor_label(input)
        self.widget.cursorLabel.setText(text)
        self.multiple_datasets_controller.set_channel_cursor(input)

    def format_cursor_label(self, input):
        if len(input):
            hName = input['hName']
            hValue= input['hValue']
            hUnit = input['hUnit']
            vName = input['vName']
            vValue= input['vValue']
            text = "%s = %0.3f%s, %sI(%s) = %.1f" \
                               % (hName,hValue,hUnit," ",vName,vValue)
        else:
            text = ''
        return text

    ########################################################################################
    ########################################################################################    

    def setStyle(self, Style):
        
        if Style==1:
            WStyle = 'plastique'
            file = open(os.path.join(self.style_path, "stylesheet.qss"))
            stylesheet = file.read()
            self.app.setStyleSheet(stylesheet)
            file.close()
            self.app.setStyle(WStyle)
        else:
            WStyle = "windowsvista"
            self.app.setStyleSheet(" ")
            #self.app.setPalette(self.win_palette)
            self.app.setStyle(WStyle)
      
        
    ########################################################################################
    ########################################################################################
