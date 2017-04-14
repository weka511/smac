#{
 transfer.m

 Copyright (C) 2015 Greenweaves Software Pty Ltd

 This is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This software is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; with out even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.
 
 This script calculates the eigenvalues and eigenvectors of the transfer matrix from exercise 1.8,
 and iterates the matrix to show convergence the dumb way.

 #}
TRANSFER=[
  0.5,0.25,0,0.25,0,0,0,0,0;...
  0.25,0.25,0.25,0,0.25,0,0,0,0;...
  0,0.25,0.5,0,0,0.25,0,0,0;...
  0.25,0,0,0.25,0.25,0,0.25,0,0;...
  0,0.25,0,0.25,0,0.25,0,0.25,0;...
  0,0,0.25,0,0.25,0.25,0,0,0.25;...
  0,0,0,0.25,0,0,0.5,0.25,0;...
  0,0,0,0,0.25,0,0.25,0.25,0.25;...
  0,0,0,0,0,0.25,0,0.25,0.5...
  ];

display("Transfer Matrix")
display(TRANSFER)


[EVECTORS,EVALUES]=eig(TRANSFER);

display ("Eigenvalues")
display(sum(EVALUES,2))

display("Eigenvectors")
display(EVECTORS)

product=eye(size(TRANSFER));

for i = 1:100
  product=product*TRANSFER;
  if i%10
    display(product)
  endif
endfor

display(product)
