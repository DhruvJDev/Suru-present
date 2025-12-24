import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import sys
import os

# -------------------------------------------
# 🔧 FIX IMPORT ERROR BY ADDING PROJECT ROOT
# -------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

# -------------------------------------------
# ✅ Backend imports (will now work)
# -------------------------------------------
from module import speak
from main import listen, process_command


# ---------- Global Flags ----------
listening = False
animate = True


# ---------- Handle Command ----------
def handle_command():
    global listening, animate
    listening = True
    animate = True

    listen_button.config(text="🛑 STOP", fg="#C43201", bg="#8B0000")
    threading.Thread(target=animate_glow, daemon=True).start()

    try:
        output_box.insert(tk.END, "🎤 Listening...\n")
        output_box.see(tk.END)

        command = listen()
        if command:
            output_box.insert(tk.END, f"🗣️ You said: {command}\n")
            output_box.insert(tk.END, "🤖 Processing...\n\n")
            output_box.see(tk.END)

            process_command(command)

            output_box.insert(tk.END, "✅ Task Completed.\n\n")
            output_box.see(tk.END)

    except Exception as e:
        output_box.insert(tk.END, f"⚠️ Error: {str(e)}\n\n")
        speak.say("Something went wrong.")
        output_box.see(tk.END)

    listening = False
    animate = False
    listen_button.config(text="🎤 LISTEN", fg="#000000", bg="#006400")


# ---------- Toggle Listening ----------
def toggle_listening():
    global listening, animate
    if not listening:
        threading.Thread(target=handle_command, daemon=True).start()
    else:
        listening = False
        animate = False
        output_box.insert(tk.END, "🛑 Stopped listening.\n\n")
        speak.say("Stopped listening.")
        listen_button.config(text="🎤 LISTEN", fg="#000000", bg="#006400")
        output_box.see(tk.END)


# ---------- Glow Animation ----------
def animate_glow():
    glow_intensity = 0
    direction = 1
    while animate:
        glow_canvas.delete("all")
        color = f"#{0:02x}{int(255 - glow_intensity * 3):02x}{120:02x}"

        glow_canvas.create_oval(
            150 - glow_intensity, 150 - glow_intensity,
            150 + glow_intensity, 150 + glow_intensity,
            outline=color, width=6
        )

        app.update_idletasks()
        glow_intensity += direction * 3

        if glow_intensity > 70 or glow_intensity < 10:
            direction *= -1

        time.sleep(0.04)

    glow_canvas.delete("all")


# ---------- GUI Setup ----------
app = tk.Tk()
app.title("Suru A.I.")
app.geometry("700x750")
app.configure(bg="#1E1E1E")

# Title
title_label = tk.Label(
    app,
    text="🧠 Suru A.I.",
    font=("Arial Rounded MT Bold", 30),
    fg="#00FF99",
    bg="#1E1E1E"
)
title_label.pack(pady=20)

# Glow Canvas
glow_canvas = tk.Canvas(app, width=300, height=300, bg="#1E1E1E", highlightthickness=0)
glow_canvas.pack(pady=10)

# Listen Button
listen_button = tk.Button(
    app,
    text="🎤 LISTEN",
    font=("Arial", 20, "bold"),
    bg="#006400",
    fg="black",
    width=15,
    height=2,
    relief="flat",
    command=toggle_listening
)
listen_button.pack(pady=20)

# Output Box
output_box = scrolledtext.ScrolledText(
    app,
    width=70,
    height=15,
    font=("Consolas", 13),
    bg="#2C2C2C",
    fg="white",
    insertbackground="white"
)
output_box.pack(pady=10)
output_box.insert(tk.END, "👋 Welcome to Suru A.I. Desktop Interface\n\n")
output_box.see(tk.END)

# Run GUI
app.mainloop()