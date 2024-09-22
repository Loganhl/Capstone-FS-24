import pywin.framework
import pywin32_system32
import pywin
import win32serviceutil
import win32event
import win32service
import socket
import servicemanager

class KsLogService(win32serviceutil.ServiceFramework):
    """base class to create a windows service python"""
    
    _svc_name = "kslogservice"
    _svc_display_name ='kslogger'

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
        super().__init__(args)
        
    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name,''))
        self.main()
    
    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass
    
    def stop(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass
    