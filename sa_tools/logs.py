# -*- coding: UTF-8 -*-

#
# version:   20190605
# developer: alexander@konyukov.com
#

import logging
import json
import sys

from datetime   import datetime
from __init__   import __version__
from __init__   import __application__
from __init__   import __log_type__

logger = logging.getLogger()

class saLogs:
  APP = None
  MSG_TYPE = None

  def __init__(self):
    self.APP = __application__
    self.MSG_TYPE = __log_type__
  
  def info(self, msg, **kwargs):
    tmp = {}
    tmp['timestamp'] = str(datetime.utcnow()) + " UTC"
    #tmp['version'] = __version__
    #tmp['message_type'] = self.MSG_TYPE
    #tmp['application'] = self.APP
    tmp['level'] = 'info'

    tmp['msg'] = msg

    try :
      if  kwargs is not None: 
        for key, value in kwargs.items():
          tmp[key] = str(value)
    except :
      pass

    try :
      logger.warning( json.dumps(tmp) )
    except :
      print ( "---- INFO ----------------------" )
      print ( tmp )
      print ( "----- E N D ----------------" )

  def error(self, msg, **kwargs): 
    tmp = {}
    tmp['timestamp'] = str(datetime.utcnow()) + " UTC"
    #tmp['version'] = __version__
    #tmp['message_type'] = self.MSG_TYPE
    #tmp['application'] = self.APP
    tmp['level'] = 'error'

    tmp['msg'] = msg

    try :
      if  kwargs is not None: 
        for key, value in kwargs.items():
          tmp[key] = str(value)
    except :
      pass

    try :
      logger.warning( json.dumps(tmp) )
    except :
      print ( "---- ERROR ----------------------" )
      print ( tmp )
      print ( "----- E N D ----------------" )

  def warning(self, msg, **kwargs): 
    tmp = {}
    tmp['timestamp'] = str(datetime.utcnow()) + " UTC"
    #tmp['version'] = __version__
    #tmp['message_type'] = self.MSG_TYPE
    #tmp['application'] = self.APP
    tmp['level'] = 'warning'

    tmp['msg'] = msg

    try :
      if  kwargs is not None: 
        for key, value in kwargs.items():
          tmp[key] = str(value)
    except :
      pass

    try :
      logger.warning( json.dumps(tmp) )
    except :
      print ( "---- WARNING ----------------------" )
      print ( tmp )
      print ( "----- E N D ----------------" )

  def debug(self, msg, **kwargs): 
    tmp = {}
    tmp['timestamp'] = str(datetime.utcnow()) + " UTC"
    #tmp['version'] = __version__
    #tmp['message_type'] = self.MSG_TYPE
    #tmp['application'] = self.APP
    tmp['level'] = 'debug'

    tmp['msg'] = msg

    try :
      if  kwargs is not None: 
        for key, value in kwargs.items():
          tmp[key] = str(value)
    except :
      pass

    try :
      logger.warning( json.dumps(tmp) )
    except :
      print ( "---- DEBUG ----------------------" )
      print ( tmp )
      print ( "----- E N D ----------------" )

