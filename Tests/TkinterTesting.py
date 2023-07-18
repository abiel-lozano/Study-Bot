# Colors:
# > #09B898 = teal
# > #9ae6d8 = light teal

import tkinter as tk
from tkinter import messagebox

def check_selection():
    language = languageVar.get()
    topic = topicVar.get()
    selectionText.set(f"Selected language: {language}\nSelected topic: {topic}")

# Create the main window
window = tk.Tk()
window.title("Study-Bot")
window.geometry("300x315")  # Set the window size

# Set the background color
window.configure(bg="#09B898")

# Create the title label
titleLabel = tk.Label(window, text="Study-Bot", font=("Nunito", 16, "bold"), bg="#9ae6d8")
titleLabel.pack(pady=10)

# Create the language dropdown
languageLabel = tk.Label(window, text="Select Language:", bg="#9ae6d8")
languageLabel.pack(pady=10)  # Add vertical spacing
languageVar = tk.StringVar(window)
languageDropdown = tk.OptionMenu(window, languageVar, "English", "Spanish")
languageDropdown.config(width=10)  # Increase the width of the dropdown
languageDropdown.pack()

# Create the topic dropdown
topicLabel = tk.Label(window, text="Select Topic:", bg="#9ae6d8")
topicLabel.pack(pady=10)  # Add vertical spacing
topicVar = tk.StringVar(window)
topicDropdown = tk.OptionMenu(window, topicVar, "Chemistry", "Physics")
topicDropdown.config(width=10)  # Increase the width of the dropdown
topicDropdown.pack()

# Create the "Check" button
checkButton = tk.Button(window, text="Check", command=check_selection, bg="#9ae6d8")
checkButton.pack(pady=10)  # Add vertical spacing

# Create the selection text label
selectionText = tk.StringVar()
selectionLabel = tk.Label(window, textvariable=selectionText, bg="#9ae6d8")
selectionLabel.pack()

# Create the buttons frame
buttonsFrame = tk.Frame(window, bg="#09B898")
buttonsFrame.pack(pady=10)

# Create the "Ask another question" button
askButton = tk.Button(buttonsFrame, text="Ask another question", bg="#9ae6d8")
askButton.pack(side="left", padx=5)

# Create the "Exit" button
exitButton = tk.Button(buttonsFrame, text="Exit", bg="#9ae6d8")
exitButton.pack(side="left", padx=5)

# Run the main event loop
window.mainloop()