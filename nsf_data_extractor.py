import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import os
import csv
import json
from datetime import datetime

API_BASE_URL = "http://api.nsf.gov/services/v1/awards.json"

def fetch_awards_for_year(year, status_text):
    """
    Fetch all award data for a given year using the NSF API,
    paginate through results, and save CSV and JSON.
    """
    # --- Debugging & Progress ---
    status_text.insert(tk.END, f"\n[INFO] Starting data fetch for year {year}\n")
    status_text.see(tk.END)
    
    # Build folder name
    folder_name = f"awards_{year}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        status_text.insert(tk.END, f"[DEBUG] Created folder: {folder_name}\n")
    else:
        status_text.insert(tk.END, f"[DEBUG] Folder already exists: {folder_name}\n")
    status_text.see(tk.END)
    
    # Output file paths
    csv_file_path = os.path.join(folder_name, f"{year}_awards.csv")
    json_file_path = os.path.join(folder_name, f"{year}_awards.json")
    
    # Prepare CSV
    # Include the fields you requested plus our original fields
    csv_headers = [
        "id", "agency", "awardeeName", "title", "abstractText",
        "fundsObligatedAmt",       # (1)
        "estimatedTotalAmt",       # (2)
        "pdPIName",                # (5)
        "coPDPI",                  # (6)
        "poName",                  # (7)
        "startDate",               # (9)
        "expDate",                 # (10)
        "primaryProgram"           # (11)
    ]
    csv_file = open(csv_file_path, mode="w", newline="", encoding="utf-8")
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    csv_writer.writeheader()
    
    # Prepare JSON aggregator
    all_awards_json = []
    
    # Date range for that year
    date_start = f"01/01/{year}"
    date_end = f"12/31/{year}"
    
    # NSF only returns 25 items per page, so we must loop
    offset = 1
    rpp = 25
    
    total_records_fetched = 0
    
    while True:
        # Prepare query params, including the new fields in printFields
        params = {
            "dateStart": date_start,      # Award Date Start
            "dateEnd": date_end,          # Award Date End
            "rpp": rpp,
            "offset": offset,
            "printFields": (
                "id,agency,awardeeName,title,abstractText,"
                "fundsObligatedAmt,estimatedTotalAmt,pdPIName,"
                "coPDPI,poName,startDate,expDate,primaryProgram"
            )
        }
        
        # --- Debugging & Progress ---
        status_text.insert(tk.END, f"[DEBUG] Fetching records {offset} to {offset + rpp - 1}...\n")
        status_text.see(tk.END)
        
        try:
            response = requests.get(API_BASE_URL, params=params, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            status_text.insert(tk.END, f"[ERROR] Request failed for year {year}: {e}\n")
            status_text.see(tk.END)
            break
        
        data = response.json()
        
        # Check if 'response' and 'award' exist in the returned data
        if ("response" in data) and ("award" in data["response"]):
            awards = data["response"]["award"]
            if not awards:
                # No more awards to fetch, break out of loop
                status_text.insert(tk.END, f"[INFO] No more awards found for offset={offset}. Stopping.\n")
                status_text.see(tk.END)
                break
            
            # Write awards to CSV and also aggregate to JSON
            for award in awards:
                row_data = {
                    "id": award.get("id", ""),
                    "agency": award.get("agency", ""),
                    "awardeeName": award.get("awardeeName", ""),
                    "title": award.get("title", ""),
                    "abstractText": award.get("abstractText", ""),
                    "fundsObligatedAmt": award.get("fundsObligatedAmt", ""),
                    "estimatedTotalAmt": award.get("estimatedTotalAmt", ""),
                    "pdPIName": award.get("pdPIName", ""),
                    "coPDPI": award.get("coPDPI", ""),
                    "poName": award.get("poName", ""),
                    "startDate": award.get("startDate", ""),
                    "expDate": award.get("expDate", ""),
                    "primaryProgram": award.get("primaryProgram", "")
                }
                csv_writer.writerow(row_data)
                all_awards_json.append(row_data)
            
            fetched_count = len(awards)
            total_records_fetched += fetched_count
            
            # --- Debugging & Progress ---
            status_text.insert(tk.END, f"[INFO] Fetched {fetched_count} records in this batch. (Total so far: {total_records_fetched})\n")
            status_text.see(tk.END)
            
            # Increment offset
            offset += rpp
        else:
            # Possibly an error or no 'award' key found
            status_text.insert(tk.END, "[WARN] No award data found in response. Possibly done or invalid params.\n")
            status_text.see(tk.END)
            break
    
    # Close CSV file
    csv_file.close()
    
    # Write JSON file
    with open(json_file_path, "w", encoding="utf-8") as jf:
        json.dump(all_awards_json, jf, indent=2)
    
    # Check for empty files
    if total_records_fetched == 0:
        status_text.insert(tk.END, f"[WARN] No records downloaded for year {year}. CSV and JSON might be empty.\n")
    else:
        status_text.insert(tk.END, f"[INFO] Finished fetching {total_records_fetched} records for year {year}.\n")
        status_text.insert(tk.END, f"[INFO] Data saved to:\n     {csv_file_path}\n     {json_file_path}\n")
    status_text.see(tk.END)

def on_download_click(year_vars, status_text):
    """
    Callback for the "Download" button. Gathers selected years,
    and calls fetch_awards_for_year() for each selected year.
    """
    selected_years = []
    for y_var in year_vars:
        if year_vars[y_var].get() == 1:
            selected_years.append(y_var)
    
    if not selected_years:
        messagebox.showwarning("No Years Selected", "Please select at least one year to download data.")
        return
    
    status_text.insert(tk.END, "[INFO] Starting download process...\n")
    status_text.see(tk.END)
    
    for year in selected_years:
        fetch_awards_for_year(year, status_text)
    
    status_text.insert(tk.END, "\n[INFO] All selected years processed.\n")
    status_text.see(tk.END)

def create_gui():
    """
    Create a Tkinter GUI that allows the user to select multiple years
    and then download NSF award data for each selected year.
    """
    root = tk.Tk()
    root.title("NSF Awards Downloader")
    
    # Frame to hold checkboxes
    frame_checkboxes = tk.Frame(root)
    frame_checkboxes.pack(padx=10, pady=5, fill=tk.X)
    
    # For demonstration, let's say we offer a range of years
    # You can expand or customize as you like
    possible_years = list(range(2010, datetime.now().year + 1))
    
    # Dictionary to map {year: tk.IntVar()}
    year_vars = {}
    
    # Create checkboxes for each year
    row_count = 0
    col_count = 0
    for y in possible_years:
        if col_count == 10:  # wrap after some columns
            row_count += 1
            col_count = 0
        var = tk.IntVar()
        chk = tk.Checkbutton(frame_checkboxes, text=str(y), variable=var)
        chk.grid(row=row_count, column=col_count, sticky="w")
        year_vars[y] = var
        col_count += 1
    
    # Frame for buttons
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(padx=10, pady=5, fill=tk.X)
    
    btn_download = tk.Button(frame_buttons, text="Download", command=lambda: on_download_click(year_vars, text_log))
    btn_download.pack(side=tk.LEFT, padx=5)
    
    # Scrolled Text for status / debugging logs
    text_log = scrolledtext.ScrolledText(root, width=100, height=20)
    text_log.pack(padx=10, pady=5)
    
    # Start Tk main loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
