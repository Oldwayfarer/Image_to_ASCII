# Image to ASCII processer

#### Introduction

This programm will process your image or gif animation into the set of ASCII symbols

#### Dependencies

For this application you need a python virsion 3.5 or greater and get PIL and curses libraries installed. It runs via terminal

#### Supported files

Supported image formats: BMP, EPS, GIF, JPEG, PDF, PNG, PNM, TIFF

#### Keys

* **Size** Use `-w size` key to control size\n
* **Adjustment** If proportions in the processed image feels broken use `-a multiplier` key to fix it\n
* **Save** In case you want to keep your current options use `-s` key. It will create a save file\n
* **User dictionary** You can use your own dictionaries by `-d path_to_dictionary` key. Format of dictionary {number: [list of  symbols]}
* **Silent mode** If you don't want to see any extra information while processing use `--silent` key
* **No curses mode** Old school mode without curses and animation. Enables via `--nocurses` key
* **Color mode** Color image or animation displaying(works only in curses). Enables via `--color` key
* **export** You can export processed image into .json save file. Use `--export` key
* **Use existing processed image** Reproduce an existing save file wich path given as the first parameter. Use `--use` key.
