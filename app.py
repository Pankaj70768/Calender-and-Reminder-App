from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from time import strftime
from plyer import notification
from datetime import datetime, timedelta
import threading
import time
import winsound
import speech_recognition as sr

# ---------------- WINDOW ---------------- #

root = Tk()

root.title("📅 Ultimate Calendar Reminder App")

# FIXED SIZE
root.geometry("900x1200")

root.config(bg="#1e1e2f")

root.resizable(True, True)

# ---------------- TITLE ---------------- #

title = Label(
    root,
    text="📅 Calendar Reminder App",
    font=("Poppins", 28, "bold"),
    bg="#1e1e2f",
    fg="#00ffcc"
)

title.pack(pady=10)

# ---------------- CLOCK ---------------- #

clock_label = Label(
    root,
    font=("Poppins", 18, "bold"),
    bg="#1e1e2f",
    fg="#ffd166"
)

clock_label.pack()

def update_time():

    current_time = strftime('%I:%M:%S %p')
    current_date = strftime('%d-%m-%Y')

    clock_label.config(
        text=f"⏰ {current_time}\n📅 {current_date}"
    )

    clock_label.after(1000, update_time)

update_time()

# ---------------- CALENDAR ---------------- #

cal = Calendar(
    root,
    selectmode="day",
    date_pattern="mm/dd/yy",
    background="#2b2b3c",
    foreground="white",
    headersbackground="#ff4b5c",
    headersforeground="white",
    selectbackground="#00ffcc",
    normalbackground="#2b2b3c",
    normalforeground="white",
    weekendbackground="#2b2b3c",
    weekendforeground="#ff6b81"
)

cal.pack(pady=15)

# ---------------- SEARCH ---------------- #

search_label = Label(
    root,
    text="🔍 Search Reminder",
    font=("Poppins", 14, "bold"),
    bg="#1e1e2f",
    fg="white"
)

search_label.pack()

search_entry = Entry(
    root,
    width=30,
    font=("Poppins", 12),
    bg="#2b2b3c",
    fg="white",
    insertbackground="white",
    bd=0
)

search_entry.pack(pady=8, ipady=6)

# ---------------- REMINDER ---------------- #

label = Label(
    root,
    text="📝 Enter Reminder",
    font=("Poppins", 14, "bold"),
    bg="#1e1e2f",
    fg="white"
)

label.pack()

reminder_entry = Entry(
    root,
    width=40,
    font=("Poppins", 14),
    bg="#2b2b3c",
    fg="white",
    insertbackground="white",
    bd=0
)

reminder_entry.pack(pady=8, ipady=8)

# ---------------- TIME ---------------- #

time_label = Label(
    root,
    text="⏰ Enter Time (HH:MM AM/PM)",
    font=("Poppins", 14, "bold"),
    bg="#1e1e2f",
    fg="white"
)

time_label.pack()

time_entry = Entry(
    root,
    width=25,
    font=("Poppins", 14),
    bg="#2b2b3c",
    fg="white",
    insertbackground="white",
    bd=0
)

time_entry.pack(pady=8, ipady=8)

# ---------------- CATEGORY ---------------- #

category_label = Label(
    root,
    text="📂 Select Category",
    font=("Poppins", 14, "bold"),
    bg="#1e1e2f",
    fg="white"
)

category_label.pack()

categories = [
    "Meeting",
    "Holiday",
    "Birthday",
    "Exam",
    "Task"
]

category_var = StringVar()

category_dropdown = ttk.Combobox(
    root,
    textvariable=category_var,
    values=categories,
    state="readonly",
    font=("Poppins", 12),
    width=22
)

category_dropdown.pack(pady=8)

category_dropdown.current(0)

# ---------------- BUTTON FRAME ---------------- #

button_frame = Frame(
    root,
    bg="#1e1e2f"
)

button_frame.pack(pady=10)

# ---------------- REMINDER BOX ---------------- #

display_label = Label(
    root,
    text="📋 Saved Reminders",
    font=("Poppins", 14, "bold"),
    bg="#1e1e2f",
    fg="#00ffcc"
)

display_label.pack()

scrollbar = Scrollbar(root)

scrollbar.pack(side=RIGHT, fill=Y)

reminder_box = Text(
    root,
    width=70,
    height=4,
    font=("Consolas", 12),
    bg="#2b2b3c",
    fg="white",
    insertbackground="white",
    bd=0,
    yscrollcommand=scrollbar.set
)

scrollbar.config(command=reminder_box.yview)

reminder_box.pack(pady=10)

# ---------------- COLORS ---------------- #

reminder_box.tag_config("Meeting", foreground="#00ff99")
reminder_box.tag_config("Holiday", foreground="#ff4b5c")
reminder_box.tag_config("Birthday", foreground="#ff66ff")
reminder_box.tag_config("Exam", foreground="#ffd166")
reminder_box.tag_config("Task", foreground="#66ccff")

# ---------------- HIGHLIGHT DATE ---------------- #

def highlight_date(date, category):

    colors = {
        "Meeting": "#00ff99",
        "Holiday": "#ff4b5c",
        "Birthday": "#ff66ff",
        "Exam": "#ffd166",
        "Task": "#66ccff"
    }

    cal.calevent_create(date, category, category)

    cal.tag_config(
        category,
        background=colors[category],
        foreground="black"
    )

# ---------------- LOAD OLD REMINDERS ---------------- #

try:

    with open("reminders.txt", "r") as file:

        reminders = file.readlines()

        for line in reminders:
            reminder_box.insert(END, line)

except:
    pass

    # ---------------- NOTIFICATION ---------------- #

def show_notification(title, message):

    winsound.Beep(1000, 500)

    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

# ---------------- VOICE INPUT ---------------- #

def voice_input():

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            messagebox.showinfo(
                "Voice Assistant",
                "Speak now..."
            )

            audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio)

            reminder_entry.delete(0, END)

            reminder_entry.insert(0, text)

            messagebox.showinfo(
                "Voice Result",
                f"You said: {text}"
            )

    except:

        messagebox.showerror(
            "Error",
            "Could not recognize voice"
        )

# ---------------- ADD REMINDER ---------------- #

def add_reminder():

    reminder = reminder_entry.get()

    reminder_time = time_entry.get()

    category = category_var.get()

    date = cal.get_date()

    selected_date = cal.selection_get()

    if reminder == "" or reminder_time == "":

        messagebox.showwarning(
            "Warning",
            "Please fill all fields"
        )

    else:

        text = f"[{category}] {date} | {reminder_time} | {reminder}\n"

        start_index = reminder_box.index(END)

        reminder_box.insert(END, text)

        end_index = reminder_box.index(END)

        reminder_box.tag_add(
            category,
            start_index,
            end_index
        )

        highlight_date(selected_date, category)

        with open("reminders.txt", "a") as file:
            file.write(text)

        messagebox.showinfo(
            "Success",
            "Reminder Added Successfully"
        )

        reminder_entry.delete(0, END)

        time_entry.delete(0, END)

# ---------------- DELETE ---------------- #

def delete_reminder():

    try:

        reminder_box.delete("sel.first", "sel.last")

        messagebox.showinfo(
            "Deleted",
            "Reminder Deleted Successfully"
        )

    except:

        messagebox.showwarning(
            "Warning",
            "Select reminder text first"
        )

# ---------------- SEARCH ---------------- #

def search_reminder():

    reminder_box.tag_remove("highlight", "1.0", END)

    search_text = search_entry.get()

    if search_text == "":
        return

    start_pos = "1.0"

    while True:

        start_pos = reminder_box.search(
            search_text,
            start_pos,
            stopindex=END,
            nocase=True
        )

        if not start_pos:
            break

        end_pos = f"{start_pos}+{len(search_text)}c"

        reminder_box.tag_add(
            "highlight",
            start_pos,
            end_pos
        )

        start_pos = end_pos

    reminder_box.tag_config(
        "highlight",
        background="yellow",
        foreground="black"
    )

# ---------------- CLEAR ---------------- #

def clear_all():

    reminder_box.delete("1.0", END)

    with open("reminders.txt", "w") as file:
        file.write("")

    messagebox.showinfo(
        "Cleared",
        "All reminders deleted"
    )

# ---------------- THEME ---------------- #

dark_mode = True

def toggle_theme():

    global dark_mode

    if dark_mode:

        root.config(bg="white")

        title.config(bg="white", fg="black")

        clock_label.config(bg="white", fg="blue")

        label.config(bg="white", fg="black")

        time_label.config(bg="white", fg="black")

        category_label.config(bg="white", fg="black")

        display_label.config(bg="white", fg="black")

        search_label.config(bg="white", fg="black")

        footer.config(bg="white", fg="gray")

        dark_mode = False

    else:

        root.config(bg="#1e1e2f")

        title.config(bg="#1e1e2f", fg="#00ffcc")

        clock_label.config(bg="#1e1e2f", fg="#ffd166")

        label.config(bg="#1e1e2f", fg="white")

        time_label.config(bg="#1e1e2f", fg="white")

        category_label.config(bg="#1e1e2f", fg="white")

        display_label.config(bg="#1e1e2f", fg="#00ffcc")

        search_label.config(bg="#1e1e2f", fg="white")

        footer.config(bg="#1e1e2f", fg="gray")

        dark_mode = True

# ---------------- BUTTONS ---------------- #

add_button = Button(
    button_frame,
    text="➕ Add Reminder",
    command=add_reminder,
    bg="#ff4b5c",
    fg="white",
    font=("Poppins", 12, "bold"),
    padx=12,
    pady=6,
    border=0
)

add_button.grid(row=0, column=0, padx=5, pady=5)

delete_button = Button(
    button_frame,
    text="❌ Delete",
    command=delete_reminder,
    bg="#ff3333",
    fg="white",
    font=("Poppins", 12, "bold"),
    padx=12,
    pady=6,
    border=0
)

delete_button.grid(row=0, column=1, padx=5, pady=5)

search_button = Button(
    button_frame,
    text="🔍 Search",
    command=search_reminder,
    bg="#00b894",
    fg="white",
    font=("Poppins", 12, "bold"),
    padx=12,
    pady=6,
    border=0
)

search_button.grid(row=1, column=0, padx=5, pady=5)

clear_button = Button(
    button_frame,
    text="🗑️ Clear All",
    command=clear_all,
    bg="#6c5ce7",
    fg="white",
    font=("Poppins", 12, "bold"),
    padx=12,
    pady=6,
    border=0
)

clear_button.grid(row=1, column=1, padx=5, pady=5)

theme_button = Button(
    button_frame,
    text="🌙 Toggle Theme",
    command=toggle_theme,
    bg="#0984e3",
    fg="white",
    font=("Poppins", 12, "bold"),
    padx=12,
    pady=6,
    border=0
)

theme_button.grid(row=2, column=0, columnspan=2, pady=5)

# ---------------- VOICE BUTTON ---------------- #

voice_button = Button(
    button_frame,
    text="🎤 Voice Input",
    command=voice_input,
    bg="#fdcb6e",
    fg="black",
    font=("Poppins", 12, "bold"),
    padx=12,
    pady=6,
    border=0
)

voice_button.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=5
)


# ---------------- CHECK REMINDERS ---------------- #

def check_reminders():

    while True:

        now = datetime.now()

        try:

            with open("reminders.txt", "r") as file:

                reminders = file.readlines()

                for line in reminders:

                    clean_line = line.replace("[", "").replace("]", "")

                    parts = clean_line.strip().split("|")

                    if len(parts) >= 3:

                        left_part = parts[0].strip()

                        date_str = left_part.split()[-1]

                        time_str = parts[1].strip()

                        message = parts[2].strip()

                        reminder_datetime = datetime.strptime(
                            f"{date_str} {time_str}",
                            "%m/%d/%y %I:%M %p"
                        )

                        before_5 = reminder_datetime - timedelta(minutes=5)

                        if now.strftime("%Y-%m-%d %H:%M") == before_5.strftime("%Y-%m-%d %H:%M"):

                            show_notification(
                                "⏰ Upcoming Reminder",
                                f"{message} in 5 minutes"
                            )

                        if now.strftime("%Y-%m-%d %H:%M") == reminder_datetime.strftime("%Y-%m-%d %H:%M"):

                            show_notification(
                                "🔔 Reminder Alert",
                                message
                            )

        except:
            pass

        time.sleep(30)

# ---------------- THREAD ---------------- #

threading.Thread(
    target=check_reminders,
    daemon=True
).start()

# ---------------- FOOTER ---------------- #

footer = Label(
    root,
    text="Made with ❤️ using Python",
    font=("Poppins", 10),
    bg="#1e1e2f",
    fg="gray"
)

footer.pack(side=BOTTOM, pady=5)

# ---------------- RUN ---------------- #

root.mainloop()