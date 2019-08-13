# Image to ASCII processer

#### Introduction

This programm will turn your image or gif animation into the set of pretty ASCII characters

#### Requirements

To run this application you will need a python virsion 3.5 or greater and install PIL and curses modules

#### Supported image formats

BMP, EPS, GIF, JPEG, PDF, PNG, PNM, TIFF

#### Keys

* **Width** Use `-w size` key to control image width
* **Adjustment** If proportions in the processed image feels broken use `-a multiplier` key to adjust them
* **Save parameters state** If you want to keep your current options use `-s` key. It will create a save file
* **User dictionary** You can set your own set of symbols by `-d /path/to/dictionary` key. Format of dictionary: `{number: [list of symbols]...}`
* **Silent mode** If you don't want to see any extra information use `--silent` key
* **No curses mode** mode without curses (animation not supported). Use `--nocurses` key
* **Colorized mode** Colored result of processing (does'nt implemented in nocurses mode). Enables via `--color` key
* **export image to save file**  Export processed image into .json file. Use `--export` key
* **Use existing processed image** Reproduce an existing save file wich path to it as the first parameter. `--use` key.
