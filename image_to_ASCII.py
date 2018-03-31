#!/usr/bin/env python3

import json
import random
import sys
from PIL import Image
    
ASCII_dict={
'1':[' '],
'2':['.'],
'3':[',','-'],
'4':[':',';'],
'5':['*','+','='],
'6':['x','o','n'],
'7':['l','k','j'],
'8':['f','t','h'],
'9':['b','d'],
'10':['#','&'],
'11':['C','Z'],
'12':['O','G'],
'13':['K'],
'14':['X'],
'15':['B'],
'16':['M']
}

def get_awer(pixel):
    return((pixel[0]+pixel[1]+pixel[2]) // 3)
    
def get_ASCII(awerage):
    if(awerage>=0 and awerage<=15):
        return(random.choice(ASCII_dict['1']))
    elif(awerage>=16 and awerage<=31):
        return(random.choice(ASCII_dict['2']))
    elif(awerage>=32 and awerage<=47):
        return(random.choice(ASCII_dict['3']))
    elif(awerage>=48 and awerage<=63):
        return(random.choice(ASCII_dict['4']))
    elif(awerage>=64 and awerage<=79):
        return(random.choice(ASCII_dict['5']))
    elif(awerage>=80 and awerage<=95):
        return(random.choice(ASCII_dict['6']))
    elif(awerage>=96 and awerage<=111):
        return(random.choice(ASCII_dict['7']))
    elif(awerage>=112 and awerage<=127):
        return(random.choice(ASCII_dict['8']))
    elif(awerage>=128 and awerage<=143):
        return(random.choice(ASCII_dict['9']))
    elif(awerage>=144 and awerage<=159):
        return(random.choice(ASCII_dict['10']))
    elif(awerage>=160 and awerage<=175):
        return(random.choice(ASCII_dict['11']))
    elif(awerage>=176 and awerage<=191):
        return(random.choice(ASCII_dict['12']))
    elif(awerage>=192 and awerage<=207):
        return(random.choice(ASCII_dict['13']))
    elif(awerage>=208 and awerage<=223):
        return(random.choice(ASCII_dict['14']))
    elif(awerage>=224 and awerage<=239):
        return(random.choice(ASCII_dict['15']))
    elif(awerage>=240 and awerage<=255):
        return(random.choice(ASCII_dict['16']))
    else:
         return(awerage)

def JSON_save():
    C=' '
    while((C.upper()!='N')and(C.upper()!='Y')):
        C=input("Configurate image? Y/N:")
    if(C.upper()=='N'):
        try:
            save=open('im_to_ASCII_save.json')
        except FileNotFoundError:
            options = ('1.5','100')
            return(options)
        else:
            try:
                options=json.load(save)
            except JSONDecodeError:
                print("Bad save file. Try to rewrite it")
                exit(-1)
            return(options)
    elif(C.upper()=='Y'):
        try:
            proportion_adj=float(input("Enter the proportions multiplier: "))
            ASCII_width=int(input("Enter Image size: "))
        except ValueError:
            print('Shuld be represented with a number')
            exit(-1) 
        else:
            with open('im_to_ASCII_save.json','w') as save:
                options=(str(proportion_adj),str(ASCII_width))
                json.dump(options,save)
                return(options)

def main():
    if((len(sys.argv)!=2)):
        print("Invalid arguments\nFORMAT: '<program_name> <Filename.png>'")
        exit(-1)
    try:
        with Image.open(sys.argv[1],'r') as image:
            width,height = image.size
            options=JSON_save()
            width=int(width*float(options[0]))
            image=image.resize((width,height),Image.ANTIALIAS)
            pixels=image.load()
            i_shift=0
            j_shift=0
            awerage=0
            shift=width // int(options[1])
            while i_shift+shift<height:
                while j_shift+shift<width:
                    for i in range(i_shift,shift+i_shift):
                        for j in range(j_shift,shift+j_shift):
                            awerage+=get_awer(pixels[j,i])
                    print(get_ASCII(awerage//(shift**2)),end='')
                    awerage=0
                    j_shift+=shift
                j_shift=0
                i_shift+=shift
                print('')
    except FileNotFoundError:
        print("file "+sys.argv[1]+" Doesn't exist")
    except OSError:
        print('can not identify image: "'+sys.argv[1]+'"')
if __name__=="__main__":
    main()

