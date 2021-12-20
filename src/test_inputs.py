import inputs.process_inputs as process_input
import inputs.process_input_fig as process_fig
import numpy as np
import os

# Note because of import errors, tests are in this directory, rather than the tests directory.
# More test should be included in the future for process_inputs, including for a model_file


# Fromt process_input_fig
def test_process_ax1_noname():
    fig1 = '111 2d_surface L2 N4 M4'
    f_out, ax, L, N, M, ptype = process_fig.process_input_fig(fig1)
    assert f_out == None
    assert ax == [111]
    assert ptype == ['2d_surface']
    assert L[0] == [2]
    assert N[0] == [4]
    assert M[0] == [4]
    
    # Running tests results in a log file to be created                                                        
    # Remove 'input_log.txt' from test                                                                         
    if os.path.exists('input_log.txt'):
        os.remove('input_log.txt')

        
def test_process_ax1_name():
    fig1 = 'Figure1: 111 2d_radial L4 N2 M2'
    f_out, ax, L, N, M, ptype = process_fig.process_input_fig(fig1)
    assert f_out == 'Figure1'
    assert ax == [111]
    assert ptype == ['2d_radial']
    assert L[0] == [4]
    assert N[0] == [2]
    assert M[0] == [2]

    # Running tests results in a log file to be created                                                        
    # Remove 'input_log.txt' from test                                                                         
    if os.path.exists('input_log.txt'):
        os.remove('input_log.txt')


def test_process_ax2_name():
    fig1 = 'Figure1: 121 2d_radial L4 N2 M2; 122 2d_radial L2 N6 M2'
    f_out, ax, L, N, M, ptype = process_fig.process_input_fig(fig1)
    assert f_out == 'Figure1'
    assert ax == [121, 122]
    assert ptype == ['2d_radial', '2d_radial']
    assert L == [[4], [2]]
    assert N == [[2], [6]]
    assert M == [[2], [2]]

    # Running tests results in a log file to be created                                                        
    # Remove 'input_log.txt' from test                                                                         
    if os.path.exists('input_log.txt'):
        os.remove('input_log.txt')

        
def test_process_ax1_disp():
    fig1 = 'Figure1: 111 dispersion L[1,2,3] N[1][1,2][1,2,3]'
    f_out, ax, L, N, M, ptype = process_fig.process_input_fig(fig1)
    assert f_out == 'Figure1'
    assert ax == [111]
    assert ptype == ['dispersion']
    assert L[0] == [1, 2, 3]
    assert N[0] == [[1], [1,2], [1,2,3]]
    assert M[0] == None

    # Running tests results in a log file to be created                                                        
    # Remove 'input_log.txt' from test                                                                         
    if os.path.exists('input_log.txt'):
        os.remove('input_log.txt')    

        
def test_process_ax1_disp_all():
    fig1 = 'Figure1: 111 dispersion L[2-4] N_all[2-6]'
    f_out, ax, L, N, M, ptype = process_fig.process_input_fig(fig1)
    assert f_out == 'Figure1'
    assert ax == [111]
    assert ptype == ['dispersion']
    assert L[0] == [2, 3, 4]
    assert N[0] == [[2, 3, 4, 5, 6], [2, 3, 4, 5, 6], [2, 3, 4, 5, 6]]
    assert M[0] == None

    # Running tests results in a log file to be created                                                    
    # Remove 'input_log.txt' from test                                                                         
    if os.path.exists('input_log.txt'):
        os.remove('input_log.txt')



# From process_inputs
def test_str2array():
    output = process_input.str2array('1,2,3,4,5',',')
    assert output == [1, 2, 3, 4, 5]


def test_nearest():
    output, index = process_input.nearest([2, 4, 6, 8, 10], 5)
    assert output == 4 and index == 1


def test_evalEQ():
    output = process_input.eval_equation('1+2*r+r**2', 0, 10, 2)
    assert output == [1, 9, 25, 49, 81]


def test_process_inputs_eq1():
    class ExClass:
        n = ['2,3']
        l = ['4,5,6']
        nrange = None
        lrange = None
        figure_output = None
        output_file = None
        model_file = None
        eq_vp = None
        eq_rho = ['4380']
        eq_vs = ['5930']
        r_min = ['2891000']
        r_max = ['6371000']
        Nr = ['10']
        mode_type = ['toroidal']
        int_method = ['euler']

    inputs = ExClass()
    test_class = process_input.process_inputs(inputs)
    assert test_class.mtype == 'toroidal'
    assert test_class.method == 'euler'
    assert test_class.l == [4, 5, 6]
    assert test_class.n == [2, 3]
    assert test_class.rho == [4380, 4380, 4380, 4380, 4380, 4380, 4380, 4380, 4380, 4380]
    assert test_class.mu == [154022262000, 154022262000, 154022262000, 154022262000, 154022262000, 154022262000, 154022262000, 154022262000, 154022262000, 154022262000]
    assert test_class.rr == [2891000., 3239000., 3587000., 3935000., 4283000., 4631000., 4979000., 5327000., 5675000., 6023000., 6371000.]
    assert test_class.dr == [348000.0, 348000.0, 348000.0, 348000.0, 348000.0, 348000.0, 348000.0, 348000.0, 348000.0, 348000.0]

    # Running tests results in a log file to be created                                                    
    # Remove 'input_log.txt' from test                                                                         
    if os.path.exists('input_log.txt'):
        os.remove('input_log.txt')
    
    
def test_process_inputs_eq2():
    class ExClass:
        nrange = ['2,5']
        lrange = ['4,6']
        n = None
        l = None
        figure_output = None
        output_file = None
        model_file = None
        eq_vp = None
        eq_rho = ['2*r+r**2']
        eq_vs = ['r+3680']
        r_min = ['3891000']
        r_max = ['5371000']
        Nr = ['10']
        mode_type = ['toroidal']
        int_method = ['rk4']

    inputs = ExClass()
    test_class = process_input.process_inputs(inputs)
    
    assert test_class.mtype == 'toroidal'
    assert test_class.method == 'rk4'
    assert test_class.l == [4, 5, 6]
    assert test_class.n == [2, 3, 4, 5]

    # Running tests results in a log file to be created                                                        
    # Remove 'input_log.txt' from test                                                                        
    if os.path.exists('input_log.txt'):
        os.remove('input_log.txt')
