import tkinter as tk

def check_selection():
    language = languageVar.get()
    topic = topicVar.get()
    selectionText.set(f"Selected language: {language}\nSelected topic: {topic}")

# Create the main window
window = tk.Tk()
window.title("Study-Bot")
window.geometry("450x470")

# Set the background color
window.configure(bg="#09B898")

# Create the title label
titleLabel = tk.Label(window, text="Study-Bot", font=("Leelawadee", 24, "bold"), bg="#9ae6d8")
titleLabel.pack(pady=15)

# Create the language dropdown
languageLabel = tk.Label(window, text="Select Language:", bg="#9ae6d8", font=("Leelawadee", 12))
languageLabel.pack(pady=15)
languageVar = tk.StringVar(window)
languageDropdown = tk.OptionMenu(window, languageVar, "English", "Spanish")
languageDropdown.config(width=15)
languageDropdown.pack()

# Create the topic dropdown
topicLabel = tk.Label(window, text="Select Topic:", bg="#9ae6d8", font=("Leelawadee", 12))
topicLabel.pack(pady=15)
topicVar = tk.StringVar(window)
topicDropdown = tk.OptionMenu(window, topicVar, "Chemistry", "Physics")
topicDropdown.config(width=15)
topicDropdown.pack()

# Create the "Check" button
checkButton = tk.Button(window, text="Check", command=check_selection, bg="#9ae6d8", font=("Leelawadee", 12))
checkButton.pack(pady=15)

# Create the selection text label
selectionText = tk.StringVar()
selectionLabel = tk.Label(window, textvariable=selectionText, bg="#9ae6d8", font=("Leelawadee", 12))
selectionLabel.pack()

# Create the buttons frame
buttonsFrame = tk.Frame(window, bg="#09B898")
buttonsFrame.pack(pady=15)

# Create the "Ask another question" button
askButton = tk.Button(buttonsFrame, text="Ask another question", bg="#9ae6d8", font=("Leelawadee", 12))
askButton.pack(side="left", padx=10)

# Create the "Exit" button
exitButton = tk.Button(buttonsFrame, text="Exit", bg="#9ae6d8", font=("Nunito", 12))
exitButton.pack(side="left", padx=10)

# Run the main event loop
window.mainloop()
