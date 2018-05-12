#!/usr/bin/env python3

from time import sleep
import curses
import argparse
import json
import random
from PIL import Image
from PIL import ImageSequence
from PIL import ImageColor
from time import time

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
    'E01': "Can not find file.",
    'E02': "Wrong format of file.",
    'E03': "Width can not be less then zero.",
    'E04': "Adjustment can not be less then zero.",
    'E05': "Can not find dictionary file.",
    'E06': "Can not decode dictionary file. Check if it is json file.",
    'E07': "Too big width of ASCII image. Should be less then the original's.",
    'E08': "Can not process animation in nocurses mode",
    'E09': "Can not export and import at the same time",
    'E10': "Wrong format of ASCII save"
}


def end_safe(exit_code):
    """Finalize a curses session"""
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    if exit_code:
        print(errors[exit_code])
    exit(exit_code)


def get_pair(color):
    """Converts RGB tuple into one of avalable colors"""
    if color[0] < 50 and color[1] < 50 and color[2] < 50:
        return 7
    elif color[0] > 194 and color[1] > 194 and color[2] > 194:
        return 8
    elif abs(color[0] - color[2]) < 30 and abs(color[1] - color[0]) < 30 and abs(color[1] - color[2]) < 30:
        if (color[0]+color[1]+color[2])//3 > 127:
            return 8
        else:
            return 7
    elif color[0] >= color[1] and color[0] >= color[2]:
        if abs(color[1] - color[2]) > 50:
            if color[1] > color[2]:
                return 6
            else:
                return 5
        else:
            return 1
    elif color[1] >= color[2] and color[1] >= color[0]:
        if abs(color[0] - color[2]) > 50:
            if color[0] > color[2]:
                return 10
            else:
                return 4
        else:
            return 2
    elif color[2] >= color[1] and color[2] >= color[0]:
        if abs(color[1] - color[0]) > 50:
            if color[0] > color[1]:
                return 5
            else:
                return 4
        else:
            return 3
    else:
        return 7


def Image_displaying(stdscr, frames, color_map, _color):
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
        stdscr.addstr(curses.LINES-1, 0, "[arrows key]-navigation [q]-exit")
    else:
        stdscr.addstr(curses.LINES-1, 0, "[q] - exit")
    stdscr.refresh()
    if len(frames[0][0]) > curses.COLS-1:
        visible_cols = curses.COLS
    else:
        visible_cols = len(frames[0][0])
    if len(frames[0]) > curses.LINES - 3:
        visible_lines = curses.LINES - 2
    else:
        visible_lines = len(frames[0])
    if _color:
        curses.init_color(10, 255, 0, 128)
        curses.init_color(11, 128, 255, 0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(9, 10, curses.COLOR_BLACK)
        curses.init_pair(10, 11, curses.COLOR_BLACK)
    while True:
        for i in range(0, visible_lines):
            for j in range(0, visible_cols):
                add = frames[frame % frame_num][i+current_line][current_col+j]
                color = color_map[frame % frame_num][i+current_line][current_col+j]
                if _color:
                    stdscr.addstr(i, j, add, curses.color_pair(get_pair(color)))
                else:
                    stdscr.addstr(i, j, add)
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
        frame += 1
        if frame_num != 1:
            sleep(t)


def get_ascii(average, dictionary):
    """Return the ASCII symbol.
       base on the average value of the pixel parameters.

    """
    return random.choice(dictionary[str(int((average/256) * len(dictionary)))])


def json_dump(size, adjustment, dictionary):
    """Creates or modifies save file"""
    try:
        save = open('im_to_ASCII_save.json', 'w')
    except FileNotFoundError:
        print('Can not create a save file')
    else:
        options = (str(size), str(adjustment), dictionary)
        json.dump(options, save)


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


def check_use(use):
    if len(use) == 2:
        if len(use[0]) != len(use[1]):
            return 0
        width = len(use[0][0])
        _width = len(use[0][0][0])
        for i in range(len(use[0])):
            try:
                if len(use[0][i]) != width or len(use[1][i]) != width:
                    return 0
            except ValueError:
                return 0
            for j in range(width):
                if not(isinstance(use[0][i][j], list) and isinstance(use[1][i][j], list)):
                    return 0
                if len(use[0][i][j]) != _width or len(use[1][i][j]) != _width:
                    return 0
                for k in range(_width):
                    if not(isinstance(use[0][i][j][k], str) and isinstance(use[1][i][j][k], list)):
                        return 0
                    if len(use[0][i][j][k]) != 1 or len(use[1][i][j][k]) != 3:
                        return 0
                    for b in range(3):
                        try:
                            if not (int(use[1][i][j][k][b]) <= 255 and int(use[1][i][j][k][b]) >= 0):
                                return 0
                        except ValueError:
                            return 0
                        except TypeError:
                            return 0
    else:
        return 0
    return 1


def use_save(save_name):
    try:
        save_file = open(save_name)
    except FileNotFoundError:
        end_safe('E01')
    try:
        use = json.load(save_file)
    except json.decoder.JSONDecodeError:
        end_safe('E02')
    if check_use(use):
        return use
    else:
        end_safe('E10')


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


def processer(pixels, stdscr, width, height, size,
              dictionary, silent, frame_num):
    line = []
    lines = []
    color_map = []
    color_line = []
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
                    average += (pixels[j, i][0]+pixels[j, i][1]+pixels[j, i][2]) // 3
            line.append(get_ascii(average // (shift**2), dictionary))
            color_line.append(pixels[j, i])
            if silent and stdscr:
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
        color_map.append(color_line)
        color_line = []
        line = []
    return (lines, color_map)


def main():
    parser = argparse.ArgumentParser(description='Process image into ASCII.')
    parser.add_argument('Image_name',
                        help='Name of the file to process or display')
    parser.add_argument('-w', type=int, help='Number of symbols in line')
    parser.add_argument('-a', type=float,
                        help='Proportions adjustment multiplier')
    parser.add_argument('-s', nargs='?', default=0, const=1,
                        help='Save the current paramerters')
    parser.add_argument('-d', type=str,
                        help='JSON Dictionary file')
    parser.add_argument('--silent', nargs='?', default=1, const=0,
                        help='Run the aplication silently')
    parser.add_argument('--nocurses', nargs='?', default=1, const=0,
                        help="""
Simply output text into stdout(GIF animation not supported)
                            """)
    parser.add_argument('--color', nargs='?', default=0, const=1,
                        help='Color mode(Available in curses)')
    parser.add_argument('--export', nargs='?', default=0, const=1,
                        help="""
Creates a save file with processed image or animation.
                             """)
    parser.add_argument('--use', nargs='?', default=0, const=1,
                        help="""
Use first parameter as a path
to existing save file to reproduce it
                            """)
    args = parser.parse_args()

    if args.export and args.use:
        end_safe('E09')
    if args.nocurses:
        stdscr = curses.initscr()
        curses.start_color()
        stdscr.keypad(True)
        curses.noecho()
        curses.curs_set(0)
    else:
        stdscr = 0
    if not args.use:
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
    if args.silent and args.nocurses and (not args.use):
        stdscr.addstr(1, 0, 'Converting image to ASCII...', curses.A_BOLD)
        stdscr.addstr(2, 0, "0 %")
        stdscr.addstr(2, 4, "[          ]", curses.A_BOLD)
        stdscr.refresh()
    if not args.nocurses:
        args.color = 0
    elif not curses.has_colors():
        args.color = 0
    if args.s:
        json_dump(size, adjustment, dictionary)
    i = 0
    if adjustment == 1:
        adjustment += 0.001
    frames = []
    color_map = []
    frame_num = 0
    if not(args.use):
        for frame in ImageSequence.Iterator(image):
            frame_num += 1
        image.close()
        if frame_num != 1 and not args.nocurses:
            print(errors['E08'])
            exit('E08')
        image = Image.open(args.Image_name)
        if args.silent and args.nocurses:
            stdscr.addstr(3, 0, "0" + " "*(len(str(frame_num))-1) + "/{}".format(frame_num))
        for frame in ImageSequence.Iterator(image):
            width, height = frame.size
            width = int(width * adjustment)
            frame = frame.convert("RGB", palette=Image.ADAPTIVE, colors=256)
            frame = frame.resize((width, height), Image.ANTIALIAS)
            frame_ASCII, frame_color = processer(frame.load(), stdscr, width, height, size, dictionary, args.silent, frame_num)
            frames.append(frame_ASCII)
            color_map.append(frame_color)
            if args.silent and args.nocurses:
                i += 1
                stdscr.addstr(2, 0, "0 %")
                stdscr.addstr(2, 4, "[          ]", curses.A_BOLD)
                stdscr.addstr(3, 0, str(i))
                stdscr.refresh()
        image.close()
    else:
        frames, color_map = use_save(args.Image_name)
    if args.export:
        try:
            processed = open('Processed_image_'+str(time())+'.json', 'w')
        except FileNotFoundError:
            print('Can not save processed image')
        json.dump((frames, color_map), processed)
        processed.close()
    if args.nocurses:
        Image_displaying(stdscr, frames, color_map, args.color)
        stdscr.clear()
        stdscr.refresh()
    else:
        for i in range(0, len(frames[0])):
            for j in range(0, len(frames[0][0])):
                print(frames[0][i][j], end='')
            print('')
    if args.nocurses:
        end_safe(0)

if __name__ == "__main__":
    main()
