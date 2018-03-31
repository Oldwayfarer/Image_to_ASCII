#!/usr/bin/env python3

import argparse
import json
import random
import sys
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

def json_save():
    c = ' '
    while (c.upper()!='N') and (c.upper()!='Y') :
        c = input("Configure image? Y/N:")
    if c.upper() == 'N':
        try:
            save = open('im_to_ASCII_save.json')
        except FileNotFoundError:
            options = ('1.5', '100')
            return options
        else:
            try:
                options = json.load(save)
            except JSONDecodeError:
                print("Bad save file. Try to rewrite it")
                exit(-1)
            return options
    elif c.upper() == 'Y':
        try:
            proportion_adj = float(input("Enter the proportions multiplier: "))
            ascii_width = int(input("Enter Image size: "))
        except ValueError:
            print("Should be represented with a number")
            exit(-1) 
        else:
            with open('im_to_ASCII_save.json', 'w') as save:
                options = (str(proportion_adj), str(ascii_width))
                json.dump(options, save)
                return options

def main():
    if len(sys.argv) != 2 :
        print("Invalid arguments\nFORMAT: '<program_name> <Filename.png>'")
        exit(-1)
    try:
        with Image.open(sys.argv[1], 'r') as image:
            width,height = image.size
            options = json_save()
            width = int(width*float(options[0]))
            image = image.resize((width, height), Image.ANTIALIAS)
            pixels = image.load()
            i_shift = 0
            j_shift = 0
            average = 0
            shift = width // int(options[1])
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
        print("file " + sys.argv[1] + " Doesn't exist")
    except OSError:
        print('can not identify image: "' + sys.argv[1] + '"')

if __name__ == "__main__":
    main()

