#!/usr/bin/env python3
import bluetooth
import argparse
import time
import sys
from PIL import Image, ImageOps, ImageEnhance
from tqdm import tqdm
import qrcode
from cairosvg import svg2png
from io import BytesIO

parser = argparse.ArgumentParser(description="Print an image to a Peripage A6 via Bluetooth")
parser.add_argument("BTMAC",help="BT MAC address of the Peripage A6")

parser.add_argument("-i", "--imagefile",type=str, help="Image file to be printed (JPG,PNG,TIF...)")
parser.add_argument("-s","--svg",type=str,help="SVG file to be printed (.svg / .svgz")
parser.add_argument("-qr","--qrcode",type=str, help="Content of the QR code to be printed")
parser.add_argument("-b", "--brightness", type=float, help="Adjust the brightness using a factor ")
parser.add_argument("-c", "--contrast", type=float, help = "Enhance contrast using a factor")
parser.add_argument("-nf","--nofeed", action="store_true", help="Do not feed extra paper after printing (use for seamless printing")
args = parser.parse_args();

host = args.BTMAC
printargs=0

if (args.imagefile):
    printargs=printargs+1
if (args.qrcode):
    printargs=printargs+1
if (args.svg):
    printargs=printargs+1

if (printargs>1):
    print("ERROR: Please specfiy only one printing mode out of --imagefile, --qr or --svg")
    sys.exit(1)

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


def loadImageFromFileName(filename):
    # Load Image and process it
    img = Image.open(filename)
    return img

def loagImageFromSVG(filename):
    png_data = svg2png(file_obj=open(filename,"rb"),background_color="#FFFFFF",output_width=384)
    return Image.open(BytesIO(png_data))

def printImage(img):
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

    new_width = 384 #Peripage A6 image width
    scale = new_width / float(img_width)
    new_height = int(img_height * scale)

    print ("Source image dimensions: ", img_width, img_height)
    print ("Printing image dimensions:", new_width, new_height)

    if (new_height>65535):
        print ("Target image height is too large. Can't print this (yet)")
        sys.exit(1)

    img = img.resize((384, new_height), Image.ANTIALIAS)

    img = img.convert("1")
    # write chunks of 122 bytes to printer
    cmd = bytes.fromhex("10fffe01")
    sock.send(cmd)
    chunksize = 122
    sock.send(bytes.fromhex("000000000000000000000000"))
    height_bytes=(new_height).to_bytes(2, byteorder="little")
    cmd = bytes.fromhex("1d7630003000")+height_bytes
    sock.send(cmd)

    # send image to printer
    image_bytes = img.tobytes()

    print("Printing %d chunks" % (len(image_bytes)/chunksize))
    print()
    for i in tqdm(range(0, len(image_bytes), chunksize)):
        chunk = image_bytes[i:i + chunksize]
        sock.send(chunk)
        time.sleep(0.02)
    if not args.nofeed:
        print("Feeding...")
        emptyLine=[0 for i in range(1,122)];
        for i in range(1,35):
            sock.send(bytes(emptyLine))
            time.sleep(0.02)
    sock.send(bytes.fromhex("1b4a4010fffe45"))
    print("Printing complete")


print("Connecting")
sock.connect((host, 1))

deviceName = getDeviceName()
print("Device Name", deviceName)
print("Device Info", getFWDPI())
print("Serial Number", getSerial())

print("Resetting device")
reset()

if args.imagefile:
    print("Printing image", args.imagefile)
    printImage(loadImageFromFileName(args.imagefile))
if args.qrcode:
    print("Printing QR code with content:", args.qrcode)
    printImage(qrcode.make(args.qrcode))
if (args.svg):
    print("Printing SVG fike", args.svg)
    printImage(loagImageFromSVG(args.svg))