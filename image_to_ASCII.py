#!/usr/bin/env python3

from time import sleep
import curses
import argparse
import json
import random
from PIL import Image
from PIL import ImageSequence

default_ascii_dict = {
    '0': [' '],
    '1': ['.'],
    '2': [',', '-'],
    '3': ['*', '+', '='],
    '4': [':', ';'],
    '5': ['x', 'o', 'n'],
    '6': ['l', 'k', 'j'],
    '7': ['f', 't', 'h'],
    '8': ['b', 'd'],
    '9': ['#', '&'],
    '10': ['C', 'Z'],
    '11': ['O', 'G'],
    '12': ['K'],
    '13': ['X'],
    '14': ['B'],
    '15': ['M']
}


errors = {
    'E01': "Can not find image file.",
    'E02': "Wrong format of file.",
    'E03': "Width can not be less then zero.",
    'E04': "Adjustment can not be less then zero.",
    'E05': "Can not find dictionary file.",
    'E06': "Can not decode dictionary file. Check if it is json file.",
    'E07': "Too big width of ASCII image. Should be less then the original's."
}


def end_safe(exit_code):
    """Finalize a curses session"""
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    if exit_code:
        print(errors[exit_code])
    exit(exit_code)


def Image_displaying(stdscr, frames):
    """Controls curses session"""
    frame_num = len(frames)
    if frame_num != 1:
        stdscr.nodelay(True)
    current_line = 0
    current_col = 0
    frame = 0
    t = 0.05
    for i in range(0, curses.COLS):
        stdscr.addstr(curses.LINES-2, i, ' ', curses.A_REVERSE)
    if frame_num == 1:
        stdscr.addstr(curses.LINES-1, 0, "[arrows key] - navigation [q] - exit")
    else:
        stdscr.addstr(curses.LINES-1, 0, "[q] - exit")
    #if len(frames) != 1:
    #    stdscr.addstr(curses.LINES - 1, 37, "[s] [f] - make animation slower/faster")
    stdscr.refresh()
    if len(frames[0][0]) > curses.COLS-1:
        visible_cols = curses.COLS
    else:
        visible_cols = len(frames[0][0])
    if len(frames[0]) > curses.LINES - 3:
        visible_lines = curses.LINES - 2
    else:
        visible_lines = len(frames[0])
    while True:
        for i in range(0, visible_lines):
            add = frames[frame % frame_num][i+current_line][current_col:visible_cols+current_col]
            stdscr.addstr(i, 0, add)
        stdscr.refresh
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == 259 and frame_num == 1:
            if current_line > 0:
                current_line -= 1
        elif key == 258 and frame_num == 1:
            if current_line < len(frames[0])-curses.LINES:
                current_line += 1
        elif key == 260 and frame_num == 1:
            if current_col > 0:
                current_col -= 1
        elif key == 261 and frame_num == 1:
            if current_col < len(frames[0][0])-curses.COLS:
                current_col += 1
        #elif key == ord('s'):
        #    t += 0.01
        #elif key == ord('w'):
        #    t -= 0.01
        #else:
        #    f = 0
        frame += 1
        if frame_num != 1:
            sleep(t)
        #while (not f) and len(frames) != 1:
        #    if stdscr.getch() == -1:
        #        break


def get_average(pixel):
    """Return the average value of three pixel parameters."""
    if isinstance(pixel, tuple):
        r = (pixel[0]+pixel[1]+pixel[2]) // 3
    else:
        r = pixel
    return r


def get_ascii(average, dictionary):
    """Return the ASCII symbol.
       base on the average value of the pixel parameters.

    """
    return random.choice(dictionary[str(int((average/256) * len(dictionary)))])


def json_dump(size, adjustment, dictionary):
    """Creates or modifies save file"""
    try:
        with open('im_to_ASCII_save.json', 'w') as save:
            options = (str(size), str(adjustment), dictionary)
            json.dump(options, save)
    except FileNotFoundError:
        print('Can not create a save file')


def json_load():
    """Reads data from save file if it does exist and not corrupted
        also check saves if they are correct
    """
    try:
        save = open('im_to_ASCII_save.json')
    except FileNotFoundError:
        return 0
    try:
        options = json.load(save)
    except json.decoder.JSONDecodeError:
        return 0
    save.close()
    if len(options) != 3:
        return 0
    try:
        int(options[0])
        float(options[1])
    except ValueError:
        return 0
    if not dict_checker(options[2]):
        return 0
    return options


def dict_checker(check_dict):
    """Check that dict has valid keys and values."""
    try:
        if len(check_dict) > 255 or len(check_dict) == 0:
            return 0
        for i in range(0, len(check_dict)):
            if not (str(i) in check_dict.keys()):
                return 0
        for i in check_dict.values():
            if not (isinstance(i, list) or isinstance(i, str)):
                return 0
        return 1
    except AttributeError:
        return 0


def processer(pixels, stdscr, width, height, size, dictionary, silent, frame_num):
    line = ''
    lines = []
    i_shift = 0
    j_shift = 0
    average = 0
    shift = width // size
    if frame_num != 1:
        if height//shift > curses.LINES-2 and shift != 0:
            shift = height//(curses.LINES-2)
        if width//shift > curses.COLS and shift != 0:
            shift = width//(curses.COLS)
    if shift == 0:
        end_safe('E07')
    area = (height//shift) * (width//shift)
    current_area = 0
    current_percent = 0
    spaces = 0
    flag = 0
    while i_shift + shift < height:
        while j_shift + shift < width:
            for i in range(i_shift, shift + i_shift):
                for j in range(j_shift, shift + j_shift):
                    average += get_average(pixels[j, i])
            line += get_ascii(average // (shift**2), dictionary)
            if silent:
                current_area += 1
                percent = (current_area*100)//area
                if current_percent != percent:
                    current_percent = percent
                    stdscr.addstr(2, 0, str(percent))
                    if percent % 10 == 0 and percent//10 != flag:
                        flag = percent//10
                        spaces += 1
                        stdscr.addstr(2, spaces+4, ' ', curses.A_REVERSE)
                    stdscr.refresh()
            average = 0
            j_shift += shift
        j_shift = 0
        i_shift += shift
        lines.append(line)
        line = ''
    return lines


def main():
    parser = argparse.ArgumentParser(description='Process image into ASCII.')
    parser.add_argument('Image_name', help='Name of the image to process')
    parser.add_argument('-w', type=int, help='Number of symbols in line(Don\'t work with animation for now)')
    parser.add_argument('-a', type=float,
                        help='Proportions adjustment multiplier')
    parser.add_argument('-s', nargs='?', default=0, const=1,
                        help='Save the current paramerters')
    parser.add_argument('-d', type=str,
                        help='JSON Dictionary file')
    parser.add_argument('--silent', nargs='?', default=1, const=0,
                        help='Run the aplication silently')
    args = parser.parse_args()

    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.noecho()
    curses.curs_set(0)

    try:
        image = Image.open(args.Image_name)
    except FileNotFoundError:
        end_safe('E01')
    except OSError:
        end_safe('E02')
    options = json_load()
    size = 100
    adjustment = 1.5
    dictionary = default_ascii_dict
    if options:
        size = int(options[0])
        adjustment = float(options[1])
        dictionary = options[2]
    if args.w:
        if args.w < 0:
            end_safe('E03')
        size = args.w
    if args.a:
        if args.a < 0:
            end_safe('E04')
        adjustment = args.a
    if args.d:
        if args.d.upper() == 'DEFAULT':
            dictionary = default_ascii_dict
        else:
            try:
                json_dict = open(args.d)
                new_dict = json.load(json_dict)
                json_dict.close()
                if dict_checker(new_dict):
                    dictionary = new_dict
                else:
                    if not dictionary:
                        dictionary = default_ascii_dict
            except FileNotFoundError:
                end_safe('E05')
            except json.decoder.JSONDecodeError:
                end_safe('E06')
    if args.silent:
        stdscr.addstr(1, 0, 'Converting image to ASCII...', curses.A_BOLD)
        stdscr.addstr(2, 0, "0 %")
        stdscr.addstr(2, 4, "[          ]", curses.A_BOLD)
        stdscr.refresh()
    if args.s:
        json_dump(size, adjustment, dictionary)
    i = 0
    if adjustment == 1:
        adjustment += 0.001
    frames = []
    frame_num = 0
    for frame in ImageSequence.Iterator(image):
        frame_num += 1
    image.close()
    image = Image.open(args.Image_name)
    if args.silent:
        stdscr.addstr(3, 0, "0" + " "*(len(str(frame_num))-1) + "/{}".format(frame_num))
    for frame in ImageSequence.Iterator(image):
        width, height = frame.size
        width = int(width * adjustment)
        frame.convert('RGB')
        frame = image.resize((width, height), Image.ANTIALIAS)
        frames.append(processer(frame.load(), stdscr, width, height, size, dictionary, args.silent, frame_num))
        if args.silent:
            i += 1
            stdscr.addstr(2, 0, "0 %")
            stdscr.addstr(2, 4, "[          ]", curses.A_BOLD)
            stdscr.addstr(3, 0, str(i))
            stdscr.refresh()
    image.close()
    stdscr.clear()
    stdscr.refresh()
    Image_displaying(stdscr, frames)
    end_safe(0)

if __name__ == "__main__":
    main()
