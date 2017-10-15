"""Simple Time Series analysis
"""

import os
import pkg_resources
import configparser

from oPyScope.core import file_handles

class DataHandler(object):
    """Base class to load data objects

    Args:
        file_path (str): The path to the data file to load from
        conf_path (str, optional): Path to the configuration file to use

    Attributes:
        data (np.array): The loaded data
    """
    
    def __init__(self, file_path, conf_path = None):
        self._configure(conf_path)
        self._load_data(file_path)

    def _configure(self, conf_path):
        """Initialises the object with the user defined parameters.

        Args:
            conf_path (str): The path to read the data file, if None the default
                is used.

        Raises:
            FileNotFoundError: if the conf_path does not exist.
        """

        # Configure the object
        if conf_path is None:
            conf_str = pkg_resources.resource_string("oPyScope.resources", 
                                                     "ScopeTimeSeriesDefault.ini")
            conf_str = conf_str.decode("ascii")
            self.conf = configparser.ConfigParser()
            self.conf.read_string(conf_str)
        else:
            if not(os.path.exist(conf_path)):
                raise FileNotFoundError("%s not found" % conf_path)
            self.conf = configparser.ConfigParser()
            self.conf.read(conf_path)

    def _load_data(self, file_path):
        """Reads data from specified file_path using defined extension (conf)

        Args:
            file_type (str): Path to data file

        Raises:
            FileNotFoundError: if the specified file_path does not exist
            ValueError: if the specified file_path does not match the extension
                specified in the configuration
        """

        expected_file_ext = self.conf['input']['file_type'] 
        
        if not(os.path.exists(file_path)):
            raise FileNotFoundError("%s as data file not found" % file_path)
        elif not(file_path.endswith(expected_file_ext)):
            raise ValueError("%s does not match the defined extension %s" %
                             (file_path, expected_file_ext))

        # Load the data
        if expected_file_ext == 'csv':
            self.data = file_handles.get_data_csv(file_path, 
                                                    delimiter=self.conf['csv_handle']['delimiter'],
                                                    skip_header=int(self.conf['csv_handle']['skip_header']))
        else:
            raise Exception("Data is not loaded for SignalProcessor object")
            #TODO: Implement proper exception class