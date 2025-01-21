import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import requests
import os
import csv
import json
from datetime import datetime
from fpdf import FPDF

# Configure appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

API_BASE_URL = "http://api.nsf.gov/services/v1/awards.json"

# Define tiered red flag words
RED_FLAG_WORDS = {
    "Tier 1 (Critical)": [  # Most "woke"
        "social justice", "systemic racism", "anti-racism", "white privilege",
        "decolonization", "intersectionality", "cultural appropriation",
        "radical inclusion", "anti-oppression", "equity lens"
    ],
    "Tier 2 (High)": [
        "diversity", "equity", "inclusion", "BIPOC", "LGBTQIA+",
        "marginalized communities", "gender equity", "racial justice",
        "microaggressions", "cultural humility"
    ],
    "Tier 3 (Moderate)": [
        "accessibility", "representation", "community engagement",
        "empowerment", "holistic approach", "disparity", "underserved",
        "neurodiversity", "safe space", "allyship"
    ],
    "Tier 4 (Common)": [  # Least concerning
        "innovative", "cutting-edge", "synergy", "leverage", "game-changing",
        "revolutionary", "disruptive", "paradigm", "unprecedented", "scalable",
        "framework", "sustainability", "impactful", "stakeholder", "inclusive"
    ]
}

class NSFAnalyzer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("NSF Awards Analyzer")
        self.root.geometry("1200x800")
        
        self.selected_words = {tier: [] for tier in RED_FLAG_WORDS.keys()}
        self.setup_gui()
        
    def setup_gui(self):
        # Main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel for controls
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="y", padx=5)
        
        # Year selection
        year_frame = ctk.CTkFrame(left_panel)
        year_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(year_frame, text="Select Year:").pack()
        years = [str(y) for y in range(2010, datetime.now().year + 1)]
        self.year_var = ctk.StringVar(value=str(datetime.now().year))
        year_menu = ctk.CTkOptionMenu(year_frame, values=years, variable=self.year_var)
        year_menu.pack(pady=5)
        
        # Red flag word selection
        word_frame = ctk.CTkFrame(left_panel)
        word_frame.pack(fill="both", expand=True, pady=5)
        
        ctk.CTkLabel(word_frame, text="Red Flag Categories").pack(pady=5)
        
        # Create scrollable frame for tiers
        scroll_frame = ctk.CTkScrollableFrame(word_frame)
        scroll_frame.pack(fill="both", expand=True)
        
        # Add checkboxes for each tier
        self.tier_vars = {}
        for tier, words in RED_FLAG_WORDS.items():
            tier_frame = ctk.CTkFrame(scroll_frame)
            tier_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(tier_frame, text=tier).pack()
            
            for word in words:
                var = ctk.BooleanVar()
                self.tier_vars[word] = var
                cb = ctk.CTkCheckBox(tier_frame, text=word, variable=var)
                cb.pack(anchor="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(left_panel)
        button_frame.pack(fill="x", pady=5)
        
        ctk.CTkButton(button_frame, text="Analyze", command=self.fetch_and_analyze).pack(fill="x", pady=2)
        ctk.CTkButton(button_frame, text="Generate Report", command=self.generate_report).pack(fill="x", pady=2)
        
        # Right panel for results
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=5)
        
        # Results list
        self.results_list = ctk.CTkTextbox(right_panel)
        self.results_list.pack(fill="both", expand=True)
        
    def fetch_awards(self, year):
        # Check for cached JSON file
        folder_name = f"awards_{year}"
        json_file_path = os.path.join(folder_name, f"{year}_awards.json")
        
        # Try to load cached data first
        if os.path.exists(json_file_path):
            try:
                self.results_list.insert(ctk.END, f"Found cached data for {year}...\n")
                self.root.update()
                
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    awards = json.load(f)
                    self.results_list.insert(ctk.END, f"Loaded {len(awards)} awards from cache.\n")
                    self.root.update()
                    return awards
            except Exception as e:
                self.results_list.insert(ctk.END, f"Error reading cached data: {str(e)}\n")
                self.root.update()
        
        # If no cache exists or cache read failed, fetch from API
        self.results_list.insert(ctk.END, "No cached data found. Fetching from NSF API...\n")
        self.root.update()
        
        awards = []
        offset = 1
        rpp = 25
        
        try:
            while True:
                params = {
                    "dateStart": f"01/01/{year}",
                    "dateEnd": f"12/31/{year}",
                    "rpp": rpp,
                    "offset": offset,
                    "printFields": "id,title,abstractText,awardeeName,fundsObligatedAmt"
                }
                
                response = requests.get(API_BASE_URL, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if not ("response" in data and "award" in data["response"]):
                    break
                    
                batch = data["response"]["award"]
                if not batch:
                    break
                    
                awards.extend(batch)
                offset += rpp
                
                self.results_list.insert(ctk.END, f"Fetched {len(awards)} awards...\n")
                self.results_list.see(ctk.END)
                self.root.update()
            
            # Cache the fetched data
            if awards:
                try:
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    
                    with open(json_file_path, 'w', encoding='utf-8') as f:
                        json.dump(awards, f, indent=2)
                    self.results_list.insert(ctk.END, f"Cached {len(awards)} awards for future use.\n")
                    self.root.update()
                except Exception as e:
                    self.results_list.insert(ctk.END, f"Warning: Could not cache data: {str(e)}\n")
                    self.root.update()
                
        except Exception as e:
            self.results_list.insert(ctk.END, f"Error fetching awards: {str(e)}\n")
            self.root.update()
            raise
        
        return awards
    
    def fetch_and_analyze(self):
        year = self.year_var.get()
        selected_words = {tier: [] for tier in RED_FLAG_WORDS.keys()}
        
        # Check if any words are selected
        any_selected = False
        for tier, words in RED_FLAG_WORDS.items():
            for word in words:
                if self.tier_vars[word].get():
                    selected_words[tier].append(word)
                    any_selected = True
        
        if not any_selected:
            messagebox.showwarning("Warning", "Please select at least one word to analyze.")
            return
        
        self.results_list.delete("1.0", ctk.END)
        self.results_list.insert(ctk.END, f"Analyzing awards for {year}...\n\n")
        self.root.update()  # Force GUI update
        
        try:
            # Show progress
            self.results_list.insert(ctk.END, "Fetching awards from NSF API...\n")
            self.root.update()
            awards = self.fetch_awards(year)
            
            if not awards:
                self.results_list.insert(ctk.END, "No awards found for selected year.\n")
                return
                
            self.results_list.insert(ctk.END, f"Analyzing {len(awards)} awards...\n")
            self.root.update()
            self.analyze_awards(awards, selected_words)
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Failed to connect to NSF API: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def analyze_awards(self, awards, selected_words):
        results = {tier: [] for tier in RED_FLAG_WORDS.keys()}
        
        for award in awards:
            abstract = award.get("abstractText", "").lower()
            
            for tier, words in selected_words.items():
                if any(word.lower() in abstract for word in words):
                    results[tier].append({
                        "id": award.get("id", ""),
                        "title": award.get("title", ""),
                        "awardee": award.get("awardeeName", ""),
                        "amount": float(award.get("fundsObligatedAmt", 0)),
                        "abstract": award.get("abstractText", ""),
                        "matched_words": [w for w in words if w.lower() in abstract]
                    })
        
        # Sort results by amount in descending order
        for tier in results:
            results[tier].sort(key=lambda x: x["amount"], reverse=True)
        
        self.display_results(results)
    
    def highlight_red_flags(self, text, matched_words):
        """Highlight red flag words in the abstract."""
        for word in matched_words:
            text = text.replace(word.lower(), f"**{word}**")  # Highlighting with asterisks
        return text
    
    def display_results(self, results):
        self.results_list.delete("1.0", ctk.END)
        
        for tier, awards in results.items():
            if awards:
                self.results_list.insert(ctk.END, f"\n{tier} Matches:\n")
                self.results_list.insert(ctk.END, "=" * 50 + "\n")
                
                total_funding = sum(award["amount"] for award in awards)
                self.results_list.insert(ctk.END, f"Total Funding: ${total_funding:,.2f}\n")
                self.results_list.insert(ctk.END, f"Number of Awards: {len(awards)}\n\n")
                
                for award in awards:
                    highlighted_abstract = self.highlight_red_flags(award['abstract'].lower(), award['matched_words'])
                    self.results_list.insert(ctk.END, f"Title: {award['title']}\n")
                    self.results_list.insert(ctk.END, f"Awardee: {award['awardee']}\n")
                    self.results_list.insert(ctk.END, f"Amount: ${award['amount']:,.2f}\n")
                    self.results_list.insert(ctk.END, f"Abstract: {highlighted_abstract}\n")
                    self.results_list.insert(ctk.END, f"Matched Words: {', '.join(award['matched_words'])}\n")
                    self.results_list.insert(ctk.END, "-" * 40 + "\n")
    
    def generate_report(self):
        report_text = self.results_list.get("1.0", ctk.END)
        if not report_text.strip():
            messagebox.showwarning("Warning", "No results to generate report from. Please analyze data first.")
            return
            
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "NSF Awards Analysis Report", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        
        # Split text into lines and add to PDF
        for line in report_text.split("\n"):
            # Encode the line to handle special characters
            line = line.encode('latin-1', 'replace').decode('latin-1')  # Replace unencodable characters
            pdf.multi_cell(0, 10, line)
        
        try:
            filename = f"nsf_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(filename)
            messagebox.showinfo("Success", f"Report saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NSFAnalyzer()
    app.run()