#!/usr/bin/env python
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


import sys
import os
import glob
import thread
import time

from xmlrpclib import Server
try:
 import pygtk
except:
  pass
try:
  import gtk
  import gtk.glade
except:
  print "You need to install pyGTK or GTKv2 ",
  print "or set your PYTHONPATH correctly."
  sys.exit(1)

import gobject
# other GUI elements
import newvps
import vpsprops
import progress

easyvz_version = "0.1"
gladefile="glade/ezvz.glade"

class appgui:
  def __init__(self):
    """
    In this init we are going to display the main
    ezvz window
    """

    self.LoginTree = gtk.glade.XML(gladefile, 'winLogin')
    self.winLogin = self.LoginTree.get_widget('winLogin')
    self.winLogin.show()
    
    dic = { "on_btnQuit_clicked":(gtk.main_quit),
	    "on_btnConnect_clicked":self.on_btnConnect_clicked,
            "on_winLogin_destroy":(gtk.main_quit)
          }

    self.LoginTree.signal_autoconnect (dic)
    
  def show_main_win(self):
    self.MainTree = gtk.glade.XML (gladefile,'winEzvz')
    self.winMain = self.MainTree.get_widget('winEzvz')

    dic = { "on_winEzvz_destroy":(gtk.main_quit),
	    "on_btnVpsHalt_clicked":self.on_btnVpsHalt_clicked,
            "on_btnVpsStart_clicked":self.on_btnVpsStart_clicked,
            "on_tbNew_clicked": self.on_tbNew_clicked,
            "on_btnVpsForceHalt_clicked": self.on_btnVpsHalt_clicked,
            "on_btnVpsReboot_clicked": self.on_btnVpsReboot_clicked,
            "on_btnExec_clicked": self.on_btnExec_clicked,
            "on_tbProperties_clicked": self.on_tbProperties_clicked,
            "on_tbAbout_clicked":self.on_tbAbout_clicked,
            "on_tbDestroy_clicked": self.on_tbDestroy_clicked,
            "on_tbRefresh_clicked": self.on_tbRefresh_clicked
            }

    self.MainTree.signal_autoconnect (dic)

    self.liststore = gtk.ListStore(gtk.gdk.Pixbuf, str, gtk.gdk.Pixbuf, str, str)

    self.icon_dic = {}
    icons = glob.glob('icons/*.png')
    for icon in icons:
        file_name = icon.split('/')
        file_name = file_name[-1]  # get the file name from path
        file_name = file_name[:-4] # remove the extension
        self.icon_dic[file_name] = gtk.gdk.pixbuf_new_from_file(icon)
        
    # construct the main TreeView

    self.treeview = self.MainTree.get_widget('tvEZ')
    self.construct_list()
    self.populate_treeview()
    self.treeview.set_model(self.liststore)

    self.cellVPS = gtk.CellRendererText()
    self.cellStatus = gtk.CellRendererPixbuf()
    self.cellIP = gtk.CellRendererText()
    self.cellHN = gtk.CellRendererText()
    self.cellpb = gtk.CellRendererPixbuf()
        
    self.tvPixmapcol = gtk.TreeViewColumn('', self.cellpb, pixbuf=0)
    self.tvVPScol = gtk.TreeViewColumn('VPS ID', self.cellVPS, text=1)
    self.tvStatuscol = gtk.TreeViewColumn('Status', self.cellStatus, pixbuf=2)
    self.tvIPcol = gtk.TreeViewColumn('IP Address', self.cellIP, text=3)
    self.tvHNcol = gtk.TreeViewColumn('Host name', self.cellHN, text=4)

    self.treeview.append_column(self.tvPixmapcol)
    self.treeview.append_column(self.tvVPScol)
    self.treeview.append_column(self.tvStatuscol)
    self.treeview.append_column(self.tvHNcol)
    self.treeview.append_column(self.tvIPcol)

    self.treeselection = self.treeview.get_selection()
    self.treeselection.connect('changed',self.tv_select_func)


    # construct the "Information" TreeView
    self.lsinfo = gtk.ListStore(str, str)
    self.infoview = self.MainTree.get_widget('tvInfo')
    self.populate_treeview()
    self.infoview.set_model(self.lsinfo)

    self.cellItem = gtk.CellRendererText()
    self.cellValue = gtk.CellRendererText()
        
    self.tvItemCol = gtk.TreeViewColumn('Item', self.cellItem, text=0)
    self.tvValueCol = gtk.TreeViewColumn('Value', self.cellValue, text=1)

    self.infoview.append_column(self.tvItemCol)
    self.infoview.append_column(self.tvValueCol)

    self.statusbar = self.MainTree.get_widget('sbMain')
    self.sb_context_id = self.statusbar.get_context_id('EasyVZ')
    self.statusbar.push(self.sb_context_id, 'Connected and Ready')

    # start a timeout callback to update
    # hardware node statistics, every 10 secs
    self.display_hn_status()
    gobject.timeout_add(10000, self.timer_thread) 
    return

  def populate_treeview(self):
      """ Populates the treeview with information from the dictionary
      vps_list. Call construct_list to first populate the dict"""
      
      self.liststore.clear() # clear the list store
      vpsids = self.vps_list.keys() # get VPS IDs from list
      
      for vpsid in vpsids:
          templist = []

          dist_name = self.vps_list[vpsid]['distro']
          
          if self.icon_dic.has_key(dist_name):
              templist.append(self.icon_dic[dist_name])
          else:
              templist.append(self.icon_dic['linux_logo'])
            
          templist.append(vpsid)
          status = self.myserver.get_status(vpsid)
          
          if status == "running":
              pixbuf = self.treeview.render_icon(gtk.STOCK_YES,gtk.ICON_SIZE_MENU)
          else:
              pixbuf = self.treeview.render_icon(gtk.STOCK_NO,gtk.ICON_SIZE_MENU)
              
          templist.append(pixbuf)
          templist.append(' '.join(self.myserver.get_ip(vpsid)))
          templist.append(self.myserver.get_hostname(vpsid))
          self.liststore.append(templist)
      return

  def construct_list(self):
    self.vps_list = {}
    vpsids = self.myserver.get_list(0)

    if len(vpsids) == 0: return # no dialog if list len = 0
    
    parent = self.MainTree.get_widget("winEzvz")
    prog = progress.progress(gladefile, parent)
    
    incr = 1.0 / float(len(vpsids))
    frac = 0.0

    for vpsid in vpsids:
        prog.set_fraction(frac)
        frac = frac + incr
                
        vps_info = self.get_vps_details(vpsid)
        prog.set_label("Getting info on VPS " + str(vpsid) + "...")
        self.vps_list[int(vpsid)] = vps_info

        while gtk.events_pending():
            gtk.main_iteration(False)


    prog.destroy()
    return

  def connect_to_server(self, hostname, port):
      # do check for exceptions here man
      self.myserver = Server("http://" + hostname + ":" + port)

  def do_backend_start(self, vpsid):
      self.thread_status = self.myserver.start_vps(vpsid)
      self.thread_done = 1

  def do_backend_restart(self, vpsid):
      self.thread_status = self.myserver.restart_vps(vpsid)
      self.thread_done = 1

  def do_backend_exec(self, vpsid, command):
      self.thread_status = self.myserver.vps_exec(vpsid, command)
      self.thread_done = 1

  def do_backend_stop(self, vpsid, force):
      self.thread_status = self.myserver.stop_vps(vpsid, force)
      self.thread_done = 1

  def do_backend_destroy(self, vpsid):
      self.thread_status = self.myserver.vps_destroy(vpsid)
      self.thread_done = 1

  def get_vps_details(self, vpsid):
      # given a VPS ID, return a dictionary containing its details
      tempdic = {}
      tempdic['distro']=self.myserver.get_distro_name(vpsid)
      tempdic['ips'] = self.myserver.get_ip(vpsid)
      tempdic['hostname'] = self.myserver.get_hostname(vpsid)
      tempdic['status'] = self.myserver.get_status(vpsid)
      tempdic['nameservers'] = self.myserver.get_nameservers(vpsid)

      tempdic['kmemsize'] = self.myserver.get_vps_kmemsize(vpsid, 0)
      tempdic['kmemsize.m'] = self.myserver.get_vps_kmemsize(vpsid, "m")
      tempdic['kmemsize.b'] = self.myserver.get_vps_kmemsize(vpsid, "b")
      tempdic['kmemsize.l'] = self.myserver.get_vps_kmemsize(vpsid, "l")
      tempdic['kmemsize.f'] = self.myserver.get_vps_kmemsize(vpsid, "f")
    
      tempdic['numproc'] = self.myserver.get_vps_numproc(vpsid, 0)
      tempdic['numproc.m'] = self.myserver.get_vps_numproc(vpsid, "m")
      tempdic['numproc.b'] = self.myserver.get_vps_numproc(vpsid, "b")
      tempdic['numproc.l'] = self.myserver.get_vps_numproc(vpsid, "l")
      tempdic['numproc.f'] = self.myserver.get_vps_numproc(vpsid, "f")

      tempdic['shmpages'] = self.myserver.get_vps_shmpages(vpsid, 0)
      tempdic['shmpages.m'] = self.myserver.get_vps_shmpages(vpsid, "m")
      tempdic['shmpages.b'] = self.myserver.get_vps_shmpages(vpsid, "b")
      tempdic['shmpages.l'] = self.myserver.get_vps_shmpages(vpsid, "l")
      tempdic['shmpages.f'] = self.myserver.get_vps_shmpages(vpsid, "f")

      tempdic['numtcpsock'] = self.myserver.get_vps_numtcpsock(vpsid, 0)
      tempdic['numtcpsock.m'] = self.myserver.get_vps_numtcpsock(vpsid, "m")
      tempdic['numtcpsock.b'] = self.myserver.get_vps_numtcpsock(vpsid, "b")
      tempdic['numtcpsock.l'] = self.myserver.get_vps_numtcpsock(vpsid, "l")
      tempdic['numtcpsock.f'] = self.myserver.get_vps_numtcpsock(vpsid, "f")

      tempdic['numfile'] = self.myserver.get_vps_numfile(vpsid, 0)
      tempdic['numfile.m'] = self.myserver.get_vps_numfile(vpsid, "m")
      tempdic['numfile.b'] = self.myserver.get_vps_numfile(vpsid, "b")
      tempdic['numfile.l'] = self.myserver.get_vps_numfile(vpsid, "lfff")
      tempdic['numfile.f'] = self.myserver.get_vps_numfile(vpsid, "f")

      tempdic['tcpsndbuf'] = self.myserver.get_vps_tcpsndbuf(vpsid, 0)
      tempdic['tcpsndbuf.m'] = self.myserver.get_vps_tcpsndbuf(vpsid, "m")
      tempdic['tcpsndbuf.b'] = self.myserver.get_vps_tcpsndbuf(vpsid, "b")
      tempdic['tcpsndbuf.l'] = self.myserver.get_vps_tcpsndbuf(vpsid, "l")
      tempdic['tcpsndbuf.f'] = self.myserver.get_vps_tcpsndbuf(vpsid, "f")

      tempdic['tcprcvbuf'] = self.myserver.get_vps_tcprcvbuf(vpsid, 0)
      tempdic['tcprcvbuf.m'] = self.myserver.get_vps_tcprcvbuf(vpsid, "m")
      tempdic['tcprcvbuf.b'] = self.myserver.get_vps_tcprcvbuf(vpsid, "b")
      tempdic['tcprcvbuf.l'] = self.myserver.get_vps_tcprcvbuf(vpsid, "l")
      tempdic['tcprcvbuf.f'] = self.myserver.get_vps_tcprcvbuf(vpsid, "f")

      tempdic['othersockbuf'] = self.myserver.get_vps_othersockbuf(vpsid, 0)
      tempdic['othersockbuf.m'] = self.myserver.get_vps_othersockbuf(vpsid, "m")
      tempdic['othersockbuf.b'] = self.myserver.get_vps_othersockbuf(vpsid, "b")
      tempdic['othersockbuf.l'] = self.myserver.get_vps_othersockbuf(vpsid, "l")
      tempdic['othersockbuf.f'] = self.myserver.get_vps_othersockbuf(vpsid, "f")

      tempdic['dgramrcvbuf'] = self.myserver.get_vps_dgramrcvbuf(vpsid, 0)
      tempdic['dgramrcvbuf.m'] = self.myserver.get_vps_dgramrcvbuf(vpsid, "m")
      tempdic['dgramrcvbuf.b'] = self.myserver.get_vps_dgramrcvbuf(vpsid, "b")
      tempdic['dgramrcvbuf.l'] = self.myserver.get_vps_dgramrcvbuf(vpsid, "l")
      tempdic['dgramrcvbuf.f'] = self.myserver.get_vps_dgramrcvbuf(vpsid, "f")

      tempdic['numothersock'] = self.myserver.get_vps_numothersock(vpsid, 0)
      tempdic['numothersock.m'] = self.myserver.get_vps_numothersock(vpsid, "m")
      tempdic['numothersock.b'] = self.myserver.get_vps_numothersock(vpsid, "b")
      tempdic['numothersock.l'] = self.myserver.get_vps_numothersock(vpsid, "l")
      tempdic['numothersock.f'] = self.myserver.get_vps_numothersock(vpsid, "f")

      tempdic['lockedpages'] = self.myserver.get_vps_lockedpages(vpsid, 0)
      tempdic['lockedpages.m'] = self.myserver.get_vps_lockedpages(vpsid, "m")
      tempdic['lockedpages.b'] = self.myserver.get_vps_lockedpages(vpsid, "b")
      tempdic['lockedpages.l'] = self.myserver.get_vps_lockedpages(vpsid, "l")
      tempdic['lockedpages.f'] = self.myserver.get_vps_lockedpages(vpsid, "f")

      tempdic['privvmpages'] = self.myserver.get_vps_privvmpages(vpsid, 0)
      tempdic['privvmpages.m'] = self.myserver.get_vps_privvmpages(vpsid, "m")
      tempdic['privvmpages.b'] = self.myserver.get_vps_privvmpages(vpsid, "b")
      tempdic['privvmpages.l'] = self.myserver.get_vps_privvmpages(vpsid, "l")
      tempdic['privvmpages.f'] = self.myserver.get_vps_privvmpages(vpsid, "f")

      tempdic['physpages'] = self.myserver.get_vps_physpages(vpsid, 0)
      tempdic['physpages.m'] = self.myserver.get_vps_physpages(vpsid, "m")
      tempdic['physpages.b'] = self.myserver.get_vps_physpages(vpsid, "b")
      tempdic['physpages.l'] = self.myserver.get_vps_physpages(vpsid, "l")
      tempdic['physpages.f'] = self.myserver.get_vps_physpages(vpsid, "f")

      tempdic['vmguarpages'] = self.myserver.get_vps_vmguarpages(vpsid, 0)
      tempdic['vmguarpages.m'] = self.myserver.get_vps_vmguarpages(vpsid, "m")
      tempdic['vmguarpages.b'] = self.myserver.get_vps_vmguarpages(vpsid, "b")
      tempdic['vmguarpages.l'] = self.myserver.get_vps_vmguarpages(vpsid, "l")
      tempdic['vmguarpages.f'] = self.myserver.get_vps_vmguarpages(vpsid, "f")

      tempdic['oomguarpages'] = self.myserver.get_vps_oomguarpages(vpsid, 0)
      tempdic['oomguarpages.m'] = self.myserver.get_vps_oomguarpages(vpsid, "m")
      tempdic['oomguarpages.b'] = self.myserver.get_vps_oomguarpages(vpsid, "b")
      tempdic['oomguarpages.l'] = self.myserver.get_vps_oomguarpages(vpsid, "l")
      tempdic['oomguarpages.f'] = self.myserver.get_vps_oomguarpages(vpsid, "f")

      tempdic['dcachesize'] = self.myserver.get_vps_dcachesize(vpsid, 0)
      tempdic['dcachesize.m'] = self.myserver.get_vps_dcachesize(vpsid, "m")
      tempdic['dcachesize.b'] = self.myserver.get_vps_dcachesize(vpsid, "b")
      tempdic['dcachesize.l'] = self.myserver.get_vps_dcachesize(vpsid, "l")
      tempdic['dcachesize.f'] = self.myserver.get_vps_dcachesize(vpsid, "f")

      tempdic['numflock'] = self.myserver.get_vps_numflock(vpsid, 0)
      tempdic['numflock.m'] = self.myserver.get_vps_numflock(vpsid, "m")
      tempdic['numflock.b'] = self.myserver.get_vps_numflock(vpsid, "b")
      tempdic['numflock.l'] = self.myserver.get_vps_numflock(vpsid, "l")
      tempdic['numflock.f'] = self.myserver.get_vps_numflock(vpsid, "f")

      tempdic['numpty'] = self.myserver.get_vps_numpty(vpsid, 0)
      tempdic['numpty.m'] = self.myserver.get_vps_numpty(vpsid, "m")
      tempdic['numpty.b'] = self.myserver.get_vps_numpty(vpsid, "b")
      tempdic['numpty.l'] = self.myserver.get_vps_numpty(vpsid, "l")
      tempdic['numpty.f'] = self.myserver.get_vps_numpty(vpsid, "f")

      tempdic['numsiginfo'] = self.myserver.get_vps_numsiginfo(vpsid, 0)
      tempdic['numsiginfo.m'] = self.myserver.get_vps_numsiginfo(vpsid, "m")
      tempdic['numsiginfo.b'] = self.myserver.get_vps_numsiginfo(vpsid, "b")
      tempdic['numsiginfo.l'] = self.myserver.get_vps_numsiginfo(vpsid, "l")
      tempdic['numsiginfo.f'] = self.myserver.get_vps_numsiginfo(vpsid, "f")
      
      tempdic['numfile'] = self.myserver.get_vps_numfile(vpsid, 0)
      tempdic['numfile.m'] = self.myserver.get_vps_numfile(vpsid, "m")
      tempdic['numfile.b'] = self.myserver.get_vps_numfile(vpsid, "b")
      tempdic['numfile.l'] = self.myserver.get_vps_numfile(vpsid, "l")
      tempdic['numfile.f'] = self.myserver.get_vps_numfile(vpsid, "f")

      tempdic['numiptent'] = self.myserver.get_vps_numiptent(vpsid, 0)
      tempdic['numiptent.m'] = self.myserver.get_vps_numiptent(vpsid, "m")
      tempdic['numiptent.b'] = self.myserver.get_vps_numiptent(vpsid, "b")
      tempdic['numiptent.l'] = self.myserver.get_vps_numiptent(vpsid, "l")
      tempdic['numiptent.f'] = self.myserver.get_vps_numiptent(vpsid, "f")

      tempdic['cpulimit'] = self.myserver.get_vps_cpulimit(vpsid)
      tempdic['cpulunits'] = self.myserver.get_vps_cpulunits(vpsid)
                
      # get 'start on boot' and other things beyond these
      return tempdic

  def update_vps_info(self, vpsid):
      vps_info = self.get_vps_details(vpsid)
      self.vps_list[int(vpsid)] = vps_info
      return

  def timer_thread(self):
      # currently updates hardware node usage stats
      self.display_hn_status()
      return True
      
####CALLBACKS
  def on_tbRefresh_clicked(self, widget):
      self.construct_list()
      self.populate_treeview()

  def on_tbDestroy_clicked(self, widget):
    vpsid = self.get_selected_vps()

    if vpsid == 0:
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , "No VPS selected.\nPlease select a VPS from the list.")
        dlg.run()
        dlg.destroy()
        return 

    if self.vps_list[int(vpsid)]['status'] == 'running':
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , \
        "The VPS you are trying to destroy in currently running!\nStop it before you continue")
        dlg.run()
        dlg.destroy()
        return

    dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, \
    gtk.BUTTONS_YES_NO , "The selected VPS will be destroyed! Are you sure?")
    answer = dlg.run()
    dlg.destroy()

    if answer == gtk.RESPONSE_YES:
        # This operation can take long. Start it in a thread so that
        # the GUI remains responsive
        self.thread_done = 0
        thread.start_new(self.do_backend_destroy, (vpsid,))

        parent = self.MainTree.get_widget("winEzvz")
        prog = progress.progress(gladefile, parent)
        prog.set_label("Destroying VPS " + str(vpsid) + ". Please wait...")

        while self.thread_done == 0:
            while gtk.events_pending():
                gtk.main_iteration(False)
            prog.pulse()
            time.sleep(.25)
        
        prog.destroy()
    
        self.statusbar.pop(self.sb_context_id)

        del self.vps_list[int(vpsid)]
        self.populate_treeview()

    return

  def on_btnConnect_clicked(self, widget):
      entHost = self.LoginTree.get_widget('entHost')
      entPort = self.LoginTree.get_widget('entPort')
      host = entHost.get_text()
      port = entPort.get_text()
      
      if(host.strip() == ''):
          host = "localhost"

      if(port.strip() == ''):
          port = "8086"
            
      self.connect_to_server(host, port)
      #FIXME if unable to connect to server, dont show winMain
      self.winLogin.hide()
      self.show_main_win()

  def on_btnExec_clicked(self, widget):
    vpsid = self.get_selected_vps()
    entRunCmd = self.MainTree.get_widget('entRunCmd')
    command = entRunCmd.get_text()

    if vpsid == 0:
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , "No VPS selected.\nPlease select a VPS from the list.")
        dlg.run()
        dlg.destroy()
        return
    
    if self.vps_list[int(vpsid)]['status'] == 'stopped':
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , \
        "The VPS in which you are trying to\nrun a command is currently not running.")
        dlg.run()
        dlg.destroy()
        return
        
    self.statusbar.push(self.sb_context_id, 'Running command, please wait')
    while gtk.events_pending():
        gtk.main_iteration(False)

    # this operation can take long. Start it in a thread so that
    # the GUI remains responsive
    self.thread_done = 0
    thread.start_new(self.do_backend_exec, (vpsid,command))

    parent = self.MainTree.get_widget("winEzvz")
    prog = progress.progress(gladefile, parent)
    prog.set_label("Running command on " + str(vpsid) + ". Please wait...")

    while self.thread_done == 0:
        while gtk.events_pending():
            gtk.main_iteration(False)
        prog.pulse()
        time.sleep(.25)
        
    prog.destroy()
    
    self.statusbar.pop(self.sb_context_id)

    cmdRunCmd.set_text('')

#    self.update_vps_info(vpsid)
#    self.populate_treeview()
    return

  def on_btnVpsReboot_clicked(self, widget):
    vpsid = self.get_selected_vps()
    if vpsid == 0:
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , "No VPS selected.\nPlease select a VPS from the list.")
        dlg.run()
        dlg.destroy()
        return
    
    if self.vps_list[int(vpsid)]['status'] == 'stopped':
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , "The VPS you are trying to restart is currently not running.")
        dlg.run()
        dlg.destroy()
        return
    
    self.statusbar.push(self.sb_context_id, 'Restarting VPS, please wait')
    while gtk.events_pending():
        gtk.main_iteration(False)

    # this operation can take long. Start it in a thread so that
    # the GUI remains responsive
    self.thread_done = 0
    thread.start_new(self.do_backend_restart, (vpsid,))

    parent = self.MainTree.get_widget("winEzvz")
    prog = progress.progress(gladefile, parent)
    prog.set_label("Restarting VPS " + str(vpsid) + ". Please wait...")

    while self.thread_done == 0:
        while gtk.events_pending():
            gtk.main_iteration(False)
        prog.pulse()
        time.sleep(.25)
        
    prog.destroy()
    
    self.statusbar.pop(self.sb_context_id)

    if self.thread_status == 0:
        print "VPS start successful"
    else:
        print "VPS start failed"

    self.update_vps_info(vpsid)
    self.populate_treeview()
    return

  def on_tbNew_clicked(self, widget):
      winMain = self.MainTree.get_widget('winEzvz')
      newvpsgui = newvps.newvps(self.myserver, gladefile, winMain, self)
      return

  def on_tbProperties_clicked(self, widget):
      vpsid = int(self.get_selected_vps())
      if vpsid == 0:
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , "No VPS selected.\nPlease select a VPS from the list.")
        dlg.run()
        dlg.destroy()
        return

      winMain = self.MainTree.get_widget('winEzvz')
      propsgui = vpsprops.vpsprops(vpsid, self.vps_list[vpsid], self.myserver, gladefile, winMain, self)
      return
  
  def tv_select_func(self, info):
      selected_vps = int(self.get_selected_vps())

      self.lsinfo.clear()

      for k in self.vps_list[selected_vps].keys():
          self.lsinfo.append([k,self.vps_list[selected_vps][k]])
     
      return True

  def on_btnVpsHalt_clicked(self,widget):
    """
    This is a common callback for 'Halt' and 'Force Halt' operations.
    Depending on the widget name, we conditionally execute code.
    """
    vpsid = self.get_selected_vps()
    if vpsid == 0:
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , "No VPS selected.\nPlease select a VPS from the list.")
        dlg.run()
        dlg.destroy()
        return
    if self.vps_list[int(vpsid)]['status'] == 'stopped':
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , "The VPS you are trying to halt is not running.")
        dlg.run()
        dlg.destroy()
        return
    
    self.statusbar.push(self.sb_context_id, 'Halting VPS, please wait') 
    while gtk.events_pending():
        gtk.main_iteration(False)

    if widget.name == 'btnVpsHalt':
        force = 0
    else:
        force = 1
    
    self.thread_done = 0
    thread.start_new(self.do_backend_stop, (vpsid, force))

    parent = self.MainTree.get_widget("winEzvz")
    prog = progress.progress(gladefile, parent)
    prog.set_label("Stoping VPS " + str(vpsid) + ". Please wait...")

    while self.thread_done == 0:
        while gtk.events_pending():
            gtk.main_iteration(False)
        prog.pulse()
        time.sleep(.25)

    prog.destroy()
    
    self.statusbar.pop(self.sb_context_id)

    if self.thread_status == 0:
        print "VPS stop successful"
    else:
        print "VPS stop failed"

    self.update_vps_info(vpsid)
    self.populate_treeview()

  def on_btnVpsStart_clicked(self, widget):
    vpsid = self.get_selected_vps()
    if vpsid == 0:
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , "No VPS selected.\nPlease select a VPS from the list.")
        dlg.run()
        dlg.destroy()
        return
    
    if self.vps_list[int(vpsid)]['status'] == 'running':
        dlg = gtk.MessageDialog(self.winMain, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, \
        gtk.BUTTONS_OK , "The VPS you are trying to start is currently running.")
        dlg.run()
        dlg.destroy()
        return
    
    self.statusbar.push(self.sb_context_id, 'Starting VPS, please wait')
    while gtk.events_pending():
        gtk.main_iteration(False)

    # this operation can take long. Start it in a thread so that
    # the GUI remains responsive
    self.thread_done = 0
    thread.start_new(self.do_backend_start, (vpsid,))

    parent = self.MainTree.get_widget("winEzvz")
    prog = progress.progress(gladefile, parent)
    prog.set_label("Starting VPS " + str(vpsid) + ". Please wait...")

    while self.thread_done == 0:
        while gtk.events_pending():
            gtk.main_iteration(False)
        prog.pulse()
        time.sleep(.25)
        
    prog.destroy()
    
    self.statusbar.pop(self.sb_context_id)

    if self.thread_status == 0:
        print "VPS start successful"
    else:
        print "VPS start failed"

    self.update_vps_info(vpsid)
    self.populate_treeview()
    return

  def on_tbAbout_clicked(self, widget):
      about = gtk.AboutDialog()
      about.set_name("EasyVZ")
      about.set_version(easyvz_version)
      about.set_comments("A Graphical frontend for openVZ")
      about.set_copyright("(c) 2006, Shuveb Hussain\n(c) 2006, Binary Karma")
      about.set_website("http://binarykarma.com")
      about.set_authors(['Shuveb Hussain <shuveb@binarykarma.com>'])
      about.run()
      about.destroy()
            
  def get_selected_vps(self):
      self.treeview = self.MainTree.get_widget('tvEZ')

      (model, iter) = self.treeselection.get_selected()
      if iter == None: return 0
      return model.get_value(iter, 1)

  def display_hn_status(self):
      pbDisk = self.MainTree.get_widget('pbDisk')
      pbMem = self.MainTree.get_widget('pbMem')
      pbSwap = self.MainTree.get_widget('pbSwap')
      pbCPU = self.MainTree.get_widget('pbCPU')

      values = self.myserver.get_vz_part_status()
      fraction  = float(values[1])/(float(values[0])/100)
      pbDisk.set_fraction(float(fraction)/100)
      pbDisk.set_text("%d%% used" % fraction)
      
      values = self.myserver.get_hn_mem_status()
      fraction  = float(values[1])/(float(values[0])/100)
      pbMem.set_fraction(float(fraction)/100)
      #print values
      pbMem.set_text("%d/%d used,%dM in cache" % (values[1], values[0], values[2]))
      
      values = self.myserver.get_hn_swap_status()
      fraction  = float(values[1])/(float(values[0])/100)
      pbSwap.set_fraction(float(fraction)/100)
      pbSwap.set_text("%d%%" % fraction)

      values = self.myserver.get_hn_cpu_status()
      #print values
      pbCPU.set_fraction(values[1]/100)
      pbCPU.set_text("%.02f%% busy, %d tasks" % (values[1], values[0]))

    
#start the app...
gtk.threads_init()
app=appgui()
gtk.main()

