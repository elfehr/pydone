# PyDone

![PyDone icon: a snake and a pen, crossing and forming an ampersand.](./PyDone.svg =250x)
A python 3 script to display and edit text-based to-do lists with a simple user interface.


## Installation

Needs python 3 and tkinter.
Start python in a terminal to check the version:
```console
$ python
Python 3.7.1
>>> import tkinter
```
If there is no error, everything should be good. Otherwise you need to install tkinter.
On Ubuntu:
```console
$ apt-get python3-tk
```
On Archlinux/Manjaro:
```console
$ sudo pacman -S tk
```
Then download the project with:
```console
$ git clone git@gitlab.com:eyuku/pydone.git
```
or by [downloading the archive](https://gitlab.com/eyuku/pydone/-/archive/master/pydone-master.zip).

## Usage
### Start the script
In the folder where you downloaded the files, run
```console
$ python PyDone.py example &
```
to open the example list, or
```console
$ python PyDone.py <file> &
```
to open an arbitrary file. If the file doesn't exist it will be created, and if no filename is given, an empty list opens and will be saved under the name 'pydone_default'. The file is a simple text file with the exact content displayed in the interface (minus the formatting).
![Screenshot.](https://gitlab.com/eyuku/pydone/raw/master/screenshot.png)
### Use the list
#### Basic tasks
* Lines containing `[]`,`[ ]` or `[x]` are list items. The box doesn't need to be at the beginning of the line, but only what follows it will change color. Pressing `Ctrl`+`Space` will mark the task on the current line as done/undone. Done tasks are greyed out.
* Other lines (except the ones starting with `--`) are considered as category titles.
* Identation with tabs (again not necesserily at the beginning of the line) is used to describe subtasks. The parent task is greyed out as long as all its direct subtasks are not marked as done, so that the current tasks stand out.
* A new task with can be inserted under the current line with `Alt'+'a`.  Its box will be at the same level as the current line. Similarly, a child task can be inserted with `Alt'+'c`.
#### Deadlines, tags and urgency
* `//` can be used to add a deadline. Everything following `//` will be highlighted until the end of the line or until the next `--`.
* `--` can be used to add a tag. Everything following `--` will be highlighted until the end of the line or until the next `//`.
* Tags are highlighted with a default color, except for custom tags. Any line starting with `--` is considered as a custom tag definition. The syntax is `--tag = color`. The tag can be any number of words. Available colors names for tkinter can be found for example [there](http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter). It the color is not recognized, the definition is ignored. Several tag definitions can be on the same line, with no separation. Spaces around `--` and `=` don't matter. An empty color name removes completely the highlighting.
* For each `!` anywhere on the line, the task or title gains one level of urgency and its color changes to be more and more visible. Three levels are defined.
* Tasks marked as done are completely greyed out, including deadines and tags. Taks hidden because their subtasks are not done still display deadline and tag highlighting.
#### Saving!
Pressing `Ctrl`+`s` will overwrite the open file or write in ‘pydone_default' if no filename was given. It also refreshes the display so that colors are updated. An unsavec file is indicated by a star in the window title.

### Summary of keyboard shortcuts
* `Ctrl`+`s`: saves and apply formatting rules.
* `Ctrl`+`Space`: toggles done/to do on the current line.
* `Alt`+`a`: insert new task under the current line, at the same level.
* `Alt`+`c`: insert new task under the current line, with one more level of identation.
* `Alt`+`t`: Add one level of identation to the current line.
* `Alt`+`T`: Remove one level of identation to the current line.


## [Unlicense](https://gitlab.com/eyuku/pydone/blob/e09a48f2cf2ddcb971668dcae406531dc210341b/LICENSE)

Do whatever with this code, just be aware that's my first experience of python!
