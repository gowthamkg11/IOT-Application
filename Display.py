import sys
import RPi.GPIO as GPIO
from time import sleep
import os
from I2C_device import *
 
# LCD Address
ADDRESS = 0x3f # base address as detected with i2cdetect above
 
# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80
 
# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00
 
# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00
 
# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00
 
# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00
 
# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00
 
En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

#Play button
PLAY= 17



# Define some device constants
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line 
 
class DisplayLcd(object):
    
   #initializes objects and lcd
   def __init__(self, addr=ADDRESS, port=1):
      self.device = I2C_device(addr, port)
      self.write(LCD_FUNCTIONSET | LCD_8BITMODE)
      self.write(LCD_RETURNHOME)
      self.write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      self.write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      self.write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
      sleep(0.2)
 
   # clocks EN to latch command
   def strobe(self, data):
      self.device.write_cmd(data | En | LCD_BACKLIGHT)
      sleep(.0005)
      self.device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
      sleep(.0001)
 
   def write_four_bits(self, data):
      self.device.write_cmd(data | LCD_BACKLIGHT)
      self.strobe(data)
 
   # write a command to lcd
   def write(self, cmd, mode=0):
      self.write_four_bits(mode | (cmd & 0xF0))
      self.write_four_bits(mode | ((cmd << 4) & 0xF0))
 
   # put string function
   def display_string(self, string, line):
      if line == 1:
         self.write(0x80)
      if line == 2:
         self.write(0xC0)
      if line == 3:
         self.write(0x94)
      if line == 4:
         self.write(0xD4)
      for char in string:
         self.write(ord(char), Rs)
 
   # clear lcd and set to home
   def clear(self):
      self.write(LCD_CLEARDISPLAY)
      self.write(LCD_RETURNHOME)
 
   #Writing values into LCD
   def send_to_LCD(self):
      f=os.popen("mpc current")
      list1=f.readlines()
      str1=''.join(list1)
      str1.ljust(20,' ')
      j=str1[0:20]
      k=str1[21:40]
      l=str1[41:60]
      m=str1[61:80]
      n=str1[81:100]
      self.clear()
      self.display_string(j,1)
      self.display_string(k,2)
      self.display_string(l,3)
      self.display_string(m,4)
      self.display_string(n,1)
           
               
            