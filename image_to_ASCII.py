#!/usr/bin/env python3

import argparse
import json
import random
from PIL import Image

default_ascii_dict = {
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
    
def get_ascii(average, dictionary):
    """Return the ASCII symbol.
       base on the average value of the pixel parameters.

    """
    if 256//len(dictionary) > len(dictionary):
        divider = 256//len(dictionary)
    else:
        divider = len(dictionary)
    return random.choice(dictionary[str(average // divider)])

def json_dump(size, adjustment, dictionary):
    """Creates or modifies save file"""
    try:
        with open('im_to_ASCII_save.json','w') as save:
            options = (str(size), str(adjustment), dictionary)
            json.dump(options, save)
    except FileNotFoundError:
        print('Can not create a save file')
         
def json_load():
    """Reads data from save file if it does exist and not corrupted"""
    try:
        with open('im_to_ASCII_save.json') as save:
            try:
                return json.load(save)
            except json.decoder.JSONDecodeError:
                print('ERROR: save file collapsed. Try to rewrite it')
                return ('100', '1.5', default_ascii_dict)
    except FileNotFoundError:
        print('Can not find a save file')

def save_dict_checker(check_dict):
    """Check that dict has valid keys and values."""
    try:
        for i in range(0, len(check_dict)):
            if not (str(i) in check_dict.keys()):
                print('Missing an "{}" key in the dictionary'.format(i))
                return 0
        for i in check_dict.values():
            if not (isinstance(i, list) or isinstance(i, str)):
                print("Element {} is not a list".format(i))
                return 0
        return 1
    except AttributeError:
        print('Your save file should contain the dictionary (-h to see more information).')
        return 0

def main():
    parser = argparse.ArgumentParser(description = 'Process image into ASCII text.')
    parser.add_argument('Image_name', help = 'Name of the image to process')
    parser.add_argument('-w', type = int, help = 'Number of symbols in line')
    parser.add_argument('-a', type = float, help = 'Proportions adjustment multiplier')
    parser.add_argument('-s', nargs ='?', default = 0, const = 1,
                        help = 'Save the current paramerters to use them as the default')
    parser.add_argument('-d', type = str, 
                        help = 'New json vocabulary file. Format: {"Range":["List of symbols"]}. "default" to set default values')
    args = parser.parse_args()

    try:
        with Image.open(args.Image_name) as image:
            options = json_load()
            size = 100
            adjustment = 1.5
            dictionary = default_ascii_dict
            if options:
                 size = int(options[0])
                 adjustment = float(options[1])
                 dictionary = options[2]
            if args.w:
                if args.w<0:
                    print('Width can not be negative: -w ', args.w)
                    exit(-1)
                size = args.w
            if args.a:
                if args.a < 0:
                    print('Adjustment can not be negative: -a ', args.a)
                adjustment = args.a
            if args.d:
                if args.d.upper() == 'DEFAULT':
                    dictionary = default_ascii_dict
                else:
                    try:
                        json_dict = open(args.d)
                        new_dict = json.load(json_dict)
                        if save_dict_checker(new_dict):
                            dictionary = new_dict
                        else:
                            if not dictionary:
                                dictionary = default_ascii_dict
                    except FileNotFoundError:
                        print('Can not find file "{}"'.format(args.d))
                        exit(-1)
                    except json.decoder.JSONDecodeError:
                        print('Wrong format of save file')
                        exit(-1)
            if args.s:
                json_dump(size, adjustment, dictionary)

            width,height = image.size
            if adjustment == 1:
                adjustment += 0.001
            width = int(width * adjustment)
            image = image.resize((width, height), Image.ANTIALIAS)
            pixels = image.load()
            i_shift = 0
            j_shift = 0
            average = 0
            shift = width // size
            while i_shift+shift < height:
                while j_shift + shift < width:
                    for i in range(i_shift, shift + i_shift):
                        for j in range(j_shift, shift + j_shift):
                            average += get_average(pixels[j, i])
                    print(get_ascii(average // (shift**2), dictionary), end = '')
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

