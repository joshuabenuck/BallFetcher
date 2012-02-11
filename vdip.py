import serial
import binascii
import sys

def read(p):
    value = ""
    while 1:
        c = p.read(100)
        value += binascii.hexlify(c)
        print c
        if c == "": break
    return value

classes = {"ff":"Vendor Specific", "08":"Mass Storage", "0a":"CDC-Data",
  "02":"Communications and CDC Control"}
def formatDescriptor(d):
  #d = d[1:]
  if d[:2] == "00": return
  print "Record: ", d
  print "Address: ", d[:2]
  print "Control Endpoint 0 Size: ", d[2:4]
  print "Pipe In End Point Number: ", d[4:6]
  print "Pipe In End Point Size: ", d[6:8]
  print "Pipe Out End Point Number: ", d[8:10]
  print "Pipe Out End Point Size: ", d[10:12]
  print "Data Toggles: ", d[12:14]
  print "Device Type: ", d[14:16]
  print "Reserved: ", d[16:18]
  print "Location: ", d[18:20]
  print "MI Index: ", d[20:22]
  print "Device Class: ", classes[d[22:24]]
  print "Device Sub Class: ", d[24:26]
  print "Device Protocol: ", d[26:28]
  print "Vendor ID: ", d[28:32]
  print "Product ID: ", d[32:36]
  print "BCD: ", d[36:40]
  print "Device Speed: ", d[40:42]
  print ""

def enumerate(p):
    print "Enumerating bus."
    devices = ["\x00", "\x01", "\x02", "\x03", "\x04", "\x05", "\x06", 
               "\x07", "\x08", "\x09", "\x0A", "\x0B", "\x0C", "\x0D", 
               "\x0E", "\x0F"]
    for d in devices:
        p.write("QD %s\r"%d)
        descriptor = read(p)
        formatDescriptor(descriptor)

print "Opening."
p = serial.Serial("/dev/tty.usbserial-FTD5L1K2", 9600, timeout=1)
print "Writing QP2."
#p.write("QP1\r")
p.write("QP2\r")
print read(p)

#enumerate(p)
print "Setting device."
p.write("SC \x00\r")
print read(p)

print "Setup for IN packet."
"""
#define USB_SETUP_TYPE_VENDOR                   0x40
#define USB_SETUP_DEVICE_TO_HOST                0x80
#define USB_SETUP_RECIPIENT_DEVICE              0x00
int AndroidAccessory::getProtocol(byte addr)
{
    uint16_t protocol = -1;
    usb.ctrlReq(addr, 0,
                USB_SETUP_DEVICE_TO_HOST |
                USB_SETUP_TYPE_VENDOR |
                USB_SETUP_RECIPIENT_DEVICE,
                ACCESSORY_GET_PROTOCOL, 0, 0, 0, 2, (char *)&protocol);
    return protocol;
}
"""
USB_SETUP_DEVICE_TO_HOST = 0x80
USB_SETUP_TYPE_VENDOR = 0x40
USB_SETUP_RECIPIENT_DEVICE = 0x00
# Request Type
# 0 10 00000 = 0x80
# 1 10 00000 = 0xC0
# Request Type
# 0x51
request = {"type":"c0",
           "request":"33",
           "value":"0000", "index":"0000",
           "length":"0200"}
cmd = "SSU $%(type)s%(request)s%(value)s%(index)s%(length)s\r"%request
print cmd
p.write(cmd)
print read(p)

print "Reading."
p.write("DRD\r")
response = read(p)
if response[:2] != "10":
    print "Device does not support accessory mode."
    sys.exit(0)
print "Device supports accessory mode version 1!"

"""
request = {"type":"c0", "request":"33",
           "value":"0000", "index":"0000",
           "length":"0200"}
cmd = "SSU $%(type)s%(request)s%(value)s%(index)s%(length)s\r"%request
print cmd
p.write(cmd)
print read(p)
"""

#enumerate(p)
