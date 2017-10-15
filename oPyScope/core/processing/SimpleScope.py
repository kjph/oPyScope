"""Simple Time Series analysis
"""

from oPyScope.core.signal.DigitalTS import DigitalTS

class SimpleScope(DigitalTS):
    """Object to analyse Osilloscope data
    """

    def get_bit_sequence_edge(self, bit_period, time_start = 0, time_end = None):
        """Iterates over the data and determines the bit sequence

        Args:
            - bit_period (float): the expected period of a bit
            - sig_change_tol (float): the maximize change in signal before its considered
                                      a digital signal change
        """
        
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