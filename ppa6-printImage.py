#!/usr/bin/env python3
import bluetooth
import sys

if (len(sys.argv)<3):
    print("Error: not enough parameters")
    print("Use:")
    print("./ppa6-printImage.py [BT MAC ADDRESS OF PERIPAGE A6] [RAW IMAGE FILE]")
    sys.exit(1)

host=sys.argv[1]
imageFile=sys.argv[2]

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

def getDeviceName():
    cmd = bytes.fromhex("10ff3011")
    sock.send(cmd)
    data = sock.recv(1024)
    return data

def getFWDPI():
    cmd = bytes.fromhex("10ff20f1")
    sock.send(cmd)
    data = sock.recv(1024)
    return data

def getSerial():
    cmd = bytes.fromhex("10ff20f2")
    sock.send(cmd)
    data = sock.recv(1024)
    return data

def reset():
    cmd = bytes.fromhex("10ff50f1")
    sock.send(cmd)
    data = sock.recv(1024)
    cmd = bytes.fromhex("000000000000000000000000")
    sock.send(cmd)
    return data

def reset2():
    cmd = bytes.fromhex("10ff100002")
    sock.send(cmd)
    data = sock.recv(1024)
    return data

def newline():
    cmd = bytes.fromhex("10fffe01")
    sock.send(cmd)
    sock.send('\n')


def printString(outputString):
    cmd = bytes.fromhex("10fffe01")
    sock.send(cmd)
    line=bytes(outputString, "ascii")
    sock.send(line)

def printImage(filename):
    binaryFile = open (filename,"rb")
    #write chunks of 122 bytes to printer
    cmd = bytes.fromhex("10fffe01")
    sock.send(cmd)
    chunksize=122
    sock.send(bytes.fromhex("000000000000000000000000"))
    #cmd = bytes.fromhex("1d76300030008001")
    cmd = bytes.fromhex("1d76300030008005")
    sock.send(cmd)


    bArray = bytes(binaryFile.read())
    for i in range(0,len(bArray),chunksize):
        chunk = bArray[i:i+chunksize]
        print("Sending chunk", i, chunk)
        sock.send(chunk)


print("Connecting")
sock.connect((host,1))

deviceName = getDeviceName()
print ("Device Name", deviceName)
print ("Device Info", getFWDPI())
print ("Serial Number", getSerial())

print ("Resetting device", reset())
printImage(imageFile)
