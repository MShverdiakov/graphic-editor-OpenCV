from tkinter import *
from tkinter import colorchooser, filedialog, messagebox
import PIL.ImageGrab as ImageGrab
# from PIL import Image
import os
import tkinter as tk

CANVAS_WIDTH = 700
CANVAS_HEIGHT = 500
brush_size = 3
color = "black"
X = 0
Y = 0
TOOL = ""
WHITE_COLOR = False
CURRENT_ELEMENT = None
DELETE = None
IS_FIRST = None
BACKGROUND_COLOR = "white"
COLOR_PENCIL = False
ERASER_COLOR_BACKGROUND = True


def pencil():
    global TOOL, WHITE_COLOR
    TOOL = "pencil"
    WHITE_COLOR = False
    canvas.bind("<Button-1>", paint_pencil)


def paint_pencil(event):
    global X, Y
    X = event.x
    Y = event.y
    canvas.bind("<B1-Motion>", paint)


def brush():
    global TOOL, WHITE_COLOR
    TOOL = "brush"
    WHITE_COLOR = False
    canvas.bind("<B1-Motion>", paint)


def rectangle():
    global TOOL, WHITE_COLOR
    TOOL = "rectangle"
    WHITE_COLOR = False
    canvas.bind('<Button-1>', paint_rectangle)


def paint_rectangle(event):
    global color, X, Y, DELETE, IS_FIRST
    X = event.x
    Y = event.y
    IS_FIRST = True
    DELETE = True
    canvas.bind('<B1-Motion>', paint)
    canvas.bind('<ButtonRelease-1>', stop_deleting)


def circle():
    global TOOL, WHITE_COLOR
    TOOL = "circle"
    WHITE_COLOR = False
    canvas.bind('<Button-1>', paint_circle)


def paint_circle(event):
    global X, Y, IS_FIRST, DELETE
    X = event.x
    Y = event.y
    IS_FIRST = True
    DELETE = True
    canvas.bind('<B1-Motion>', paint)
    canvas.bind('<ButtonRelease-1>', stop_deleting)


def color_change(new_color):
    if (new_color == ""):
        (rgb, hx) = colorchooser.askcolor()
        new_color = hx
    global color
    color = new_color


def anisotropic_system():
    global TOOL
    TOOL = 'antisotropic_axes'
    # canvas.scale("x", 0, 0, 1, -1)  # Инвертирование оси Y
    # canvas.scale("xy", 0, 0, 1, 0.5)  # Масштабирование оси Y
    paint_anisotropic_system()


def paint_anisotropic_system():
    # Create a window
    window = tk.Tk()

    # Function to handle button click event
    def handle_button_click():
        # Get the values entered by the user
        x_left = float(x_left_entry.get())
        x_right = float(x_right_entry.get())
        y_bottom = float(y_bottom_entry.get())
        y_top = float(y_top_entry.get())

        # Call the draw_axes function with the provided parameters
        draw_axes(x_left, x_right, y_bottom, y_top)

        # Close the window
        window.destroy()

    # Create labels and entry fields for the parameters
    x_left_label = tk.Label(window, text="x_left:")
    x_left_label.pack()
    x_left_entry = tk.Entry(window)
    x_left_entry.pack()

    x_right_label = tk.Label(window, text="x_right:")
    x_right_label.pack()
    x_right_entry = tk.Entry(window)
    x_right_entry.pack()

    y_bottom_label = tk.Label(window, text="y_bottom:")
    y_bottom_label.pack()
    y_bottom_entry = tk.Entry(window)
    y_bottom_entry.pack()

    y_top_label = tk.Label(window, text="y_top:")
    y_top_label.pack()
    y_top_entry = tk.Entry(window)
    y_top_entry.pack()

    # Create a button to submit the values
    submit_button = tk.Button(window, text="Submit", command=handle_button_click)
    submit_button.pack()


def draw_axes(x_left, x_right, y_bottom, y_top):
    dx = CANVAS_WIDTH / (x_right - x_left)
    dy = CANVAS_HEIGHT / (y_top - y_bottom)

    cx = -x_left * dx
    cy = y_top * dy

    if (x_left == 0 or y_bottom == 0):
        cy -= 20
        cx += 5
    # elif (x_left < 0 and x_right < 0):
    #     cy = CANVAS_HEIGHT / 2
    #     cx = CANVAS_WIDTH / 2
    if (y_bottom >= 0):
        cy = CANVAS_HEIGHT - 25
    elif (y_top <= 0):
        cy = 5
    if (x_left >= 0):
        cx = 5
    elif (x_right <= 0):
        cx = CANVAS_WIDTH - 25
    canvas.create_line(0, cy, CANVAS_WIDTH, cy, fill='black')
    canvas.create_line(cx, 0, cx, CANVAS_HEIGHT, fill='black')

    interval_num = 12
    x_step = (x_right - x_left) / interval_num
    x = x_left
    while x <= x_right:
        x_canvas = (x - x_left) * dx
        canvas.create_line(x_canvas, cy - 3, x_canvas, cy + 3, fill="black")
        canvas.create_text(x_canvas, cy + 15, text=str(round(x, 1)), font="Verdana 7", fill="black")
        x += x_step
    y_step = (y_top - y_bottom) / interval_num
    y = y_top
    while y >= y_bottom:
        y_canvas = (y - y_top) * dy
        canvas.create_line(cx - 3, -y_canvas, cx + 3, -y_canvas, fill="black")
        canvas.create_text(cx + 20, -y_canvas, text=str(round(y, 1)), font="Verdana 7", fill="black")
        y -= y_step


def save_paint():
    # filename = filedialog.asksaveasfilename(defaultextension='.bmp')
    # canvas.postscript(file="image.eps", colormode="color")
    # img = Image.open("image.eps")
    # img.save(filename)
    # img.close()
    # messagebox.showinfo('Paint says ', 'image is saved as ' + str(filename))
    # os.startfile(filename)
    # os.remove("image.esp")

    filename = filedialog.asksaveasfilename(defaultextension='.bmp')
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    im = ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
    if filename is None:  # on cancel, don't save
        return
    # ImageGrab.grab().crop((x + 17, y + 40, x1 + 500, y1 + 500)).save(filename)
    # ImageGrab.grab().crop((x + 17, y + 40, x + 17 + 897, y + 40 + 633)).save(filename)
    # print(x, y, x1, y1)
    messagebox.showinfo('Paint says ', 'image is saved as ' + str(filename))
    os.startfile(filename)


def erase():
    global TOOL, WHITE_COLOR
    TOOL = "brush"
    WHITE_COLOR = True
    canvas.bind("<B1-Motion>", paint)


def clear_all():
    canvas.configure(background="white")
    canvas.delete("all")


def paint(event):
    global brush_size, color, CURRENT_ELEMENT, TOOL, X, Y, DELETE, IS_FIRST
    if (TOOL == "pencil"):
        x1 = X
        y1 = Y
        X = event.x
        Y = event.y

        brush_size_change(choose_size.get())
        if (color != WHITE_COLOR):
            canvas.create_line(x1, y1, X, Y, fill=color, width=brush_size)
        else:
            canvas.create_line(x1, y1, X, Y, width=brush_size)


    elif (TOOL == "brush"):
        brush_size_change(choose_size.get())
        x1 = event.x - brush_size
        x2 = event.x + brush_size
        y1 = event.y - brush_size
        y2 = event.y + brush_size

        colorr = color
        if (WHITE_COLOR):
            if (ERASER_COLOR_BACKGROUND):
                colorr = BACKGROUND_COLOR
            else:
                colorr = "white"
        CURRENT_ELEMENT = canvas.create_oval(x1, y1, x2, y2,
                                             fill=colorr, outline=colorr)
    elif (TOOL == "rectangle"):
        x1 = X
        y1 = Y
        x2 = event.x
        y2 = event.y

        brush_size_change(choose_size.get())
        if (color != WHITE_COLOR):
            CURRENT_ELEMENT = canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=brush_size)
        else:
            CURRENT_ELEMENT = canvas.create_rectangle(x1, y1, x2, y2, width=brush_size)
        if (IS_FIRST):
            IS_FIRST = False
        elif (DELETE):
            delete_last()
        canvas.bind('<Button-1>', paint_rectangle)

    elif (TOOL == "circle"):
        Xa = X
        Xb = event.x
        Ya = Y
        Yb = event.y
        radius = ((Xa - Xb) ** 2 + (Ya - Yb) ** 2) ** 0.5
        x1 = X - radius
        y1 = Y - radius
        x2 = X + radius
        y2 = Y + radius

        brush_size_change(choose_size.get())
        if (color != WHITE_COLOR):
            CURRENT_ELEMENT = canvas.create_oval(x1, y1, x2, y2, outline=color, width=brush_size)
        else:
            CURRENT_ELEMENT = canvas.create_oval(x1, y1, x2, y2, width=brush_size)
        if (IS_FIRST):
            IS_FIRST = False
        elif (DELETE):
            delete_last()
        canvas.bind('<Button-1>', paint_circle)


def delete_last():
    global CURRENT_ELEMENT, DELETE
    if (DELETE):
        canvas.delete(CURRENT_ELEMENT - 1)


def stop_deleting(event):
    global DELETE
    DELETE = False


def brush_size_change(new_size):
    global brush_size
    brush_size = new_size


root = Tk()
root.title("LR3_Shverdiakov")

canvas = Canvas(root,
                width=CANVAS_WIDTH,
                height=CANVAS_HEIGHT,
                bg="white")
root.resizable(False, False)

pencil_btn = Button(text="Карандаш", width=10, command=lambda: pencil())
brush_btn = Button(text="Кисть", width=10, command=lambda: brush())
rectangle_btn = Button(text="Прямоугольник", width=15, command=lambda: rectangle())
circle_btn = Button(text="Окружность", width=15, command=lambda: circle())
choose_color_btn = Button(text="Изменить цвет", width=15, command=lambda: color_change(""))
choose_size = Scale(from_=2, to=20, orient=HORIZONTAL)
anisotropic_btn = Button(text="Система координат", width=17, command=lambda: anisotropic_system())
save_btn = Button(text="Сохранить как", width=17, command=lambda: save_paint())
erase_btn = Button(text="Ластик", width=10, command=lambda: erase())
clear_all_btn = Button(text="Удалить всё", width=10, command=lambda: clear_all())

canvas.grid(row=2, column=0, columnspan=7, padx=5, pady=5, sticky=E + W + S + N)
canvas.columnconfigure(6, weight=1)
canvas.rowconfigure(2, weight=1)

pencil_btn.grid(row=0, column=1)
brush_btn.grid(row=1, column=1)
rectangle_btn.grid(row=0, column=2)
circle_btn.grid(row=1, column=2)
choose_color_btn.grid(row=0, column=3)
choose_size.grid(row=1, column=3)
anisotropic_btn.grid(row=0, column=4)
save_btn.grid(row=1, column=4)
erase_btn.grid(row=0, column=6, sticky=W)
clear_all_btn.grid(row=1, column=6, sticky=W)

root.mainloop()