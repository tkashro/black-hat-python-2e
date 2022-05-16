#!/usr/bin/env python3
import os
import servicemanager
import shutil
import subprocess
import sys

import win32event
import win32service
import win32serviceutil


SRCDIR = 'C:\\Users\\thomas\\work'
TGTDIR = 'C:\\Windows\\TEMP'


class BHServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "BlackHatService"
    _svc_display_name_ = "Black Hat Service"
    _svc_description_ = ("Executes VBScripts at regular intervals." +
                         " What could possibly go wrong?")

    def __init__(self, args):
        self.vbs = os.path.join(TGTDIR, 'bhservice_task.vbs')
        self.timeout = 1000 * 60

        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.main()

    def main(self):
        while True:
            ret_code = win32event.WaitForSingleObject(
                self.hWaitStop, self.timeout
            )
            if ret_code == win32event.WAIT_OBJECT_O:
                servicemanager.LogInfoMsg('Service is stopping')
                break
            src = os.path.join(SRCDIR, 'bhservice_taks.vbs')
            subprocess.call('cscript.exe {0}'.format(self.vbs), shell=False)
            os.unlink(self.vbs)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(BHServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(BHServerSvc)
