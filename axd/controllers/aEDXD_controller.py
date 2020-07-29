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


import os.path, sys
from PyQt5 import uic, QtWidgets,QtCore, QtGui
from  PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QWidget, QLabel
from PyQt5.QtCore import QObject, pyqtSignal, Qt
import numpy as np
from functools import partial
import json
import copy
from hpm.widgets.CustomWidgets import FlatButton, DoubleSpinBoxAlignRight, VerticalSpacerItem, NoRectDelegate, \
    HorizontalSpacerItem, ListTableWidget, VerticalLine, DoubleMultiplySpinBoxAlignRight
from hpm.widgets.PltWidget import plotWindow
from pathlib import Path
from utilities.HelperModule import calculate_color
from numpy import arange
from PyQt5.QtWidgets import QMainWindow
from utilities.HelperModule import getInterpolatedCounts
from hpm.widgets.UtilityWidgets import save_file_dialog, open_file_dialog, open_files_dialog
from axd.models.aEDXD_model import aEDXD_model
from axd.widgets.aEDXD_widget import aEDXDWidget
from axd.controllers.aEDXD_config_controller import aEDXDConfigController

from .. import style_path

############################################################

class aEDXDController(QObject):
    def __init__(self, app, theme):
        super().__init__()
        self.app = app
        self.style_path = style_path

        self.model = aEDXD_model()
        self.display_window = aEDXDWidget(app)
        self.progress_bar = self.display_window.progress_bar
        self.config_controller = aEDXDConfigController(self.model,self.display_window)
        self.create_connections()
        self.display_window.raise_widget()
        self.progress_bar.setValue(0)
        self.setStyle(theme)

    def closeEvent(self, QCloseEvent, *event):
        self.app.closeAllWindows()

    def raise_widget(self):
        self.show()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
        self.raise_()  

    def create_connections(self):
        self.display_window.file_op_act.triggered.connect(self.load_project)
        self.display_window.file_save_act.triggered.connect(self.save_project)
        self.display_window.file_save_hdf5_act.triggered.connect(self.save_hdf5)
        self.display_window.file_exp_sf_act.triggered.connect(self.save_sq)
        self.display_window.file_exp_pdf_act.triggered.connect(self.save_pdf)
        self.display_window.file_exp_data_act.triggered.connect(self.save_data)
        self.display_window.file_exp_sf_inv_act.triggered.connect(self.save_sf_inverse)

        self.display_window.tools_files_act.triggered.connect(self.show_files)
        self.display_window.tools_peaks_act.triggered.connect(self.show_rois)
        self.display_window.tools_atoms_act.triggered.connect(self.show_atoms)
        self.display_window.opts_proc_act.triggered.connect(self.show_options)
        self.display_window.opts_sq_act.triggered.connect(self.show_sq_options)
        self.display_window.opts_gr_act.triggered.connect(self.show_gr_options)
        
        self.model.primary_beam_updated.connect(self.primary_beam_updated)
        self.model.structure_factor_updated.connect(self.structure_factor_updated)
        self.model.G_r_updated.connect(self.G_r_updated)
        self.model.Sf_filtered_updated.connect(self.sf_filtered_updated)
        
        self.config_controller.params_changed_signal.connect(self.spectra_changed)
    
    def save_data(self):

        key = 'outputsavedirectory'
        if key in self.model.params:
            od = self.model.params[key]
        else: od = None
        filename = save_file_dialog(self.display_window,'Export data files',od)
        if filename:
            od = os.path.dirname(filename)
            self.model.params[key] = od
            fc = self.config_controller.files_controller
            fc.save_file(filename)

    def save_sq(self):
        key = 'outputsavedirectory'
        if key in self.model.params:
            od = self.model.params[key]
        else: od = None
        filename = save_file_dialog(self.display_window,'Export S(q)',od)
        if filename:
            od = os.path.dirname(filename)
            self.model.params[key] = od
            sf = self.model.structure_factor
            sf.save_structure_factor(filename)

    def save_pdf(self):
        key = 'outputsavedirectory'
        if key in self.model.params:
            od = self.model.params[key]
        else: od = None
        filename = save_file_dialog(self.display_window,'Export G(r)',od)
        if filename:
            od = os.path.dirname(filename)
            self.model.params[key] = od
            pdf = self.model.pdf_object
            pdf.save_pdf(filename)

    def save_sf_inverse(self):
        key = 'outputsavedirectory'
        if key in self.model.params:
            od = self.model.params[key]
        else: od = None
        filename = save_file_dialog(self.display_window,'Export the inverse Fourier filtered S(q)',od)
        if filename:
            od = os.path.dirname(filename)
            self.model.params[key] = od
            sf = self.model.pdf_inverse_object
            sf.save_sf_inverse(filename)

    def primary_beam_updated (self):
        self.disp_primary_beam()

    def structure_factor_updated (self):
        self.disp_sq()

    def G_r_updated (self):
        self.disp_pdf()

    def sf_filtered_updated(self):
        self.disp_sq_filtered()

    def save_project(self):
        filename='saved_config_test.cfg'
        self.config_controller.save_config_file()

    def save_hdf5(self):
        filename='saved_config_test.cfg'
        self.config_controller.save_hdf5()

    def load_project(self):
        #self.model.reset_model()
        config_file = 'saved_config_test.cfg'
        self.config_controller.load_config_file()
        
        
    def spectra_changed(self):
        if self.model.isCongigured():
            self.progress_bar.setValue(0)
            self.model.primary()
            self.progress_bar.setValue(50)
            self.model.sf_normalization()
            self.progress_bar.setValue(75)
            self.model.pdf()
            self.progress_bar.setValue(90)
            self.model.pdf_inverse()
            self.progress_bar.setValue(100)
        else:
            self.clear_plots()

    def clear_plots(self):
        self.display_window.primary_beam_widget.fig.clear()
        self.display_window.sq_widget.fig.clear()
        self.display_window.pdf_widget.fig.clear()
        self.display_window.inverse_widget.fig.clear()
    
    def disp_primary_beam(self):
        self.display_window.primary_beam_widget.fig.clear()
        
        if self.model.primary_beam.done == True:
            #self.display_window.tabWidget.setCurrentIndex(2)
            # plot the primary beam fit
            if len(self.model.ttharray):
                pb = self.model.primary_beam
                x = pb.params['x']
                y = pb.params['y']
                tth = self.model.ttharray[-1]
                color = self.config_controller.files_controller.colors[tth]
                self.display_window.primary_beam_widget.fig.add_scatter_plot(x,y,color = color,opacity=100)
                pbx=pb.out_params['primary_beam_x']
                pby=pb.out_params['primary_beam_y']
                self.display_window.primary_beam_widget.fig.add_line_plot(pbx,pby,(255,0,0),3)
                self.display_window.primary_beam_widget.setText(pb.note,1)
        
    def disp_sq(self):
        self.display_window.sq_widget.fig.clear()
        if self.model.structure_factor.done == True:
            #self.display_window.tabWidget.setCurrentIndex(3)
            if len(self.model.ttharray):
                sf = self.model.structure_factor
                S_q = sf.out_params['S_q_fragments']
                colors = self.config_controller.files_controller.sq_colors
                for i in range(len(S_q)):
                    color = colors[i]
                    self.display_window.sq_widget.fig.add_scatter_plot(S_q[i][0],S_q[i][1],color,100)
                    #plt.errorbar(S_q[i][0],S_q[i][1],yerr=S_q[i][2],fmt='.',capsize=1.0)
                self.display_window.sq_widget.fig.add_line_plot(sf.out_params['q_even'],sf.out_params['sq_even'],Width=2)

    def disp_pdf(self):
        #self.display_window.tabWidget.setCurrentIndex(4)
        self.display_window.pdf_widget.fig.clear()
        if len(self.model.ttharray):
            pdf = self.model.pdf_object
            r = pdf.out_params['r']
            gr = pdf.out_params['gr']
            self.display_window.pdf_widget.fig.add_line_plot(r,gr,Width=2)
            
    def disp_sq_filtered(self):
        #self.display_window.tabWidget.setCurrentIndex(5)
        self.display_window.inverse_widget.fig.clear()
        if len(self.model.ttharray):
            sf  = self.model.pdf_inverse_object
            r = sf.out_params['r_f']
            gr = sf.out_params['gr_f']
            self.display_window.pdf_widget.fig.add_line_plot(r,gr,color=(255,0,0),Width=1)
            
            qq = sf.params['qq']
            sq = sf.params['sq']
            self.display_window.inverse_widget.fig.add_line_plot(qq,sq,Width=2)
            q_inv = sf.out_params['q_inv']
            sq_inv = sf.out_params['sq_inv']
            self.display_window.inverse_widget.fig.add_line_plot(q_inv,sq_inv,color = (255,0,0),Width=1)
        
    def show_display(self):
        self.display_window.raise_widget()
    
    #config
    def show_atoms(self):
        self.config_controller.show_atoms()

        
    def show_options(self):
        self.config_controller.show_options()

    def show_gr_options(self):
        self.config_controller.show_gr_options()  

    def show_sq_options(self):
        self.config_controller.show_sq_options() 

    def show_files(self):
        self.config_controller.show_files()

    def show_rois(self):
        self.config_controller.show_rois()

    def setStyle(self, Style):
        print('style:  ' + str(Style))
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