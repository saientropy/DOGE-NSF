import customtkinter as ctk  # pip install customtkinter
import pandas as pd
from tkinter import filedialog, ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from fpdf import FPDF  # pip install fpdf

# --------------------- CONFIGURE APPEARANCE & THEME --------------------- #
ctk.set_appearance_mode("System")   # "System", "Dark", or "Light"
ctk.set_default_color_theme("blue") # "blue", "green", "dark-blue"

# --------------------- RED-FLAG WORDS LIST --------------------- #
RED_FLAG_WORDS = [
    # --- Original sample set ---
    "innovative", "cutting-edge", "synergy", "leverage", "game-changing",
    "revolutionary", "disruptive", "paradigm", "unprecedented", "scalable",
    "diversity", "equity", "inclusion", "women", "underrepresented",
    "gender", "race", "social justice", "holistic", "empowerment",
    "framework", "sustainability", "impactful", "stakeholder", "inclusive",
    "transformation", "intersectionality", "accessible", "empirical",
    "methodology", "outreach", "collaboration", "potential", "scalability",
    "climate change", "AI-driven", "blockchain", "metaverse", "cryptocurrency",
    
    # --- Newly added DEI/social-justice terms ---
    "Equity",
    "Inclusion",
    "Diversity",
    "Intersectionality",
    "Social Justice",
    "Systemic Racism",
    "Anti-Racism",
    "Cultural Competency",
    "Microaggressions",
    "Implicit Bias",
    "White Privilege",
    "BIPOC",
    "LGBTQIA+",
    "Gender Non-Conforming",
    "Allyship",
    "Decolonization",
    "Restorative Justice",
    "Safe Space",
    "Trigger Warning",
    "Cultural Appropriation",
    "Marginalized Communities",
    "Underserved Populations",
    "Disparity",
    "Representation",
    "Accessibility",
    "Neurodiversity",
    "Empowerment",
    "Affirmative Action",
    "Equitable Access",
    "Inclusive Practices",
    "Cultural Humility",
    "Anti-Oppression",
    "Equity Lens",
    "Radical Inclusion",
    "Community Engagement",
    "Diversity Training",
    "Socioeconomic Disadvantage",
    "Gender Equity",
    "Racial Justice",
    "Holistic Approach"
]

# Global variable to store the DataFrame
data = None

# --------------------- FUNCTIONS --------------------- #
def filter_by_keywords(df, keywords):
    """Filter abstracts containing any of the specified keywords (case-insensitive)."""
    if not keywords:
        # If no keywords provided, just return original DataFrame and sum
        return df, df["estimatedTotalAmt"].sum()
    
    pattern = "|".join(keywords)
    filtered = df[df["abstractText"].str.contains(pattern, case=False, na=False)]
    total_funding = filtered["estimatedTotalAmt"].sum()
    return filtered, total_funding

def analyze_file(filepath):
    """Read CSV into a DataFrame, ensuring types are correct."""
    try:
        df = pd.read_csv(filepath)
        # Ensure columns exist; fill missing abstract text with empty strings
        df["abstractText"] = df.get("abstractText", "").fillna("").astype(str)
        # Convert funding column to float; fill missing with 0
        df["estimatedTotalAmt"] = df.get("estimatedTotalAmt", 0).fillna(0).astype(float)
        return df
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file: {e}")
        return None

def upload_file():
    """Handle file upload and display initial data if successful."""
    filepath = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")],
        title="Select a CSV File"
    )
    if not filepath:
        return
    
    global data
    data = analyze_file(filepath)
    if data is not None:
        # After loading new data, display everything or apply current filters
        display_data(data)
        update_display()  # Refresh display to apply any existing keywords

def update_display():
    """Update the data table based on entered keywords."""
    if data is None:
        return
    
    # Gather keywords from the entry
    keywords = keyword_entry.get().split(",")
    keywords = [k.strip() for k in keywords if k.strip()]
    
    filtered, total_funding = filter_by_keywords(data, keywords)
    display_data(filtered)
    total_label.configure(text=f"Total Funding: ${total_funding:,.2f}")

def add_keyword(word):
    """Add a red-flag word to the keyword entry and refresh display."""
    current_keywords = keyword_entry.get().strip()
    if current_keywords:
        updated = f"{current_keywords}, {word}"
    else:
        updated = word
    
    keyword_entry.delete(0, ctk.END)
    keyword_entry.insert(0, updated)
    update_display()

def display_data(filtered_df):
    """Populate the Treeview with the filtered DataFrame."""
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)
    
    # Insert new rows
    for _, row_data in filtered_df.iterrows():
        # Use str(...) for safety in case columns are missing
        tree.insert(
            "",
            "end",
            values=(
                str(row_data.get("id", "")),
                str(row_data.get("awardeeName", "")),
                str(row_data.get("title", "")),
                str(row_data.get("abstractText", "")),
                f"{row_data.get('estimatedTotalAmt', 0):,.2f}"
            )
        )

def show_full_abstract(event):
    """Open a new window to display the full abstract text on double-click."""
    selected_item = tree.selection()
    if not selected_item:
        return
    abstract = tree.item(selected_item)["values"][3]
    
    abstract_window = ctk.CTkToplevel(root)
    abstract_window.title("Full Abstract")
    abstract_window.geometry("800x600")
    
    scrolled_text = ScrolledText(abstract_window, wrap="word", font=("Arial", 12))
    scrolled_text.pack(expand=True, fill="both")
    scrolled_text.insert(ctk.END, abstract)
    scrolled_text.config(state="disabled")

def generate_report():
    """
    Generate a PDF report of the top 10 most-funded abstracts 
    based on the currently filtered data.
    """
    if data is None:
        messagebox.showinfo("No Data", "Please upload and filter data first.")
        return
    
    # Gather current filter keywords
    keywords = keyword_entry.get().split(",")
    keywords = [k.strip() for k in keywords if k.strip()]
    filtered, _ = filter_by_keywords(data, keywords)
    
    if filtered.empty:
        messagebox.showinfo("No Data", "No records match the current filter.")
        return
    
    # Sort by 'estimatedTotalAmt' descending and get top 10
    top_10 = filtered.nlargest(10, "estimatedTotalAmt")

    # Prompt user to save the PDF
    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF file", "*.pdf")],
        title="Save Report as PDF"
    )
    if not save_path:
        return  # User canceled saving
    
    # --------------------- Generate PDF with FPDF --------------------- #
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Title
    pdf.cell(0, 10, "Top 10 Most-Funded Projects Report", ln=True, align="C")
    pdf.ln(10)  # extra space
    
    # Table headers
    pdf.set_font("Arial", "B", 12)
    pdf.cell(20, 10, "Rank", border=1)
    pdf.cell(50, 10, "Awardee", border=1)
    pdf.cell(40, 10, "Funding", border=1)
    pdf.cell(80, 10, "Title", border=1, ln=True)
    
    # Table rows
    pdf.set_font("Arial", "", 12)
    rank = 1
    for _, row_data in top_10.iterrows():
        awardee = str(row_data.get("awardeeName", "")[:20])  # truncated
        title = str(row_data.get("title", "")[:30])          # truncated
        funding_str = f"${row_data.get('estimatedTotalAmt', 0):,.2f}"
        
        pdf.cell(20, 10, str(rank), border=1)
        pdf.cell(50, 10, awardee, border=1)
        pdf.cell(40, 10, funding_str, border=1)
        pdf.cell(80, 10, title, border=1, ln=True)
        rank += 1
    
    # Add second page for full abstracts
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Full Abstracts", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    rank = 1
    for _, row_data in top_10.iterrows():
        pdf.multi_cell(0, 10, f"#{rank} - {row_data.get('title', '')}")
        pdf.multi_cell(0, 10, f"Awardee: {row_data.get('awardeeName', '')}")
        pdf.multi_cell(0, 10, f"Funding: ${row_data.get('estimatedTotalAmt', 0):,.2f}")
        pdf.multi_cell(0, 10, f"Abstract:\n{row_data.get('abstractText', '')}")
        pdf.ln(5)  # space between entries
        rank += 1
    
    # Save PDF
    pdf.output(save_path)
    messagebox.showinfo("Success", f"Report generated and saved:\n{save_path}")

# --------------------- CREATE THE MAIN UI --------------------- #
root = ctk.CTk()
root.title("Project Red Flag Analyzer (Modern UI)")
root.geometry("1400x900")

# ----- Top Frame: Upload & Keywords ----- #
frame_top = ctk.CTkFrame(root)
frame_top.pack(pady=10, fill="x", padx=10)

upload_button = ctk.CTkButton(frame_top, text="Upload CSV", command=upload_file, width=120)
upload_button.pack(side="left", padx=10)

keyword_label = ctk.CTkLabel(frame_top, text="Enter Keywords (comma-separated):")
keyword_label.pack(side="left", padx=10)

keyword_entry = ctk.CTkEntry(frame_top, width=400, placeholder_text="e.g. synergy, disruptive")
keyword_entry.pack(side="left", padx=10)

keyword_button = ctk.CTkButton(frame_top, text="Apply Filters", command=update_display, width=120)
keyword_button.pack(side="left", padx=10)

# ----- Funding Total Label ----- #
total_label = ctk.CTkLabel(root, text="Total Funding: $0.00", font=("Arial", 14))
total_label.pack(pady=10)

# ----- Red-Flag Words Buttons ----- #
frame_buttons = ctk.CTkFrame(root)
frame_buttons.pack(pady=10, fill="x", padx=10)

red_flag_label = ctk.CTkLabel(frame_buttons, text="Quick-Add Red-Flag Words:")
red_flag_label.pack(anchor="w", pady=(0, 5))

button_container = ctk.CTkFrame(frame_buttons)
button_container.pack(pady=5, fill="x")

# Display red-flag words in a grid (5 columns)
cols = 5
for idx, word in enumerate(RED_FLAG_WORDS):
    btn = ctk.CTkButton(button_container, text=word, command=lambda w=word: add_keyword(w), width=120)
    row = idx // cols
    col = idx % cols
    btn.grid(row=row, column=col, padx=5, pady=5)

# ----- Table for Results ----- #
tree_columns = ("ID", "Awardee Name", "Title", "Abstract", "Funding Amount")
tree = ttk.Treeview(root, columns=tree_columns, show="headings", height=20)

for col in tree_columns:
    tree.heading(col, text=col)
    if col == "Abstract":
        tree.column(col, width=500)
    else:
        tree.column(col, width=150)

tree.pack(pady=10, fill="both", expand=True)
tree.bind("<Double-1>", show_full_abstract)

# ----- Generate Report Button ----- #
report_button = ctk.CTkButton(root, text="Generate Report", command=generate_report, width=200)
report_button.pack(pady=10)

# ----- Start the GUI Main Loop ----- #
root.mainloop()
