#Peripage A6 F622: Direct printing via Bluetooth 

**The goal of this project is to openly faciliate printing on the Peripage A6 F622. We aim mostly at Linux here, but due to the use of Python this script should be portable to any environment supported by [PyBluez](https://github.com/pybluez/pybluez)**

##Introduction
The Peripage A6 F622 is an inexpensive portable thermo printer. It provides both Bluetooth and USB connectivity. Unlike most other thermo printers it **does not** seem to support ESC/POS or any other standardized printer control language. 

Out of the box, the Peripage A6 F622 can be only controlled using a proprietary app (iOS / Anndroid). There is also a driver for Windows with many limitations, most notably the need of defining a page size before printing; this is a huge limitation, as the Peripage prints on continuous form paper.

The script provided here was built based on an analysis of captured Bluetooth traffic between the printer and an Android device. The Peripage A6 uses the serial profile (BTSPP) and RFCOMM. 

##Prerequisites

- Python 3
- [PyBluez](https://github.com/pybluez/pybluez) is installed and working
- Imagemagick 

The first step is to identify the Bluetooth MAC address of your printer. On Linux, this can be easily done using `hcitool`:

```bash
elias@luna:~$ hcitool scan
Sc`anning ...
B5:5B:13:08:F6:22	PeriPage_F622
elias@luna:~$ 
```

##Preparing an image for printing
Right now, the script does not yet accept images in native formats such as PNG or JPEG (TODO). As of now, the images have to be converted to raw bitmaps for printing.

For best results, you're should convert the image to a 1-bit monochrome image in GIMP or any tool that provides you visual feedback about dithering.
However, you can also simply convert arbitary image using `convert` as follows:

```bash
convert -resize 384x -negate +dither -monochrome -depth 1 IMAGE.JPG gray:image.data
``` 

## Printing

With the image converted and the BT MAC known, printing is straightforward
```bash
./ppa6-printImage.py [BT MAC ADDRESS] [RAW IMAGE FILE]
``` 

*Example*
```bash
/ppa6-printImage.py B5:5B:13:08:F6:22 ../statlib.data 
``` 

## Status and future work

This script is currently a proof of concept. The goal was simply to make printing work. There are a lot of unknowns yet with regard to the actual printer communication.

Todo:
- Native image support
- Printer scanning & auto-detection
- Text print
- Licence

