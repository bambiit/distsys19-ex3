from Tkinter import *
from LowLevelGUI import *
import time
import datetime
import thread

class DWatchGUI:

  def __init__(self, parent, eventhandler):
    self.GUI = LowLevelGUI(parent, self)

    self.eventhandler = eventhandler
    self.start_holding_button = 0
    self.backgroundChronoMode = False
    self.display_time_mode = True

    self.handleEventOn()
  
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
    print "topRightPressed"

  def topRightReleased(self):
    self.eventhandler.event("lightOff")
    print "topRightReleased"
  
  def topLeftPressed(self):
    print "topLeftPressed"
    self.backgroundChronoModeOff()

  def topLeftReleased(self):
    print "topLeftReleased"
    self.eventhandler.event("changeMode")
    
  def bottomRightPressed(self):
    self.start_holding_button = datetime.datetime.now()
    self.eventhandler.event("bottomRightPressed")

    if self.display_time_mode is False:
      self.eventhandler.event("initChrono")

  def chronoRunning(self):
      for i in range(25):
        self.increaseChronoByOne()

  def backgroundChrono(self):
    if(self.backgroundChronoMode == True):
      time.sleep(0.25)
      self.chronoRunning()
      self.backgroundChrono()

  def startThreadBackgroundChrono(self):
    if self.backgroundChronoMode == True:
      thread.start_new_thread(self.backgroundChrono, ())

  def backgroundChronoModeOn(self):
    self.backgroundChronoMode = True

  def backgroundChronoModeOff(self):
    self.backgroundChronoMode = False

  def bottomRightReleased(self):
    self.eventhandler.event("released")
    diff = datetime.datetime.now() - self.start_holding_button
    holding_duration = round(float(diff.total_seconds()), 1)

    if holding_duration >= 2:
      self.eventhandler.event("finishEdit")
    elif holding_duration >= 1.5:
      self.eventhandler.event("editTime")
    self.start_holding_button = 0

  def bottomLeftPressed(self):
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
    self.refreshTimeDisplay()    

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
    if self.display_time_mode:
      self.GUI.increaseTimeBySecond()
      self.refreshTimeDisplay()

    while self.display_time_mode == False:
      self.GUI.increaseTimeBySecond()
      time.sleep(1)

  # Stop waiting for edit, expired for 5 seconds
  def waitingEditExpired(self):
    self.eventhandler.event("finishEdit")

  # Turn on/off Time Display Mode
  def turnOffTimeDisplayMode(self):
    self.display_time_mode = False
    thread.start_new_thread(self.updateRunningTime, ())

  def turnOnTimeDisplayMode(self):
    self.display_time_mode = True
