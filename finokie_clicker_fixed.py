import tkinter as tk
import colorsys
import pygame
import json
import os
import time
from time import sleep

# WARNING YOU HAVE TO RUN " pip install pygame " TO RUN THIS PROGRAM
pygame.mixer.init()

print("Launching App...")

# ---------------- THEME SYSTEM ----------------
THEME_FILE = "theme.json"

LIGHT_THEME = {
    "bg": "white",
    "fg": "black",
    "panel": "gray90",
    "button_bg": "#e0e0e0"
}

DARK_THEME = {
    "bg": "#121212",
    "fg": "white",
    "panel": "#1e1e1e",
    "button_bg": "#2a2a2a"
}

def load_theme():
    if os.path.exists(THEME_FILE):
        try:
            with open(THEME_FILE, "r") as f:
                return DARK_THEME if json.load(f)["mode"] == "dark" else LIGHT_THEME
        except:
            return LIGHT_THEME
    return LIGHT_THEME

def save_theme(theme):
    with open(THEME_FILE, "w") as f:
        json.dump({"mode": "dark" if theme == DARK_THEME else "light"}, f)

current_theme = load_theme()

# ---------------- Window ----------------
window = tk.Tk()
window.title("FINOKIE CLICKER")
window.geometry("1920x1080")
window.config(bg=current_theme["bg"])

print("App Loaded!")

# ---------------- Globals ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR)

finokie_image = None
score = 0
score_label = None
click_count = 0
click_count_label = None

title_canvas = None
title_text = None
hue = 0
animation_running = False

shop_frame = None
theme_button = None

click_power = 1
click_upgrade_cost = 10
click_power_label = None
shop_cost_label = None

cursor_upgrade_cost = 50
cursor_upgrade_level = 0
cursor_label = None
cursor_cost_label = None

# Sound loading with error handling
try:
    click_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Click.wav"))
    upgrade_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Upgrade.wav"))
    major_upgrade = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "MajorUpgrade.wav"))
    Music_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Geometry Dash Stay Inside Me.wav"))
    letsgo = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "letsgo.wav"))
except:
    print("Warning: Could not load sound files. Sounds will be disabled.")
    click_sound = None
    upgrade_sound = None
    major_upgrade = None
    Music_sound = None
    letsgo = None

# ---------------- THEME APPLY ----------------
def apply_theme(widget):
    try:
        widget.config(bg=current_theme["bg"])
    except:
        pass
    
    for child in widget.winfo_children():
        try:
            if isinstance(child, tk.Frame):
                child.config(bg=current_theme["panel"])
            elif isinstance(child, tk.Button):
                child.config(
                    bg=current_theme["button_bg"],
                    fg=current_theme["fg"],
                    activebackground=current_theme["fg"],
                    activeforeground=current_theme["bg"]
                )
            elif isinstance(child, tk.Checkbutton):
                child.config(
                    bg=current_theme["bg"],
                    fg=current_theme["fg"],
                    activebackground=current_theme["bg"],
                    activeforeground=current_theme["fg"],
                    selectcolor=current_theme["button_bg"]
                )
            elif isinstance(child, tk.Label):
                child.config(bg=current_theme["bg"], fg=current_theme["fg"])
            elif isinstance(child, tk.Canvas):
                child.config(bg=current_theme["bg"])
        except:
            pass
        apply_theme(child)

def toggle_theme():
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    save_theme(current_theme)
    apply_theme(window)

# ---------------- Rainbow title ----------------
def animate_title():
    global hue, animation_running
    
    if not animation_running:
        return
        
    if title_canvas is None or title_text is None:
        return
    
    try:
        hue = (hue + 0.01) % 1
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        colour = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

        title_canvas.itemconfig(title_text, fill=colour)
        window.after(50, animate_title)
    except:
        pass

def create_rainbow_title(text):
    global title_canvas, title_text, animation_running

    title_canvas = tk.Canvas(
        window,
        height=100,
        highlightthickness=0,
        bg=current_theme["bg"]
    )
    title_canvas.pack(fill="x", pady=10)

    title_text = title_canvas.create_text(
        0, 50,
        text=text,
        font=("Calibri", 48, "bold")
    )

    def center_title(event=None):
        w = title_canvas.winfo_width()
        title_canvas.coords(title_text, w // 2, 50)

    title_canvas.bind("<Configure>", center_title)
    center_title()

    animation_running = True
    animate_title()

# ---------------- Lets Go Diagonal Text ----------------
def show_lets_go_text(duration=2000):
    canvas = tk.Canvas(
        window,
        width=1900,
        height=1080,
        bg=current_theme["bg"],
        highlightthickness=0
    )
    canvas.place(x=0, y=0)

    canvas.create_text(
        960, 540,
        text="FINOKIE CLICKER LET'S GO!!!!!!!!!!!!!!!!!!!!!!!!",
        font=("Calibri", 80, "bold"),
        fill=current_theme["fg"],
        angle=340  # diagonal
    )

    # auto-remove after duration
    window.after(duration, canvas.destroy)

# ---------------- Shop functions ----------------
def open_shop():
    shop_frame.place(relx=1.0, rely=0.5, anchor="e", x=-20)

def close_shop():
    shop_frame.place_forget()

def buy_click_upgrade():
    global score, click_power, click_upgrade_cost
    if score >= click_upgrade_cost:
        score -= click_upgrade_cost
        click_power += 1
        click_upgrade_cost = int(click_upgrade_cost * 1.5)
        score_label.config(text=f"Score: {score}")
        click_power_label.config(text=f"Click Power: {click_power}")
        shop_cost_label.config(text=f"Cost: {click_upgrade_cost}")
        if upgrade_sound:
            upgrade_sound.play()

def buy_cursor_upgrade():
    global score, click_power, cursor_upgrade_cost, cursor_upgrade_level
    if score >= cursor_upgrade_cost:
        score -= cursor_upgrade_cost
        click_power *= 2
        cursor_upgrade_level += 1
        cursor_upgrade_cost *= 2
        score_label.config(text=f"Score: {score}")
        click_power_label.config(text=f"Click Power: {click_power}")
        cursor_label.config(text=f"Cursor Refinement Lv: {cursor_upgrade_level}")
        cursor_cost_label.config(text=f"Cost: {cursor_upgrade_cost}")
        if major_upgrade:
            major_upgrade.play()

# ---------------- Click function ----------------
def click_image():
    global score, click_count
    score += click_power
    click_count += 1
    score_label.config(text=f"Score: {score}")
    click_count_label.config(text=f"Clicks: {click_count}")
    if click_sound:
        click_sound.play()

# ---------------- Main game screen ----------------
def game():
    global finokie_image, score_label, animation_running, click_count_label
    global shop_frame, click_power_label, shop_cost_label
    global cursor_label, cursor_cost_label, theme_button

    animation_running = False
    
    for widget in window.winfo_children():
        widget.destroy()

    create_rainbow_title("FINOKIE CLICKER")

    # Theme toggle checkbutton - created AFTER title so it's on top
    theme_var = tk.BooleanVar(value=(current_theme == DARK_THEME))
    theme_button = tk.Checkbutton(
        window,
        text="Dark Mode",
        variable=theme_var,
        font=("Calibri", 14, "bold"),
        command=toggle_theme,
        selectcolor=current_theme["button_bg"],
        relief="raised",
        bd=2,
        padx=10,
        pady=5
    )
    theme_button.place(x=10, y=10)

    tk.Button(
        window,
        text="SHOP",
        font=("Calibri", 24),
        command=open_shop
    ).pack(pady=10)

    shop_frame = tk.Frame(window, bd=4, relief="ridge", bg=current_theme["panel"])

    tk.Label(shop_frame, text="SHOP", font=("Calibri", 36, "bold")).pack(pady=10)

    click_power_label = tk.Label(
        shop_frame, text=f"Click Power: {click_power}", font=("Calibri", 24)
    )
    click_power_label.pack(pady=5)

    shop_cost_label = tk.Label(
        shop_frame, text=f"Cost: {click_upgrade_cost}", font=("Calibri", 24)
    )
    shop_cost_label.pack(pady=5)

    tk.Button(
        shop_frame, text="BUY +1 CLICK POWER",
        font=("Calibri", 20),
        command=buy_click_upgrade
    ).pack(pady=10)

    cursor_label = tk.Label(
        shop_frame,
        text=f"Cursor Refinement Lv: {cursor_upgrade_level}",
        font=("Calibri", 20)
    )
    cursor_label.pack(pady=5)

    cursor_cost_label = tk.Label(
        shop_frame, text=f"Cost: {cursor_upgrade_cost}", font=("Calibri", 20)
    )
    cursor_cost_label.pack(pady=5)

    tk.Button(
        shop_frame,
        text="BUY CURSOR UPGRADE (2x click)",
        font=("Calibri", 18),
        command=buy_cursor_upgrade
    ).pack(pady=10)

    tk.Button(
        shop_frame,
        text="CLOSE",
        font=("Calibri", 20),
        command=close_shop
    ).pack(pady=10)

    # Image loading with error handling
    try:
        finokie_image = tk.PhotoImage(
            file=os.path.join(ASSETS_DIR, "Finokie.png")
        ).subsample(2, 2)
    except:
        print("Warning: Could not load Finokie.png image.")
        finokie_image = None

    score_label = tk.Label(
        window, text=f"Score: {score}", font=("Calibri", 36)
    )
    score_label.pack(pady=10)

    click_count_label = tk.Label(
        window, text=f"Clicks: {click_count}", font=("Calibri", 24)
    )
    click_count_label.pack(pady=5)

    if finokie_image:
        tk.Button(
            window, image=finokie_image,
            command=click_image, borderwidth=0
        ).pack(pady=40)
    else:
        tk.Button(
            window, text="CLICK ME!",
            font=("Calibri", 36),
            width=15, height=5,
            command=click_image
        ).pack(pady=40)

    tk.Button(
        window, text="EXIT",
        width=20, height=2,
        font=("Calibri", 24),
        command=window.destroy
    ).pack(pady=20)

    apply_theme(window)

# ---------------- Start menu ----------------
def Start_Menu():
    if Music_sound:
        Music_sound.play()
    global animation_running, theme_button
    
    animation_running = False
    
    for widget in window.winfo_children():
        widget.destroy()

    create_rainbow_title("FINOKIE CLICKER")

    # Theme toggle checkbutton - created AFTER title so it's on top
    theme_var = tk.BooleanVar(value=(current_theme == DARK_THEME))
    theme_button = tk.Checkbutton(
        window,
        text="Dark Mode",
        variable=theme_var,
        font=("Calibri", 14, "bold"),
        command=toggle_theme,
        selectcolor=current_theme["button_bg"],
        relief="raised",
        bd=2,
        padx=10,
        pady=5
    )
    theme_button.place(x=10, y=10)

    tk.Label(
        window, text="Made By Finley Patterson",
        font=("Calibri", 14, "bold")
    ).pack(pady=5)

    tk.Button(
        window, text="START",
        width=100, height=5,
        font=("Calibri", 30),
        command=game
    ).pack(pady=10)

    tk.Button(
        window, text="EXIT",
        width=100, height=5,
        font=("Calibri", 30),
        command=window.destroy
    ).pack(pady=10)

    # PLAY LETSGO SOUND AND SHOW DIAGONAL TEXT
    if letsgo:
        letsgo.play()
    show_lets_go_text(2000)

    apply_theme(window)

# ---------------- Launch ----------------
Start_Menu()
window.mainloop()
print("APP EXITED BY USER")
