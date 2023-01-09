# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageColor
   
class Text:
    
    def __init__(self,max_width=384, fontsize=20, fontname='DejaVuSans.ttf', fill = 0, align = 'left', spacing = 4, margin = 0, stroke_width = 0, stroke_fill = None):
        self.max_width = max_width
        self.fontsize = fontsize
        self.fontname = fontname
        self.font = ImageFont.truetype(font = self.fontname, size = self.fontsize)
        self.fill = fill
        
        self.align = align
        self.spacing = spacing
        self.margin = margin
        self.stroke_width = stroke_width
        self.stroke_fill = stroke_fill
        
        if self.fill in [None, 0, 255] and self.stroke_fill in [None, 0, 255] and self.stroke_width == 0:
            self.contain_grey = False
        else:
             self.contain_grey = True   
        
    def set_font(self, fontsize = None, fontname = None, fill = None, align = None, spacing = None, margin = None, stroke_width = None, stroke_fill = None):
        if fontsize != None:
            self.fontsize=fontsize
        if fontname != None:
            self.fontname = fontname
        if fill != None:
            self.fill = fill
        if align != None:
            self.align = align
        if spacing != None:
            self.spacing = spacing
        if margin != None:
            self.margin = margin   
        if stroke_width != None:
            self.stroke_width = stroke_width
        if stroke_fill != None:
            self.stroke_fill = stroke_fill
            
        if self.fill in [None, 0, 255] and self.stroke_fill in [None, 0, 255] and self.stroke_width == 0:
            self.contain_grey = False
        else:
             self.contain_grey = True   
        self.font = ImageFont.truetype(font = self.fontname, size = self.fontsize)
        
        
    def __text_wrap(self, text):
        # wrap text to make it fit in the maximum width
        str_out = ""
        for line in text.split('\n'):
            tmp = ""
            for word in line.split():
                if self.font.getsize(tmp + " " + word)[0]+ self.margin > self.max_width:
                    tmp = tmp[:-1]
                    str_out += tmp
                    tmp = "\n" + word + " "
                else:
                    tmp += word + " "
            tmp = tmp[:-1]
            str_out += tmp + "\n"
        str_out = str_out[:-1]

        # Create tmp image to calculate the size of the text
        draw = ImageDraw.Draw(Image.new('L', (10, 10),255))
        width, height = draw.textsize(str_out, font = self.font, spacing = self.spacing, stroke_width = self.stroke_width)

        return str_out, width, height
        
    def print(self, text):
        text, width, height = self.__text_wrap(text)
        
        # Generate grey image only if necessary
        if self.contain_grey:
            img = Image.new('L', (self.max_width, height + self.spacing), ImageColor.getcolor("White", "L"))
        else:
            img = Image.new('1', (self.max_width, height + self.spacing), ImageColor.getcolor("White", "1"))
        draw = ImageDraw.Draw(img)
        
        if self.align == "left":
            xy = (self.margin, 0)
        elif self.align == "center":
            xy = ((self.max_width - width) / 2,0)
        elif self.align == "right":
            xy = (self.max_width - width-self.margin, 0)
        
        draw.text(xy,text, font = self.font, fill = self.fill, align = self.align, spacing = self.spacing, stroke_width = self.stroke_width , stroke_fill = self.stroke_fill)
        
        # Convert the image in black and white
        if self.contain_grey:
            img = img.convert(mode = "1")
        return img