# Peripage A6 F622: Direct printing via Bluetooth 

**The goal of this project is to openly faciliate printing on the Peripage A6 F622. We aim mostly at Linux here, but due to the use of Python this script should be portable to any environment supported by [PyBluez](https://github.com/pybluez/pybluez)**

## Introduction
The Peripage A6 F622 is an inexpensive portable thermo printer. It provides both Bluetooth and USB connectivity. Unlike most other thermo printers it **does not** seem to support ESC/POS or any other standardized printer control language. 

So far, the Peripage A6 F622 can be only controlled using a proprietary app (iOS / Anndroid). There is also a driver for Windows with many limitations, most notably the need of defining a page size before printing; this is a huge limitation, as the Peripage prints on continuous form paper.

The script provided here was built based on an analysis of captured Bluetooth traffic between the printer and an Android device. The Peripage A6 uses the serial profile (BTSPP) and RFCOMM. 

## Prerequisites

- Python 3 and PIP
- Peripage A6 printer (obviously)

### Install dependencies

This script requires the following dependencies:
- Pybluez
- Pillow
- Argparse
- tqdm

You can simply install all requirements using PIP:

```bash
pip install -r requirements.txt
```

The next step is to identify the Bluetooth MAC address of your printer. On Linux, this can be easily done using `hcitool`:

```bash
elias@luna:~$ hcitool scan
Scanning ...
B5:5B:13:08:F6:22	PeriPage_F622
elias@luna:~$ 
```
## Printing
With the image converted and the BT MAC known, printing is straightforward
```bash
./ppa6-printImage.py [BT MAC ADDRESS] [IMAGE FILE]
``` 
You can use all common raster image formats for printing (PNG, JPG, GIF...)

*Example*
```bash
/ppa6-printImage.py B5:5B:13:08:F6:22 image.jpg
``` 

### Manipulating brightness and contrast for printing
In many cases, the print quality dramatically improves if the brightness or the contrast
of the image is adjusted. This can be done using the `-b` and `-b` parameters.

*Example*
The example reduces the contrast using a factor of 0.75 and increases the brightness using a factor of 1.5.

```bash
/ppa6-printImage.py -c 0.75 -b 1.5 B5:5B:13:08:F6:22 image.jpg
``` 

## Status and future work

This script is a proof of concept. gThe goal was simply to make printing work. There are a lot of unknowns yet with regard to the actual printer communication.

Todo:
- Printer scanning & auto-detection
- Text print

