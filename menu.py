import tkinter as tk
from tkinter import ttk

# Main window
root = tk.Tk()
root.title("Cool Dropdown")
root.geometry("350x200")
root.configure(bg="#1e1e1e")

# Style configuration
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Cool.TCombobox",
    fieldbackground="#2b2b2b",
    background="#2b2b2b",
    foreground="white",
    arrowcolor="white",
    borderwidth=0,
    padding=6
)

style.map(
    "Cool.TCombobox",
    fieldbackground=[("readonly", "#2b2b2b")],
    foreground=[("readonly", "white")],
    background=[("readonly", "#2b2b2b")]
)

# Label
label = tk.Label(
    root,
    text="Select Mode",
    bg="#1e1e1e",
    fg="white",
    font=("Segoe UI", 12)
)
label.pack(pady=15)

# Dropdown values
options = ["Easy", "Medium", "Hard", "Expert"]

selected = tk.StringVar()
selected.set(options[0])

# Dropdown (Combobox)
dropdown = ttk.Combobox(
    root,
    textvariable=selected,
    values=options,
    state="readonly",
    style="Cool.TCombobox",
    font=("Segoe UI", 11)
)
dropdown.pack(pady=10)

# Button to show selection
def show_selection():
    print("Selected:", selected.get())

btn = tk.Button(
    root,
    text="Confirm",
    command=show_selection,
    bg="#3a7afe",
    fg="white",
    font=("Segoe UI", 10),
    relief="flat",
    padx=15,
    pady=6
)
btn.pack(pady=20)

root.mainloop()
