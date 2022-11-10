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


from ast import Return
import imp
import re
import pyqtgraph as pg
import numpy as np
from numpy.core.records import array
from pyqtgraph.graphicsItems.PlotDataItem import dataType
from scipy import interpolate
from math import sqrt, sin, pi
import utilities.centroid as centroid
import copy
import json
import time
from hpm.models.mcareader import McaReader
from hpm.widgets.UtilityWidgets import xyPatternParametersDialog
import os
import utilities.CARSMath as CARSMath
from utilities.filt import spectra_baseline
from .mcaComponents import *
from .mcareaderGeStrip import *

from epics import caput, caget, PV

class MCA():  # 
    

    """ Device-independent MultiChannel Analyzer (MCA) class """
    def __init__(self, file=None, file_settings = None, *args, **filekw):
        """
        Creates new Mca object.  The data are initially all zeros, and the number
        of channels is 4000.
        
        Keywords:
            file:
                Name of a file to read into the new Mca object with read_file()
                
        Example:
            m = Mca('my_spectrum.dat')
        """
        
        self.dx_type = 'edx'

        self.name = ''
        self.file_name = ''
        self.file_saved_timestamp = None
        self.file_settings = file_settings # not used in this based class, used in device dependent class

        self.max_rois = 32
        self.n_detectors = 1
        self.nchans = 4000
        self.data = [np.ones(self.nchans)]
        self.data_processed = np.ones(self.nchans)
        self.baseline = [np.ones(self.nchans)]
        self.baseline_state = 0
        
        self.rois = [[]]
        self.rois_from_file = [[]]
        self.rois_from_det = [[]]
        self.auto_process_rois = True

        self.calibration = [McaCalibration()]
        self.calibration_processed = McaCalibration()
        self.elapsed = [McaElapsed()]
        self.presets = McaPresets()
        self.environment = []

        self.wavelength = None  # persistent wavelength for axd mode useful when loading files without wavelength, e.g. *.chi
        #if (file != None):
        #    self.read_file(file, **filekw)
        self.fileIO = mcaFileIO()

        

    ########################################################################
    def get_calibration(self):
        """ Returns the Mca calibration, as an McaCalibration object """
        return self.calibration

    ########################################################################
    def set_calibration(self, calibration, det = 0):
        """
        Sets the Mca calibration.
        
        Inputs:
            calibration:
                An McaCalibration object
        """
        self.calibration[det] = calibration

    ########################################################################
    def get_presets(self):
        """ Returns the Mca presets, as an McaCPresets object """
        return self.presets

    ########################################################################
    def set_presets(self, presets):
        """
        Sets the Mca presets.
        
        Inputs:
            presets:
                An McaPresets object
        """
        self.presets = presets

    ########################################################################
    def get_elapsed(self):
        """ Returns the Mca elapsed parameters, as an McaElapsed object """
        return self.elapsed

    ########################################################################
    def set_elapsed(self, elapsed):
        """
        Sets the Mca elapsed parameters.
        
        Inputs:
            elapsed:
                An McaElapsed object
        """
        self.elapsed = copy.copy(elapsed)

    ########################################################################
    def get_name(self):
        """ Returns the Mca name as a string """
        return self.name

    def get_name_base(self):
        name = os.path.basename(self.file_name)
        
        return name


    

    ########################################################################
    def set_name(self, name):
        """
        Sets the Mca name.
        
        Inputs:
            name:
                A string
        """
        self.name = name

    ########################################################################
    
    def get_file_rois(self, energy=0):
        """ Returns the Mca ROIS, as a list of McaROI objects """
        rois = copy.copy(self.rois_from_file)
     
        return rois 
    
    def get_det_rois(self, energy=0):
        """ Returns the Mca ROIS, as a list of McaROI objects """
        rois = copy.copy(self.rois_from_det)
       
        return rois 
    
    def get_rois(self, energy=0):
        """ Returns the Mca ROIS, as a list of McaROI objects """
        rois = copy.copy(self.rois)
      
        return rois

    def get_rois_offline(self, energy=0):
        """ Returns the Mca ROIS, as a list of McaROI objects, dont override with epics mca etc """
        
        rois = copy.copy(self.rois)
        '''
        if (energy != 0):
            for roi in rois:
                roi.left = self.calibration.channel_to_energy(roi.left)
                roi.right = self.calibration.channel_to_energy(roi.right)
        '''
        return rois

    def compute_get_rois(self):
        self.compute_rois()

        rois = copy.copy(self.rois)

    def compute_rois(self):
        for det in self.rois:
                for roi in det:
                    self.compute_roi(roi, det)

    def compute_roi(self, roi, detector=0):
        ## computes and updates the centroid/energy/fwhm of a roi
        ## ideally should be called when a new roi is added or data updated
        ## the goal is to simplify things for users of this class, centroids/energy of roi 
        ## should always be ready for the user 
        #start_time = time.time()
        

        [roi, fwhm_chan] = centroid.computeCentroid(self.data[detector], roi, 1)
        roi.fwhm = fwhm_chan
        roi.fwhm_E = (self.calibration[detector].channel_to_energy(roi.centroid + 
                                        fwhm_chan/2.) - 
                            self.calibration[detector].channel_to_energy(roi.centroid - 
                                        fwhm_chan/2.))
        roi.fwhm_q = (self.calibration[detector].channel_to_q(roi.centroid + 
                                        fwhm_chan/2.) - 
                            self.calibration[detector].channel_to_q(roi.centroid - 
                                        fwhm_chan/2.))
        roi.fwhm_d = (self.calibration[detector].channel_to_d(roi.centroid + 
                                        fwhm_chan/2.) - 
                            self.calibration[detector].channel_to_d(roi.centroid - 
                                        fwhm_chan/2.))      
        roi.fwhm_tth = (self.calibration[detector].channel_to_tth(roi.centroid + 
                                        fwhm_chan/2.) - 
                            self.calibration[detector].channel_to_tth(roi.centroid - 
                                        fwhm_chan/2.))                             

        roi.energy = self.calibration[detector].channel_to_energy(roi.centroid)
        roi.two_theta = self.calibration[detector].channel_to_tth(roi.centroid)
        roi.q = self.calibration[detector].channel_to_q(roi.centroid)
        roi.d_spacing = self.calibration[detector].channel_to_d(roi.centroid)


    ########################################################################
    def set_rois(self, rois, energy=0, detector=0, source='file'):
        """
        Sets the region-of-interest parameters for the MCA.
        The rois information is contained in an object of class McaRoi.
        This routine is not needed if the information in the McaRoi instance
        is already in channel units.  It is needed if the information in the
        .left and .right fields is in terms of energy.

        Inputs:
            rois:
                A list of objects of type McaROI
                
        Keywords:
            energy:
                Set this flag to indicate that the .left and .right fields
                of rois are in units of energy rather than channel number.
                
        Example:
            mca = Mca('mca.001')
            r1 = McaROI()
            r1.left = 5.4
            r1.right = 5.6
            r2 = McaROI()
            r2.left = 6.1
            r2.right = 6.2
            mca.set_rois([r1,r2], energy=1)
        """
        if source == 'file':
            self.rois_from_file[detector] = []
            set_rois = self.rois_from_file
        elif source == 'controller':
            self.rois[detector]  = []
            set_rois = self.rois
        elif source == 'detector':
            self.rois_from_det[detector]  = []
            set_rois = self.rois_from_det
        
        for roi in rois:
            '''if self.auto_process_rois :
                self.compute_roi(roi, 0)'''
            
            '''
            if (energy == 1):
                r.left =  self.calibration.energy_to_channel(r.left, clip=1)
                r.right = self.calibration.energy_to_channel(r.right, clip=1)
            '''
            lbl = roi.label
            if len(lbl)> 12:
                if ' ' in lbl:
                    parts = lbl.split(' ')
                    end = parts[-1]
                    end = end[:3]
                    start = parts[0]
                    start = start[:8]
                    lbl = start + ' ' +end
                else:
                    lbl = lbl[:12]
            roi.label = lbl
            set_rois[detector].append(roi)


    ########################################################################
    
    def add_roi(self, roi, energy=0, detector=0, source='file'):
        """
        This procedure adds a new region-of-interest to the MCA.

        Inputs:
            roi: An object of type mcaROI.
            
        Kyetwords:
            energy:
                Set this flag to 1 to indicate that the .left and .right 
                fields of roi are in units of energy rather than channel 
                number.
                
        Example:
            mca = Mca('mca.001')
            roi = McaROI()
            roi.left = 500
            roi.right = 600
            roi.label = 'Fe Ka'
            mca,add_roi(roi)
        """

        if source == 'file':
            
            set_rois = self.rois_from_file
        elif source == 'controller':
            set_rois = self.rois
        elif source == 'detector':
            set_rois = self.rois_from_det

        r = copy.copy(roi)
        if self.auto_process_rois :
            self.compute_roi(r, detector)
        '''
        if (energy == 1):
            r.left = self.calibration.energy_to_channel(r.left, clip=1)
            r.right = self.calibration.energy_to_channel(r.right, clip=1)
        '''
        set_rois[detector].append(r)

        # Sort ROIs.  This sorts by left channel.
        tempRois = copy.copy(set_rois[detector])
        tempRois.sort()
        
        set_rois[detector] = tempRois
        
    
    def add_rois(self, rois, energy=0, detector = 0, source ='file'):
        """
        Adds multiple new ROIs to the epicsMca.

        Inputs:
            rois:
                List of McaROI objects.
        """

        if source == 'file':
            
            set_rois = self.rois_from_file
        elif source == 'controller':
            set_rois = self.rois

        elif source == 'detector':
            set_rois = self.rois_from_det
       
        n_new_rois = len(rois)
        nrois = len(set_rois[detector])
        new_total = n_new_rois + nrois
        if new_total > self.max_rois:
            extra = new_total - self.max_rois 
            keep = n_new_rois - extra
            rois = rois[:keep]

        for roi in rois:
            r = copy.copy(roi)
            if self.auto_process_rois :
                self.compute_roi(r, detector)
            '''
            if (energy == 1):
                r.left = self.calibration.energy_to_channel(r.left, clip=1)
                r.right = self.calibration.energy_to_channel(r.right, clip=1)
            '''
            set_rois[detector].append(r)

            # Sort ROIs.  This sorts by left channel.
            tempRois = copy.copy(set_rois[detector])
            tempRois.sort()
            
            set_rois[detector] = tempRois

    def change_roi_use(self, ind, use, detector=0):
        roi = self.rois[detector][ind].use = use
            
    
    def clear_rois(self, source, detector):
        self.set_rois([], detector=detector,source=source)

    

    ########################################################################
    def get_data(self):
        """ Returns the data (counts) from the Mca """
        return self.data

    ########################################################################
    def set_data(self, data):
        """
        Copies an array of data (counts) to the Mca.

        Inputs:
            data:
                A Numeric array of data (counts).
        """
        self.data = data
        
        
        
        #if self.auto_process_rois :
        #    for det in self.rois:
        #        for roi in det:
        #            self.compute_roi(roi, det)

    ########################################################################

    def get_baseline(self):
        baselines = []
        for d in self.data:
            
            baselines.append(spectra_baseline(d, 0.04, 50, method='gust'))
       
        self.baselines = baselines
        return self.baselines

    def get_bins(self,detector=0):
        n = len(self.data[detector])
        return np.linspace(0,n-1, n) 

    

    def get_energy(self, detector):
        """
        Returns a list containing the energy of each channel in the MCA spectrum.

        Procedure:
            Simply returns mca.channel_to_energy() for each channel
            
        Example:
            from Mca import *
            mca = Mca('mca.001')
            energy = mca.get_energy()
        """
        channels = np.arange(len(self.data[detector]))
        return self.calibration[detector].channel_to_energy(channels)
    ########################################################################
    def get_roi_counts(self, background_width=1):
        """
        Returns a tuple (total, net) containing the total and net counts of
        each region-of-interest in the MCA.

        Kyetwords:
            background_width:
                Set this keyword to set the width of the background region on either
                side of the peaks when computing net counts.  The default is 1.
                
        Outputs:
            total:  The total counts in each ROI.
            net:    The net counts in each ROI.

            The dimension of each list is NROIS, where NROIS
            is the number of currently defined ROIs for this MCA.  It returns
            and empty list for both if NROIS is zero.
            
        Example:
            mca = Mca('mca.001')
            total, net = mca.get_roi_counts(background_width=3)
            print 'Net counts = ', net
        """
        total = []
        net = []
        nchans = len(self.data)
        for roi in self.rois:
            left = roi.left
            ll = max((left-background_width+1), 0)
            if (background_width > 0):
                bgd_left = sum(self.data[ll:(left+1)]) / (left-ll+1)
            else: bgd_left = 0.
            right = roi.right
            rr = min((right+background_width-1), nchans-1)
            if (background_width > 0):
                bgd_right = sum(self.data[right:rr+1]) / (rr-right+1)
            else: bgd_right = 0.
            total_counts = self.data[left:right+1]
            total.append(sum(total_counts))
            n_sel        = right - left + 1
            bgd_counts   = bgd_left + np.arange(n_sel,dtype=float)/(n_sel-1) * \
                                    (bgd_right - bgd_left)
            net_counts   = total_counts - bgd_counts
            net.append(sum(net_counts))
        return (total, net)
    ########################################################################    

    ########################################################################
    

    ########################################################################
    def find_roi(self, left, right, energy=0, detector =0):
        """
        This procedure finds the index number of the ROI with a specified
        left and right channel number.

        Inputs:
            left:
                Left channel number (or energy) of this ROI
                
            right:
                Right channel number (or energy) of this ROI
            
        Keywords:
            energy:
                Set this flag to 1 to indicate that Left and Right are in units
                of energy rather than channel number.
                
        Output:
            Returns the index of the specified ROI, -1 if the ROI was not found.
            
        Example:
            mca = Mca('mca.001')
            index = mca.find_roi(100, 200)
        """
        l = left
        r = right
        if (energy == 1):
            l = self.calibration.energy_to_channel(l, clip=1)
            r = self.calibration.energy_to_channel(r, clip=1)
        index = 0
        for roi in self.rois[detector]:
            if (l == roi.left) and (r == roi.right): return index
            index = index + 1
        return -1

    ########################################################################
    def delete_roi(self, index, detector=0):
        """
        This procedure deletes the specified region-of-interest from the MCA.

        Inputs:
            index:  The index of the ROI to be deleted, range 0 to len(mca.rois)
            
        Example:
            mca = Mca('mca.001')
            mca.delete_roi(2)
        """
        del self.rois[detector][index]


    ########################################################################

    ########################################################################
    def get_environment(self):
        """
        Returns a list of McaEnvironment objects that contain the environment
        parameters of the Mca.
        """
        return self.environment

    ########################################################################
    def set_environment(self, environment):
        """
        Copies a list of McaEnvironment objects to the Mca object.

        Inputs:
            environment:
                A list of McaEnvironment objects.
        """
        self.environment = environment

    def write_file(self, file, netcdf=0):
        """
        Writes Mca or Med objects to a disk file.
        
        It calls Mca.write_netcdf_file if the netcdf keyword flg is set,

        Note that users who want to read such files with Python are strongly
        encouraged to use Mca.read_file()

        Inputs:
            file:
                The name of the disk file to write.
                
        Keywords:
            netcdf:
                Set this flag to write the file in netCDF format, otherwise
                the file is written in ASCII format.  See the documentation
                for Mca.write_ascii_file and Mca.write_netcdf_file for 
                information on the formats.
    
        Example:
            mca = Mca()
            mca.write_file('mca.001')
        """
        # Call the get_xxx() methods to make sure things are up to date
        data = self.get_data()
        calibration = self.get_calibration()
        elapsed = self.get_elapsed()
        presets = self.get_presets()
        rois = self.get_rois()
        environment = self.get_environment()
        

        if (netcdf != 0):
            pass
            #    write_netcdf_file(file, data, calibration, elapsed, presets, rois, environment)
        else:
            try:
                self.fileIO.write_ascii_file(file, data, calibration, elapsed, presets, rois, environment)
                self.file_name=file
                
            except:
                return [file, False]

        
        return [file, True]

    
    ########################################################################
    
    
    def read_file(self, file, netcdf=0, detector=0):
        """
        Reads a disk file into an MCA object.  If the netcdf=1 flag is set it
        reads a netcdf file, else it assumes the file is ASCII.
        If the data file has multiple detectors then the detector keyword can be
        used to specify which detector data to return.

        Inputs:
            file:
                The name of the disk file to read.
                
        Keywords:
            netcdf:
                Set this flag to read files written in netCDF format, otherwise
                the routine assumes that the file is in ASCII format.
                See the documentation for Mca.write_ascii_file and
                Mca.write_netcdf_file for information on the formats.

            detector:
                Specifies which detector to read if the file has multiple detectors.
           
                
        Example:
            mca = Mca()
            mca.read_file('mca.001')
        """
        if (netcdf != 0):
            pass
            #r = read_netcdf_file(file)
        else:
            if file.endswith('.mca'):
                [r, success] = self.fileIO.read_mca_file(file)
            elif file.endswith('.chi'):
                [r, success] = self.fileIO.read_chi_file(file, wavelength=self.wavelength)
                wavelength = r['calibration'][0].wavelength
                self.wavelength = wavelength
            elif file.endswith('.xy'):
                [r, success] = self.fileIO.read_chi_file(file, wavelength=self.wavelength)
                wavelength = r['calibration'][0].wavelength
                self.wavelength = wavelength
            else:
                [r, success] = self.fileIO.read_ascii_file(file)
     
        if success == True:
            self.file_name=file
            self.calibration = r['calibration']
            self.data = r['data']
            self.nchans = len(r['data'][0])
            self.n_detectors=len(self.data)
            self.rois_from_file = [[]]*self.n_detectors
            self.rois = [[]]*self.n_detectors
            self.elapsed = r['elapsed']
            rois = r['rois']
   
            for i , roi in enumerate(rois):
                self.set_rois(roi, detector=i) 
            self.environment = r['environment']
            self.name = os.path.split(file)[-1]
            self.dx_type = r['dx_type']
    
        return([file,success])

    def save_peaks_csv(self,file):

        self.fileIO.write_peaks(file, self.rois[0])

    def export_pattern(self, filename, unit='channel', unit_='#',detector=0,header=None, subtract_background=False):
        """
        Saves the current data pattern.
        :param filename: where to save
        :param header: you can specify any specific header
        :param subtract_background: whether or not the background set will be used for saving or not
        """
        y = self.data[detector]
        channels = np.arange(len(y))

        if filename.endswith('.fxye'):
            unit = 'q'
            unit_=  "A^-1"
        if unit == 'E':
            x = self.calibration[detector].channel_to_energy(channels)
        elif unit == 'q':
            x = self.calibration[detector].channel_to_q(channels)
        elif unit == 'd':
            x = self.calibration[detector].channel_to_d(channels)
        else: x = channels

        if filename.endswith('.xy'):
            self.fileIO.write_pattern(filename,x,y,unit,unit_, header=self._create_xy_header(unit))
        elif filename.endswith('.fxye'):
            self.fileIO.write_pattern(filename,x,y,unit,unit_, header=self._create_fxye_header(filename,"q_A^-1"))
        else:
            self.fileIO.write_pattern(filename,x,y,unit,unit_)

    def _create_xy_header(self, unit):
        """
        Creates the header for the xy file format (contains information about calibration parameters).
        :return: header string
        """
        header = self.make_headers()
        header = header.replace('\r\n', '\n')
        header = '# ' + unit + '\t I'
        return header

    def _create_fxye_header(self, filename, unit):
        """
        Creates the header for the fxye file format (used by GSAS and GSAS-II) containing the calibration information
        :return: header string
        """
        header = 'Generated file ' + filename + ' using hpMCA\n'
        header = header + self.make_headers()
        
        lam = 1
        if unit == 'q_A^-1':
            con = 'CONQ'
        else:
            con = 'CONS'

        header = header + '\nBANK\t1\tNUM_POINTS\tNUM_POINTS ' + con + '\tMIN_X_VAL\tSTEP_X_VAL ' + \
                 '{0:.5g}'.format(lam * 1e10) + ' 0.0 FXYE'
        return header

    def make_headers(self, hdr="#", has_mask=None, has_dark=None, has_flat=None,
                     polarization_factor=None, normalization_factor=None,
                     metadata=None):
        """
        :param hdr: string used as comment in the header
        :type hdr: str
        :param has_dark: save the darks filenames (default: no)
        :type has_dark: bool
        :param has_flat: save the flat filenames (default: no)
        :type has_flat: bool
        :param polarization_factor: the polarization factor
        :type polarization_factor: float

        :return: the header
        :rtype: str
        """
        

        header_lst = "" 
        '''["Mask applied: %s" % has_mask,
                       "Dark current applied: %s" % has_dark,
                       "Flat field applied: %s" % has_flat,
                       "Polarization factor: %s" % polarization_factor,
                       "Normalization factor: %s" % normalization_factor]'''

        if metadata is not None:
            header_lst += ["", "Headers of the input frame:"]
            header_lst += [i.strip() for i in json.dumps(metadata, indent=2).split("\n")]
        header = "\n".join(["%s %s" % (hdr, i) for i in header_lst])

        return header

        
########################################################################

class McaPresets():
    """
    The preset time and counts for an Mca.
    
    Fields:
        .live_time       # Preset live time in seconds
        .real_time       # Preset real time in seconds
        .read_time       # Time that the Mca was last read in seconds
        .total_counts    # Preset total counts between the preset
                        #    start and stop channels
        .start_channel   # Start channel for preset counts
        .end_channel     # End channel for preset counts
        .dwell           # Dwell time per channel for MCS devices
        .channel_advance # Channel advance source for MCS hardware:
                        #    0=internal, 1=external
        .prescale        # Prescaling setting for MCS hardware
    """
    def __init__(self):
        self.live_time = 0.
        self.real_time = 0.
        self.total_counts = 0.
        self.start_channel = 0
        self.end_channel = 0
        self.dwell = 0.
        self.channel_advance = 0
        self.prescale = 0

    

########################################################################

########################################################################
class mcaFileIO():
    def __init__(self):
        pass


        
    def read_mca_file (self, file, tth=15):  #amptek type file

        
        r = {}
        loaded = False
        mca_type = -1
        test_1 = test_read_mca_file_type1(file)
        if test_1:
            mca_type = 1
        else:
            test_0 = self.test_read_mca_file_type0(file)
            if test_0:
                mca_type = 0
        
        if mca_type == 0:
            [r, loaded] = self.read_mca_file_type0(file, tth)
        elif mca_type == 1:
            [r, loaded] = read_mca_file_type1(file, tth)
            
        return [r, loaded]

        
        
    def test_read_mca_file_type0(self, file):
        mcafile = McaReader(file)
        
        ans = mcafile.get_live_time()
        type_0 = ans != None
        return type_0

    def read_mca_file_type0 (self, file, tth=15):  #amptek type file

        mcafile = McaReader(file)
        elapsed = McaElapsed()
        r = {}
        loaded = False
        

        elapsed.live_time = mcafile.get_live_time()
        elapsed.real_time = mcafile.get_real_time()
        elapsed.start_time = mcafile.get_start_time()
        calibration = McaCalibration(dx_type='edx')
        
        cal_func = mcafile.get_calibration_function()
        if cal_func is not None:
            calibration.offset, calibration.slope = cal_func
        file_rois = mcafile.get_rois()
        rois = []
        for r in file_rois:
            roi = McaROI()
            roi.left = int(r[0])
            roi.right = int(r[1])
            rois.append(roi)
        data = mcafile.get_data()
        basefile=os.path.basename(file)
        #tth = xyPatternParametersDialog.showDialog(basefile,'tth',15)
        calibration.two_theta= tth
        
        r['n_detectors'] = 1
        r['calibration'] = [calibration]
        r['elapsed'] = [elapsed]
        r['rois'] = [rois]
        r['data'] = [data]
        r['environment'] = []
        r['dx_type'] = 'edx'
        loaded = True
        return [r, loaded]
        #mcafile.plot()

 

    def read_ascii_file(self, file):
        """
        Reads a disk file.  The file format is a tagged ASCII format.
        The file contains the information from the Mca object which it makes sense
        to store permanently, but does not contain all of the internal state
        information for the Mca.  This procedure reads files written with
        write_ascii_file().

        Inputs:
            file:
                The name of the disk file to read.
                
        Outputs:
            Returns a dictionary of the following type:
            'n_detectors': int,
            'calibration': [McaCalibration()],
            'elapsed':     [McaElapsed()],
            'rois':        [[McaROI()]]
            'data':        [Numeric.array]
            'environment': [[McaEnvironment()]]
            
        Example:
            m = read_ascii_file('mca.001')
            m['elapsed'][0].real_time

        Modification by RH Dec. 30 2021
        Version 3.1A
        Added a distionction between EDX and ADX files.
        For ADX files a WAVELENGTH field is written rather than TWO_THETA.
        For ADX data is written as float, for EDX the as int.
        """
        try:
            fp = open(file, 'r')
        except:
            return [None, False]
        line = ''
        start_time = ''
        max_rois = 0
        data = None
        
        environment = []
        n_detectors = 1  # Assume single element data
        elapsed = [McaElapsed()]
        calibration = [McaCalibration()]
        rois = [[]]
        dx_type = ''
        try:
            
            while(1):
                line = fp.readline()
                if (line == ''): break
                pos = line.find(' ')
                if (pos == -1): pos = len(line)
                tag = line[0:pos]
                value = line[pos:].strip()
                values = value.split()
                if (tag == 'VERSION:'):
                    pass
                elif (tag == 'DATE:'):  
                    start_time = value
                elif (tag == 'ELEMENTS:'):
                    n_detectors  = int(value)
                    for det in range(1, n_detectors):
                        elapsed.append(McaElapsed())
                        calibration.append(McaCalibration())
                        rois.append([])
                elif (tag == 'CHANNELS:'):
                    nchans = int(value)
                elif (tag == 'ROIS:'):
                    nrois = []
                    for d in range(n_detectors):
                        nrois.append(int(values[d]))
                    max_rois = max(nrois)
                    for d in range(n_detectors):
                        for r in range(nrois[d]):
                            rois[d].append(McaROI())
                elif (tag == 'REAL_TIME:'):
                    for d in range(n_detectors):
                        elapsed[d].start_time = start_time
                        elapsed[d].real_time = float(values[d])
                elif (tag == 'LIVE_TIME:'):  
                    for d in range(n_detectors):
                        elapsed[d].live_time = float(values[d])
                elif (tag == 'CAL_OFFSET:'):
                    for d in range(n_detectors):
                        calibration[d].offset = float(values[d])
                elif (tag == 'CAL_SLOPE:'):
                    for d in range(n_detectors):
                        calibration[d].slope = float(values[d])
                elif (tag == 'CAL_QUAD:'):  
                    for d in range(n_detectors):
                        calibration[d].quad = float(values[d])
                elif (tag == 'TWO_THETA:'):
                    for d in range(n_detectors):
                        calibration[d].two_theta = float(values[d])
                        calibration[d].set_dx_type('edx')
                        calibration[d].units = 'keV'
                    data_type = int
                    dx_type = 'edx'
                elif (tag == 'WAVELENGTH:'):
                    for d in range(n_detectors):
                        calibration[d].wavelength = float(values[d])
                        calibration[d].set_dx_type('adx')
                        calibration[d].units = 'degrees'
                    data_type = float
                    dx_type = 'adx'
                elif (tag == 'ENVIRONMENT:'):
                    env = McaEnvironment()
                    p1 = value.find('=')
                    env.name = value[0:p1]
                    p2 = value[p1+2:].find('"')
                    env.value = value[p1+2: p1+2+p2]
                    env.description = value[p1+2+p2+3:-1]
                    environment.append(env)
                elif (tag == 'DATA:'):
                    
                    data = []
                    for d in range(n_detectors):
                        data.append(np.zeros(nchans,  dtype=data_type))
                    for chan in range(nchans):
                        line = fp.readline()
                        counts = line.split()
                        for d in range(n_detectors):
                            data[d][chan]=data_type(counts[d])
                    
                else:
                    for i in range(max_rois):
                        roi = 'ROI_'+str(i)+'_'
                        if (tag == roi+'LEFT:'):
                            for d in range(n_detectors):
                                if (i < nrois[d]):
                                    rois[d][i].left = int(values[d])
                                #break
                        elif (tag == roi+'RIGHT:'):
                            for d in range(n_detectors):
                                if (i < nrois[d]):
                                    rois[d][i].right = int(values[d])
                                #break
                        elif (tag == roi+'LABEL:'):
                            labels = value.split('&')
                            for d in range(n_detectors):
                                if (i < nrois[d]):
                                    rois[d][i].label = labels[d].strip()
                                #break
                        else:
                           
                            pass
            
            # Make sure DATA array is defined, else this was not a valid data file
            if (data == None): return [None, False]
            fp.close()
            # Built dictionary to return
            r = {}
            r['n_detectors'] = n_detectors
            r['calibration'] = calibration
            r['elapsed'] = elapsed
            r['rois'] = rois
            r['data'] = data
            r['environment'] = environment
            r['dx_type'] = dx_type
            
            return [r, True]
        except:
            return [None, False]

    def compute_tth_calibration_coefficients(self, tth):
        chan = np.linspace(0,len(tth)-1,len(tth))[::50]
        tth = tth[::50]
        weights = np.ones(len(tth)) 
        coeffs = CARSMath.polyfitw(chan, tth, weights, 1)
        return coeffs
        

    def read_chi_file(self, filename, wavelength=None):  #fit2d or dioptas chi type file
        if filename.endswith('.chi') or filename.endswith('.xy'):
            '''fp = open(filename, 'r')
            first_line = fp.readline()
            second_line = fp.readline()
            unit = second_line.strip().upper()[:1]  # reserved for future functionality
            fp.close()'''
            
            skiprows = 4
            data = np.loadtxt(filename, skiprows=skiprows)
            
            x = data.T[0]
            y = data.T[1]
            basefile=os.path.basename(filename)
            #name = basefile.split('.')[:-1][0]


            coeffs = self.compute_tth_calibration_coefficients(x)
            if wavelength == None:

                wavelength = xyPatternParametersDialog.showDialog(basefile,'wavelength',.4)

            r = {}
            r['n_detectors'] = 1
            r['calibration'] = [McaCalibration(offset=coeffs[0],
                                               slope=coeffs[1],
                                               quad=0, 
                                               two_theta= np.mean(x),
                                               units='degrees',
                                               wavelength=wavelength)]
            r['calibration'][0].set_dx_type('adx')
            r['elapsed'] = [McaElapsed()]
            r['rois'] = [[]]
            r['data'] = [y]
            r['environment'] = []
            r['dx_type'] = 'adx'
            return[r,True]
            
        return [None, False]
        
    #######################################################################
    def write_ascii_file(self, file, data, calibration, elapsed, presets, rois,
                        environment):
        """
        Writes Mca or Med data to a disk file.  The file 
        format is a tagged ASCII format.  The file contains the information 
        from the Mca object which it makes sense to store permanently, but 
        does not contain all of the internal state information for the Mca.  
        Files written with this routine can be read with read_ascii_file(), which
        is called by Mca.read_file() if the netcdf flag is 0.

        This procedure is typically not called directly, but is called
        by Mca.write_file if the netcdf=1 keyword is not used.

        This function can be used for writing for Mca objects, in which case
        each input parameter is an object, such as McaElapsed, etc.
        It can also be used for writing Med objects, in which case each input
        parameter is a list.

        If the rank of data is 2 then this is an Med, and the number of detectors
        is the first dimension of data

        Inputs:
            file:
                The name of the disk file to write.
                
            data:
                The data to write.  Either 1-D array or list of 1-D arrays.

            calibration:
                An object of type McaCalibration, or a list of such objects.

            elapsed:
                An object of type McaElapsed, or a list of such objects.

            presets:
                An object of type McaPresets, or a list of such objects.

            rois:
                A list of McaROI objects, or a list of lists of such objects.
            
            environment:
                A list of McaEnvironment objects, or a list of lists of such objects.
        
        Modification by RH Dec. 30 2021
        Version 3.1A
        Added a distionction between EDX and ADX files.
        For ADX files a WAVELENGTH field is written rather than TWO_THETA.
        For ADX data is written as float, for EDX the as int.
        """



        if (np.ndim(data) == 2):
            n_det = len(data)
        else:
            n_det = 1
        fformat = '%f ' * n_det
        eformat = '%e ' * n_det
        iformat = '%d ' * n_det
        sformat = '%s ' * n_det
        if (n_det == 1):
            # commented out since attributes are already stored as lists (with future outlook for multiple detectors) - RH
            """ # For convenience we convert all attributes to lists
            data = data
            rois = rois
            calibration = calibration
            presets = presets
            elapsed = elapsed
            """
        nchans = len(data[0])
        dx_type = calibration[0].dx_type
        version = '3.1A' if dx_type == 'adx'  else '3.1'
        start_time = elapsed[0].start_time

        fp = open(file, 'w')
        fp.write('VERSION:    '+version+'\n')
        fp.write('ELEMENTS:   '+str(n_det)+'\n')
        fp.write('DATE:       '+str(start_time)+'\n')
        fp.write('CHANNELS:   '+str(nchans)+'\n')

        nrois = []
        for roi in rois:
            nrois.append(len(roi))
        fp.write('ROIS:       '+(iformat % tuple(nrois))+'\n')
        real_time=[]; live_time=[]
        for e in elapsed:
            real_time.append(e.real_time)
            live_time.append(e.live_time)
        fp.write('REAL_TIME:  '+(fformat % tuple(real_time))+'\n')
        fp.write('LIVE_TIME:  '+(fformat % tuple(live_time))+'\n')
        offset=[]; slope=[]; quad=[]; two_theta=[]; wavelength=[]
        for c in calibration:
            offset.append(c.offset)
            slope.append(c.slope)
            quad.append(c.quad)
            if c.dx_type == 'edx':
                two_theta.append(c.two_theta)
            if c.dx_type == 'adx':
                wavelength.append(c.wavelength)
        fp.write('CAL_OFFSET: '+(eformat % tuple(offset))+'\n')
        fp.write('CAL_SLOPE: '+(eformat % tuple(slope))+'\n')
        fp.write('CAL_QUAD: '+(eformat % tuple(quad))+'\n')
        if c.dx_type == 'edx':
            fp.write('TWO_THETA: '+(fformat % tuple(two_theta))+'\n')
            data_format = iformat
        if c.dx_type == 'adx':
            fp.write('WAVELENGTH: '+(fformat % tuple(wavelength))+'\n')
            data_format = fformat

        for i in range(max(nrois)):
            num = str(i)
            left=[]; right=[]; label=[]
            for d in range(n_det):
                if (i < nrois[d]):
                    left.append(rois[d][i].left)
                    right.append(rois[d][i].right)
                    label.append(rois[d][i].label + '&')
                else:
                    left.append(0)
                    right.append(0)
                    label.append(' &')
            fp.write('ROI_'+num+'_LEFT:  '+(iformat % tuple(left))+'\n')
            fp.write('ROI_'+num+'_RIGHT:  '+(iformat % tuple(right))+'\n')
            fp.write('ROI_'+num+'_LABEL:  '+(sformat % tuple(label))+'\n')
        for e in environment:
            fp.write('ENVIRONMENT: '       + str(e.name) +
                                    '="'  + str(e.value) +
                                    '" (' + str(e.description) + ')\n')
        fp.write('DATA: \n')
        counts = np.zeros(n_det)
        for i in range(nchans):
            for d in range(n_det):
                counts[d]=data[d][i]
            fp.write((data_format % tuple(counts))+'\n')
        fp.close()


    def write_pattern(self, filename, x, y, unit, unit_, header=None):
        """
        Saves the x, y data pattern.
        :param filename: where to save
        :param header: you can specify any specific header
        """
        
        file_handle = open(filename, 'w')
        num_points = len(x)

        if filename.endswith('.chi'):
            if header is None or header == '':
                file_handle.write(filename + '\n')
                file_handle.write(unit + ' ('+ unit_+')''\n\n')
                file_handle.write("       {0}\n".format(num_points))
            else:
                file_handle.write(header)
            for ind in range(num_points):
                file_handle.write(' {0:.7E}  {1:.7E}\n'.format(x[ind], y[ind]))
        elif filename.endswith('.fxye'):
            factor = 100
            if header is not None:
                if 'CONQ' in header:
                    factor = 1
                header = header.replace('NUM_POINTS', '{0:.6g}'.format(num_points))
                header = header.replace('MIN_X_VAL', '{0:.6g}'.format(factor*x[0]))
                header = header.replace('STEP_X_VAL', '{0:.6g}'.format(factor*(x[1]-x[0])))

                file_handle.write(header)
                file_handle.write('\n')
            for ind in range(num_points):
                file_handle.write('\t{0:.6g}\t{1:.6g}\t{2:.6g}\n'.format(factor*x[ind], y[ind], sqrt(abs(y[ind]))))
        else:
            if header is not None:
                file_handle.write(header)
                file_handle.write('\n')
            for ind in range(num_points):
                file_handle.write('{0:.9E}  {1:.9E}\n'.format(x[ind], y[ind]))
        file_handle.close()

    def write_peaks(self, file, rois, background=None):
        """
        Writes a list of obejcts of type McaPeak to a disk file.
        If the background parameter is present it also writes the background
        structure to the file.
        
        Inputs:
            file:
                The name of a disk file to be written ;
            peaks:
                A list of McaPeak objects
                
        Keywords:
            background:
                An object of type McaBackground
                
        Example:
            r = read_peaks('my_peaks.pks')
            peaks = r['peaks']
            peaks[1].initial_energy = 6.4
            write_peaks('mypeaks.pks', peaks)
        """
        lines = []
        if (background != None):
            lines.append('Background_exponent,'     + str(background.exponent)+'\n')
            lines.append('Background_top_width,'    + str(background.top_width)+'\n')
            lines.append('Background_bottom_width,' + str(background.bottom_width)+'\n')
            lines.append('Background_tangent,'      + str(background.tangent)+'\n')
            lines.append('Background_compress,'     + str(background.compress)+'\n')
        lines.append('centroid,'+'fwhm,'+'energy,'+'fwhm_E,'+'q,'+'fwhm_q,'+'d_spacing,'+'fwhm_d,'+'label'+'\n')
        for r in rois:
            lines.append('{:.4e}'.format(r.centroid) + ', ' + 
                        '{:.4e}'.format(r.fwhm)    + ', ' + 
                        '{:.4e}'.format(r.energy) + ', ' + 
                        '{:.4e}'.format(r.fwhm_E)    + ', ' + 
                        '{:.4e}'.format(r.q)   + ', ' + 
                        '{:.4e}'.format(r.fwhm_q)      + ', ' + 
                        '{:.4e}'.format(r.d_spacing)   + ', ' + 
                        '{:.4e}'.format(r.fwhm_d)      + ', ' + 
                        r.label + '\n')
        fp = open(file, 'w')
        fp.writelines(lines)
        fp.close()

