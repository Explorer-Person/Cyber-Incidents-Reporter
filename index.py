from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

def login_with_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Open login page
        page.goto("https://www.csidb.net/accounts/login/")

        # Target the specific login form
        login_form_selector = 'form[method="post"]'
        
        username = 'YOUR_USERNAME'
        password = 'YOUR_PASSWORD'
        # Fill in the login credentials within the correct form
        page.fill(f'{login_form_selector} input[name="login"]', username)
        page.fill(f'{login_form_selector} input[name="password"]', password)

        # Click the login button inside the login form
        page.click(f'{login_form_selector} button[type="submit"]')

        # Navigate to the advanced search page
        advanced_search_url = "https://www.csidb.net/csidb/advsearch/i/"
        page.goto(advanced_search_url)
        
        page.click('#closeDisclaimer')
        
        print(f"Advanced search page URL: {page.url}")

        filter_form_selector = 'form[action="/csidb/advsearch/i/"]'
        page.select_option(f'{filter_form_selector} select[name="attack_location"]', label="Turkey")
        page.click(f'{filter_form_selector} input[type="submit"]')

        cookies = page.context.cookies()
        sessionid = None
        for cookie in cookies:
            print(f"Found cookie: {cookie['name']}")
            if cookie['name'] == 'sessionid':
                
                sessionid = cookie['value']
                break

        print(f"Extracted sessionid: {sessionid}")

        page_number = 1
        while True:
            has_table = send_request_with_sessionid(page_number, sessionid)
            if not has_table:
                break
            time.sleep(1)  # Add a delay to avoid being blocked
            page_number += 1
            
        browser.close()


import requests

def send_request_with_sessionid(page_number, sessionid):
    # Define the URL
    url = f"https://www.csidb.net/csidb/sr/i/?page={page_number}"

    # Define the headers
    headers = {
    "Cookie": f"sessionid={sessionid}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Print the response details
    # print(f"Response Status Code: {response.status_code}")
    # print(f"Response Headers: {response.headers}")
    # print(f"Response Text:\n{response.text}")
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate the table (adjust the selector based on the actual table structure)
        table = soup.find("table")  # Find the first <table> element
        if table:
            # Extract table rows
            rows = table.find_all("tr")
            table_data = []

            for row in rows:
                # Extract all columns (cells) in the row
                cells = row.find_all(["td", "th"])  # Includes <th> for headers
                row_data = [cell.get_text(strip=True) for cell in cells]  # Extract and clean text
                table_data.append(row_data)

            # Save the data to a CSV file
            if page_number == 1:
                # Create a new file and write headers and data for the first page
                with open("table_content.csv", "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Column 1", "Column 2", "Column 3"])  # Replace with actual headers
                    writer.writerows(table_data)
            else:
                # Append data for subsequent pages
                with open("table_content.csv", "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerows(table_data)

            print("Table content saved to table_content.csv")
            return True  # Continue the loop
        else:
            print("No table found in the response.")
            return False  # Stop the loop
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return False  # Stop the loop




login_with_playwright()
