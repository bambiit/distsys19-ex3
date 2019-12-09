from Tkinter import *
from LowLevelGUI import *
import time
import datetime
import thread

LIGHT_DURATION_MS = 2000

class DWatchGUI:

  def __init__(self, parent, eventhandler):
    self.GUI = LowLevelGUI(parent, self)

    self.eventhandler = eventhandler
    self.parent = parent
    self.start_holding_button = 0
    self.chrono_mode = False
    self.display_time_mode = True
    self.edit_mode = False
    self.is_edit_mode_while_pressing_a_button = False

    self.handleEventOn()

    self.lightOffTimer = None
  
  def handleEventOn(self):
    self.eventhandler.event("on")
  
  def wait(self):
    self.eventhandler.event("lightOff2")
    print "wait"

  # -----------------------------------
  # Events to be sent to the Statechart
  # -----------------------------------

  def topRightPressed(self):
    self.eventhandler.event("lightOn")
    if self.lightOffTimer is not None:
      self.parent.after_cancel(self.lightOffTimer)
    print "topRightPressed"

  def topRightReleased(self):
    self.lightOffTimer = self.parent.after(LIGHT_DURATION_MS, self.lightOff)
    print "topRightReleased"

  def lightOff(self):
    self.eventhandler.event("lightOff")


  def topLeftPressed(self):
    print "topLeftPressed"

  def topLeftReleased(self):
    print "topLeftReleased"
    if self.display_time_mode:
      self.turnOnChronoMode()
      self.turnOffTimeDisplayMode()
      self.refreshChronoDisplay()

    elif self.chrono_mode:
      self.eventhandler.event("display_time_mode")
      self.turnOffChronoMode()
      self.turnOnTimeDisplayMode()
      self.refreshTimeDisplay()

    
  def bottomRightPressed(self):
    self.start_holding_button = datetime.datetime.now()
    self.eventhandler.event("bottomRightPressed")
    if self.display_time_mode:
      self.current_mode_while_pressing_a_button = False
    elif self.edit_mode:
      self.is_edit_mode_while_pressing_a_button = True
    elif self.chrono_mode:
      self.eventhandler.event("initChrono")


  def chronoRunning(self):
      for i in range(25):
        self.increaseChronoByOne()
      if self.chrono_mode:
        self.refreshChronoDisplay()

  def bottomRightReleased(self):
    self.eventhandler.event("released")
    diff = datetime.datetime.now() - self.start_holding_button
    holding_duration = round(float(diff.total_seconds()), 1)

    if self.display_time_mode and not self.is_edit_mode_while_pressing_a_button:
      if holding_duration >= 1.5:
        self.eventhandler.event("editTime")

    elif self.edit_mode or self.is_edit_mode_while_pressing_a_button:
      if holding_duration >= 2:
        self.eventhandler.event("finishEdit")
        self.is_edit_mode_while_pressing_a_button = False
        print"PLEASE"



  def bottomLeftPressed(self):
    if self.chrono_mode:
      self.eventhandler.event("resetChrono")
    self.eventhandler.event("increase")
    self.eventhandler.event("setAlarm")

  def bottomLeftReleased(self):
    self.eventhandler.event("stopInc")
    self.eventhandler.event("onoff")
    print "bottomLeftReleased"

  def alarmStart(self):
    self.eventhandler.event("alarming")
    print "alarmStart"

  # -----------------------------------
  # Interaction with the GUI elements
  # -----------------------------------
  #Modify the state:

  def refreshTimeDisplay(self):
    self.GUI.drawTime()

  def refreshChronoDisplay(self):
    self.GUI.drawChrono()

  def refreshDateDisplay(self):
    self.GUI.drawDate()

  def refreshAlarmDisplay(self):
    self.GUI.drawAlarm()
 
  def increaseTimeByOne(self):
    self.GUI.increaseTimeByOne()

  def resetChrono(self):
    self.GUI.resetChrono()
    
  def increaseChronoByOne(self):
    self.GUI.increaseChronoByOne()
    
  #Select current display:
  
  def startSelection(self):
    self.GUI.startSelection()
    
  def selectNext(self):
    self.GUI.selectNext() 
       
  #Modify the state corresponing to the selection 
  def increaseSelection(self):
    self.GUI.increaseSelection()
        
  def stopSelection(self):
    self.GUI.stopSelection()
                    
         
  #Light / Alarm:
  
  def setIndiglo(self):
    self.GUI.setIndiglo()
    
  def unsetIndiglo(self):
    self.GUI.unsetIndiglo()
    
  def setAlarm(self):
    self.GUI.setAlarm()

  # Query 
  def getTime(self):
    return self.GUI.getTime()

  def getAlarm(self):
    return self.GUI.getAlarm()
     
  #Check if time = alarm set time
  def checkTime(self):
    if self.GUI.getTime()[0] == self.GUI.getAlarm()[0] and self.GUI.getTime()[1] == self.GUI.getAlarm()[1] and self.GUI.getTime()[2] == self.GUI.getAlarm()[2]:
      return True
    else:
      return False


  # Update running time for every second
  def updateRunningTime(self):
    self.increaseTimeByOne()
    if self.display_time_mode or self.edit_mode:
      self.refreshTimeDisplay()

  # Turn on/off Time Display Mode

  def turnOnEditMode(self):
    self.edit_mode = True

  def turnOffEditMode(self):
    self.edit_mode = False

  def turnOnTimeDisplayMode(self):
    self.display_time_mode = True

  def turnOffTimeDisplayMode(self):
    self.display_time_mode = False

  def turnOnChronoMode(self):
    self.chrono_mode = True

  def turnOffChronoMode(self):
    self.chrono_mode = False