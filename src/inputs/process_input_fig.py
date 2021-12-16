from inputs.process_inputs import str2array, add2log, add2log_break


def process_input_fig(str_in):
    """                                                                                                                                      
    Processes the users inputs regarding the figure outputs and returns figure and axis specifications including figure name,               
    axes list, N and L values, and plot type.                                                                                                


    :param str_in: Figure output information. (e.g."figure1: 121 2D_radial_plot L4 N2 M4; 122 dispersion L[1,2,3] N[1][1,2][1,2,3]")         
    :type str_in: string
    
    """  

     # If there is a filename inputed, separate the output file name and store
    if str_in.find(":") != 1:
        fname_sep = str_in.split(":")
        fname_out = fname_sep[0]
        start = 1
    else:
        fname_sep = str_in
        fname_out = None
        start = 0

    # Separate figure specifications
    ax_list = []
    ptype = []
    L = []
    N = []
    M = []
    # Run through the remaining input
    for i in range(start, len(fname_sep)):
        fig_sep = fname_sep[i].split(";")
        for k in range(len(fig_sep)):
            ax_sep = fig_sep[k].split(" ")
            # Removes empty strings
            new_axsep = [j for j in ax_sep if j]
            
            # Store values for ax and plot type
            ax_list.append(int(new_axsep[0]))
            ptype.append(new_axsep[1].lower())

            # Check if plot type exists
            assert ptype[k] == 'dispersion' or ptype[k] == '2d_radial' or ptype[k] == '2d_surface' or ptype[k] == '3d_animated','Plot type does not exist. See\
 Readme for details. \n'
            
            # For all plot types
            l = new_axsep[2].replace('L', '')

            # If its NOT a dispersion plot
            if ptype[k] != 'dispersion':
                l_values = [eval(x) for x in l]
                n = new_axsep[3].replace('N', '')
                n_values = [eval(x) for x in n]
                m = new_axsep[4].replace('M', '')
                m_values = [eval(x) for x in m]

                # Check m values    
                assert all(isinstance(x, int) for x in m_values), 'M values must be integers. \n'                                                               
                assert all(m >= 0 for m in m_values), 'M values must be zero or greater. \n'  

            # If its a dispersion plot
            elif ptype[k] == 'dispersion':
                # L values
                m_values = None
                l_temp = l.replace('[', '').replace(']', '')
                if len(l_temp) > 1:
                    # If there is more than one value
                    if '-' in l_temp:
                        l_array = str2array(l_temp, '-')
                        l_values = [*range(l_array[0], l_array[1] + 1)]
                    else:
                        l_values = str2array(l_temp, ',')
                else:
                    l_values = [eval(x) for x in l]

                # N values
                # Apply the same n values for each l
                if "n_all" in new_axsep[3].lower():
                    n = new_axsep[3].lower().replace('n_all', '')
                    n_temp = n.replace('[', '').replace(']', ' ').split(' ')
                    new_n = [j for j in n_temp if j]

                    # Create sublists with the same n values for each l
                    n_values = [[]] * len(l_values)
                    if len(new_n[0]) > 1:
                        # If there is more than a single value
                        if new_n[0].find("-") == 1:
                            n_array = sorted(str2array(new_n[0], '-'))
                            n_val = [*range(n_array[0], n_array[1] + 1)]
                        else:
                            n_val = str2array(new_n[0], ',')

                    else:
                        n_val = [eval(x) for x in new_n]

                    for j in range(len(l_values)):
                        n_values[j] = n_val
                    
                # Apply different n values for each l
                else:
                    n = new_axsep[3].replace('N', '')
                    if len(n) > 1:
                        n_rep = n.replace('[', '').replace(']', ' ').split(' ')
                        new_n = [j for j in n_rep if j]
                        n_values = []
                        for i in range(len(new_n)):
                            if new_n[i].find("-") == 1:
                                n_array = sorted(str2array(new_n[i], '-'))
                                n_list = [*range(n_array[0], n_array[1] + 1)]
                            else:
                                n_list = str2array(new_n[i], ',')
                            n_values.append(n_list)
                    else:
                        n_values = [eval(x) for x in n]

            # Store n, l and m values
            L.append(l_values)
            N.append(n_values)
            M.append(m_values)

            # Check if all inputs are valid                                                                                                    
            assert len(l_values) == len(n_values),'Error: Must have corresponding number of n and l values. See Readme for details. \n'       
            # Check all N and L values are zero or greater and integers                                                                        
            #assert all(isinstance(x, int) for x in n_values), 'N values must be integers. \n'                                                  
            #assert all(n >= 0 for n in n_values), 'N values must be zero or greater. \n'                                                  
            assert all(isinstance(x, int) for x in l_values), 'L values must be integers. \n'                                            
            assert all(l >= 0 for l in l_values), 'L values must be zero or greater. \n'

    #---------------------------------------------------------------------------------------------------------------------- 
    # Add figure specifications to the input log
    add2log("Figure Name", fname_out,1)                                                                                                      
    add2log_break("s")
    for j in range(0,len(ax_list)):                                                                                                            
        add2log("Axis", ax_list[j],1)                                                                                                        
        add2log("ptype", ptype[j],1)                                                                                                         
        add2log("L", L[j],1)                                                                                                                 
        add2log("N", N[j],1)                                                                                                                 
        add2log("M", M[j],1)                                                                                                                
        add2log_break("s")                                                                                                                   
    add2log_break("l")

    return fname_out, ax_list, L, N, M, ptype

