###########################################################################
#  (c) 2006, Shuveb Hussain <shuveb@binarykarma.com>
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

import gtk
import gtk.glade

class progress:
    def __init__(self, gladefile, parent):
      self.glade = gtk.glade.XML (gladefile,'winProgress')
      self.winProgress = self.glade.get_widget('winProgress')
      self.winProgress.set_transient_for(parent)
      self.pb = self.glade.get_widget('pb')
      self.lbl = self.glade.get_widget('lblTitle')
        
    def pulse(self):
        self.pb.pulse()

    def set_label(self, label):
        self.lbl.set_text(label)

    def set_fraction(self, fraction):
        self.pb.set_fraction(fraction)
            
    def destroy(self):
        self.winProgress.destroy()
