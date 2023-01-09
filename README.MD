# Peripage A6 F622: Direct printing via Bluetooth

**This scripts enables printing on the Peripage A6 F622. We aim mostly at Linux here, but due to the use of Python this script should be portable to any environment supported by [PyBluez](https://github.com/pybluez/pybluez)**

## Introduction
The Peripage A6 F622 is an inexpensive portable thermo printer. It provides both Bluetooth and USB connectivity. Unlike most other thermo printers it **does not** seem to support ESC/POS or any other standardized printer control language.

So far, the Peripage A6 F622 can be only controlled using a proprietary app (iOS / Anndroid). There is also a driver for Windows with many limitations, most notably the need of defining a page size before printing; this is a huge limitation, as the Peripage prints on continuous form paper.

The script provided here was built based on an analysis of captured Bluetooth traffic between the printer and an Android device. The Peripage A6 uses the serial profile (BTSPP) and RFCOMM.

Essentially, the script takes an input images, scales it to the printers native X resolution of 384 pixels, and then sends it to the printer.

**Please note:** This script is mostly a proof of concept. Printing stuff works mostly fine. However, don't expect a
polished Python3 library here. Kudos go out to [bitrate16](https://github.com/bitrate16) for turning this
hack into a proper Python3 library, [ppa6](https://github.com/bitrate16/ppa6-python)!

## What is currently working?
- Printing Images (JPG, PNG,...)
- Printing SVG files  
- Direct printing of QR codes
- Manipulation of Brightness  / Contrast (via Image)
- Toggle Paper feeding

## Prerequisites

- Python 3 and PIP
- Peripage A6 printer (obviously)

### Install dependencies

This script requires the following dependencies:
- Pybluez (Bluetooth connectivity)
- Pillow (Image handling)
- argparse (Argument parser)
- tqdm (Progress bar)
- qrcode (qr code generation)
- cairosvg (svg rendering)

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
## Printing Images
Once you know the BT MAC address, printing is straightforward
```bash
./ppa6-print.py -i [IMAGE FILE] [BT MAC ADDRESS]
```
You can use all common raster image formats for printing (PNG, JPG, GIF...)

*Example*
```bash
./ppa6-print.py -i image.jpg B5:5B:13:08:F6:22
```

## Printing SVG files
Similarly, printing SVG files is straightforward. Internally, the image is first
rasterized using [cairosvg](https://cairosvg.org/).

*Example*
```bash
./ppa6-print.py --svg myvectorimage.svg B5:5B:13:08:F6:22
```

## Printing QR Codes
For the sake of convenience, the script allows QR codes to be generated and printed directly in one go. Simply pass in in the content for the QR code using the `-qr`option.

*Example*
```bash
./ppa6-print.py -qr "http://www.weingaertner.org" B5:5B:13:08:F6:22
```

## Manipulating brightness and contrast for printing
In many cases, the print quality dramatically improves if the brightness or the contrast
of the image is adjusted. This can be done using the `-b` and `-b` parameters.

*Example*
The example reduces the contrast using a factor of 0.75 and increases the brightness using a factor of 1.5.

```bash
./ppa6-print.py -c 0.75 -b 1.5 -i image.jpg  B5:5B:13:08:F6:22
```

### Disabling feeding
The script feeds some extra paper after printing to ease cutting. This can be disabled using the `-nf` parameter.

Example
```bash
# no paper feeding
./ppa6-print.py -nf- i image.jpg B5:5B:13:08:F6:22
```

## Status and future work

This script is a proof of concept. The goal was simply to make printing work. There are a lot of unknowns yet with regard to the actual printer communication. Help and PRs are welcome!

Todo:
- Printer scanning & auto-detection
- Text print
