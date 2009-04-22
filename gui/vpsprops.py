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

import gtk
import gtk.glade
import thread
import progress
import validate
import time

class vpsprops:
    def __init__(self, vpsid, vps_details, rpcserver, gladefile, parentwin, parentclass):
        self.glade = gtk.glade.XML (gladefile,'winProperties')
        self.winProp = self.glade.get_widget('winProperties')
        self.winProp.set_transient_for(parentwin)
        self.rpcserver = rpcserver
        self.gladefile = gladefile
        self.vpsid = vpsid
        self.vps_details = vps_details
        self.parentclass = parentclass

        #print vps_details
        #register signal callback handlers

        dic = {
            "on_btnDeleteIP_clicked": self.on_btnDeleteIP_clicked,
            "on_btnAddIP_clicked": self.on_btnAddIP_clicked,
            "on_btnSaveHostname_clicked": self.on_btnSaveHostname_clicked,
            "on_btnDeleteNS_clicked": self.on_btnDeleteNS_clicked,
            "on_btnAddNS_clicked":self.on_btnAddNS_clicked,
            "on_btnClose_clicked":self.on_btnClose_clicked,
            "on_btnNetAdvSave_clicked":self.on_btnNetAdvSave_clicked,
            "on_btnMemSave_clicked":self.on_btnMemSave_clicked,
            "on_btnMiscSave_clicked":self.on_btnMiscSave_clicked,
            "on_btnChangePasswd_clicked":self.on_btnChangePasswd_clicked,
            "on_btnAddUser_clicked":self.on_btnAddUser_clicked,
            "on_btnCPUSave_clicked":self.on_btnCPUSave_clicked
            }

        self.glade.signal_autoconnect (dic)

        # fill up the VPS properties
        self.fill_properties()

    def on_btnNetAdvSave_clicked(self, widget):
        # Validate numtcpsock
        if not validate.isnum(self.numtcpsock_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of TCP Sockets: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.numtcpsock_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of TCP Sockets: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.numtcpsock_b.get_text()) > int(self.numtcpsock_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of TCP Sockets:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return
        # Validate tcpsendbuf
        if not validate.isnum(self.tcpsndbuf_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "TCP send buf size: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.tcpsndbuf_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "TCP send buf size: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.tcpsndbuf_b.get_text()) > int(self.tcpsndbuf_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "TCP send buf size:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate tcprcvbuf
        if not validate.isnum(self.tcprcvbuf_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "TCP recv buf size: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.tcprcvbuf_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "TCP recv buf size: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.tcprcvbuf_b.get_text()) > int(self.tcprcvbuf_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "TCP recv buf size:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate othersockbuf
        if not validate.isnum(self.othersockbuf_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Other socket buf size: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.othersockbuf_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Other socket buf size: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.othersockbuf_b.get_text()) > int(self.othersockbuf_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Other socket buf size:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate dgramrcvbuf
        if not validate.isnum(self.dgramrcvbuf_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "UDP rcv buf size: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.dgramrcvbuf_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "UDP rcv buf size: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.dgramrcvbuf_b.get_text()) > int(self.dgramrcvbuf_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "UDP rcv buf size:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate numothersock
        if not validate.isnum(self.numothersock_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of other sockets: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.numothersock_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of other sockets: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.numothersock_b.get_text()) > int(self.numothersock_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of other sockets:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        self.rpcserver.set_vps_numtcpsock(self.vpsid, int(self.numtcpsock_b.get_text()),\
                                          int(self.numtcpsock_l.get_text()))
        self.rpcserver.set_vps_tcpsndbuf(self.vpsid, int(self.tcpsndbuf_b.get_text()),\
                                          int(self.tcpsndbuf_l.get_text()))
        self.rpcserver.set_vps_tcprcvbuf(self.vpsid, int(self.tcprcvbuf_b.get_text()),\
                                          int(self.tcprcvbuf_l.get_text()))
        self.rpcserver.set_vps_othersockbuf(self.vpsid, int(self.othersockbuf_b.get_text()),\
                                          int(self.othersockbuf_l.get_text()))
        self.rpcserver.set_vps_dgramrcvbuf(self.vpsid, int(self.dgramrcvbuf_b.get_text()),\
                                          int(self.dgramrcvbuf_l.get_text()))
        self.rpcserver.set_vps_numothersock(self.vpsid, int(self.numothersock_b.get_text()),\
                                          int(self.numothersock_l.get_text()))
        
    def on_btnMemSave_clicked(self, widget):
        # Validate kmemsize
        if not validate.isnum(self.kmemsize_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Kernel mem size: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.kmemsize_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Kernel mem size: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.kmemsize_b.get_text()) > int(self.kmemsize_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Kernel mem size:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate lockedpages
        if not validate.isnum(self.lockedpages_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Locked pages: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.lockedpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Locked pages: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.lockedpages_b.get_text()) > int(self.lockedpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Locked pages:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate lockedpages
        if not validate.isnum(self.privvmpages_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Private VM pages: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.privvmpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Private VM pages: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.privvmpages_b.get_text()) > int(self.privvmpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Private VM pages:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate shmpages
        if not validate.isnum(self.shmpages_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Shared memory pages: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.shmpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Shared memory pages: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.shmpages_b.get_text()) > int(self.shmpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Shared memory pages:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate physpages
        if not validate.isnum(self.physpages_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Physical memory pages: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.physpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Physical memory pages: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.physpages_b.get_text()) > int(self.physpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Physical memory pages:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate vmguarpages
        if not validate.isnum(self.vmguarpages_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "VM guar pages: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.vmguarpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "VM guar pages: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.vmguarpages_b.get_text()) > int(self.vmguarpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "VM guar pages:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate oomguarpages
        if not validate.isnum(self.oomguarpages_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "OOM guar pages: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.oomguarpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "OOM guar pages: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.oomguarpages_b.get_text()) > int(self.oomguarpages_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "OOM guar pages:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate dcachesize
        if not validate.isnum(self.dcachesize_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Disk cache size: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.dcachesize_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Disk cache size: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.dcachesize_b.get_text()) > int(self.dcachesize_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Disk cache size:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return
        
        self.rpcserver.set_vps_kmemsize(self.vpsid, int(self.kmemsize_b.get_text()), \
                                        int(self.kmemsize_l.get_text()))
        self.rpcserver.set_vps_lockedpages(self.vpsid, int(self.lockedpages_b.get_text()), \
                                        int(self.lockedpages_l.get_text()))
        self.rpcserver.set_vps_privvmpages(self.vpsid, int(self.privvmpages_b.get_text()), \
                                        int(self.privvmpages_l.get_text()))
        self.rpcserver.set_vps_shmpages(self.vpsid, int(self.shmpages_b.get_text()), \
                                        int(self.shmpages_l.get_text()))
        self.rpcserver.set_vps_physpages(self.vpsid, int(self.physpages_b.get_text()), \
                                        int(self.physpages_l.get_text()))
        self.rpcserver.set_vps_vmguarpages(self.vpsid, int(self.vmguarpages_b.get_text()), \
                                        int(self.vmguarpages_l.get_text()))
        self.rpcserver.set_vps_oomguarpages(self.vpsid, int(self.oomguarpages_b.get_text()), \
                                        int(self.oomguarpages_l.get_text()))
        self.rpcserver.set_vps_dcachesize(self.vpsid, int(self.dcachesize_b.get_text()), \
                                        int(self.dcachesize_l.get_text()))

    def on_btnMiscSave_clicked(self, widget):
        # Validate numflock
        if not validate.isnum(self.numflock_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of file locks: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.numflock_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of file locks: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.numflock_b.get_text()) > int(self.numflock_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of file locks:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate numpty
        if not validate.isnum(self.numpty_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of PTYs: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.numpty_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of PTYs: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.numpty_b.get_text()) > int(self.numpty_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of PTYs:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate numfile
        if not validate.isnum(self.numfile_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of open files: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.numfile_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of open files: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.numfile_b.get_text()) > int(self.numfile_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of open files:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate numsiginfo
        if not validate.isnum(self.numsiginfo_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of SIGINFO: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.numsiginfo_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of SIGINFO: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.numsiginfo_b.get_text()) > int(self.numsiginfo_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of SIGINFO:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return

        # Validate numiptent
        if not validate.isnum(self.numiptent_b.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of IPTENT: Barrier wrong.")
            dlg.run()
            dlg.destroy()
            return

        if not validate.isnum(self.numiptent_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of IPTENT: Limit wrong.")
            dlg.run()
            dlg.destroy()
            return

        if int(self.numiptent_b.get_text()) > int(self.numiptent_l.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No of IPTENT:\nBarrier can't be greater than limit")
            dlg.run()
            dlg.destroy()
            return
        
        self.rpcserver.set_vps_numflock(self.vpsid, int(self.numflock_b.get_text()), \
                                        int(self.numflock_l.get_text()))
        self.rpcserver.set_vps_numpty(self.vpsid, int(self.numpty_b.get_text()), \
                                        int(self.numpty_l.get_text()))
        self.rpcserver.set_vps_numfile(self.vpsid, int(self.numfile_b.get_text()), \
                                        int(self.numfile_l.get_text()))
        self.rpcserver.set_vps_numsiginfo(self.vpsid, int(self.numsiginfo_b.get_text()), \
                                        int(self.numsiginfo_l.get_text()))
        self.rpcserver.set_vps_numiptent(self.vpsid, int(self.numiptent_b.get_text()), \
                                        int(self.numiptent_l.get_text()))
        
    def on_btnChangePasswd_clicked(self, widget):
        if self.ent_passwd.get_text() != self.ent_confirm_passwd.get_text():
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Change password: Passwords don't match")
            dlg.run()
            dlg.destroy()

        #checking one is enough, since we have already checked equality
        if self.ent_passwd.get_text().strip() == '':
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Change password: Password field can't be blank")
            dlg.run()
            dlg.destroy()

        treeiter = self.cmb_user_name.get_active_iter()
        listmodel = self.cmb_user_name.get_model()
        username = listmodel.get_value(treeiter, 0)

        self.rpcserver.set_vps_user_pass(self.vpsid, username, self.ent_passwd.get_text())

        dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, \
        gtk.BUTTONS_OK , "Request processed")
        dlg.run()
        dlg.destroy()

    def on_btnAddUser_clicked(self, widget):
        if self.ent_passwd_new.get_text() != self.ent_confirm_passwd_new.get_text():
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Add new user: Passwords don't match")
            dlg.run()
            dlg.destroy()

        #checking one is enough, since we have already checked for equality
        if self.ent_passwd_new.get_text().strip() == '':
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Add new user: Password field can't be blank")
            dlg.run()
            dlg.destroy()

        self.rpcserver.set_vps_user_pass(self.vpsid, self.ent_user_new.get_text(), \
                                         self.ent_passwd_new.get_text())

        dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, \
        gtk.BUTTONS_OK , "Request processed")
        dlg.run()
        dlg.destroy()

        # clear once done
        self.ent_user_new.set_text('')
        self.ent_passwd_new.set_text('')
        self.ent_confirm_passwd_new.set_text('')

    def on_btnClose_clicked(self, widget):
        self.parentclass.update_vps_info(self.vpsid)
        self.parentclass.populate_treeview()
        self.winProp.destroy()

    def on_btnCPUSave_clicked(self, widget):
        #FIXME do the validation here, dude

        if(self.sb_max_procs_lim.get_value() < self.sb_max_procs_bar.get_value()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "Number of processes:\nBarrier can't be greater than Limit.\nCan be equal, if you please.")
            dlg.run()
            dlg.destroy()
        
        self.rpcserver.set_vps_cpuunits(self.vpsid, int(self.hs_min_cpu.get_value()))
        self.rpcserver.set_vps_cpulimit(self.vpsid, int(self.hs_max_cpu.get_value()))
        self.rpcserver.set_vps_numproc(self.vpsid, int(self.sb_max_procs_bar.get_text()),\
                                       int(self.sb_max_procs_lim.get_text()))

    def on_btnDeleteIP_clicked(self, widget):
        ip = self.get_selected_ip()
        if ip == 0:
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "IP not selected.\nPlease select one from the list.")
            dlg.run()
            dlg.destroy()
            return
        
        self.rpcserver.vps_ipdel(self.vpsid, ip)
        selection = self.ip_tv.get_selection()
        (model, iter) = selection.get_selected()
        if iter == None: return 0
        model.remove(iter)
               
    def fill_ips(self):
        ips = self.vps_details['ips']
        # get the Treeview and set its model
        self.ip_list_store = gtk.ListStore(str)
        self.ip_tv = self.glade.get_widget('tvIP')
        self.ip_tv.set_model(self.ip_list_store)

        # create a cell renderer and column
        # add that to the treeview
        self.cellIP = gtk.CellRendererText()
        self.tvip_col = gtk.TreeViewColumn('', self.cellIP, text = 0)
        self.ip_tv.append_column(self.tvip_col)
 
        for ip in ips:
             self.ip_list_store.append([ip])
             
    def fill_nameservers(self):
        servers = self.vps_details['nameservers']
        #get the Treeview and set its model
        self.ns_list_store = gtk.ListStore(str)
        self.ns_tv = self.glade.get_widget('tvNS')
        self.ns_tv.set_model(self.ns_list_store)

        # create a cell renderer and column
        # add that to the treeview
        self.cellNS = gtk.CellRendererText()
        self.tvns_col = gtk.TreeViewColumn('', self.cellNS, text = 0)
        self.ns_tv.append_column(self.tvns_col)

        for server in servers:
            self.ns_list_store.append([server])

    def fill_net_advanced(self):
        self.numtcpsock_b = self.glade.get_widget('numtcpsock.b')
        self.numtcpsock_b.set_text(self.vps_details['numtcpsock.b'])
        self.numtcpsock_l = self.glade.get_widget('numtcpsock.l')
        self.numtcpsock_l.set_text(self.vps_details['numtcpsock.l'])

        self.tcpsndbuf_b = self.glade.get_widget('tcpsndbuf.b')
        self.tcpsndbuf_b.set_text(self.vps_details['tcpsndbuf.b'])
        self.tcpsndbuf_l = self.glade.get_widget('tcpsndbuf.l')
        self.tcpsndbuf_l.set_text(self.vps_details['tcpsndbuf.l'])

        self.tcprcvbuf_b = self.glade.get_widget('tcprcvbuf.b')
        self.tcprcvbuf_b.set_text(self.vps_details['tcprcvbuf.b'])
        self.tcprcvbuf_l = self.glade.get_widget('tcprcvbuf.l')
        self.tcprcvbuf_l.set_text(self.vps_details['tcprcvbuf.l'])

        self.othersockbuf_b = self.glade.get_widget('othersockbuf.b')
        self.othersockbuf_b.set_text(self.vps_details['othersockbuf.b'])
        self.othersockbuf_l = self.glade.get_widget('othersockbuf.l')
        self.othersockbuf_l.set_text(self.vps_details['othersockbuf.l'])

        self.dgramrcvbuf_b = self.glade.get_widget('dgramrcvbuf.b')
        self.dgramrcvbuf_b.set_text(self.vps_details['dgramrcvbuf.b'])
        self.dgramrcvbuf_l = self.glade.get_widget('dgramrcvbuf.l')
        self.dgramrcvbuf_l.set_text(self.vps_details['dgramrcvbuf.l'])

        self.numothersock_b = self.glade.get_widget('numothersock.b')
        self.numothersock_b.set_text(self.vps_details['numothersock.b'])
        self.numothersock_l = self.glade.get_widget('numothersock.l')
        self.numothersock_l.set_text(self.vps_details['numothersock.l'])

    def fill_mem_info(self):
        
        self.kmemsize_b = self.glade.get_widget('kmemsize.b')
        self.kmemsize_b.set_text(self.vps_details['kmemsize.b'])
        self.kmemsize_l = self.glade.get_widget('kmemsize.l')
        self.kmemsize_l.set_text(self.vps_details['kmemsize.l'])

        self.lockedpages_b = self.glade.get_widget('lockedpages.b')
        self.lockedpages_b.set_text(self.vps_details['lockedpages.b'])
        self.lockedpages_l = self.glade.get_widget('lockedpages.l')
        self.lockedpages_l.set_text(self.vps_details['lockedpages.l'])

        self.privvmpages_b = self.glade.get_widget('privvmpages.b')
        self.privvmpages_b.set_text(self.vps_details['privvmpages.b'])
        self.privvmpages_l = self.glade.get_widget('privvmpages.l')
        self.privvmpages_l.set_text(self.vps_details['privvmpages.l'])

        self.shmpages_b = self.glade.get_widget('shmpages.b')
        self.shmpages_b.set_text(self.vps_details['shmpages.b'])
        self.shmpages_l = self.glade.get_widget('shmpages.l')
        self.shmpages_l.set_text(self.vps_details['shmpages.l'])

        self.physpages_b = self.glade.get_widget('physpages.b')
        self.physpages_b.set_text(self.vps_details['physpages.b'])
        self.physpages_l = self.glade.get_widget('physpages.l')
        self.physpages_l.set_text(self.vps_details['physpages.l'])
        
        self.vmguarpages_b = self.glade.get_widget('vmguarpages.b')
        self.vmguarpages_b.set_text(self.vps_details['vmguarpages.b'])
        self.vmguarpages_l = self.glade.get_widget('vmguarpages.l')
        self.vmguarpages_l.set_text(self.vps_details['vmguarpages.l'])

        self.oomguarpages_b = self.glade.get_widget('oomguarpages.b')
        self.oomguarpages_b.set_text(self.vps_details['oomguarpages.b'])
        self.oomguarpages_l = self.glade.get_widget('oomguarpages.l')
        self.oomguarpages_l.set_text(self.vps_details['oomguarpages.l'])

        self.dcachesize_b = self.glade.get_widget('dcachesize.b')
        self.dcachesize_b.set_text(self.vps_details['dcachesize.b'])
        self.dcachesize_l = self.glade.get_widget('dcachesize.l')
        self.dcachesize_l.set_text(self.vps_details['dcachesize.l'])

    def fill_misc_info(self):
        self.numflock_b = self.glade.get_widget('numflock.b')
        self.numflock_b.set_text(self.vps_details['numflock.b'])
        self.numflock_l = self.glade.get_widget('numflock.l')
        self.numflock_l.set_text(self.vps_details['numflock.l'])

        self.numpty_b = self.glade.get_widget('numpty.b')
        self.numpty_b.set_text(self.vps_details['numpty.b'])
        self.numpty_l = self.glade.get_widget('numpty.l')
        self.numpty_l.set_text(self.vps_details['numpty.l'])

        self.numsiginfo_b = self.glade.get_widget('numsiginfo.b')
        self.numsiginfo_b.set_text(self.vps_details['numsiginfo.b'])
        self.numsiginfo_l = self.glade.get_widget('numsiginfo.l')
        self.numsiginfo_l.set_text(self.vps_details['numsiginfo.l'])

        self.numfile_b = self.glade.get_widget('numfile.b')
        self.numfile_b.set_text(self.vps_details['numfile.b'])
        self.numfile_l = self.glade.get_widget('numfile.l')
        self.numfile_l.set_text(self.vps_details['numfile.l'])

        self.numiptent_b = self.glade.get_widget('numiptent.b')
        self.numiptent_b.set_text(self.vps_details['numiptent.b'])
        self.numiptent_l = self.glade.get_widget('numiptent.l')
        self.numiptent_l.set_text(self.vps_details['numiptent.l'])

    def fill_cpu_info(self):
        self.hs_min_cpu = self.glade.get_widget('hsMinCPU')
        self.hs_max_cpu = self.glade.get_widget('hsMaxCPU')
        self.sb_max_procs_bar = self.glade.get_widget('sbMaxProcsBar')
        self.sb_max_procs_lim = self.glade.get_widget('sbMaxProcsLim')
        self.lbl_hn_power = self.glade.get_widget('lblHNPower')
        self.lbl_vps_power = self.glade.get_widget('lblVPSPower')
        
        hn_power = int(self.rpcserver.get_hn_power())
        self.lbl_hn_power.set_text(str(hn_power))
        self.lbl_vps_power.set_text(str(self.vps_details['cpulunits']))
        
        self.hs_min_cpu.set_range(0,hn_power)
        self.hs_min_cpu.set_value(float(self.vps_details['cpulunits']))
        self.hs_min_cpu.set_draw_value(True)

        self.hs_max_cpu.set_range(0,100)
        self.hs_max_cpu.set_value(int(self.vps_details['cpulimit']))
        self.hs_max_cpu.set_draw_value(True)

        self.sb_max_procs_bar.set_value(int(self.vps_details['numproc.b']))
        self.sb_max_procs_lim.set_value(int(self.vps_details['numproc.l']))

    def fill_users(self):
        self.cmb_user_name = self.glade.get_widget('cmbUserName')
        self.ent_passwd = self.glade.get_widget('entPasswd')
        self.ent_confirm_passwd = self.glade.get_widget('entConfirmPasswd')
        self.ent_user_new = self.glade.get_widget('entUserNew')
        self.ent_passwd_new = self.glade.get_widget('entPasswdNew')
        self.ent_confirm_passwd_new = self.glade.get_widget('entConfirmPasswdNew')

        ls = gtk.ListStore(str)
        self.cmb_user_name.set_model(ls)
        cell = gtk.CellRendererText()
        self.cmb_user_name.pack_start(cell, True)
        self.cmb_user_name.add_attribute(cell, 'text', 0)

        users = self.rpcserver.get_vps_user_list(self.vpsid)

        i=0
        for user in users:
            if user == 'root':
                pos = i
            else:
                i += 1
            ls.append([user])

        self.cmb_user_name.set_active(pos)
                
    def on_btnAddIP_clicked(self, widget):
        ent_new = self.glade.get_widget('entNewIP')
        
        if validate.validate_ip(ent_new.get_text()):
            self.rpcserver.vps_ipadd(self.vpsid, ent_new.get_text())
            self.ip_list_store.append([ent_new.get_text()])
        else:
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "IP address mal-formed.")
            dlg.run()
            dlg.destroy()
            return
            

    def on_btnSaveHostname_clicked(self, widget):
        entHN = self.glade.get_widget('entHostname')
        # FIXME validate user input here
        self.rpcserver.set_vps_hostname(self.vpsid, entHN.get_text().strip())

    def on_btnAddNS_clicked(self, widget):
        # Nameservers can only be specified as a list in one shot.
        # If a new one is added, append it to the existing list and
        # send it to the server to set it
        ent_new = self.glade.get_widget('entNewNS')

        if not validate.validate_ip(ent_new.get_text()):
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "IP address mal-formed.")
            dlg.run()
            dlg.destroy()
            return

        iter = self.ns_list_store.get_iter_first()
        servers=[]

        while True:
            if iter == None: break
            servers.append(self.ns_list_store.get_value(iter, 0))
            iter = self.ns_list_store.iter_next(iter)

        new_ns = ent_new.get_text().strip()
  
        
        # FIXME do validation on new_ns
        servers.append(new_ns)
        self.rpcserver.set_vps_nameservers(self.vpsid, servers)
        self.ns_list_store.append([new_ns])
        ent_new.set_text('')

    def on_btnDeleteNS_clicked(self, widget):
        selection = self.ns_tv.get_selection()
        (model, iter) = selection.get_selected()
        if iter == None:
            dlg = gtk.MessageDialog(self.winProp, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
            gtk.BUTTONS_OK , "No Nameserver selected.\nPlease select one from the list.")
            dlg.run()
            dlg.destroy()
            return
        model.remove(iter)

        iter = self.ns_list_store.get_iter_first()
        servers=[]

        while True:
            servers.append(self.ns_list_store.get_value(iter, 0))
            iter = self.ns_list_store.iter_next(iter)
            if iter == None:
                break
            
        print servers
            
        
    def get_selected_ip(self):
        selection = self.ip_tv.get_selection()
        (model, iter) = selection.get_selected()
        if iter == None: return 0
        return model.get_value(iter, 0)

    def fill_properties(self):
        # set the hostname
        entHN = self.glade.get_widget('entHostname')
        entHN.set_text(self.vps_details['hostname'])
        
        self.fill_ips()        
        self.fill_nameservers()
        self.fill_net_advanced()
        self.fill_mem_info()
        self.fill_misc_info()
        self.fill_cpu_info()
        self.fill_users()
