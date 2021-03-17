#!/usr/bin/env python3
import bluetooth
import argparse
from PIL import Image, ImageOps, ImageEnhance
from tqdm import tqdm


parser = argparse.ArgumentParser(description="Print an image to a Peripage A6 via Bluetooth")
parser.add_argument("BTMAC",help="BT MAC address of the Peripage A6")
parser.add_argument("imagefile",help="Image file to be printed (JPG,PNG,TIF...)")
parser.add_argument("-b", "--brightness", type=float, help="Adjust the brightness using a factor ")
parser.add_argument("-c", "--contrast", type=float, help = "Enhance contrast using a factor")

args = parser.parse_args();

host = args.BTMAC
imageFile = args.imagefile

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
    line = bytes(outputString, "ascii")
    sock.send(line)


def printImage(filename):
    # binaryFile = open (filename,"rb")


    # Load Image and process it
    img = Image.open(filename)
    img = img.convert("L")

    img_width = img.size[0]
    img_height = img.size[1]

    # brightness / contrast
    if args.brightness:
        print("Enhancing brightness with factor ", args.brightness)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(args.brightness)

    if args.contrast:
        print("Enhancing brightness with contrast ", args.contrast)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(args.contrast)

    img = ImageOps.invert(img)

    scale = 384 / float(img_width)
    new_height = img_height * scale
    img = img.resize((384, int(new_height)), Image.ANTIALIAS)

    img = img.convert("1")
    # write chunks of 122 bytes to printer
    cmd = bytes.fromhex("10fffe01")
    sock.send(cmd)
    chunksize = 122
    sock.send(bytes.fromhex("000000000000000000000000"))
    cmd = bytes.fromhex("1d76300030008005")
    sock.send(cmd)

    # send image to printer
    image_bytes = img.tobytes()

    print("Printing %d chunks" % (len(image_bytes)/chunksize))
    print()
    for i in tqdm(range(0, len(image_bytes), chunksize)):
        chunk = image_bytes[i:i + chunksize]
        sock.send(chunk)
    print("Printing complete")

print("Connecting")
sock.connect((host, 1))

deviceName = getDeviceName()
print("Device Name", deviceName)
print("Device Info", getFWDPI())
print("Serial Number", getSerial())

print("Resetting device")
reset()
printImage(imageFile)
