# Last modified pdabney@princeton.edu, 12/12/21

from process_inputs import str2array, add2log, add2log_line


def process_input_fig(str_in):
    # =======================================================================================           
    # DESCRIPTION:                                                                                     
    #   Processes the users input regarding the output figure(s).
    #                                                                                                 
    # INPUT:                                                                                         
    #    str_in         - String of the figure output information. (e.g. "figure1: 121 2D_radial
    #                     L4 N2; 122 dispersion L1,2,3 N[1][1,2][1,2,3]")
    # OUTPUT:
    #    fname_out      - File name of figure(s). Variable is set to None if no name is specified.
    #    ax_list        - List of figure axes. (e.g. ['121','122'])
    #    L              - Angular order value(s). (format: 'L4' or 'L1,2,3,4' or L1-5)
    #    N              - Radial order value(s). (format: 'N3' or 'N[1][3,4][1,2,3,4]' or  'N[1-6]'
    #                    N_all[5]')
    #    ptype          - Plot type: 'toroidal'
    # =======================================================================================  
 
    if (str_in.find(":") != 1):
        # Separate the output file name and store
        fname_sep = str_in.split(":")
        fname_out = fname_sep[0]
        start = 1
    else:
        fname_sep = str_in
        fname_out = None
        start = 0

    # Run through the remaining input
    ax_list=[]
    ptype=[]
    L=[]
    N=[]
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
            if len(l) > 1:
                # If there is more than one value                                                      
                if '-' in l:
                    l_array = str2array(l,'-')
                    l_values = range(l_array[0], l_array[1]+1)
                else:
                    l_values = str2array(l,',')
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


    # Check if all inputs are valid
    assert len(L) == len(N), \
        'Error: Must have corresponding number of n and l values. See Readme for details. \n'
    # Check all N and L values are zero or greater and integers                                             
    assert all(isinstance(x, int) for x in N), 'N values must be integers. \n'
    assert N >= 0, 'N values must be zero or greater. \n'
    assert all(isinstance(x, int) for x in L), 'L values must be integers. \n'
    assert L >= 0, 'L values must be zero or greater. \n'
    # Check is plot type exists                                                                             
    assert ptype == 'dispersion' or ptype == 'radial_2d_plot' or ptype == 'radial_2D_surface' or ptype == '3D_animated', \
        'Plot type does not exist. See Readme for details. \n'


    # Add figure values to log
    add2log("Figure Name", fname_out)
    for j in range(0,ax_list):
        add2log("Axis", ax_list[j])
        add2log("ptype", ptype[j])
        add2log("L", L[j])
        add2log("N", N[j])
        add2log("\n", "")

    add2log_line()
    
    return fname_out, ax_list, L, N, ptype
