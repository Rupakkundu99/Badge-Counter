import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from badge_counter import setup_driver, get_badge_count

def update_google_sheet(sheet_name: str):
    """
    Main function to read URLs, scrape badge counts, and update the Google Sheet.
    """
    print("Authenticating with Google Sheets...")
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    print(f"Opening spreadsheet '{sheet_name}'...")
    sheet = client.open(sheet_name).sheet1
    data = pd.DataFrame(sheet.get_all_records())

    if "Profile URL" not in data.columns:
        print("Error: Sheet must have a 'Profile URL' column.")
        return

    print("Setting up browser for scraping...")
    driver = setup_driver()
    
    print(f"Found {len(data)} profiles to check.")
    badge_counts = []

    for index, row in data.iterrows():
        url = row["Profile URL"]
        if not url or not url.startswith("http"): # Skip empty or invalid rows
            badge_counts.append("")
            continue
        
        print(f"Processing profile for: {row.get('Name', 'Unknown')}...")
        
        # For each URL, the count is found by counting the elements.
        count = get_badge_count(driver, url)
        badge_counts.append(count)
        
    driver.quit() # Close the browser instance

    data["Badge Count"] = badge_counts
    
    print("Updating Google Sheet with new badge counts...")
    # Update the entire sheet at once
    sheet.update([data.columns.values.tolist()] + data.values.tolist())
    print("Update complete!")

# --- Main execution block ---
if __name__ == "__main__":
    # Make sure this name exactly matches your Google Sheet file name
    SPREADSHEET_NAME = "Jam Tracker"
    update_google_sheet(SPREADSHEET_NAME)