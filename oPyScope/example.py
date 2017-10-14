"""Example usage of this package
"""

import os

from oPyScope.configure import configure_simple_timeseries
from oPyScope.simple import ScopeTimeSeries
from oPyScope.words import binary_seq_to_hex_words

def main():

    # Specify the path of the data
    target_path = os.path.join("../data", "dpjn01.csv")

    # Set up the configuration (Optional), default is already shipped
    configure_simple_timeseries(dir_to_save = ".", file_name = "SimpleTimeSeries")

    # Initialise the scope object
    scope = ScopeTimeSeries(target_path, conf_path="./SimpleTimeSeries.ini")
    scope.plot_signal()

    # Analyse the sequence
    bit_seq = scope.get_bit_sequence_edge(bit_period=1.4e-04)
    bit_seq.append(1);#Add the stop bit

    # Print the results
    print("\nRESULTS")
    print(binary_seq_to_hex_words(bit_seq, offset=1))
    print(binary_seq_to_hex_words(bit_seq, offset=1, endian='little'))

if __name__ == '__main__':
    main()
