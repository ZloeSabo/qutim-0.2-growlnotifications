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

import ezvzlib
import os
import sys

version = "0.1"

class EzVZbackend:
	def get_list(self, status):
		return ezvzlib.get_vpses(status)

	def get_ip(self, vpsid):
		matter =  ezvzlib.get_vps_ip(vpsid)
		print matter
		return matter

	def get_distro_name(self, vpsid):
		return ezvzlib.get_vps_distro_name(vpsid)

	def get_hostname(self, vpsid):
		return ezvzlib.get_vps_hostname(vpsid)

	def get_status(self, vpsid):
		return ezvzlib.get_vps_status(vpsid)
	
	def stop_vps(self, vpsid, force):
		return ezvzlib.stop_vps(vpsid, force)

	def start_vps(self, vpsid):
		return ezvzlib.start_vps(vpsid)

	def restart_vps(self, vpsid):
		return ezvzlib.restart_vps(vpsid)
	
	def get_nameservers(self, vpsid):
		return ezvzlib.get_nameservers(vpsid)

	def get_configurations(self):
		return ezvzlib.get_configurations()

	def get_template_caches(self):
		return ezvzlib.get_template_caches()

	def create_vps(self, vpsid, template, profile):
		return ezvzlib.create_vps(vpsid, template, profile)

	def set_vps_on_boot(self, vpsid, on_boot):
		return ezvzlib.set_vps_on_boot(vpsid, on_boot)

	def set_vps_hostname(self, vpsid, hostname):
		return ezvzlib.set_vps_hostname(vpsid, hostname)

	def vps_ipadd(self, vpsid, ipadd):
		return ezvzlib.vps_ipadd(vpsid, ipadd)

	def vps_ipdel(self, vpsid, ipadd):
		return ezvzlib.vps_ipdel(vpsid, ipadd)

	def set_vps_nameservers(self, vpsid, nameservers):
		return ezvzlib.set_vps_nameservers(vpsid, nameservers)

	def vps_exec(self, vpsid, command):
		return ezvzlib.vps_exec(vpsid, command)

	def get_vz_part_status(self):
		return ezvzlib.get_vz_part_status()
	
	def get_hn_mem_status(self):
		return ezvzlib.get_hn_mem_status()
		
	def get_hn_swap_status(self):
		return ezvzlib.get_hn_swap_status()

	def get_hn_cpu_status(self):
		return ezvzlib.get_hn_cpu_status()

	def get_vps_kmemsize(self, vpsid, which):
		return ezvzlib.get_vps_kmemsize(vpsid, which)

	def set_vps_kmemsize(self, vpsid, bar, lim):
		return ezvzlib.set_vps_kmemsize(vpsid, bar, lim)

	def get_vps_lockedpages(self, vpsid, which):
		return ezvzlib.get_vps_lockedpages(vpsid, which)

	def set_vps_lockedpages(self, vpsid, bar, lim):
		return ezvzlib.set_vps_lockedpages(vpsid, bar, lim)

	def get_vps_privvmpages(self, vpsid, which):
		return ezvzlib.get_vps_privvmpages(vpsid, which)

	def set_vps_privvmpages(self, vpsid, bar, lim):
		return ezvzlib.set_vps_privvmpages(vpsid, bar, lim)

	def get_vps_shmpages(self, vpsid, which):
		return ezvzlib.get_vps_shmpages(vpsid, which)

	def set_vps_shmpages(self, vpsid, bar, lim):
		return ezvzlib.set_vps_shmpages(vpsid, bar, lim)

	def get_vps_numproc(self, vpsid, which):
		return ezvzlib.get_vps_numproc(vpsid, which)

	def set_vps_numproc(self, vpsid, bar, lim):
		return ezvzlib.set_vps_numproc(vpsid, bar, lim)

	def get_vps_physpages(self, vpsid, which):
		return ezvzlib.get_vps_physpages(vpsid, which)

	def set_vps_physpages(self, vpsid, bar, lim):
		return ezvzlib.set_vps_physpages(vpsid, bar, lim)

	def get_vps_vmguarpages(self, vpsid, which):
		return ezvzlib.get_vps_vmguarpages(vpsid, which)

	def set_vps_vmguarpages(self, vpsid, bar, lim):
		return ezvzlib.set_vps_vmguarpages(vpsid, bar, lim)

	def get_vps_oomguarpages(self, vpsid, which):
		return ezvzlib.get_vps_oomguarpages(vpsid, which)

	def set_vps_oomguarpages(self, vpsid, bar, lim):
		return ezvzlib.set_vps_oomguarpages(vpsid, bar, lim)

	def get_vps_numtcpsock(self, vpsid, which):
		return ezvzlib.get_vps_numtcpsock(vpsid, which)

	def set_vps_numtcpsock(self, vpsid, bar, lim):
		return ezvzlib.set_vps_numtcpsock(vpsid, bar, lim)

	def get_vps_numflock(self, vpsid, which):
		return ezvzlib.get_vps_numflock(vpsid, which)

	def set_vps_numflock(self, vpsid, bar, lim):
		return ezvzlib.set_vps_numflock(vpsid, bar, lim)

	def get_vps_numpty(self, vpsid, which):
		return ezvzlib.get_vps_numpty(vpsid, which)

	def set_vps_numpty(self, vpsid, bar, lim):
		return ezvzlib.set_vps_numpty(vpsid, bar, lim)

	def get_vps_numsiginfo(self, vpsid, which):
		return ezvzlib.get_vps_numsiginfo(vpsid, which)

	def set_vps_numsiginfo(self, vpsid, bar, lim):
		return ezvzlib.set_vps_numsiginfo(vpsid, bar, lim)

	def get_vps_tcpsndbuf(self, vpsid, which):
		return ezvzlib.get_vps_tcpsndbuf(vpsid, which)

	def set_vps_tcpsndbuf(self, vpsid, bar, lim):
		return ezvzlib.set_vps_tcpsndbuf(vpsid, bar, lim)

	def get_vps_tcprcvbuf(self, vpsid, which):
		return ezvzlib.get_vps_tcprcvbuf(vpsid, which)

	def set_vps_tcprcvbuf(self, vpsid, bar, lim):
		return ezvzlib.set_vps_tcprcvbuf(vpsid, bar, lim)

	def get_vps_othersockbuf(self, vpsid, which):
		return ezvzlib.get_vps_othersockbuf(vpsid, which)

	def set_vps_othersockbuf(self, vpsid, bar, lim):
		return ezvzlib.set_vps_othersockbuf(vpsid, bar, lim)

	def get_vps_dgramrcvbuf(self, vpsid, which):
		return ezvzlib.get_vps_dgramrcvbuf(vpsid, which)

	def set_vps_dgramrcvbuf(self, vpsid, bar, lim):
		return ezvzlib.set_vps_dgramrcvbuf(vpsid, bar, lim)

	def get_vps_numothersock(self, vpsid, which):
		return ezvzlib.get_vps_numothersock(vpsid, which)

	def set_vps_numothersock(self, vpsid, bar, lim):
		return ezvzlib.set_vps_numothersock(vpsid, bar, lim)

	def get_vps_dcachesize(self, vpsid, which):
		return ezvzlib.get_vps_dcachesize(vpsid, which)

	def set_vps_dcachesize(self, vpsid, bar, lim):
		return ezvzlib.set_vps_dcachesize(vpsid, bar, lim)

	def get_vps_numfile(self, vpsid, which):
		return ezvzlib.get_vps_numfile(vpsid, which)

	def set_vps_numfile(self, vpsid, bar, lim):
		return ezvzlib.set_vps_numfile(vpsid, bar, lim)

	def get_vps_numiptent(self, vpsid, which):
		return ezvzlib.get_vps_numiptent(vpsid, which)

	def set_vps_numiptent(self, vpsid, bar, lim):
		return ezvzlib.set_vps_numiptent(vpsid, bar, lim)

	def get_vps_diskspace(self, vpsid, which):
		return ezvzlib.get_vps_diskspace(vpsid, which)

	def set_vps_diskspace(self, vpsid, bar, lim):
		return ezvzlib.set_vps_diskspace(vpsid, bar, lim)

	def get_vps_disknodes(self, vpsid, which):
		return ezvzlib.get_vps_disknodes(vpsid, which)

	def set_vps_disknodes(self, vpsid, bar, lim):
		return ezvzlib.set_vps_disknodes(vpsid, bar, lim)

	def get_vps_laverage(self, vpsid):
		return ezvzlib.get_vps_laverage(vpsid)

	def get_vps_cpulimit(self, vpsid):
		return ezvzlib.get_vps_cpulimit(vpsid)

	def set_vps_cpulimit(self, vpsid, cpulimit):
		return ezvzlib.set_vps_cpulimit(vpsid, cpulimit)

	def get_vps_cpulunits(self, vpsid):
		return ezvzlib.get_vps_cpulunits(vpsid)

	def set_vps_cpuunits(self, vpsid, cpuunits):
		return ezvzlib.set_vps_cpuunits(vpsid,cpuunits)

	def get_hn_power(self):
		return ezvzlib.get_hn_power()

	def get_vps_user_list(self, vpsid):
		return ezvzlib.get_vps_user_list(vpsid)

	def set_vps_user_pass(self, vpsid, user, passwd):
		return ezvzlib.set_vps_user_pass(vpsid, user, passwd)

	def vps_destroy(self, vpsid):
		return ezvzlib.vps_destroy(vpsid)
	
from SimpleXMLRPCServer import SimpleXMLRPCServer
print "\n\nEasyVZ " + version +  ", (c) 2006, Binary Karma.\n(c) 2006, Shuveb Hussain <shuveb@binarykarma.com>.\nhttp://www.binarykarma.com\n"
server = SimpleXMLRPCServer(("", 8086))
server.register_instance(EzVZbackend())
print "Waiting for client..."
server.serve_forever()

