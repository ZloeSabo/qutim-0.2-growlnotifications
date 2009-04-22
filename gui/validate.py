###########################################################################
#  (c) 2006, Shuveb Hussain <shuveb@binarykarma.com>
#  (c) 2006, Binary Karma
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111, USA.
##########################################################################

def isnum(x):
    try:
        int(x)
        return 1
    except:
        return 0

def validate_ip(ip):
    ip = ip.split('.')

    if len(ip) < 4:
        return False

    for part in ip:
        if not isnum(part): return False
        if int(part)<0 or int(part)>254: return False

    return True

            
