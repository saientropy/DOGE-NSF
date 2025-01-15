import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter.scrolledtext import ScrolledText

# Predefined list of red-flag words
RED_FLAG_WORDS = [
    "innovative", "cutting-edge", "synergy", "leverage", "game-changing",
    "revolutionary", "disruptive", "paradigm", "unprecedented", "scalable",
    "diversity", "equity", "inclusion", "women", "underrepresented",
    "gender", "race", "social justice", "holistic", "empowerment",
    "framework", "sustainability", "impactful", "stakeholder", "inclusive",
    "transformation", "intersectionality", "accessible", "empirical",
    "methodology", "outreach", "collaboration", "potential", "scalability"
]

# Function to filter abstracts by keywords
def filter_by_keywords(data, keywords):
    filtered_data = data[data["abstractText"].str.contains("|".join(keywords), case=False, na=False)]
    total_funding = filtered_data["estimatedTotalAmt"].sum()
    return filtered_data, total_funding

# Function to analyze the file
def analyze_file(filepath):
    try:
        data = pd.read_csv(filepath)
        data["abstractText"] = data["abstractText"].fillna("").astype(str)
        data["estimatedTotalAmt"] = data["estimatedTotalAmt"].fillna(0).astype(float)
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file: {e}")
        return None

# Function to handle file upload
def upload_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")], title="Select a CSV File"
    )
    if not filepath:
        return
    
    global data
    data = analyze_file(filepath)
    if data is not None:
        display_data(data)

# Function to update display dynamically
def update_display():
    keywords = keyword_entry.get().split(",")
    keywords = [k.strip() for k in keywords if k.strip()]
    filtered_data, total_funding = filter_by_keywords(data, keywords)
    display_data(filtered_data)
    total_label.config(text=f"Total Funding: ${total_funding:,.2f}")

# Function to handle red-flag button clicks
def add_keyword(word):
    current_keywords = keyword_entry.get()
    updated_keywords = f"{current_keywords}, {word}" if current_keywords else word
    keyword_entry.delete(0, tk.END)
    keyword_entry.insert(0, updated_keywords)
    update_display()

# Function to display data in the table
def display_data(filtered_data):
    for row in tree.get_children():
        tree.delete(row)
    for _, row in filtered_data.iterrows():
        tree.insert(
            "", "end", 
            values=(row["id"], row["awardeeName"], row["title"], row["abstractText"], row["estimatedTotalAmt"])
        )

# Function to display the full abstract in a new window
def show_full_abstract(event):
    selected_item = tree.selection()
    if not selected_item:
        return
    abstract = tree.item(selected_item)["values"][3]
    abstract_window = tk.Toplevel(root)
    abstract_window.title("Full Abstract")
    abstract_window.geometry("800x600")
    scrolled_text = ScrolledText(abstract_window, wrap=tk.WORD, font=("Arial", 12))
    scrolled_text.insert(tk.END, abstract)
    scrolled_text.pack(expand=True, fill="both")
    scrolled_text.config(state=tk.DISABLED)

# Create the GUI
root = tk.Tk()
root.title("Project Red Flag Analyzer")
root.geometry("1400x900")

# File Upload Section
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

upload_button = tk.Button(frame_top, text="Upload CSV", command=upload_file, width=20)
upload_button.pack(side="left", padx=10)

keyword_label = tk.Label(frame_top, text="Enter Keywords (comma-separated):")
keyword_label.pack(side="left", padx=10)

keyword_entry = tk.Entry(frame_top, width=50)
keyword_entry.pack(side="left", padx=10)

keyword_button = tk.Button(frame_top, text="Apply Filters", command=update_display, width=15)
keyword_button.pack(side="left", padx=10)

# Total Funding Display
total_label = tk.Label(root, text="Total Funding: $0.00", font=("Arial", 14))
total_label.pack(pady=10)

# Red-Flag Buttons Section
frame_buttons = tk.LabelFrame(root, text="Red-Flag Words", padx=10, pady=10)
frame_buttons.pack(pady=10)

for idx, word in enumerate(RED_FLAG_WORDS):
    button = tk.Button(frame_buttons, text=word, command=lambda w=word: add_keyword(w), width=15)
    button.grid(row=idx // 5, column=idx % 5, padx=5, pady=5)

# Table for Displaying Results
columns = ("ID", "Awardee Name", "Title", "Abstract", "Funding Amount")
tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200 if col != "Abstract" else 400)
tree.pack(pady=20, fill="both", expand=True)
tree.bind("<Double-1>", show_full_abstract)

# Start the GUI
root.mainloop()
