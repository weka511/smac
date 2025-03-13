#!/usr/bin/env python

# Copyright (C) 2022-2025 Simon Crase

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

'''
    Generate Gray Codes
'''

def create_gray_codes(N):
    '''
        Create a list of k-bit Gray codes

        Parameters:
            N    Number of bits

        Returns: A list, each element being a binary number.
    '''
    k = 1
    product = [[0],[1]]

    # Stating with a list for k==1, generate lists for k==2, 3, etc, by:
    # a) prepending 0 to each member of list; and
    # b) reversing the klist, and prependong 1 to each member.
    while k < N:
        product = [[0] + code for code in product] + [[1] + code for code in product[::-1]]
        k += 1

    return product

if __name__ == '__main__':
    for gray_code in create_gray_codes(4):
        print (gray_code)
