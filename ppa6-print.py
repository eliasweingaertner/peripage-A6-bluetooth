#!/usr/bin/env python3
import bluetooth
import argparse
import time
import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFont, ImageDraw
from tqdm import tqdm
import qrcode


parser = argparse.ArgumentParser(description="Print an image to a Peripage A6 via Bluetooth")
parser.add_argument("BTMAC",help="BT MAC address of the Peripage A6")

parser.add_argument("-i", "--imagefile",type=str, help="Image file to be printed (JPG,PNG,TIF...)")
parser.add_argument("-qr","--qrcode",type=str, help="Content of the QR code to be printed")
parser.add_argument("-t", "--text", type=str, help="Text to be printed")
parser.add_argument("-b", "--brightness", type=float, help="Adjust the brightness using a factor ")
parser.add_argument("-c", "--contrast", type=float, help = "Enhance contrast using a factor")
parser.add_argument("-nf","--nofeed", action="store_true", help="Do not feed extra paper after printing (use for seamless printing")
args = parser.parse_args();

host = args.BTMAC

if (not args.imagefile) and (not args.qrcode) and (not args.text):
    print("ERROR: --imagefile, --qrcode, or --text have to be given")
    parser.print_help()
    sys.exit(1)

if len(list(filter(None, map(bool, [args.imagefile, args.qrcode, args.text])))) > 1:
    print("ERROR: Only --imagefile, --qrcode, or --text can be used")
    parser.print_help()
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


def generateImageFromString(s):
    font = ImageFont.truetype("liberation-mono/LiberationMono-Regular.ttf", 24)
    size = font.getsize_multiline(s)
    size_x = 384 if size[0] <= 384 else size[0]
    size_y = size[1]
    img = Image.new("RGBA", size=(size_x, size_y), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), s, (0, 0, 0), font=font)
    return img


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
if args.text:
    print("Printing text:", args.text)
    printImage(generateImageFromString(args.text))
