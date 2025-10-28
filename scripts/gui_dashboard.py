import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, json, os
import pyautogui
import shutil
import time
import sys

# ----------------------- Base Paths -----------------------
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Paths to scripts
CAPTURE_SCRIPT = os.path.join(SCRIPTS_DIR, "capture_dashcam.py")
UNDERSTAND_SCRIPT = os.path.join(SCRIPTS_DIR, "understand_clip.py")

# ----------------------- Functions -----------------------

def capture_clip():
    try:
        status_label.config(text="🎥 Capturing clip...", foreground="blue")
        root.update()
        subprocess.run([sys.executable, CAPTURE_SCRIPT], check=True)
        status_label.config(text="✅ Recording captured!", foreground="green")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="❌ Capture failed", foreground="red")

def understand_clip():
    try:
        status_label.config(text="🧠 Understanding clip...", foreground="blue")
        root.update()
        subprocess.run([sys.executable, UNDERSTAND_SCRIPT], check=True)
        status_label.config(text="✅ Clip understood!", foreground="green")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="❌ Understand failed", foreground="red")

def execute_workflow():
    workflow_file = os.path.join(DATA_DIR, "understood_actions.json")
    if not os.path.exists(workflow_file):
        messagebox.showerror("Error", "understood_actions.json not found! Run 'Understand Clip' first.")
        return

    with open(workflow_file, 'r') as f:
        data = json.load(f)
    
    steps = data.get("steps", [])
    for i, step in enumerate(steps, start=1):
        action = step['action']
        details = step['details']
        status_label.config(text=f"⚡ Executing step {i}/{len(steps)}: {action}", foreground="orange")
        root.update()
        try:
            if action == "open_app":
                app = details['app']
                pyautogui.press('win')
                time.sleep(0.5)
                pyautogui.write(app)
                pyautogui.press('enter')
                time.sleep(1)
            elif action == "type_text":
                pyautogui.write(details['text'])
            elif action == "save_file":
                path = details['path']
                pyautogui.hotkey('ctrl', 's')
                time.sleep(0.5)
                pyautogui.write(path)
                pyautogui.press('enter')
                time.sleep(1)
            elif action == "rename_file":
                old = details['old_name']
                new = details['new_name']
                if os.path.exists(old):
                    os.rename(old, new)
            elif action == "move_file":
                src = details['source_path']
                dst = details['destination_path']
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(src):
                    shutil.move(src, dst)
        except Exception as e:
            messagebox.showwarning("Warning", f"Failed step {action}: {str(e)}")

    status_label.config(text="✅ Workflow executed!", foreground="green")
    messagebox.showinfo("Success", "Workflow executed successfully!")

def show_summary():
    summary_file = os.path.join(DATA_DIR, "summary.txt")
    if os.path.exists(summary_file):
        with open(summary_file, 'r') as f:
            text = f.read()
        summary_window = tk.Toplevel(root)
        summary_window.title("Workflow Summary")
        summary_window.geometry("400x300")
        text_widget = tk.Text(summary_window, wrap="word", font=("Calibri", 11), padx=10, pady=10)
        text_widget.pack(expand=True, fill="both")
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
    else:
        messagebox.showwarning("Warning", "No summary available! Run 'Understand Clip' first.")

# ----------------------- GUI Setup -----------------------

root = tk.Tk()
root.title("🚀 AGI Dashcam Dashboard")
root.geometry("550x450")
root.configure(bg="#1e1e2f")

tk.Label(root, text="AGI Desktop Assistant", font=("Arial Rounded MT Bold", 24), bg="#1e1e2f", fg="#ffd700").pack(pady=20)

style = ttk.Style()
style.configure("TButton", font=("Calibri", 12), padding=8)
style.map("TButton",
          foreground=[('active', '#ffffff')],
          background=[('active', '#4caf50')])

ttk.Button(root, text="🎥 Capture Clip", width=25, command=capture_clip).pack(pady=10)
ttk.Button(root, text="🧠 Understand Clip", width=25, command=understand_clip).pack(pady=10)
ttk.Button(root, text="🤖 Execute Automation", width=25, command=execute_workflow).pack(pady=10)
ttk.Button(root, text="📄 Show Workflow Summary", width=25, command=show_summary).pack(pady=10)

status_label = tk.Label(root, text="Status: Ready", font=("Calibri", 11), bg="#1e1e2f", fg="#00ff00")
status_label.pack(side="bottom", pady=15)

tk.Label(root, text="All actions are local and offline.", font=("Calibri", 10), bg="#1e1e2f", fg="#aaaaaa").pack(side="bottom")

root.mainloop()
