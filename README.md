# oPyScope
Python package to analyse Oscilloscope data

## Installation

``` bash

$ cd ~/Somewhere/
$ git clone https://github.com/kjph/oPyScope.git
$ python -m pip install -e oPyScope

```

## Usage

1. Save your signal from the oscilloscope to a `.csv` file
2. Create a script similar to `oPyScope.example` (ensure to set the correct paths for your data file)
3. Run the script (for example `python -m oPyScope.example`)
4. Set the configuration values as required (note that the digital signal tolerances will be auto-adjusted after reading in the data)

## Example

``` py
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
    
    # Plot the signal
    scope.plot_signal()

    # Analyse the sequence
    bit_seq = scope.get_bit_sequence_edge(bit_period=1.4e-04)
    bit_seq.append(1);#Add the stop bit

    # Print the results
    print("\nRESULTS")
    print(binary_seq_to_hex_words(bit_seq, offset=1))
    print(binary_seq_to_hex_words(bit_seq, offset=1, endian='little'))
```
