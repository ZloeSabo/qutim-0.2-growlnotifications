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

import os
import sys
import glob

def get_vpses(status):
    """Returns a list of currently defined VPSes"""
    # call vzlist with the header turned off.
    # before you can confuse yourself, read the vzlist man page
    # os.popen reads the vzlist output

    vpsids = []
    output = os.popen("vzlist -a -o vpsid -H")

    while 1:
        vpsid = output.readline()
        if not vpsid: break
        vpsid = vpsid[:-1]# strip and newline char
        vpsids.append(vpsid.strip())
        print vpsid
        
    return vpsids # return the items as a list

def get_vps_ip(vpsid):
    """Given a VPS ID, get its IP address"""
    comm = "vzlist -a -o ip -H " + str(vpsid)

    ipaddrs = os.popen(comm).readline()
    ipaddrs = ipaddrs.strip()
    ipaddrs = ipaddrs.split(' ')
    return ipaddrs # this is a list of IPs
# remember, a VPS can be assigned multiple IP addresses

def get_vps_distro_name(vpsid):
    """given the VPS ID get the distro name its running"""
    # We need to do this ourselves
    # we just read the <osname-release> file from the
    # /etc directory within the VPS virtual root dirs
    # heh, this is dirty stuff man...
    
    base_path = '/vz/private/' + str(vpsid) + '/etc/'

    # first look for LSB compliant systems, they have a
    # file named '/etc/lsb-release' this will contains
    # details of the distro. Hopefully all distros will
    # switch to this standard soon, I believe

    if os.path.exists(base_path + 'lsb-release'):
        f=open(base_path + 'lsb-release')
        lines = f.readlines()
        for line in lines:
            line  = line.split('=')
            if line[0] == 'DISTRIB_ID':
                return line[1][:-1].lower() # truncate '\n'

    # next look for a Debian based system, it has a
    # file named 'debian_version' in /etc
    if os.path.exists(base_path + 'debian_version'):
        return 'debian'

    # on similar lines, look for a slackware system
    # there is a /etc/slackware-version on those systems
    if os.path.exists(base_path + 'slackware-version'):
        return 'slackware'

    # next look for files named '*-release'
    file_name = glob.glob(base_path + '*-release')

    if len(file_name) == 0:
        return 'unknown'
    
    f=open(file_name[0])
    line = f.readline()
    line = line.split(' ')
    return line[0].lower()

def get_vps_hostname(vpsid):
    """Given a VPS ID, get its hostname"""
    comm = "vzlist -a -o hostname -H " + str(vpsid)
    hostname = os.popen(comm).readline()
    hostname = hostname[:-1]
    return hostname

def get_vps_status(vpsid):
    """Given a VPS ID, get its hostname"""
    comm = "vzlist -a -o status -H " + str(vpsid)
    status = os.popen(comm).readline()
    status = status[:-1]
    return status

def stop_vps(vpsid, force):
    """Given the VPS ID, stop it"""
    if force == 1:
        force = " --fast"
    else:
        force = ""
        
    status = os.system('vzctl stop ' + str(vpsid) + force)
    return status

def start_vps(vpsid):
    """Given the VPS ID, start it"""
    status = os.system('vzctl start ' + str(vpsid))
    return status

def restart_vps(vpsid):
    """Given the VPS ID, restart it"""
    status = os.system('vzctl restart ' + str(vpsid))
    return status

def vps_exec(vpsid, command):
    status = os.system('vzctl exec ' + str(vpsid) + ' ' + command)
    return status

def get_nameservers(vpsid):
    """Given the VPS ID, fetch its name servers"""
    # go read the VPS's private area and get /etc/resolv.conf
    resolv_path = '/vz/private/' + str(vpsid) + '/etc/resolv.conf'
    if not os.path.exists(resolv_path):
        return []
    
    f = open(resolv_path)
    lines = f.readlines()
    nameservers = []

    for line in lines:
        line = line.split(' ')
        if line[0] == 'nameserver':
            nameservers.append(line[1][:-1])

    return nameservers
            
def get_configurations():
    config_base_path = "/etc/vz/conf/"
    config_file_pattern =  config_base_path + 've-*.conf-sample'
    configs = glob.glob(config_file_pattern)

    config_list = []

    for config in configs:
        config = config.split('/')
        config = config[-1]
        config = config[3:-12]
        config_list.append(config)

    return config_list

def get_template_caches():
    cache_base_path = "/vz/template/cache/"
    cache_file_pattern =  cache_base_path + '*.tar.gz'
    caches = glob.glob(cache_file_pattern)

    cache_list = []

    for cache in caches:
        cache = cache.split('/')
        cache = cache[-1]
        cache = cache[:-7]
        cache_list.append(cache)

    return cache_list

def create_vps(vpsid, template, profile):
    """ Given the VPS ID, template cache name and
    profile name, create the VPS """
    command = "vzctl create " + str(vpsid) + " --ostemplate " + template + " --config " + profile
    print command
    status=os.system(command)
    return status

def set_vps_on_boot(vpsid, on_boot):
    if on_boot == 0:
        setting = "no"
    else:
        setting = "yes"

    command = "vzctl set " + str(vpsid) + " --onboot " + setting + " --save"
    print command
    status = os.system(command)
    return status


def set_vps_hostname(vpsid, hostname):
    command = "vzctl set " + str(vpsid) + " --hostname " + hostname + " --save"
    print command
    status = os.system(command)
    return status

def vps_ipadd(vpsid, ip):
    command = "vzctl set " + str(vpsid) + " --ipadd " + ip + " --save"
    print command
    status = os.system(command)
    return status

def vps_ipdel(vpsid, ip):
    command = "vzctl set " + str(vpsid) + " --ipdel " + ip + " --save"
    print command
    status = os.system(command)
    return status

def set_vps_nameservers(vpsid, nameservers):
    comm=""
    for ns in nameservers:
        comm = comm + " --nameserver " + ns
    
    command = "vzctl set " + str(vpsid) + comm + " --save"
    print command
    status = os.system(command)
    return status

def get_vps_name(vpsid):
    comm = "vzlist -H -o name " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_name(vpsid, name):
    comm = "vzctl set " + str(vpsid) + " --name " + name
    print comm
    status = os.system(comm)
    return status

def get_vps_kmemsize(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "kmemsize"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "kmemsize" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_kmemsize(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --kmemsize " + str(bar) + ":" + str(lim) + " --save"
    print comm
    status = os.system(comm)
    return status

def get_vps_lockedpages(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "lockedpages"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "lockedpages" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_lockedpages(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --lockedpages " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)
    
def get_vps_privvmpages(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "privvmpages"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "privvmpages" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_privvmpages(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --privvmpages " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_shmpages(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "shmpages"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "shmpages" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_shmpages(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --shmpages " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_numproc(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "numproc"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "numproc" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_numproc(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --numproc " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_physpages(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "physpages"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "physpages" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_physpages(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --physpages " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_vmguarpages(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "vmguarpages"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "vmguarpages" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_vmguarpages(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --vmguarpages " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_oomguarpages(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "oomguarpages"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "oomguarpages" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_oomguarpages(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --oomguarpages " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_numtcpsock(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "numtcpsock"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "numtcpsock" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_numtcpsock(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --numtcpsock " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_numflock(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "numflock"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "numflock" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_numflock(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --numflock " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_numpty(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "numpty"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "numpty" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_numpty(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --numpty " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_numsiginfo(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "numsiginfo"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "numsiginfo" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_numsiginfo(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --numsiginfo " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_tcpsndbuf(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "tcpsndbuf"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "tcpsndbuf" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_tcpsndbuf(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --tcpsndbuf " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_tcprcvbuf(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "tcprcvbuf"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "tcprcvbuf" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_tcprcvbuf(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --tcprcvbuf " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_othersockbuf(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "othersockbuf"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "othersockbuf" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_othersockbuf(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --othersockbuf " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_dgramrcvbuf(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "dgramrcvbuf"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "dgramrcvbuf" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_dgramrcvbuf(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --dgramrcvbuf " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_numothersock(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "numothersock"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "numothersock" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_numothersock(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --numothersock " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_dcachesize(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "dcachesize"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "dcachesize" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_dcachesize(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --dcachesize " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_numfile(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "numfile"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "numfile" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_numfile(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --numfile " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_numiptent(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "numiptent"
    elif which == 'm' or which == 'b' or which == 'l' or which == 'f':
        comm = comm + "numiptent" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_numiptent(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --numiptent " + str(bar) + ":" + str(lim) + " --save"
    print comm
    return os.system(comm)

def get_vps_diskspace(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "diskspace"
    elif which == 's' or which == 'h':
        comm = comm + "diskspace" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_diskspace(vpsid, slim, hlim):
    comm = "vzctl set " + vpsid + " --numproc " + str(slim) + ":" + str(hlim) + " --save"
    print comm
    return os.system(comm)

def get_vps_disknodes(vpsid, which):
    comm = "vzlist -H -o "
    if which == 0:
        comm = comm + "disknodes"
    elif which == 's' or which == 'h':
        comm = comm + "disknodes" + "." + which

    comm = comm + " " + str(vpsid)
    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_disknodes(vpsid, bar, lim):
    comm = "vzctl set " + str(vpsid) + " --disknodes " + str(slim) + ":" + str(hlim) + " --save"
    print comm
    return os.system(comm)

def get_vps_laverage(vpsid):
    comm = "vzlist -H -o laverage " +  str(vpsid)

    status = os.popen(comm).readline()
    status = status.strip()
    return status

def get_vps_cpulimit(vpsid):
    comm = "vzlist -H -o cpulimit " + str(vpsid)

    status = os.popen(comm).readline()
    status = status.strip()
    return status

def get_vps_cpulunits(vpsid):
    comm = "vzlist -H -o cpuunits " + str(vpsid)

    status = os.popen(comm).readline()
    status = status.strip()
    return status

def set_vps_cpuunits(vpsid, cpuunits):
    comm = "vzctl set " + str(vpsid) + " --cpuunits " + str(cpuunits) + " --save"
    return os.system(comm)

def set_vps_cpulimit(vpsid, cpulimit):
    comm = "vzctl set " + str(vpsid) + " --cpulimit " + str(cpulimit) + " --save"
    return os.system(comm)

def get_vz_part_status():
    # sample output of 'df -h':
    #--------------------------------------------------------
    # Filesystem            Size  Used Avail Use% Mounted on
    # /dev/sda2              41G   12G   29G  29% /
    #--------------------------------------------------------

    comm = "df /vz"

    line = os.popen(comm).readlines()
    line = line[1].strip() # skip header
    line=line.split()# convert words in line into a list
    return [int(line[1]), int(line[2])] # return size and used alone

def get_hn_mem_status():
    # sample output for 'free -m'
    #------------------------------------------------------------------------
    #            total       used       free     shared    buffers     cached
    #Mem:          436        413         23          0         46        152
    #-/+ buffers/cache:       214        222
    #Swap:         1019         0       1019
    #------------------------------------------------------------------------

    comm = 'free -m'
    lines = os.popen(comm).readlines()

    status=[]
    for line in lines:
        line = line.strip()
        line = line.split()
        if line[0] == "Mem:":
            status.append(int(line[1])) #total
            status.append(int(line[2])) #used
            status.append(int(line[6])) #in cache
            
    return status

def get_hn_swap_status():
    # sample output for 'free -m'
    #------------------------------------------------------------------------
    #            total       used       free     shared    buffers     cached
    #Mem:          436        413         23          0         46        152
    #-/+ buffers/cache:       214        222
    #Swap:         1019         0       1019
    #------------------------------------------------------------------------

    comm = 'free -m'
    lines = os.popen(comm).readlines()

    status=[]
    for line in lines:
        line = line.strip()
        line = line.split()
        if line[0] == "Swap:":
            status.append(int(line[1]))
            status.append(int(line[2]))
            
    return status

def get_hn_cpu_status():
    # sample output from 'top -b -n1'
    #----------------------------------------------------------------------------
    #top - 19:53:32 up  6:08,  5 users,  load average: 0.04, 0.05, 0.05
    #Tasks: 152 total,   2 running, 150 sleeping,   0 stopped,   0 zombie
    #Cpu(s):  2.6% us,  0.6% sy,  0.0% ni, 96.6% id,  0.0% wa,  0.1% hi,  0.0% si
    #Mem:    447416k total,   425456k used,    21960k free,    47396k buffers
    #Swap:  1044216k total,       64k used,  1044152k free,   156676k cached
    #----------------------------------------------------------------------------

    comm = 'top -b -n1'
    lines = os.popen(comm).readlines()

    status=[]
    for line in lines:
        line = line.strip()
        line = line.split()

        #top output consists of empty lines as well
        if len(line) < 1:
            continue

        if line[0] == "Cpu:" or line[0] == "Cpu(s):":
            usage = float(line[1][:-1]) + float(line[3][:-1]) + float(line[5][:-1]) + float(line[9][:-1]) + float(line[11][:-1]) + float(line[13][:-1])  
            status.append(usage)
            
        if line[0] == "Tasks:":
            status.append(int(line[1]))    
            
    return status

def get_hn_power():
    #sample output from vzcpucheck command
    #-------------------------------------
    #Current CPU utilization: 9000
    #Power of the node: 280997
    #-------------------------------------
    
    comm = 'vzcpucheck'
    lines = os.popen(comm).readlines()

    for line in lines:
        line = line.strip()
        line = line.split()

        if line[0] == 'Power':
            hn_power = float(line[4])


    return hn_power
    
def get_vps_user_list(vpsid):
    f = open('/vz/private/' + str(vpsid) + '/etc/passwd')
    lines = f.readlines()

    new_list = []
    for line in lines:
        line = line.split(':')
        new_list.append(line[0])

    f.close()
    return new_list

def set_vps_user_pass(vpsid, user, passwd):
    comm = "vzctl set " + str(vpsid) + " --userpasswd " + user + ':' + passwd
    return os.system(comm)

def vps_destroy(vpsid):
    comm = "vzctl destroy " +  str(vpsid)
    return os.system(comm)
