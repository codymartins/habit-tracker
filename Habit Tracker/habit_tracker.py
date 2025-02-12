import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from tkinter import Tk, Label, Checkbutton, Scale, BooleanVar, HORIZONTAL, Text, Button, END
from datetime import date

# Authenticate and connect to Google Sheets
def connect_to_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)
    return client

# Append data to the sheet
def save_to_google_sheets(data):
    client = connect_to_google_sheets()
    sheet = client.open("Habit Data").sheet1 # Replace with your sheet name
    sheet.append_row(data)

# Gather and save data
def save_data():
    today = str(date.today())

    # Gather data from GUI
    habits = {
        "exercise": exercise_var.get(),
        "read": read_var.get(),
        "meditate": meditate_var.get(),
        "sleep": sleep_scale.get(),
        "Time Outside": Outside_scale.get(),
        "Journal": journal_var.get(),
    }
    metrics = {
        "mood": mood_scale.get(),
        "energy": energy_scale.get(),
        "productivity": productivity_scale.get(),
    }
    reflection = reflection_text.get("1.0", END).strip()

    # Flatten the data into a single list for Google Sheets
    row_data = [
        today,
        habits["exercise"],
        habits["read"],
        habits["meditate"],
        habits["sleep"],
        habits["Time Outside"],
        habits["Journal"],
        metrics["mood"],
        metrics["energy"],
        metrics["productivity"],
        reflection,
    ]

    save_to_google_sheets(row_data)
    status_label.config(text="Data saved successfully!")
    reflection_text.delete("1.0", END)  # Clear reflection text box

# Create GUI window
root = Tk()
root.title("Daily Habit Tracker")

# Habits section
Label(root, text="Habits").grid(row=0, column=0, sticky="w")
exercise_var = BooleanVar()
read_var = BooleanVar()
meditate_var = BooleanVar()
journal_var = BooleanVar()
Outside_scale = Scale(root, from_=0, to=130, resolution=15, orient=HORIZONTAL)
sleep_scale = Scale(root, from_=1, to=10, orient=HORIZONTAL)
Checkbutton(root, text="Exercise", variable=exercise_var).grid(row=1, column=0, sticky="w")
Checkbutton(root, text="Read", variable=read_var).grid(row=2, column=0, sticky="w")
Checkbutton(root, text="Meditate", variable=meditate_var).grid(row=3, column=0, sticky="w")
Checkbutton(root, text="Journal", variable=journal_var).grid(row=4, column=0, sticky="w")
Label(root, text="Hours of Sleep:").grid(row=5, column=0, sticky="w")
sleep_scale.grid(row=5, column=1)
Label(root, text="Time Outside:").grid(row=6, column=0, sticky="w")
Outside_scale.grid(row=6, column=1)

# Metrics section
Label(root, text="Metrics (Rate 1-10)").grid(row=7, column=0, sticky="w")
Label(root, text="Mood:").grid(row=8, column=0, sticky="w")
mood_scale = Scale(root, from_=1, to=10, orient=HORIZONTAL)
mood_scale.grid(row=8, column=1)

Label(root, text="Energy:").grid(row=9, column=0, sticky="w")
energy_scale = Scale(root, from_=1, to=10, orient=HORIZONTAL)
energy_scale.grid(row=9, column=1)

Label(root, text="Productivity:").grid(row=10, column=0, sticky="w")
productivity_scale = Scale(root, from_=1, to=10, orient=HORIZONTAL)
productivity_scale.grid(row=10, column=1)

# Reflection section
Label(root, text="Reflection").grid(row=11, column=0, sticky="w")
reflection_text = Text(root, height=5, width=30)
reflection_text.grid(row=11, column=0, columnspan=2)

# Save Button
save_button = Button(root, text="Save", command=save_data)
save_button.grid(row=12, column=0, columnspan=2)

# Status Label
status_label = Label(root, text="", fg="green")
status_label.grid(row=13, column=0, columnspan=2)

# Run GUI
root.mainloop()

