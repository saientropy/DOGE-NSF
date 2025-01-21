import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from fpdf import FPDF

# --------------------- Configure Appearance & Theme --------------------- #
ctk.set_appearance_mode("System")   # "System", "Dark", or "Light"
ctk.set_default_color_theme("blue") # "blue", "green", "dark-blue"

# --------------------- Tiered Red-Flag Words --------------------- #
RED_FLAG_TIERS = {
    "Tier 1 (Most Woke)": [
        "Systemic Racism", "White Privilege", "Anti-Racism",
        "Implicit Bias", "Microaggressions", "BIPOC", "LGBTQ+",
        "Gender Non-Conforming", "Trigger Warning", "Safe Space",
        "Cultural Appropriation", "Radical Inclusion", "Allyship",
        "Anti-Oppression", "Equity Lens", "Restorative Justice",
        "Decolonization", "Cultural Humility"
    ],
    "Tier 2": [
        "Intersectionality", "Social Justice", "Marginalized Communities",
        "Socioeconomic Disadvantage", "Racial Justice", "Community Engagement",
        "Diversity Training"
    ],
    "Tier 3": [
        "Diversity", "Equity", "Inclusion", "Holistic Approach",
        "Representation", "Accessibility", "Neurodiversity",
        "Gender Equity", "Affirmative Action"
    ],
    "Tier 4 (Least Woke)": [
        "Innovative", "Cutting-edge", "Synergy", "Leverage",
        "Revolutionary", "Disruptive", "AI-driven",
        "Blockchain", "Cryptocurrency", "Paradigm"
    ]
}

# Merged list of ALL words (for internal searching if needed)
ALL_WORDS = []
for tier in RED_FLAG_TIERS.values():
    ALL_WORDS.extend(tier)

# Global variables
data = None        # Will hold the main DataFrame
rows_frame = None  # The frame to hold the scrollable list of rows

# --------------------- Functions --------------------- #

def analyze_file(filepath):
    """Read CSV into a DataFrame with expected columns."""
    try:
        df = pd.read_csv(filepath)
        df["abstractText"] = df.get("abstractText", "").fillna("").astype(str)
        df["estimatedTotalAmt"] = df.get("estimatedTotalAmt", 0).fillna(0).astype(float)
        return df
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file:\n{e}")
        return None

def upload_file():
    """Prompt user to select a CSV file, load and display initial data."""
    global data
    filepath = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")],
        title="Select a CSV File"
    )
    if not filepath:
        return
    
    df = analyze_file(filepath)
    if df is not None:
        data = df
        update_display()  # Refresh view with current (possibly empty) keywords

def filter_by_keywords(df, keywords):
    """
    Return a tuple (filtered_dataframe, sum_of_funding)
    by searching 'abstractText' for any of the given keywords (case-insensitive).
    """
    if not keywords:
        # If no keywords, return entire dataset
        return df, df["estimatedTotalAmt"].sum()

    pattern = "|".join(keywords)
    filtered = df[df["abstractText"].str.contains(pattern, case=False, na=False)]
    total_funding = filtered["estimatedTotalAmt"].sum()
    return filtered, total_funding

def update_display():
    """Filter data by user-entered keywords and display results in the scrollable list."""
    if data is None:
        return
    
    # Gather keywords from entry
    keywords = keyword_entry.get().split(",")
    keywords = [k.strip() for k in keywords if k.strip()]

    filtered_df, total_funding = filter_by_keywords(data, keywords)
    total_label.configure(text=f"Total Funding: ${total_funding:,.2f}")
    
    display_data_in_list(filtered_df)

def add_keyword(word):
    """Append a single red-flag word to the keyword entry and refresh display."""
    current = keyword_entry.get().strip()
    if current:
        updated = f"{current}, {word}"
    else:
        updated = word
    
    keyword_entry.delete(0, ctk.END)
    keyword_entry.insert(0, updated)
    update_display()

def display_data_in_list(filtered_df):
    """
    Display each row of 'filtered_df' as a clickable item in a scrollable frame.
    Each item includes minimal info + a 'View Abstract' button.
    """
    # Clear previous items in rows_frame
    for child in rows_frame.winfo_children():
        child.destroy()

    if filtered_df.empty:
        # Optional: display a 'no data' message
        no_data_label = ctk.CTkLabel(rows_frame, text="No results found.")
        no_data_label.pack(pady=10)
        return

    # Create a frame/item for each row
    for idx, row_data in filtered_df.iterrows():
        item_frame = ctk.CTkFrame(rows_frame)
        item_frame.pack(fill="x", pady=5, padx=5)

        # Show minimal info: Title, Awardee, Funding
        title_label = ctk.CTkLabel(
            item_frame, 
            text=f"Title: {row_data.get('title', '')}", 
            font=("Arial", 14, "bold")
        )
        title_label.pack(anchor="w", padx=5)

        awardee_label = ctk.CTkLabel(
            item_frame, 
            text=f"Awardee: {row_data.get('awardeeName', '')}", 
            font=("Arial", 12)
        )
        awardee_label.pack(anchor="w", padx=5)

        funding_label = ctk.CTkLabel(
            item_frame, 
            text=f"Funding: ${row_data.get('estimatedTotalAmt', 0):,.2f}", 
            font=("Arial", 12, "italic")
        )
        funding_label.pack(anchor="w", padx=5)

        # View Abstract button
        abstract_text = row_data.get("abstractText", "")
        view_btn = ctk.CTkButton(
            item_frame, 
            text="View Abstract", 
            command=lambda txt=abstract_text: show_full_abstract(txt)
        )
        view_btn.pack(anchor="e", padx=5, pady=(5, 0))

        # Optional separator
        separator = ctk.CTkLabel(item_frame, text="-" * 80)
        separator.pack(fill="x", pady=5)

def show_full_abstract(abstract):
    """
    Opens a new window with a scrollable text widget containing the full abstract.
    """
    abstract_window = ctk.CTkToplevel(root)
    abstract_window.title("Full Abstract")
    abstract_window.geometry("800x600")

    scrolled_text = ScrolledText(abstract_window, wrap="word", font=("Arial", 12))
    scrolled_text.pack(expand=True, fill="both")
    scrolled_text.insert("end", abstract)
    scrolled_text.config(state="disabled")

def generate_report():
    """
    Generate a PDF report of the top 10 most-funded items from the current filter.
    """
    if data is None:
        messagebox.showinfo("No Data", "Please upload and filter data first.")
        return

    # Get current keywords
    keywords = keyword_entry.get().split(",")
    keywords = [k.strip() for k in keywords if k.strip()]
    filtered_df, _ = filter_by_keywords(data, keywords)

    if filtered_df.empty:
        messagebox.showinfo("No Data", "No records match the current filter.")
        return

    # Sort by funding descending, take top 10
    top_10 = filtered_df.nlargest(10, "estimatedTotalAmt")

    # Prompt user to save PDF
    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF file", "*.pdf")],
        title="Save Report as PDF"
    )
    if not save_path:
        return  # user canceled

    # Create PDF with FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    pdf.cell(0, 10, "Top 10 Most-Funded Projects Report", ln=True, align="C")
    pdf.ln(5)

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
        pdf.cell(20, 10, str(rank), border=1)
        awardee = str(row_data.get("awardeeName", "")[:20])
        pdf.cell(50, 10, awardee, border=1)
        funding_str = f"${row_data.get('estimatedTotalAmt', 0):,.2f}"
        pdf.cell(40, 10, funding_str, border=1)
        title_str = str(row_data.get("title", "")[:30])
        pdf.cell(80, 10, title_str, border=1, ln=True)
        rank += 1

    # Second page for full abstracts
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Full Abstracts", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    rank = 1
    for _, row_data in top_10.iterrows():
        pdf.multi_cell(0, 10, f"{rank}. {row_data.get('title', '')}")
        pdf.multi_cell(0, 10, f"Awardee: {row_data.get('awardeeName', '')}")
        pdf.multi_cell(0, 10, f"Funding: ${row_data.get('estimatedTotalAmt', 0):,.2f}")
        pdf.multi_cell(0, 10, f"Abstract:\n{row_data.get('abstractText', '')}")
        pdf.ln(5)
        rank += 1
    
    pdf.output(save_path)
    messagebox.showinfo("Report Generated", f"Report saved:\n{save_path}")

# --------------------- Create the Main UI --------------------- #
root = ctk.CTk()
root.title("NSF Grant Scam Detector (Beta)")
root.geometry("1200x800")

# Top frame: Upload & Keywords
frame_top = ctk.CTkFrame(root)
frame_top.pack(pady=10, fill="x", padx=10)

upload_button = ctk.CTkButton(frame_top, text="Upload CSV", command=upload_file, width=120)
upload_button.pack(side="left", padx=10)

keyword_label = ctk.CTkLabel(frame_top, text="Keywords (comma-separated):")
keyword_label.pack(side="left", padx=5)

keyword_entry = ctk.CTkEntry(frame_top, width=300, placeholder_text="e.g. synergy, disruptive")
keyword_entry.pack(side="left", padx=5)

apply_button = ctk.CTkButton(frame_top, text="Apply Filters", command=update_display, width=120)
apply_button.pack(side="left", padx=10)

# Show total funding
total_label = ctk.CTkLabel(root, text="Total Funding: $0.00", font=("Arial", 14))
total_label.pack(pady=10)

# Red-Flag Word Buttons by Tier
tiers_frame = ctk.CTkFrame(root)
tiers_frame.pack(pady=10, fill="x", padx=10)

for tier_name, words_list in RED_FLAG_TIERS.items():
    tier_label = ctk.CTkLabel(tiers_frame, text=tier_name + ":", font=("Arial", 13, "bold"))
    tier_label.pack(anchor="w", pady=(10,5))

    # Container for that tier's buttons
    tier_btn_container = ctk.CTkFrame(tiers_frame)
    tier_btn_container.pack(anchor="w", padx=10)
    
    # Decide how many columns you want for each tier
    col_count = 4
    for idx, w in enumerate(words_list):
        btn = ctk.CTkButton(
            tier_btn_container, 
            text=w, 
            command=lambda word=w: add_keyword(word), 
            width=150
        )
        r = idx // col_count
        c = idx % col_count
        btn.grid(row=r, column=c, padx=5, pady=5)

# Scrollable frame for data rows
scroll_frame = ctk.CTkScrollableFrame(root, width=1100, height=400)
scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

rows_frame = scroll_frame  # We'll place each row directly in scroll_frame

# Report button
report_button = ctk.CTkButton(root, text="Generate Report", command=generate_report, width=180)
report_button.pack(pady=10)

root.mainloop()
