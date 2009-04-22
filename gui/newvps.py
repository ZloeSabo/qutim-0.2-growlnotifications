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
import thread
import progress
import time
import validate

class newvps:
    def __init__(self, rpcserver, gladefile, parentwin, parentclass):
      self.glade = gtk.glade.XML (gladefile,'winNew')
      self.winNew = self.glade.get_widget('winNew')
      self.winNew.set_transient_for(parentwin)
      self.rpcserver = rpcserver
      self.gladefile = gladefile
      self.vps_list = rpcserver.get_list(0)
      self.parentclass = parentclass
      #register signal callback handlers
      dic = {
	    "on_btnCancel_clicked":self.on_btnCancel_clicked,
            "on_btnCreate_clicked":self.on_btnCreate_clicked
            }

      self.glade.signal_autoconnect (dic)
      self.populate_profile()
      self.populate_templates()

# call back functions
    def on_btnCancel_clicked(self, widget):
        self.winNew.destroy()
        
    def on_btnCreate_clicked(self, widget):
        
        cmbProfile = self.glade.get_widget('cmbProfile')
        cmbTemplate = self.glade.get_widget('cmbTemplate')
        entVPSID = self.glade.get_widget('entVPSID')
        entHostname = self.glade.get_widget('entHostname')
        entIPAddress = self.glade.get_widget('entIPAddress')
        entNameserver = self.glade.get_widget('entNameserver')
        chkOnBoot = self.glade.get_widget('chkOnBoot')
        
        vpsid = entVPSID.get_text()
        hn = entHostname.get_text()
        ns = entNameserver.get_text()
        ip = entIPAddress.get_text()

        treeiter = cmbProfile.get_active_iter()
        listmodel = cmbProfile.get_model()
        profile = listmodel.get_value(treeiter ,0)

        treeiter = cmbTemplate.get_active_iter()
        listmodel = cmbTemplate.get_model()
        template = listmodel.get_value(treeiter ,0)

        if vpsid in self.vps_list:
            dlg = gtk.MessageDialog(self.winNew, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "VPS ID already in use")
            dlg.run()
            dlg.destroy()
            return
            
        if profile.strip() == '':
            dlg = gtk.MessageDialog(self.winNew, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Profile not selected")
            dlg.run()
            dlg.destroy()
            return

        if template.strip() == '':
            dlg = gtk.MessageDialog(self.winNew, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Template not selected")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(entVPSID.get_text()):
            dlg = gtk.MessageDialog(self.winNew, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "VPS ID needs to be numeric")
            dlg.run()
            dlg.destroy()
            return

        if entHostname.get_text().strip() == '':
            dlg = gtk.MessageDialog(self.winNew, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Please set a host name")
            dlg.run()
            dlg.destroy()
            return

        if not validate.validate_ip(entIPAddress.get_text().strip()):
            dlg = gtk.MessageDialog(self.winNew, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "IP address malformed")
            dlg.run()
            dlg.destroy()
            return
        
        if len(ns.strip()) > 0:
            if not validate.validate_ip(ns.strip()):
                dlg = gtk.MessageDialog(self.winNew, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
                                        gtk.BUTTONS_OK , "Name server IP address malformed")
                dlg.run()
                dlg.destroy()
                return
       
        if chkOnBoot.get_active():
            on_boot = 1
        else:
            on_boot = 0

        self.thread_done = 0

        prog = progress.progress(self.gladefile, self.winNew)
        
        thread.start_new(self.do_backend_create_vps, (int(vpsid), profile, template, ip, ns, hn, on_boot))
        while self.thread_done == 0:
            while gtk.events_pending():
                gtk.main_iteration(False)
            prog.pulse()
            time.sleep(.25)

        prog.destroy()

        entVPSID.set_text('')
        entHostname.set_text('')
        entNameserver.set_text('')
        entIPAddress.set_text('')

        self.parentclass.update_vps_info(vpsid)
        self.parentclass.populate_treeview()
        
    def populate_profile(self):    
        configs = self.rpcserver.get_configurations()
        cmbProfile = self.glade.get_widget('cmbProfile')
        
        liststore = gtk.ListStore(str)
        cmbProfile.set_model(liststore)
        cell = gtk.CellRendererText()
        cmbProfile.pack_start(cell, True)
        cmbProfile.add_attribute(cell, 'text', 0)

        if len(configs) == 0:
            dlg = gtk.MessageDialog(self.winNew, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No configs defined.\n Looks like you've got a broken openVZ installation")
            dlg.run()
            dlg.destroy()
            return

        i=0
        for config in configs:
           if config == "vps.basic":
               pos = i
           else:
               i += 1 
           liststore.append([config])

        cmbProfile.set_active(pos)


    def populate_templates(self):
        caches = self.rpcserver.get_template_caches()
        cmbTemplate = self.glade.get_widget('cmbTemplate')
        
        liststore = gtk.ListStore(str)
        cmbTemplate.set_model(liststore)
        cell = gtk.CellRendererText()
        cmbTemplate.pack_start(cell, True)
        cmbTemplate.add_attribute(cell, 'text', 0)

        if len(caches) == 0:
            dlg = gtk.MessageDialog(self.winNew, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK, "No template caches found.\n Please fetch some template caches and install them in /vz/template/cache")
            dlg.run()
            dlg.destroy()
            return

        for cache in caches:
           liststore.append([cache])

        cmbTemplate.set_active(0)
        
    def do_backend_create_vps(self, vpsid, profile, template, ip, ns, hn, on_boot):
        self.rpcserver.create_vps(vpsid, template, profile)
        self.rpcserver.vps_ipadd(vpsid, ip)
        self.rpcserver.set_vps_hostname(vpsid, hn)
        self.rpcserver.set_vps_nameservers(vpsid, ns)
        self.rpcserver.set_vps_on_boot(vpsid, on_boot)
        self.thread_done = 1
        
        # also set thread status here
        
