#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess
import picamera
import time
import cups

conn = cups.Connection()

# GPIO setup
GPIO.setmode(GPIO.BCM)
SWITCH = 24
GPIO.setup(SWITCH, GPIO.IN)
RESET = 25
GPIO.setup(RESET, GPIO.IN)
PRINT_LED = 22
POSE_LED = 18
BUTTON_LED = 23
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)
GPIO.output(PRINT_LED, False)

while True:
  if (GPIO.input(SWITCH)):
    snap = 0
    while snap < 4:
      print("pose!")
      GPIO.output(BUTTON_LED, False)
      GPIO.output(POSE_LED, True)
      time.sleep(1.5)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.4)
        GPIO.output(POSE_LED, True)
        time.sleep(0.4)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.1)
        GPIO.output(POSE_LED, True)
        time.sleep(0.1)
      GPIO.output(POSE_LED, False)
      print("SNAP")

      gpout = subprocess.check_output("raspistill -o /home/pi/photobooth_images/qfc/{time.strftime("%H:%M:%S")}.jpg", stderr=subprocess.STDOUT, shell=True)
      print(gpout)
      if "ERROR" not in gpout: 
        snap += 1
      GPIO.output(POSE_LED, False)
      time.sleep(0.2)
    print("please wait while your photos print...")
    GPIO.output(PRINT_LED, True)
    # build image and send to printer
    subprocess.call("sudo /home/pi/scripts/photobooth/assemble_and_print", shell=True)
    # TODO: implement a reboot button
    # Wait to ensure that print queue doesn't pile up
    # TODO: check status of printer instead of using this arbitrary wait time

    # this should find the print queue and return the job state
    #conn.getJobAttributes(printer_returns)["job-state"]
    #but I'm not sure how to check to see if it equals 9 - job completed
    #equals 9 (IPP_JOB_COMPLETED)
    # if the print queue doesn't work, use this: 
    time.sleep(110)
    print("ready for next round")
    GPIO.output(PRINT_LED, False)
    GPIO.output(BUTTON_LED, True)
