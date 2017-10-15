"""Basic I/O for configuration of object settings
"""

import os
import configparser
from termcolor import cprint

PROMPT = ">> "

def test():
    configure_simple_timeseries()

def user_input(message, default=None, expected_type=str):
    
    if default is None:
        print("%s " % (message), end="")
    else:
        print("%s [%s]" % (message, str(default)), end="")

    ret = input(PROMPT)

    if ret == "":
        return default
    else:
        try:
            expected_type(ret)
        except ValueError:
            print("Must be of type %s" % str(expected_type))
            ret = user_input(message, default, expected_type=expected_type)
        return ret

def configure_simple_timeseries(dir_to_save = None, file_name = None):
    """ CLI walk through for configuration of Simple.ScopeTimeSeries
    """

    print("\nConfiguartion for Simple.ScopeTimeSeries\n")
    print("Press enter to use default values that are specified in the square brackets")

    if dir_to_save == None and file_name == None: 
        dir_to_save = user_input("Directory to save", default=".", expected_type=str)
        while(not(os.path.isdir(dir_to_save))):
            print("%s does not exist!" % dir_to_save)
            dir_to_save = user_input("Directory to save", default=".", expected_type=str)

        file_name = user_input("File name to use", default="ScopeTimeSeries", expected_type=str)
    
    if file_name.endswith(".ini"):
        target = os.path.join(dir_to_save, file_name)
    else:
        target = os.path.join(dir_to_save, file_name + ".ini")

    conf = configparser.ConfigParser()

    conf["input"] = {}
    conf["csv_handle"] = {}
    conf["sig_digital_tol"] = {}

    file_type = user_input("File type to read data", default="csv", expected_type=str)
    conf.set("input", "file_type", file_type)

    if file_type == 'csv':
        skip_header = user_input("Number of rows (e.g. headers) to skip", default=2, expected_type=int)
        delimiter = user_input("CSV Delimiter", default=",", expected_type=str)

        conf.set("csv_handle", "skip_header", str(skip_header))
        conf.set("csv_handle", "delimiter", delimiter)

    high_min = user_input("Digital High min value", default = 1.5, expected_type=float)
    high_max = user_input("Digital High max value", default = 3.3, expected_type=float)
    low_min = user_input("Digital Low min value", default = 0, expected_type=float)
    low_max = user_input("Digital Low max value", default = 1.4, expected_type=float)
    time_edge = user_input("Rise/Fall Time expected", default = 1.96e-6, expected_type=float)
    sig_grad_factor = user_input("Edge detection gradient scale factor", default = 0.5, expected_type=float)

    conf.set("sig_digital_tol", "high_min", "%0.9f" % high_min)
    conf.set("sig_digital_tol", "high_max", "%0.9f" % high_max)
    conf.set("sig_digital_tol", "low_min", "%0.9f" % low_min)
    conf.set("sig_digital_tol", "low_max", "%0.9f" % low_max)
    conf.set("sig_digital_tol", "time_edge", "%0.9f" % time_edge)
    conf.set("sig_digital_tol", "sig_grad_factor", "%0.9f" % sig_grad_factor)
    


    with open(target, 'w') as configfile:
        conf.write(configfile)

if __name__ == '__main__':
    test()