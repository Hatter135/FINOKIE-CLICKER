import tkinter as tk
import colorsys
import pygame
import json
import os

# WARNING YOU HAVE TO RUN " pip install pygame " TO RUN THIS PROGRAM
pygame.mixer.init()

print("Launching App...")

# ---------------- THEME SYSTEM ----------------
THEME_FILE = "theme.json"

LIGHT_THEME = {
    "bg": "white",
    "fg": "black",
    "panel": "gray90"
}

DARK_THEME = {
    "bg": "#121212",
    "fg": "white",
    "panel": "#1e1e1e"
}

def load_theme():
    if os.path.exists(THEME_FILE):
        with open(THEME_FILE, "r") as f:
            return DARK_THEME if json.load(f)["mode"] == "dark" else LIGHT_THEME
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
finokie_image = None
score = 0
score_label = None
title_canvas = None
title_text = None
shop_frame = None

click_power = 1
click_upgrade_cost = 10
click_power_label = None
shop_cost_label = None

cursor_upgrade_cost = 50
cursor_upgrade_level = 0
cursor_label = None
cursor_cost_label = None

click_sound = pygame.mixer.Sound(r"C:\Users\finle\OneDrive - New College Durham\Documents\Main Program\L3 IT\Programing\College Python Work\GUI Creation\image\Recording (9).wav")
upgrade_sound = pygame.mixer.Sound(r"C:\Users\finle\OneDrive - New College Durham\Documents\Main Program\L3 IT\Programing\College Python Work\GUI Creation\image\Recording (12).wav")
major_upgrade = pygame.mixer.Sound(r"C:\Users\finle\OneDrive - New College Durham\Documents\Main Program\L3 IT\Programing\College Python Work\GUI Creation\image\Recording (13).wav")

hue = 0

# ---------------- THEME APPLY ----------------
def apply_theme(widget):
    widget.config(bg=current_theme["bg"])
    for child in widget.winfo_children():
        try:
            if isinstance(child, tk.Frame):
                child.config(bg=current_theme["panel"])
            elif isinstance(child, tk.Button):
                child.config(
                    bg=current_theme["bg"],
                    fg=current_theme["fg"],
                    activebackground=current_theme["fg"],
                    activeforeground=current_theme["bg"]
                )
            elif isinstance(child, (tk.Label, tk.Canvas)):
                child.config(
                    bg=current_theme["bg"],
                    fg=current_theme["fg"]
                )
        except:
            pass
        apply_theme(child)

def toggle_theme():
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    save_theme(current_theme)
    apply_theme(window)

# ---------------- Shop functions ----------------
def open_shop():
    shop_frame.place(relx=1.0, rely=0.5, anchor="e")

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
        upgrade_sound.play()

def buy_cursor_upgrade():
    global score, click_power, cursor_upgrade_cost, cursor_upgrade_level
    if score >= cursor_upgrade_cost:
        score -= cursor_upgrade_cost
        click_power *= 2
        cursor_upgrade_level += 1
        cursor_upgrade_cost *= 2
        score_label.config(text=f"Score: {score}")
        cursor_label.config(text=f"Cursor Refinement Lv: {cursor_upgrade_level}")
        cursor_cost_label.config(text=f"Cost: {cursor_upgrade_cost}")
        major_upgrade.play()

# ---------------- Rainbow title ----------------
def animate_title():
    global hue
    if title_canvas is None or title_text is None:
        return

    hue = (hue + 0.01) % 1
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    title_canvas.itemconfig(
        title_text,
        fill=f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    )

    window.after(50, animate_title)

# ---------------- Click function ----------------
def click_image():
    global score
    score += click_power
    score_label.config(text=f"Score: {score}")
    click_sound.play()

# ---------------- Main game screen ----------------
def game():
    global finokie_image, score_label
    global title_canvas, title_text
    global shop_frame, click_power_label, shop_cost_label
    global cursor_label, cursor_cost_label

    for widget in window.winfo_children():
        widget.destroy()

    # Theme toggle
    tk.Button(
        window, text="🌙 / 🌞",
        font=("Calibri", 14),
        command=toggle_theme
    ).place(relx=0.98, rely=0.02, anchor="ne")

    # Title
    title_canvas = tk.Canvas(window, height=100, highlightthickness=0)
    title_canvas.pack(pady=10)

    title_text = title_canvas.create_text(
        960, 50,
        text="FINOKIE CLICKER",
        font=("Calibri", 48, "bold")
    )
    animate_title()

    # SHOP button
    tk.Button(
        window,
        text="SHOP",
        font=("Calibri", 24),
        command=open_shop
    ).pack(pady=10)

    # ---------------- Shop frame ----------------
    shop_frame = tk.Frame(window, bd=4, relief="ridge")

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

    # ---------------- Finokie button ----------------
    finokie_image = tk.PhotoImage(
        file=r"C:\Users\finle\OneDrive - New College Durham\Documents\Main Program\L3 IT\Programing\College Python Work\GUI Creation\image\Finokie.png"
    ).subsample(2, 2)

    score_label = tk.Label(
        window, text=f"Score: {score}", font=("Calibri", 36)
    )
    score_label.pack(pady=10)

    tk.Button(
        window, image=finokie_image,
        command=click_image, borderwidth=0
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
    tk.Button(
        window, text="🌙 / 🌞",
        font=("Calibri", 14),
        command=toggle_theme
    ).place(relx=0.98, rely=0.02, anchor="ne")

    tk.Label(
        window, text="FINOKIE CLICKER",
        font=("Calibri", 72, "bold")
    ).pack(pady=50)

    tk.Button(
        window, text="START",
        width=100, height=5,
        font=("Calibri", 30),
        command=game
    ).pack(pady=5)

    tk.Button(
        window, text="EXIT",
        width=100, height=5,
        font=("Calibri", 30),
        command=window.destroy
    ).pack(pady=5)

    apply_theme(window)

# ---------------- Launch ----------------
Start_Menu()
window.mainloop()
print("APP EXITED BY USER")
