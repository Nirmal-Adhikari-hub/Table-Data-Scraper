import requests
import pandas as pd
from bs4 import BeautifulSoup

# List of all state codes
state_codes = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

records_per_page = 20  # Number of records per page

# Create a list to store all extracted data
all_extracted_data = []

# Loop through all state codes
for state_code in state_codes:
    # Loop through pages until no more records are found
    page_number = 1
    while True:
        start_row = (page_number - 1) * records_per_page + 1
        end_row = page_number * records_per_page

        url = f"https://www.apma.org/Directory/FindAPodiatrist.cfm?Compact=0&FirstName=&LastName=&City=&State={state_code}&Zip=&Country=United+States&startrow={start_row}&endrow={end_row}"

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table containing the podiatrist records
        table = soup.find("table")

        # Find all rows in the table
        rows = table.find_all("tr")

        # If no more records found, break the loop
        if len(rows) <= 1:
            break

        # Loop through rows starting from the second row (index 1)
        for row in rows[1:]:
            # Find the first cell (column) in the row
            first_cell = row.find("td")
            if first_cell:
                # Extract name from the <strong> tag
                strong_tag = first_cell.find("strong")
                name = strong_tag.get_text(strip=True).replace('\n', ' ') if strong_tag else ""

                # Extract remaining content as address, excluding <a> tags
                address_parts = [part.get_text(strip=True).replace('\n', ' ') for part in first_cell.contents if part != strong_tag and part.name != "a"]
                address = " ".join(address_parts)

                # Append name and address to the list
                all_extracted_data.append({"Name": name, "Address": address})

        # Move to the next page
        page_number += 1
    print("Finished extracting data for", state_code)

# Convert extracted data to a pandas DataFrame
df = pd.DataFrame(all_extracted_data)

# Save DataFrame to a CSV file
csv_file = "podiatrists.csv"
df.to_csv(csv_file, index=False)

print("Data saved to podiatrists.csv")
