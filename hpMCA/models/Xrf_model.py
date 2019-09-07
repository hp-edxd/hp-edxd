import hpMCA.models.Xrf as Xrf
import os
#import time

class atom():
    def __init__(self, symbol):
        
        self.symbol = symbol
        self.Z = Xrf.atomic_number(self.symbol)
        self.show = False
        
        k_lines = { 'Ka' :False,
                    'Ka1':True,
                    'Ka2':True,
                    'Kb' :False,
                    'Kb1':True,
                    'Kb2':True }
        l_lines = { 'La1':False,
                    'Lb1':False,
                    'Lb2':False,
                    'Lg1':False,
                    'Lg2':False,
                    'Lg3':False,
                    'Lg4':False,
                    'Ll':False }
        self.toggles = { 'Ka':['Ka1','Ka2'],
                    'Kb':['Kb1','Kb2'],
                    'Ka1':['Ka'],
                    'Kb1':['Kb'],
                    'Ka2':['Ka'],
                    'Kb2':['Kb']}
        
        # dict = {key: [e, selected]}
        self.k_selection = dict()
        for k in k_lines:
            e = Xrf.lookup_xrf_line(self.symbol + ' ' + k)
            #if (e != 0.):
            self.k_selection.update({k:[e, k_lines[k]]})
        self.l_selection = dict()
        for l in l_lines:
            e = Xrf.lookup_xrf_line(self.symbol + ' ' + l)
            #if (e != 0.):
            show = False
            self.l_selection.update({l:[e, l_lines[l] or show]})

        self.all_lines = dict()
        self.all_lines.update(self.k_selection)
        self.all_lines.update(self.l_selection)
        
    def k_all(self, select=False):
        for k in self.k_selection:
            self.k_selection[k] = select

    def l_all(self, select=False):
        for l in self.l_selection:
            self.l_selection[l] = select

    def get_e (self, line):
        return self.get_parameter(line,0)

    def is_line_checked (self, line):
        return self.get_parameter(line,1)
    
    def set_line_checked (self,line, checked):
        line = line.upper()
        for l in self.all_lines:
            if  line == l.upper(): 
                self.all_lines[l][1]=checked

        if checked:
            for l in self.toggles:
                if line == l.upper():
                    for toggle in self.toggles[l]:
                        for l in self.all_lines:
                            if  toggle.upper() == l.upper(): 
                                self.all_lines[l][1]=False

    def get_parameter (self, line, parameter):
        line = line.upper()
        for l in self.all_lines:
                  if  line == l.upper(): return self.all_lines[l][parameter]
        return None

    def get_lines (self):
        return [self.k_selection, self.l_selection]
