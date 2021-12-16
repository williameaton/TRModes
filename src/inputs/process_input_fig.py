from inputs.process_inputs import str2array, add2log, add2log_break


def process_input_fig(str_in):

    """
    Processes the users' inputs regarding the figure outputs and returns figure and axis specifications including figure name,
    axes list, N and L values, and plot type.

    :param str_in: Figure output information. (e.g."figure1: 121 2D_radial_plot L4 N2; 122 dispersion L1,2,3 N[1][1,2][1,2,3]")
    :type str_in: string

    """

    # If there is a filename inputed, separate the output file name and store 
    if (str_in.find(":") != 1):
        fname_sep = str_in.split(":")
        fname_out = fname_sep[0]
        start = 1
    else:
        fname_sep = str_in
        fname_out = None
        start = 0

        
    #---------------------------------------------------------------------------------------------------------------------- 
    # Separate figure specifications
    
    ax_list=[]; ptype=[]; L=[]; N=[]
    # Run through the remaining input
    for i in range(start, len(fname_sep)):
        fig_sep = fname_sep[i].split(";")
        for k in range(0,len(fig_sep)):
            ax_sep = fig_sep[k].split(" ")
            # Removes empty strings
            new_axsep = [j for j in ax_sep if j]

            # Store values
            ax_list.append(new_axsep[0])
            ptype.append(new_axsep[1].lower())


            # Remove N and L identifier
            l = new_axsep[2].replace('L','')
            l_temp = n.replace('[','').replace(']','')
            if len(l_temp) > 1:
                # If there is more than one value                                                      
                if '-' in l_temp:
                    l_array = str2array(l_temp,'-')
                    l_values = range(l_array[0], l_array[1]+1)
                else:
                    l_values = str2array(l_temp,',')
            else:
                l_values = [float(l)]  


            # Apply the same n values for each l
            if "n_all" in new_axsep[3].lower():
                n = new_axsep[3].lower().replace('n_all','')
                n_temp = n.replace('[','').replace(']','')
                if len(n) > 1:
                    # If there is more than a single value
                    if '-' in n:
                        n_array = sorted(str2array(n_temp,'-'))
                        n_val = range(n_array[0], n_array[1]+1)
                    else:
                        n_val = str2array(n_temp,',')
                else:
                    n_val = float(n)

                # Create sublists with the same n values for each l
                n_values = [[]] * len(l_values)
                for i in range(0,len(l_values)):
                    n_values[i] =[* n_val]


            # Apply different n values for each l
            else:
                n = new_axsep[3].replace('N','')
                if len(n) > 1:
                    # If there is more than a single value
                    n_rep = n.replace('[','').replace(']',' ').split(' ')
                    # Removes empty strings
                    new_n = [j for j in n_rep if j]
                    n_values = []
                    for i in range(len(new_n)):
                        # Appends an empty sublist inside the list that can be filled later
                        n_values.append([])
                        n_list = str2array(new_n[i],',')
                        for k in range(len(n_list)):
                            # Fill list with sublists
                            n_values[i].append(n_list[k])
                else:
                    n_values = [float(n)]

                    
            # Store n and l values
            L.append(l_values)
            N.append(n_values)

            
    #---------------------------------------------------------------------------------------------------------------------- 
    # Check if all inputs are valid
    assert len(L) == len(N), \
        'Error: Must have corresponding number of n and l values. See Readme for details. \n'
    # Check all N and L values are zero or greater and integers                                             
    assert all(isinstance(x, int) for x in N), 'N values must be integers. \n'
    assert all(n >= 0 for n in N), 'N values must be zero or greater. \n'
    assert all(isinstance(x, int) for x in L), 'L values must be integers. \n'
    assert all(l >= 0 for l in L), 'L values must be zero or greater. \n'
    # Check is plot type exists                                                                             
    assert ptype == 'dispersion' or ptype == 'radial_2d_plot' or ptype == 'radial_2D_surface' or ptype == '3D_animated', \
        'Plot type does not exist. See Readme for details. \n'

    
    #----------------------------------------------------------------------------------------------------------------------
    # Add figure values to log
    add2log("Figure Name", fname_out,1)
    for j in range(0,ax_list):
        add2log("Axis", ax_list[j],1)
        add2log("ptype", ptype[j],1)
        add2log("L", L[j],1)
        add2log("N", N[j],1)
        add2log_break("s")
        
    add2log_break("l")


    
    return fname_out, ax_list, L, N, ptype
