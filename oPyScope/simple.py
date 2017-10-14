"""Simple Time Series analysis
"""

import numpy as np 
import pkg_resources
import configparser
from matplotlib import pyplot as plt

import pyScope.input_handle

class ScopeTimeSeries(object):
    """Object to analyse Osilloscope data
    """
    
    def __init__(self, file_path, conf_path = None):
        
        self._configure(conf_path)
        self._load_signal(file_path)

    def _configure(self, conf_path):
        # Configure the object
        if conf_path is None:
            conf_str = pkg_resources.resource_string("pyScope.resources", 
                                                     "ScopeTimeSeriesDefault.ini")
            conf_str = conf_str.decode("ascii")
            self.conf = configparser.ConfigParser()
            self.conf.read_string(conf_str)
        else:
            self.conf = configparser.ConfigParser()
            self.conf.read(conf_path)

    def _load_signal(self, file_path):
        
        # Load the data
        if self.conf['input']['file_type'] == 'csv':
            #self.get_data_csv(file_path)
            self.signal = pyScope.input_handle.get_data_csv(file_path, 
                                                            delimiter=self.conf['csv_handle']['delimiter'],
                                                            skip_header=int(self.conf['csv_handle']['skip_header']))

        self._determine_signal_range()

    def _determine_signal_range(self):
            
        self.conf.set('sig_digital_tol', 'low_min', "%0.9f" % min(self.signal[:,1]))
        self.conf.set('sig_digital_tol', 'high_max', "%0.9f" % max(self.signal[:,1]))

        sig_range = max(self.signal[:,1])  - min(self.signal[:,1])
        offset = float(self.conf.get('sig_digital_tol', 'low_min'))

        self.conf.set('sig_digital_tol', 'low_max', "%0.9f" % (offset + sig_range/2 - 0.0000000000001))
        self.conf.set('sig_digital_tol', 'high_min', "%0.9f" % (offset + sig_range/2))

        time_edge = float(self.conf.get('sig_digital_tol', 'time_edge'))
        grad = sig_range*0.5 / time_edge
        self.conf.set('sig_digital_tol', 'sig_change_grad', "%0.9f" % grad)

    def plot_signal(self, offset=(None, None)):
        
        plt.plot(self.signal[:,0], self.signal[:,1])
        plt.show()

    def conv_digital(self, analog_val):
        
        low_max = float(self.conf.get('sig_digital_tol' , 'low_max'))
        low_min = float(self.conf.get('sig_digital_tol' , 'low_min'))
        high_max = float(self.conf.get('sig_digital_tol' , 'high_max'))
        high_min = float(self.conf.get('sig_digital_tol' , 'high_min'))
        
        if (analog_val <= low_max and
           analog_val >= low_min):
            return 0
        elif (analog_val <= high_max and
             analog_val >= high_min):
            return 1

    def is_edge(self, x1, y1, x2, y2):
        
        grad = (y2 - y1) / (x2 - x1)
        if grad < 0:
            direction = 0
        else:
            direction = 1

        grad = abs(grad)
        #print("Pt 1 = (%0.5f, %0.5f)\tPt2 = (%0.5f, %0.5f)\tGrad = %0.5f" % (x1, y1, x2, y2, grad))

        if grad >= float(self.conf.get('sig_digital_tol', 'sig_change_grad')):
            return direction
        else:
            return None

    def get_bit_sequence_simple(self, bit_period = None, time_start = 0, time_end = None):
        """Iterates over the data and determines the bit sequence

        Args:
            - bit_period (float): the expected period of a bit
            - sig_change_tol (float): the maximize change in signal before its considered
                                      a digital signal change
        """

        if bit_period is None:
            raise ValueError("Bit Period must be set with the keyword argument 'bit_period")
        
        # Trackers
        prev_time = None
        prev_sig = None
        time_passed = 0

        curr_digital_val = None

        dig_sequence = []

        for this_time, this_sig in zip(self.signal[:,0], self.signal[:,1]):
            
            # Skip to the important part
            if (this_time < time_start):
                continue
            elif (time_end is not None and this_time > time_end):
                break
            
            # First Bit
            if (prev_sig == None and prev_time == None):
                dig_val = self.conv_digital(this_sig)
                dig_sequence.append(dig_val)

                # Set trackers
                time_passed = 0
                prev_sig = this_sig
                prev_time = this_time
                continue

            time_passed += this_time - prev_time

            # Detect rising/falling edges
            # This is here to 'sync' up the time
            this_diff = this_sig - prev_sig
            #if (this_diff > self._edge_change_tol):

            # One signal period
            if time_passed >= bit_period:

                #print("%0.6f" % time_passed)

                dig_val = self.conv_digital(this_sig)
                dig_sequence.append(dig_val)

                # Update trackers
                time_passed = 0
                prev_time = this_time
                prev_sig = this_sig
                continue
        
        return dig_sequence


    def get_bit_sequence_edge(self, bit_period, time_start = 0, time_end = None):
        """Iterates over the data and determines the bit sequence

        Args:
            - bit_period (float): the expected period of a bit
            - sig_change_tol (float): the maximize change in signal before its considered
                                      a digital signal change
        """

        DIGITAL_HIGH = 1
        DIGITAL_LOW = 0
        
        # Trackers
        prev_time = None
        prev_sig = None
        time_passed = 0
        time_last_edge = 0

        curr_digital_val = None

        dig_sequence = []

        for this_time, this_sig in zip(self.signal[:,0], self.signal[:,1]):
            
            # Skip to the important part
            if (this_time < time_start):
                continue
            elif (time_end is not None and this_time > time_end):
                break
            
            # First Bit
            if (prev_sig == None and prev_time == None):
                dig_val = self.conv_digital(this_sig)
                dig_sequence.append(dig_val)

                # Set trackers
                time_passed = 0
                prev_sig = this_sig
                prev_time = this_time
                continue

            #Edge Detection
            dig_val = self.is_edge(prev_time, prev_sig, this_time, this_sig)

            prev_time = this_time
            prev_sig = this_sig

            if dig_val is None:
                continue
            else:
                
                time_passed = this_time - time_last_edge
                n_bits = int(round(time_passed/bit_period, 0)) - 1

                bits = [int(not(dig_val))]*n_bits
                dig_sequence.extend(bits)

                dig_sequence.append(dig_val)
                time_last_edge = this_time

        return dig_sequence