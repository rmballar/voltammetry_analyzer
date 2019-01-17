#!/usr/bin/env python3

import sys
import csv


def get_files():
    """
    Get list of files from stdin and strip any newline characters.
    Usage (Linux/Mac):
    user@machine:~$ ls| grep *.txt|python printData.py
    
    Return a list of file names.
    """
    file_list = []
    for line in sys.stdin:
        line = line.rstrip('\n')
        file_list.append(line)
    return file_list


def current_at_voltage(in_file, voltage):
    """
    Return the current at a defined voltage.
    """
    with open(in_file, 'r') as tsv_in:
        tsv_in = csv.reader(tsv_in, delimiter='\t')
        for row in tsv_in:
            try:
                if row[1]:
                    if float(voltage) == float(row[0]):
                        return float(row[1])
            except ValueError:
                next(tsv_in)
            except IndexError:
                next(tsv_in)


def current_ratio(in_file, control_file, voltage):
    in_voltage = current_at_voltage(in_file, voltage)
    ctrl_voltage = current_at_voltage(control_file, voltage)
    return in_voltage/ctrl_voltage


def write_output(file_name, line_list):
    with open(file_name, 'w') as tsv_out:
        tsv_out = csv.writer(tsv_out, delimiter='\t')
        for line in line_list:
                tsv_out.writerow(line)


def get_volume(in_file):
    temp_vol_1 = in_file.split('ul')
    temp_vol_2 = temp_vol_1[0].split('_')
    volume = float(temp_vol_2[1])
    return volume


def get_control_file(file_list):
    control_found = False
    for in_file in file_list:
        temp_vol_1 = in_file.split('ul')
        temp_vol_2 = temp_vol_1[0].split('_')
        volume = float(temp_vol_2[1])
        if volume == 0:
            control_found = True
            control_file = in_file
            return control_file
    if not control_found:
        sys.stderr.write('Control file not found!\n')


def find_np_num(file_name):
    '''
    Finds the nanopipette number from a file name
    '''
    np_num = file_name[0:4]  # Expected str: NPx_ or NPxx
    np_num = np_num.rstrip('_')
    return np_num


def get_pH(file_name):
    char_list = []
    started = False
    finished = False
    for char in file_name:
        if char == '(':
            started = True
        if started and not finished:
            char_list.append(char)
        if char == ')':
            finished = True
    pH = ''.join(char_list)
    for char in '()pH':
        pH = pH.replace(char,'')
    return float(pH)


def gnuplot_script_builder(file_list):
    script_template = ['reset',
    'set term pdfcairo enhanced',
    'set output "{0}_titration.pdf"'.format(find_np_num(file_list[0])),
    'set mxtics 5',
    'set xtics font "Sans, 10"',
    'set ytics font "Sans, 10"',
    'unset grid',
    'set key outside center right title "Solution pH" font "Times Roman, 12"',
    'set xrange [-1:1]',
    'set xlabel "Voltage [V]" font "Times Roman, 12"',
    'set ylabel "Current [nA]" font "Times Roman, 12"',
    'set palette rgb 33,13,10',
    'unset colorbox'
    ]
    plot_lines = []
    for file in file_list:
        plot_line = ' "{0}" u 1:($2*1E9) w l lc palette frac {1:5.3f}/14 lw 1.5 title "{2:5.3f}",\\\n'.format(file, 14-get_pH(file),get_pH(file))
        plot_lines.append(plot_line)
    plot_string = ''.join(plot_lines)
    plot_string = 'plot'+plot_string
    script_template.append(plot_string)
    with open('np_titration.gp', 'w') as script:
        for line in script_template:
            script.write(line+'\n')
        script.write('set output \n')


def main():
    voltage_list = [x/1000 for x in range(-900, 999, 100)]
    out_header = [['pH', 'I', 'I_pH/I_ctrl']]

    file_list = get_files()
    control_file = get_control_file(file_list)
    print('Detected control file: ' + control_file)
    for voltage in voltage_list:
        out_list = []
        for file in file_list:
            out_list.append([get_pH(file), current_at_voltage(file, voltage), current_ratio(file, control_file, voltage)])
        out_list.sort()
        out_list = out_header+out_list
        out_name = find_np_num(file_list[0])+'_'+str(voltage).replace('.',',')+'V_current'+'.tsv'
        sys.stderr.write(out_name+'\n')
        write_output(out_name, out_list)
    gnuplot_script_builder(file_list)
    print(find_np_num(file_list[0])+'.ods')


if __name__ == "__main__":
    main()

