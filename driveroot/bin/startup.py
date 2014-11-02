# -*- coding: utf-8 -*-

'''
Created on Oct 26, 2011

@author: Valik <vasnake@gmail.com>

 Copyright (C) 2010, Valik Snake
 Originally by Valik <vasnake@gmail.com>, 2010

    This file is part of MovieShell.

    MovieShell is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MovieShell is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MovieShell.  If not, see <http://www.gnu.org/licenses/>.

Russian text

Поскольку в ВыньДос 7 отменили autorun, пришлось написать загрузчик, запускающий Мувишелл.
'''

usage = 'invoke this when disk is plugged in'

import os, sys, time, re, subprocess


def getLogicalDrives(meth = '1'):
    res = []
    print 'getLogicalDrives...'
    # good one (http://stackoverflow.com/questions/827371/is-there-a-way-to-list-all-the-available-drive-letters-in-python)
    if meth == '1':
        import string
        from ctypes import windll
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1
        res = sorted(drives)
    elif meth == '2':
        import win32api
        drives = win32api.GetLogicalDriveStrings()
        drives = sorted(drives.split('\000'))
        for s in drives:
            s = s.strip()
            if s: res.append(s[0:1])
    elif meth == '3': # no network mounts
        import os, re
        drives = re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE)
        for s in drives:
            s = s.strip()
            if s: res.append(s[0:1])
    # MS wbem (http://gallery.technet.microsoft.com/scriptcenter/488836b0-84e9-4c0c-b2cf-dd19f6e70f74)
    elif meth == '4':
        ''' DriveType, DeviceID
        http://msdn.microsoft.com/en-us/library/windows/desktop/aa394173%28v=vs.85%29.aspx
        '''
        import win32com.client
        strComputer = "."
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
        colItems = objSWbemServices.ExecQuery("Select * from Win32_LogicalDisk")
        for objItem in colItems:
            s = objItem.DeviceID.strip().encode('utf8')
            if s: res.append(s[0:1])
            continue
            print '#' * 80
            print "Access: ", objItem.Access
            print "Availability: ", objItem.Availability
            print "Block Size: ", objItem.BlockSize
            print "Caption: ", objItem.Caption
            print "Compressed: ", objItem.Compressed
            print "Config Manager Error Code: ", objItem.ConfigManagerErrorCode
            print "Config Manager User Config: ", objItem.ConfigManagerUserConfig
            print "Creation Class Name: ", objItem.CreationClassName
            print "Description: ", objItem.Description
            print "Device ID: ", objItem.DeviceID # C:
            print "Drive Type: ", objItem.DriveType # 2 - removable disk
            print "Error Cleared: ", objItem.ErrorCleared
            print "Error Description: ", objItem.ErrorDescription
            print "Error Methodology: ", objItem.ErrorMethodology
            print "File System: ", objItem.FileSystem
            print "Free Space: ", objItem.FreeSpace
            print "Install Date: ", objItem.InstallDate
            print "Last Error Code: ", objItem.LastErrorCode
            print "Maximum Component Length: ", objItem.MaximumComponentLength
            print "Media Type: ", objItem.MediaType
            print "Name: ", objItem.Name
            print "Number Of Blocks: ", objItem.NumberOfBlocks
            print "PNP Device ID: ", objItem.PNPDeviceID
            print "Provider Name: ", objItem.ProviderName
            print "Purpose: ", objItem.Purpose
            print "Quotas Disabled: ", objItem.QuotasDisabled
            print "Quotas Incomplete: ", objItem.QuotasIncomplete
            print "Quotas Rebuilding: ", objItem.QuotasRebuilding
            print "Size: ", objItem.Size
            print "Status: ", objItem.Status
            print "Status Info: ", objItem.StatusInfo
            print "Supports Disk Quotas: ", objItem.SupportsDiskQuotas
            print "Supports File-Based Compression: ", objItem.SupportsFileBasedCompression
            print "System Creation Class Name: ", objItem.SystemCreationClassName
            print "System Name: ", objItem.SystemName
            print "Volume Dirty: ", objItem.VolumeDirty
            print "Volume Name: ", objItem.VolumeName
            print "Volume Serial Number: ", objItem.VolumeSerialNumber
            print "Power Management Supported: ", objItem.PowerManagementSupported
            z = objItem.PowerManagementCapabilities
            if z is None:
                a = 1
            else:
                for x in z:
                    print "Power Management Capabilities: ", x
    else:
        raise NameError('getLogicalDrives, error: unknown method')
    return sorted(res, reverse=True)
#def getLogicalDrives():


def findAndRunMovieShell():
    drives = getLogicalDrives()
    print drives
    for d in drives:
        pth = os.path.join(d+':', '.movieslist')
        if os.path.exists(pth):
            pth = os.path.join(d+':', 'ar.cmd')
            if os.path.exists(pth):
                cmd = [pth]
                subprocess.call(cmd)
                break
#~ f:\.movieslist
#~ f:\ar.cmd


if __name__ == '__main__':
    print 'sys.argv[0] = [%s], sys.path[0] = [%s]' % (sys.argv[0], sys.path[0])
    #~ sys.argv[0] = [shell.py], sys.path[0] = [c:\dat\likecd\bin]
    findAndRunMovieShell()
    sys.exit(usage)
