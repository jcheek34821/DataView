# Importing all necessary libraries from multiprocessing.connection import Listener
from threading import Thread

import cv2
import sys
import os
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from datetime import datetime
import csv

import numpy as np
import pyautogui
import operator
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from cv2 import CV_32FC1

hard_drive = ""
path_to_videos = "Yalls 2022/Regular Season(CHOPPED)/"
path_to_export = "Yalls 2022/Export/"
global_buttons = []
display_row = []
filter_row = []
buffer_array = []
data_frame = []
e1 = []
cell = ""
user_regex = ""
condition_options = ["None", "Is empty", "Is not empty", "Text contains", "Text does not contain",
                     "Text starts with", "Text ends with", "Text is exactly", "Date is", "Date is before",
                     "Date is after", "Greater than", "Greater than or equal to", "Less than",
                     "Less than or equal to", "Is equal to", "Is not equal to", "Is between", "Is not between"]
ops = {
    "==": operator.eq,
    "=": operator.eq,
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
    "<>": operator.ne,
    "*": operator.contains
}

header_row = []
ok_button = []
end_main_process = False
main_process_in_progress = False
end_filter_process = False
filter_process_in_progress = False


def text_to_image(text):
    font = ImageFont.truetype("arial.ttf", 20)
    img = Image.new("RGBA", (960, 25), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, (255, 255, 255), font=font)
    img.save("C:/Users/Jared/Desktop/img.png")


def export_to_mp4():
    print("Exporting...")
    # frame
    currentframe = 0
    width = 1920
    height = 1080

    mp4string = "new_video.mp4"
    path_count = 1
    while os.path.exists(hard_drive + path_to_export + mp4string):
        mp4string = "new_video(" + str(path_count) + ").mp4"
        path_count += 1

    # choose codec according to format needed
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(hard_drive + path_to_export + mp4string, fourcc, 30, (width, height))

    x = 0
    while True:
        temp_mp4_string = display_row[x][frame_col - 1]
        vid = cv2.VideoCapture(hard_drive + path_to_videos + display_row[x][frame_col - 1])
        if not vid.isOpened():
            print("Please select a drive")
        else:
            frame_no = int(display_row[x][frame_col]) - 45
            vid.set(1, frame_no)
            current_frame = frame_no
            while vid.isOpened():
                ute, pic_fra = vid.read()
                if ute:
                    video.write(pic_fra)
                    # current_frame = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        x = len(display_row)
                        break
                else:
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    break
                current_frame += 1
                if current_frame > frame_no + 80:
                    if x + 1 == len(display_row) or not temp_mp4_string == display_row[x + 1][frame_col - 1]:
                        x += 1
                        break
                    else:
                        x += 1
                        frame_no = int(display_row[x][frame_col]) - 45
                        current_frame = frame_no
                        vid.set(1, frame_no)
            vid.release()
            if x == len(display_row):
                break
    video.release()
    print("Video Saved")


def play_single_video(video_string, frame_no):
    vid = cv2.VideoCapture(video_string)
    if not vid.isOpened():
        print("Please select a drive")
    else:
        frame_no = frame_no - 45
        vid.set(1, frame_no)
        current_frame = frame_no
        while vid.isOpened():
            ute, pic_fra = vid.read()
            if ute:
                r = cv2.resize(pic_fra, (960, 540))
                cv2.imshow("DataView", r)
                current_frame = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
            else:
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
            current_frame += 1
            if current_frame > frame_no + 80:
                vid.set(1, frame_no)
        vid.release()


def play_multiple_video():
    x = 0
    while True:
        temp_mp4_string = display_row[x][frame_col - 1]
        vid = cv2.VideoCapture(hard_drive + path_to_videos + display_row[x][frame_col - 1])
        if not vid.isOpened():
            print("Please select a drive")
        else:
            frame_no = int(display_row[x][frame_col]) - 45
            vid.set(1, frame_no)
            current_frame = frame_no
            while vid.isOpened():
                ute, pic_fra = vid.read()
                if ute:
                    r = cv2.resize(pic_fra, (960, 540))
                    cv2.imshow("DataView", r)
                    # current_frame = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        x = len(display_row)
                        break
                else:
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    break
                current_frame += 1
                if current_frame > frame_no + 80:
                    if x + 1 == len(display_row) or not temp_mp4_string == display_row[x + 1][frame_col - 1]:
                        vid.set(1, 10000000)
                        cv2.imshow("DataView", r)
                        x += 1
                        break
                    else:
                        x += 1
                        frame_no = int(display_row[x][frame_col]) - 45
                        current_frame = frame_no
                        vid.set(1, frame_no)
            vid.release()
            if x == len(display_row):
                break


def ops_func(num):
    global cell
    global user_regex
    if num > 10 and (cell == '' or user_regex == ''):
        return False
    elif num == 1:
        return ops["=="](cell, "")
    elif num == 2:
        return not ops["=="](cell, "")
    elif num == 3:
        return ops["*"](cell, user_regex)
    elif num == 4:
        return not ops["*"](cell, user_regex)
    elif num == 5:
        return ops["=="](cell[0:len(user_regex)], user_regex)
    elif num == 6:
        return ops["=="](cell[len(cell)-len(user_regex):len(cell)], user_regex)
    elif num == 7:
        return ops["=="](cell, user_regex)
    elif num == 8:
        return ops["=="](cell, user_regex)
    elif num == 9:
        return ops["<"](date_to_days(cell), date_to_days(user_regex))
    elif num == 10:
        return ops[">"](date_to_days(cell), date_to_days(user_regex))
    elif num == 11:
        return ops[">"](float(cell), float(user_regex))
    elif num == 12:
        return ops[">="](float(cell), float(user_regex))
    elif num == 13:
        return ops["<"](float(cell), float(user_regex))
    elif num == 14:
        return ops["<="](float(cell), float(user_regex))
    elif num == 15:
        return ops["="](float(cell), float(user_regex))
    elif num == 16:
        return ops["<>"](float(cell), float(user_regex))
    elif num == 17:
        return ops[">"](getdouble(cell), float(user_regex.split(",")[0])) and ops["<"](float(cell),
                                                                                       float(user_regex.split(",")[1]))
    else:
        return not ops[">"](float(cell), float(user_regex.split(",")[0])) and ops["<"](float(cell),
                                                                                       float(user_regex.split(",")[1]))


def date_to_days(date):
    date = date.split("/")
    num = int(date[2] * 365)
    num += int(month_to_days(int(date[1])))
    num += int(date[2])
    return num


def clear_buffer_array(regex):
    x = 0
    while x < len(buffer_array):
        if buffer_array[x][4] == regex and regex == "v":
            global_buttons[buffer_array[x][1]]["text"] = buffer_array[x][2]
            buffer_array.remove(buffer_array[x])
        else:
            x += 1


def add_condition(choice):
    global cell
    choice = clicked.get()
    num = condition_options.index(choice)
    if num > 0:
        clear_buffer_array("v")
        if choice == "None":
            enable_widget(ok_button[0])
            ok_button[0]["text"] = "Value OK"
        else:
            enable_widget(ok_button[0])
            ok_button[0]["text"] = "Condition OK"
        buffer_array.append(["", "", condition_options.index(clicked.get()), "", "c"])
    elif len(buffer_array) == 0:
        ok_button[0]["text"] = "OK"
        disable_widget(ok_button[0])


def is_in(this_cell, array):
    for x in array:
        if this_cell == x:
            return True
    return False


def load_filtered_csv():
    global display_row
    global cell
    global end_filter_process
    global end_main_process
    global main_process_in_progress
    remove_rows(data_frame[0])
    display_row = list(row).copy()
    display_row.remove(display_row[0])
    main_process_in_progress = True
    for x in filter_row:
        if end_main_process:
            break
        n = filter_row.index(x)
        if len(x) > 0:
            if x[0] == "c":
                y = 0
                while y < len(display_row):
                    cell = display_row[y][n]
                    if not ops_func(x[1]):
                        display_row.remove(display_row[y])
                    else:
                        y += 1
            else:
                z = 0
                while z < len(display_row):
                    if not is_in(display_row[z][n], x):
                        display_row.remove(display_row[z])
                    else:
                        z += 1
    count = 0
    row_num = 1
    x = 0
    while x < len(display_row):
        if end_main_process:
            break
        s = ""
        for y in display_row[x]:
            s += format_text(y)
        if not v_is_toggled or (v_is_toggled and display_row[x][frame_col].strip()):
            if count % 2 == 0:
                if not display_row[x][frame_col].strip():
                    color = "#FFB8B8"
                else:
                    color = "#FFFFFF"
                temp_label = Button(
                    data_frame[0],
                    bg=color,
                    borderwidth=0,
                    text=s,
                    width=15 * len(row[0]),
                    anchor="w",
                    height=1,
                    font='courier 10 bold',
                    command=lambda a=hard_drive, b=path_to_videos,
                                   c=display_row[x][frame_col - 1], d=display_row[x][frame_col]:
                    play_single_video(str(a + b + c), int(d)))
                temp_label.grid(column=0, row=row_num, sticky="news")
            else:
                if not display_row[x][frame_col].strip():
                    color = "#D89D9D"
                else:
                    color = "#D6D6D6"
                temp_label = Button(
                    data_frame[0],
                    bg=color,
                    borderwidth=0,
                    text=s,
                    width=15 * len(row[0]),
                    anchor="w",
                    height=1,
                    font='courier 10 bold',
                    command=lambda a=hard_drive, b=path_to_videos, c=display_row[x][frame_col - 1],
                    d=display_row[x][frame_col]: play_single_video(str(a + b + c), int(d)))
                temp_label.grid(column=0, row=row_num, sticky="news")
            count += 1
            data_frame[0].update()
            root.update()
            canvas.config(scrollregion=canvas.bbox("all"))
            row_num += 1
            x += 1
        else:
            display_row.remove(display_row[x])
    end_main_process = False
    main_process_in_progress = False
    if len(display_row) > 0:
        export.configure(state="normal")


def remove_rows(local_container):
    if local_container == data_frame[0]:
        export.configure(state="disabled")
    df = local_container.winfo_children()
    for x in df:
        if df.index(x) > 0:
            x.destroy()


def size_contained():
    count = 0
    for x in filter_row:
        if not x == []:
            count += 1
    return count


def ok_filter(win, ind):
    global buffer_array
    global global_buttons
    global filter_row
    global user_regex
    global global_index_num
    global end_filter_process
    global filter_process_in_progress
    user_regex = e1[0].get()
    root.deiconify()
    win.withdraw()
    for x in buffer_array:
        if x[4] == "v":
            if not contains_value(x, filter_row[x[0]]):
                if len(filter_row[x[0]]) > 0 and filter_row[x[0]][0] == "c":
                    filter_row[x[0]] = []
                if x[3] == "a":
                    filter_row[x[0]].append(x[2])
                else:
                    filter_row[x[0]].remove(x[2])
        else:
            filter_row[ind] = []
            global_index_num = condition_options.index(clicked.get())
            filter_row[ind].append("c")
            filter_row[ind].append(x[2])
            if not e1[0].get() == "":
                filter_row[ind].append(e1[0].get())
    butt = header_row[ind]
    header = butt["text"][0:len(butt["text"]) - 1]
    if not filter_row[ind] == []:
        butt["text"] = header + " \u25BC"
    else:
        butt["text"] = header + " \u25BD"
    buffer_array = []
    remove_button.configure(state="disabled")
    if filter_process_in_progress:
        end_filter_process = True
    remove_rows(name_frame)
    e1[0].delete(0, END)
    clear_name_frame()
    name_frame.update()
    load_filtered_csv()


def cancel_filter(win):
    global buffer_array
    global global_buttons
    global end_filter_process
    if filter_process_in_progress:
        end_filter_process = True
    for x in buffer_array:
        if x[4] == "v":
            global_buttons[x[1]]["text"] = x[2]
    buffer_array = []
    global_buttons = []
    remove_rows(name_frame)
    clicked.set("None")
    remove_button.config(state="disabled")
    clear_name_frame()
    name_frame.update()
    root.deiconify()
    e1[0].delete(0, END)
    win.withdraw()


def check_value(ind, t_col):
    clear_buffer_array("c")
    clicked.set("None")
    enable_widget(ok_button[0])
    ok_button[0]["text"] = "Value OK"
    e1[0].delete(0, END)
    if "\u2713 " in global_buttons[ind]["text"]:
        global_buttons[ind]["text"] = global_buttons[ind]["text"][2:len(global_buttons[ind]["text"])]
        if not contains_value(global_buttons[ind]["text"], buffer_array):
            buffer_array.append([t_col, ind, global_buttons[ind]["text"], "r", "v"])
    else:
        if not contains_value(global_buttons[ind]["text"], buffer_array):
            buffer_array.append([t_col, ind, global_buttons[ind]["text"], "a", "v"])
        global_buttons[ind]["text"] = "\u2713 " + global_buttons[ind]["text"]


def contains_value(value, options):
    for x in options:
        if value == x:
            return True
    return False


def get_index_from_regex(regex):
    count = 0
    for x in row[0]:
        if x == regex:
            return count
        count += 1
    return 0


def month_to_days(mon):
    if (mon < 8 and mon % 2 == 1) or (mon > 7 and mon % 2 == 0):
        return 31
    elif not mon == 2:
        return 30
    else:
        return 28


def disable_widget(event):
    event.config(state="disabled")


def enable_widget(event):
    event.config(state="active")


def clear_filter_row(win, ind):
    global filter_row
    filter_row[ind] = []
    e1[0].delete(0, END)
    ok_filter(win, ind)


def clear_name_frame():
    for x in global_buttons:
        x.destroy()


def filter_col(regex):
    global cell
    global user_regex
    global global_index_num
    global global_buttons
    global end_main_process
    global end_filter_process
    global filter_process_in_progress
    if main_process_in_progress:
        end_main_process = True
    root.withdraw()
    filter_window.deiconify()

    value_options = []
    global_index_num = get_index_from_regex(regex)
    for x in display_row:
        if not contains_value(x[global_index_num], value_options):
            value_options.append(x[global_index_num])
    # value_options.remove(regex)

    if len(filter_row[global_index_num]) > 0:
        remove_button.config(state="normal")
        if filter_row[global_index_num][0] == "c":
            e1[0].delete(0, END)
            e1[0].insert(0, filter_row[global_index_num][2])

    # Add options to frame
    row_num = 0
    global_buttons = []
    name_frame.update()
    filter_window.update()
    filter_process_in_progress = True
    for x in value_options:
        if end_filter_process:
            break
        if len(filter_row[global_index_num]) == 0 or not contains_value(x, filter_row[global_index_num]) or \
                filter_row[global_index_num][0] == "c":
            global_buttons.append(Button(
                name_frame,
                text=x,
                borderwidth=0,
                command=lambda name=value_options.index(x): check_value(name, global_index_num)))
        else:
            global_buttons.append(Button(
                name_frame,
                text="\u2713 " + x,
                borderwidth=0,
                command=lambda name=value_options.index(x): check_value(name, global_index_num)))
        global_buttons[-1].grid(row=row_num, column=0, sticky=W)
        row_num += 1
        name_frame.update()
        filter_window.update()
        value_canvas.config(scrollregion=value_canvas.bbox("all"))
    filter_process_in_progress = False
    end_filter_process = False


def format_text(text):
    num = 16
    if len(text) > num:
        return text[0:num]
    else:
        return str(text).center(num, " ")


def load_csv(csv_file):
    global row
    global col
    global display_row
    global filter_row
    global frame_col
    remove_rows(data_frame[0])
    display_row.clear()
    row.clear()
    root.update()
    data_frame[0].update()
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for a in reader:
            for b in a:
                if b == "Pitch Frame":
                    frame_col = a.index(b)
                col.append(b)
            row.append(col)
            col = []
        display_row = list(row).copy()
        filter_row = [[] for _ in range(len(row[0]))]

    header_frame = Frame(data_frame[0])
    header_frame.grid(row=0, column=0, sticky=NW)
    col_num = 0
    header_row.clear()
    for x in row[0]:
        if len(x) > 10:
            t_x = x[0:10] + " \u25BD"
        else:
            t_x = x + " \u25BD"
        header_row.append(Button(
            header_frame,
            text=t_x,
            bg="#C0C0C0",
            borderwidth=1,
            width=15,
            height=1,
            font='arial 10 bold',
            command=lambda gx=x: filter_col(gx)))
        header_row[-1].grid(column=col_num, row=0, sticky=W)
        col_num += 1
    data_frame[0].update()
    root.update()
    canvas.config(scrollregion=canvas.bbox("all"))


def select_csv_file():
    if not hard_drive == "":
        filetypes = (
            ('CSV', '*.csv'),
            ('All files', '*.*')
        )
        video_string = fd.askopenfilename(
            title='Import Video',
            initialdir='C:/Users/Jared/Downloads',
            filetypes=filetypes)
        load_csv(video_string)


def toggle_video():
    global v_is_toggled
    if v_is_toggled:
        v_is_toggled = False
        v_toggle["text"] = "Video"
    elif len(row) > 0:
        play.configure(state="normal")
        v_is_toggled = True
        v_toggle["text"] = "Video" + "\u2022"
    if len(row) > 0:
        load_filtered_csv()


def select_video_drive():
    global hard_drive
    hard_drive = fd.askdirectory(title='Select Hard drive')
    hard_drive = hard_drive[0:3]
    video_drive["text"] = hard_drive[0:3]
    video_drive.configure(state="disabled")


def disable_event():
    pass


def close_out():
    root.destroy()
    filter_window.destroy()
    sys.exit()


def select_all():
    global buffer_array
    ind = 0
    buffer_array = []
    for x in global_buttons:
        if "\u2713 " not in x["text"]:
            x["text"] = "\u2713 " + x["text"]
        buffer_array.append([global_index_num, ind, global_buttons[ind]["text"], "a", "v"])
        ind += 1


def clear_all():
    global buffer_array
    buffer_array = []
    for x in global_buttons:
        if "\u2713 " in x["text"]:
            x["text"] = x["text"].replace("\u2713 ", "")


def search_buttons(event):
    global global_buttons
    reveal_all_global_buttons()
    remove_rows(name_frame)
    x = 0


def reveal_all_global_buttons():
    global global_buttons
    for x in global_buttons:
        x.place()


v_is_toggled = False
frame_col = 0

screen_width, screen_height = pyautogui.size()
mod_screen_width = screen_width - 100
mod_screen_height = int((mod_screen_width - 100) * .5625)

# create the root window
root = tk.Tk()
root.geometry(str(mod_screen_width) + "x" + str(mod_screen_height + 35) + "+0+0")
root.title('DataView')
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.protocol("WM_DELETE_WINDOW", lambda: close_out())

# create filter window
filter_window = tk.Tk()
filter_window.geometry("300x500+" + str(int((screen_width / 2) - 150)) + "+" + str(int((screen_height / 2) - 200)))
filter_window.title('Filter')
filter_window.protocol("WM_DELETE_WINDOW", disable_event)
filter_window.withdraw()

video_window = tk.Tk("Express Video Chopper")
video_window.withdraw()

label_array = []

clicked = StringVar(filter_window, 'None')

# Create Label
condition_label = Label(filter_window, text="Filter by condition: ", font="arial 12")
o_menu = tk.OptionMenu(filter_window, clicked, *condition_options, command=add_condition)
e1.clear()
e1.append(Entry(filter_window, bd=1))

condition_label.grid(row=0, column=0, sticky=W)
o_menu.grid(row=0, column=0, sticky=E)
e1[-1].grid(row=1, column=0, sticky=W, padx=5)

# Create Dropdown menu
value_label = Label(filter_window, text="Filter by value: ", font="arial 12")
value_search_entry = Entry(filter_window, bd=1)
value_search_entry.bind("<Key>", search_buttons)
value_select_all = Button(
    filter_window, borderwidth=0, text="Select All", font="arial 8 underline", command=select_all)
value_clear_all = Button(
    filter_window, borderwidth=0, text="Clear", font="arial 8 underline", command=clear_all)
value_frame = Frame(filter_window, width=290, height=200, highlightbackground="black", highlightthickness=1)

value_frame.grid_rowconfigure(0, weight=1)
value_frame.grid_columnconfigure(0, weight=1)
value_frame.grid_propagate(False)
value_label.grid(row=2, column=0, sticky=W)
value_search_entry.grid(row=3, column=0, padx=5, pady=10, sticky=W)
value_select_all.grid(row=4, column=0, padx=5, pady=10, sticky=W)
value_clear_all.grid(row=4, column=0, padx=70, pady=10, sticky=W)
value_frame.grid(row=5, column=0, padx=5)

value_canvas = tk.Canvas(value_frame, width=290, height=200)
value_canvas.grid(row=0, column=0, sticky="news")

value_v = tk.Scrollbar(value_frame, orient='vertical', command=value_canvas.yview)
value_v.grid(row=0, column=1, sticky="ns")
value_canvas.configure(yscrollcommand=value_v.set)

name_frame = tk.Frame(value_canvas, width=290, height=200)
name_frame.grid()
value_canvas.create_window((0, 0), window=name_frame, anchor='nw')

global_index_num = 0

# Create ok and cancel buttons
remove_button = Button(filter_window, text="Remove", command=lambda: clear_filter_row(filter_window, global_index_num))
ok_button.clear()
ok_button.append(Button(filter_window, text="OK", command=lambda: ok_filter(filter_window, global_index_num)))
disable_widget(ok_button[-1])
cancel = Button(filter_window, text="Cancel", command=lambda: cancel_filter(filter_window))
remove_button.grid(row=6, column=0, pady=5, sticky="news")
remove_button.config(state="disabled")
ok_button[-1].grid(row=7, column=0, pady=5, sticky="news")
cancel.grid(row=8, column=0, pady=5, sticky="news")

row = []
col = []
filtered_row = []

window_frame = tk.Frame(root)
window_frame.grid(sticky=NW)

menu_frame = tk.Frame(window_frame)
menu_frame.grid(row=0, sticky=NW)

upload = Button(
    menu_frame,
    text="Upload CSV",
    borderwidth=0,
    command=select_csv_file)
upload.grid(row=0, column=0, sticky=W, padx=10)

video_drive = Button(
    menu_frame,
    text="Drive",
    borderwidth=0,
    command=select_video_drive)
video_drive.grid(row=0, column=1, sticky=W, padx=10)

export = Button(
    menu_frame,
    text="Export",
    borderwidth=0,
    command=export_to_mp4)
export.grid(row=0, column=2, sticky=W, padx=3)
export.configure(state="disabled")

play = Button(
    menu_frame,
    text="Play",
    borderwidth=0,
    command=play_multiple_video)
play.grid(row=0, column=3, sticky=W, padx=10)
play.configure(state="disabled")

v_toggle = Button(
    menu_frame,
    text="Video",
    borderwidth=0,
    command=toggle_video)
v_toggle.grid(row=0, column=4, sticky=W, padx=10)

container = tk.Frame(window_frame, width=mod_screen_width, height=mod_screen_height)
container.grid(row=1, column=0, pady=(5, 0), sticky='nw')
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
container.grid_propagate(False)

canvas = tk.Canvas(container, width=mod_screen_width, height=mod_screen_height)
canvas.grid(row=0, column=0, sticky="news")

v = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
v.grid(row=0, column=1, sticky="ns")
h = tk.Scrollbar(container, orient='horizontal', command=canvas.xview)
h.grid(row=1, column=0, sticky="ew")
canvas.configure(xscrollcommand=h.set)
canvas.configure(yscrollcommand=v.set)

data_frame.append(tk.Frame(canvas))
canvas.create_window((0, 0), window=data_frame[0], anchor='nw')

# run the application
root.mainloop()

# Release all space and windows once done
cv2.destroyAllWindows()
