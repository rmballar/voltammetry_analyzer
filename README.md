# Voltammetry Analyzer
This program analyzes linear sweep voltammetry data from a CH Instruments 1030C Electrochemical Analyzer. Input data files should include the nanopipette number, pH and volume of acid added. voltammetry_analyzer.py outputs tab-delimited csv files for each voltage analyzed; the format of these files is: |pH|   |Current|   |CurrentRatio(I<sub>pH</sub>/I<sub>ctrl</sub>)|.

## Usage
Make sure the data files are the only .txt files in the directory then run the command below:
- Linux/macOS:
    - `ls *.txt | python3 voltammetry_analyzer.py`
- Windows (untested):
    - `dir *.txt | python3 voltammetry_analyzer.py`