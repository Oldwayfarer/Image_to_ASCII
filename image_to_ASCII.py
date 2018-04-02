#!/usr/bin/env python3

import argparse
import json
import random
from PIL import Image
    
ASCII_dict = {
        '0':[' '],
        '1':['.'],
        '2':[',', '-'],
        '3':[':', ';'],
        '4':['*', '+', '='],
        '5':['x', 'o', 'n'],
        '6':['l', 'k', 'j'],
        '7':['f', 't', 'h'],
        '8':['b', 'd'],
        '9':['#', '&'],
        '10':['C', 'Z'],
        '11':['O', 'G'],
        '12':['K'],
        '13':['X'],
        '14':['B'],
        '15':['M']
}

def get_average(pixel):
    """Return the average value of three pixel parameters."""
    return (pixel[0]+pixel[1]+pixel[2]) // 3
    
def get_ascii(average):
    """Return the ASCII symbol.
       base on the average value of the pixel parameters.

    """
    return random.choice(ASCII_dict[str(average // 16)])

def json_dump(size, adjustment):
    """Creates or modifies save file"""
        try:
            with open('im_to_ASCII_save.json','w') as save:
                options = (str(size), str(adjustment))
                json.dump(options, save)
        except FileNotFoundError:
            print('Can not create a save file')
         
def json_load():
    """Reads data from save file if it does exist and not corrupted"""
    try:
        with open('im_to_ASCII_save.json') as save:
            try:
                return json.load(save)
            except JSONDecodeError:
                print('ERROR: save file collapsed. Try to rewrite it')
                return ('100', '1.5')
    except FileNotFoundError:
        print('Can not find a save file')

def main():
    parser = argparse.ArgumentParser(description = 'Process image into ASCII text.')
    parser.add_argument('Image_name', help = 'Name of the image to process')
    parser.add_argument('-w', type = int, help = 'Number of symbols in line')
    parser.add_argument('-a', type = float, help = 'Proportions adjustment multiplier')
    parser.add_argument('-s', default = 0, type = int, choices = range(0, 2) ,
                        help = 'Save the current paramerters to use them as the default(0 - don\'t save, 1 - save)')
    args = parser.parse_args()
    try:
        with Image.open(args.Image_name) as image:
            options = json_load()
            size = 100
            adjustment = 1.5
            if options:
                 size = int(options[0])
                 adjustment = float(options[1])
            if args.w:
                size = args.w
            if args.a:
                adjustment = args.a
            if args.s:
                json_dump(size, adjustment)
            width,height = image.size
            width = int(width * adjustment)
            image = image.resize((width, height), Image.ANTIALIAS)
            pixels = image.load()
            i_shift = 0
            j_shift = 0
            average = 0
            shift = width // size
            while i_shift+shift < height:
                while j_shift+shift<width:
                    for i in range(i_shift, shift+i_shift):
                        for j in range(j_shift, shift+j_shift):
                            average += get_average(pixels[j, i])
                    print(get_ascii(average//(shift**2)), end='')
                    average = 0
                    j_shift += shift
                j_shift = 0
                i_shift += shift
                print('')
    except FileNotFoundError:
        print('file "{}" Doesn\'t exist'.format(args.Image_name))
    except OSError:
        print('can not identify image: "{}"'.format(args.Image_name))

if __name__ == "__main__":
    main()

