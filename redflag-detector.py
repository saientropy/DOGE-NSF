import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# Function to evaluate abstracts for red flags
def evaluate_abstract(abstract):
    red_flags = []
    buzzwords = [
        "innovative", "cutting-edge", "synergy", "leverage", "game-changing",
        "revolutionary", "disruptive", "paradigm", "unprecedented", "scalable",
        "diversity", "equity", "inclusion", "women", "underrepresented",
        "gender", "race", "social justice"
    ]
    vague_phrases = [
        "will attempt to", "aims to explore", "focuses on understanding",
        "intends to investigate", "could potentially"
    ]
    
    if any(word in abstract.lower() for word in buzzwords):
        red_flags.append("DEI-related or buzzword-heavy language detected.")
    if any(phrase in abstract.lower() for phrase in vague_phrases):
        red_flags.append("Vague language indicating lack of clear goals.")
    if "solve" in abstract.lower() or "completely" in abstract.lower():
        red_flags.append("Overly ambitious claims detected.")
    if len(abstract.split()) < 50:
        red_flags.append("Abstract is too short to be meaningful.")
    
    return red_flags if red_flags else ["No obvious red flags."]

# Function to analyze the uploaded CSV
def analyze_file(filepath):
    try:
        data = pd.read_csv(filepath)
        data["abstractText"] = data["abstractText"].fillna("").astype(str)
        data["red_flags"] = data["abstractText"].apply(evaluate_abstract)
        flagged_projects = data[data["red_flags"].str.len() > 0]
        total_funding = flagged_projects["estimatedTotalAmt"].sum()
        
        return data, total_funding
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file: {e}")
        return None, 0

# Function to open a file and display results
def upload_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")], title="Select a CSV File"
    )
    if not filepath:
        return
    
    data, total_funding = analyze_file(filepath)
    if data is not None:
        update_table(data)
        messagebox.showinfo(
            "Analysis Complete", f"Total Funding for Flagged Projects: ${total_funding:,.2f}"
        )

# Function to update the table with results
def update_table(data):
    for row in tree.get_children():
        tree.delete(row)
    for _, row in data.iterrows():
        tree.insert(
            "", "end", 
            values=(row["id"], row["awardeeName"], row["title"], ", ".join(row["red_flags"]), row["estimatedTotalAmt"])
        )

# Create the GUI
root = tk.Tk()
root.title("Red Flag Analyzer for Projects")

frame = tk.Frame(root)
frame.pack(pady=20)

# Upload Button
upload_button = tk.Button(frame, text="Upload CSV", command=upload_file)
upload_button.pack(pady=10)

# Table to display results
columns = ("ID", "Awardee Name", "Title", "Red Flags", "Funding Amount")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)
tree.pack(pady=10)

# Start the GUI
root.mainloop()
