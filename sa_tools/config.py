# -*- coding: UTF-8 -*-

from typing     import Dict, Any, Optional
from time       import sleep
from pathlib    import Path

from sa_tools   import saLogs
from __init__   import __app_name__

import json
import os

log   = saLogs()

class saConfig:
  def __init__(self):
    self.config = {}

    self.home = str(Path.home())
    self.config_dir = f'{self.home}/.config/{__app_name__}'
    self.config_file = f'{self.config_dir}/settings.json'

    # check if directory exists
    try :
      if not os.path.exists(self.config_dir) :
        os.mkdir(self.config_dir)
    except Exception as e :
      log.error(msg = 'Can not create directory', exception = e)
      os._exit(10)

  def __del__(self) :
    pass

  
  def load(self) :
    """
    load settings from file
    """
    if os.path.exists(self.config_file) :
      with open(self.config_file) as json_file:
        self.config = json.load(json_file)
    else :
      # create empty config
      with open(self.config_file, 'w+') as outfile:
        json.dump({}, outfile)

    return True


  def save(self) :
    """
    save current config into file
    do not save when config exist and current config is None
    """
    if len(self.config) > 0  :
      with open(self.config_file, 'w+') as outfile:
        json.dump(self.config, outfile)
    return True

  