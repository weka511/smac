Emax = 50
            
States=[((E_x + E_y + E_z), (E_x, E_y, E_z)) for E_x in range(Emax) for E_y in range(Emax) for E_z in range(Emax)]

States.sort()

for k in range(Emax):
    E,(E_x,E_y,E_z)=States[k]
    print ('{0:3d}: {1} {{{2}, {3}, {4}}}'.format(k,E,E_x,E_y,E_z))
