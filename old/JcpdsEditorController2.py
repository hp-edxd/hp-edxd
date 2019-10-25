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



from copy import deepcopy
from functools import partial

import numpy as np
from qtpy import QtWidgets, QtCore, QtGui

from ....widgets.UtilityWidgets import save_file_dialog
from ....widgets.integration.JcpdsEditorWidget import JcpdsEditorWidget

# imports for type hinting in PyCharm -- DO NOT DELETE
from ....model.util.jcpds import jcpds, jcpds_reflection
from ....model.DioptasModel import DioptasModel
from ....widgets.integration import IntegrationWidget


class JcpdsEditorController(QtCore.QObject):
    """
    JcpdsEditorController handles all the signals and changes associated with Jcpds editor widget
    """
    canceled_editor = QtCore.Signal(jcpds)

    # lattice_param_changed = QtCore.Signal()
    # eos_param_changed = QtCore.Signal()
    #
    # reflection_line_edited = QtCore.Signal()
    # reflection_line_removed = QtCore.Signal(int)
    # reflection_line_cleared = QtCore.Signal()

    def __init__(self, integration_widget, dioptas_model=None, jcpds_phase=None):
        """
        :param integration_widget: Reference to an IntegrationWidget
        :param dioptas_model: Reference to DioptasModel object
        :param jcpds_phase: Reference to JcpdsPhase object

        :type integration_widget: IntegrationWidget
        :type dioptas_model: DioptasModel
        :type jcpds_phase: jcpds
        """
        super(JcpdsEditorController, self).__init__()
        self.integration_widget = integration_widget
        self.jcpds_widget = JcpdsEditorWidget(integration_widget)
        self.phase_widget = self.integration_widget.phase_widget
        self.model = dioptas_model
        self.phase_model = self.model.phase_model
        self.create_connections()

        self.previous_header_item_index_sorted = None
        self.active = False
        self.phase_ind = -1

        if jcpds_phase is not None:
            self.show_phase(jcpds_phase)

    def show_phase(self, jcpds_phase=None, wavelength=None):
        self.start_jcpds_phase = deepcopy(jcpds_phase)
        self.jcpds_phase = jcpds_phase
        self.phase_ind = self.phase_model.phases.index(jcpds_phase)
        if wavelength is None:
            if self.model.calibration_model is not None:
                wavelength = self.model.calibration_model.wavelength * 1e10
        self.jcpds_widget.show_jcpds(jcpds_phase, wavelength)

    def create_connections(self):
        # Phase Widget Signals
        self.phase_widget.edit_btn.clicked.connect(self.edit_btn_callback)
        self.phase_widget.phase_tw.currentCellChanged.connect(self.phase_selection_changed)

        # Information fields
        self.jcpds_widget.comments_txt.editingFinished.connect(self.comments_changed)
        self.jcpds_widget.symmetry_cb.currentIndexChanged.connect(self.symmetry_changed)
        #
        # Lattice Parameter fields
        self.jcpds_widget.lattice_a_sb.valueChanged.connect(partial(self.param_sb_changed,
                                                                    widget=self.jcpds_widget.lattice_a_sb,
                                                                    param='a0'))
        self.jcpds_widget.lattice_b_sb.valueChanged.connect(partial(self.param_sb_changed,
                                                                    widget=self.jcpds_widget.lattice_b_sb,
                                                                    param='b0'))
        self.jcpds_widget.lattice_c_sb.valueChanged.connect(partial(self.param_sb_changed,
                                                                    widget=self.jcpds_widget.lattice_c_sb,
                                                                    param='c0'))

        self.jcpds_widget.lattice_ab_sb.valueChanged.connect(self.lattice_ab_changed)
        self.jcpds_widget.lattice_ca_sb.valueChanged.connect(self.lattice_ca_changed)
        self.jcpds_widget.lattice_cb_sb.valueChanged.connect(self.lattice_cb_changed)

        self.jcpds_widget.lattice_alpha_sb.valueChanged.connect(partial(self.param_sb_changed,
                                                                        widget=self.jcpds_widget.lattice_alpha_sb,
                                                                        param='alpha0'))
        self.jcpds_widget.lattice_beta_sb.valueChanged.connect(partial(self.param_sb_changed,
                                                                       widget=self.jcpds_widget.lattice_beta_sb,
                                                                       param='beta0'))
        self.jcpds_widget.lattice_gamma_sb.valueChanged.connect(partial(self.param_sb_changed,
                                                                        widget=self.jcpds_widget.lattice_gamma_sb,
                                                                        param='gamma0'))

        self.jcpds_widget.lattice_length_step_txt.editingFinished.connect(self.lattice_length_step_changed)
        self.jcpds_widget.lattice_angle_step_txt.editingFinished.connect(self.lattice_angle_step_changed)
        self.jcpds_widget.lattice_ratio_step_txt.editingFinished.connect(self.lattice_ratio_step_changed)

        # Equation of state fields
        self.jcpds_widget.eos_K_txt.editingFinished.connect(partial(self.param_txt_changed,
                                                                    widget=self.jcpds_widget.eos_K_txt,
                                                                    param='k0'))
        self.jcpds_widget.eos_Kp_txt.editingFinished.connect(partial(self.param_txt_changed,
                                                                     widget=self.jcpds_widget.eos_Kp_txt,
                                                                     param='k0p0'))
        self.jcpds_widget.eos_alphaT_txt.editingFinished.connect(partial(self.param_txt_changed,
                                                                         widget=self.jcpds_widget.eos_alphaT_txt,
                                                                         param='alpha_t0'))
        self.jcpds_widget.eos_dalphadT_txt.editingFinished.connect(partial(self.param_txt_changed,
                                                                           widget=self.jcpds_widget.eos_dalphadT_txt,
                                                                           param='d_alpha_dt'))
        self.jcpds_widget.eos_dKdT_txt.editingFinished.connect(partial(self.param_txt_changed,
                                                                       widget=self.jcpds_widget.eos_dKdT_txt,
                                                                       param='dk0dt'))
        self.jcpds_widget.eos_dKpdT_txt.editingFinished.connect(partial(self.param_txt_changed,
                                                                        widget=self.jcpds_widget.eos_dKpdT_txt,
                                                                        param='dk0pdt'))

        # Phase Model signals
        self.phase_model.phase_changed.connect(self.phase_changed)
        self.phase_model.reflection_added.connect(self.update_reflection_table)
        self.phase_model.reflection_deleted.connect(self.update_reflection_table)
        
        # Reflections Controls
        self.jcpds_widget.reflections_add_btn.clicked.connect(self.reflections_add_btn_click)
        self.jcpds_widget.reflections_delete_btn.clicked.connect(self.reflections_delete_btn_click)
        self.jcpds_widget.reflections_clear_btn.clicked.connect(self.reflections_clear_btn_click)
        self.jcpds_widget.reflection_table_model.reflection_edited.connect(self.reflection_table_changed)

        # Table Widgets events
        self.jcpds_widget.reflection_table_view.keyPressEvent = self.reflection_table_key_pressed
        self.jcpds_widget.reflection_table_view.verticalScrollBar().valueChanged.connect(self.reflection_table_scrolled)
        self.jcpds_widget.reflection_table_view.horizontalHeader().sectionClicked.connect(
            self.horizontal_header_clicked)
        #
        # Button fields
        self.jcpds_widget.reload_file_btn.clicked.connect(self.reload_file_btn_clicked)
        self.jcpds_widget.save_as_btn.clicked.connect(self.save_as_btn_clicked)
        #
        # # Closing and opening
        self.jcpds_widget.closeEvent = self.view_closed

    def edit_btn_callback(self):
        selected_row = self.phase_widget.get_selected_phase_row()
        if selected_row >= 0:
            self.show_phase(self.model.phase_model.phases[selected_row])
            self.show_view()

    def phase_selection_changed(self, row, *_):
        if self.active:
            self.show_phase(self.model.phase_model.phases[row])

    def phase_changed(self, ind):
        if self.active and self.phase_ind == ind:
            self.jcpds_widget.show_jcpds(self.phase_model.phases[ind],
                                         wavelength=self.model.calibration_model.wavelength * 1e10)

    def update_filename(self):
        self.jcpds_widget.filename_txt.setText(self.jcpds_phase.filename)

    def comments_changed(self):
        self.jcpds_phase.params['comments'][0] = str(self.jcpds_widget.comments_txt.text())

    def symmetry_changed(self):
        self.phase_model.set_param(self.phase_ind, 'symmetry',
                                   str(self.jcpds_widget.symmetry_cb.currentText()).upper())

    def param_sb_changed(self, widget, param):
        self.phase_model.set_param(self.phase_ind, param, widget.value())

    def param_txt_changed(self, widget, param):
        self.phase_model.set_param(self.phase_ind, param, float(widget.text()))

    def lattice_ab_changed(self):
        ab_ratio = float(self.jcpds_widget.lattice_ab_sb.value())
        self.phase_model.set_param(self.phase_ind, 'a0',
                                   self.jcpds_phase.params['b0'] * ab_ratio)

    def lattice_ca_changed(self):
        ca_ratio = float(self.jcpds_widget.lattice_ca_sb.value())
        self.phase_model.set_param(self.phase_ind, 'c0',
                                   self.jcpds_phase.params['a0'] * ca_ratio)

    def lattice_cb_changed(self):
        cb_ratio = float(self.jcpds_widget.lattice_cb_sb.value())
        self.phase_model.set_param(self.phase_ind, 'c0',
                                   self.jcpds_phase.params['b0'] * cb_ratio)

    def lattice_length_step_changed(self):
        value = float(str(self.jcpds_widget.lattice_length_step_txt.text()))
        self.jcpds_widget.lattice_a_sb.setSingleStep(value)
        self.jcpds_widget.lattice_b_sb.setSingleStep(value)
        self.jcpds_widget.lattice_c_sb.setSingleStep(value)

    def lattice_angle_step_changed(self):
        value = float(str(self.jcpds_widget.lattice_angle_step_txt.text()))
        self.jcpds_widget.lattice_alpha_sb.setSingleStep(value)
        self.jcpds_widget.lattice_beta_sb.setSingleStep(value)
        self.jcpds_widget.lattice_gamma_sb.setSingleStep(value)

    def lattice_ratio_step_changed(self):
        value = float(str(self.jcpds_widget.lattice_ratio_step_txt.text()))
        self.jcpds_widget.lattice_ab_sb.setSingleStep(value)
        self.jcpds_widget.lattice_ca_sb.setSingleStep(value)
        self.jcpds_widget.lattice_cb_sb.setSingleStep(value)

    def reflections_delete_btn_click(self):
        rows = self.jcpds_widget.get_selected_reflections()
        self.phase_model.delete_multiple_reflections(self.phase_ind, rows)
        if self.jcpds_widget.reflection_table_model.rowCount() >= min(rows) + 1:
            self.jcpds_widget.reflection_table_view.selectRow(min(rows))
        else:
            self.jcpds_widget.reflection_table_view.selectRow(
                self.jcpds_widget.reflection_table_model.rowCount() - 1)

    def reflections_add_btn_click(self):
        self.phase_model.add_reflection(self.phase_ind)
        self.jcpds_widget.reflection_table_view.selectRow(self.jcpds_widget.reflection_table_model.rowCount() - 1)

    def reflections_clear_btn_click(self):
        self.phase_model.clear_reflections(self.phase_ind)

    def reflection_table_changed(self, row, column, value):
        if value != '':
            value = float(value)
            reflection = self.phase_model.phases[self.phase_ind].reflections[row]
            if column == 0:  # h
                reflection.h = value
            elif column == 1:  # k
                reflection.k = value
            elif column == 2:  # l
                reflection.l = value
            elif column == 3:  # intensity
                reflection.intensity = value
            self.phase_model.update_reflection(self.phase_ind, row, reflection)
            self.jcpds_widget.reflection_table_model.update_reflection_data(
                self.phase_model.phases[self.phase_ind].reflections)

    def update_reflection_table(self, phase_ind, *_):
        if phase_ind != self.phase_ind:
            return
        self.jcpds_widget.reflection_table_model.update_reflection_data(self.phase_model.phases[phase_ind].reflections)

    def reflection_table_key_pressed(self, key_press_event):
        if key_press_event == QtGui.QKeySequence.Copy:
            res = ''
            selection_ranges = self.jcpds_widget.reflection_table_view.selectedRanges()
            for range_ind in range(len(selection_ranges)):
                if range_ind > 0:
                    res += '\n'
                for row_ind in range(int(selection_ranges[range_ind].rowCount())):
                    if row_ind > 0:
                        res += '\n'
                    for col_ind in range(selection_ranges[range_ind].columnCount()):
                        if col_ind > 0:
                            res += '\t'
                        res += str(self.jcpds_widget.reflection_table_view.item(
                            selection_ranges[range_ind].topRow() + row_ind,
                            selection_ranges[range_ind].leftColumn() + col_ind).text())
            QtWidgets.QApplication.clipboard().setText(res)
        elif key_press_event == QtGui.QKeySequence.SelectAll:
            self.jcpds_widget.reflection_table_view.selectAll()

    def reflection_table_scrolled(self):
        self.jcpds_widget.reflection_table_view.resizeColumnsToContents()

    def horizontal_header_clicked(self, ind):
        if self.previous_header_item_index_sorted == ind:
            reversed_toggle = True
        else:
            reversed_toggle = False

        if ind == 0:
            self.jcpds_phase.sort_reflections_by_h(reversed_toggle)
        elif ind == 1:
            self.jcpds_phase.sort_reflections_by_k(reversed_toggle)
        elif ind == 2:
            self.jcpds_phase.sort_reflections_by_l(reversed_toggle)
        elif ind == 3:
            self.jcpds_phase.sort_reflections_by_intensity(reversed_toggle)
        elif ind == 4 or ind == 6:
            self.jcpds_phase.sort_reflections_by_d(reversed_toggle)
        elif ind == 5 or ind == 7:
            self.jcpds_phase.sort_reflections_by_d(not reversed_toggle)

        self.jcpds_widget.show_jcpds(self.jcpds_phase, wavelength=self.model.calibration_model.wavelength * 1e10)
        self.jcpds_widget.reflection_table_view.resizeColumnsToContents()

        if self.previous_header_item_index_sorted == ind:
            self.previous_header_item_index_sorted = None
        else:
            self.previous_header_item_index_sorted = ind

    def save_as_btn_clicked(self, filename=False):
        if filename is False:
            filename = save_file_dialog(self.jcpds_widget, "Save JCPDS phase.",
                                        self.model.working_directories['phase'],
                                        ('JCPDS Phase (*.jcpds);;Export Table (*.txt)'))

            if filename != '':
                if filename.endswith('.jcpds'):
                    self.phase_model.save_phase_as(self.phase_ind, filename)
                elif filename.endswith('.txt'):
                    self.export_table_data(filename)
            self.show_phase(self.jcpds_phase)

    def export_table_data(self, filename):
        fp = open(filename, 'w', encoding='utf-8')
        for col in range(self.jcpds_widget.reflection_table_view.columnCount()):
            fp.write(self.jcpds_widget.reflection_table_view.horizontalHeaderItem(col).text() + '\t')
        fp.write('\n')
        for row in range(self.jcpds_widget.reflection_table_view.rowCount()):
            line = ''
            for col in range(self.jcpds_widget.reflection_table_view.columnCount()):
                line = line + self.jcpds_widget.reflection_table_view.item(row, col).text() + '\t'
            line = line + '\n'
            fp.write(line)
        fp.close()

    def reload_file_btn_clicked(self):
        self.phase_model.reload(self.phase_ind)

    def show_view(self):
        self.active = True
        self.jcpds_widget.raise_widget()

    def close_view(self):
        self.active = False
        self.jcpds_widget.close()

    def view_closed(self, _):
        self.close_view()
