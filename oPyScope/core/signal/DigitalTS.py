"""Simple Time Series analysis
"""

from matplotlib import pyplot as plt

from oPyScope.core.DataHandler import DataHandler

class DigitalTS(DataHandler):
    """Digital Time Series object

    Attributes:
        signal (np.array): The loaded data
    """
    
    def __init__(self, *args, **kwargs):
        super(DigitalTS, self).__init__(*args, **kwargs)
        self.signal = self.data
        self._determine_signal_range()
    
    def _determine_signal_range(self):
        """Adjust signal tolerances based on data

        Note:
            The noise margins, low_min and high_max are based on the minimum and
            maximum values of the signal respectively.

            The noise margins, low_max and high_min are based on the mid-point
            of the signal

            Finally, the gradient (grad) of the signal before a edge is detected
            is determined with the time_edge conf parameter and half the signal
            range
        """
            
        self.conf.set('sig_digital_tol', 'low_min', "%0.9f" % min(self.signal[:,1]))
        self.conf.set('sig_digital_tol', 'high_max', "%0.9f" % max(self.signal[:,1]))

        sig_range = max(self.signal[:,1])  - min(self.signal[:,1])
        offset = float(self.conf.get('sig_digital_tol', 'low_min'))

        self.conf.set('sig_digital_tol', 'low_max', "%0.9f" % (offset + sig_range/2 - 0.0000000000001))
        self.conf.set('sig_digital_tol', 'high_min', "%0.9f" % (offset + sig_range/2))

        time_edge = float(self.conf.get('sig_digital_tol', 'time_edge'))
        grad_sf = float(self.conf.get('sig_digital_tol', 'sig_grad_factor'))
        grad = sig_range*grad_sf / time_edge
        self.conf.set('sig_digital_tol', 'sig_change_grad', "%0.9f" % grad)

    def plot_signal(self, offset=(None, None)):
        
        plt.plot(self.signal[:,0], self.signal[:,1])
        plt.show()

    def conv_digital(self, analog_val):
        """Converts analog signal to its corresponding digital value based on
            the configured signal tolerances

        Args:
            analog_val (float): The analog value to convert

        Returns:
            (int) The digital value

            None if the analog value is invalid
        """
        
        low_max = float(self.conf.get('sig_digital_tol' , 'low_max'))
        low_min = float(self.conf.get('sig_digital_tol' , 'low_min'))
        high_max = float(self.conf.get('sig_digital_tol' , 'high_max'))
        high_min = float(self.conf.get('sig_digital_tol' , 'high_min'))

        if (analog_val < low_min or analog_val > high_max):
            return None
        elif (analog_val <= low_max and analog_val >= low_min):
            return 0
        elif (analog_val <= high_max and analog_val >= high_min):
            return 1

    def is_edge(self, x1, y1, x2, y2):
        """Determines if two points of data are on the edge of a signal

        Args:
            x1 (float): The first point's x value
            y1 (float): The first point's y value
            x2 (float): The second point's x value
            y2 (float): The second point's y value

        Returns:
            int: the direction of the edge 1=rise, 0=fall

            None if no edge is detected
        """
        
        grad = (y2 - y1) / (x2 - x1)
        if grad < 0:
            direction = 0
        else:
            direction = 1

        grad = abs(grad)

        if grad >= float(self.conf.get('sig_digital_tol', 'sig_change_grad')):
            return direction
        else:
            return None