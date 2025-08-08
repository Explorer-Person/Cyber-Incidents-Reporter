````markdown
# Cyber Incidents Reporter 🇹🇷

An automated web scraper for extracting cyber incident reports related to Turkey from [csidb.net](https://www.csidb.net). It logs in via Playwright, filters incidents by location, and scrapes paginated results using BeautifulSoup and Requests.

---

## 📌 Features

- Logs into csidb.net using **Playwright**
- Automatically applies **"Turkey"** as location filter via advanced search
- Extracts structured data (date, victim, location, summary)
- Iterates through **paginated results**
- Bypasses login/session restriction using extracted **sessionid cookie**
- Exports the result as a **CSV** file: `table_content.csv`

---

## 🧰 Tech Stack

- Python 3.10+
- [Playwright](https://playwright.dev/python/) (for login & filter actions)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://docs.python-requests.org/)
- CSV module

---

## 🔐 Requirements

Install dependencies using:

```bash
pip install playwright beautifulsoup4 requests
playwright install
````

---

## 🚀 Usage

### 1. Configure credentials

In the script, replace:

```python
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
```

with your actual login credentials for [csidb.net](https://www.csidb.net).

---

### 2. Run the scraper

```bash
python your_script.py
```

The script will:

* Log in via browser
* Select **Turkey** as the attack location
* Extract session cookie
* Scrape each result page using `requests` + `BeautifulSoup`
* Append data to `table_content.csv`

---

## 📁 Output Format

Saved file: `table_content.csv`

```csv
Date,Victim,Location,Summary
"June 22, 2024",BtcTurk,Turkey,"Turkish cryptocurrency exchange BtcTurk was hit by a major cyberattack..."
...
```

---

## 🛡️ Notes

* Make sure to **respect terms of service** of csidb.net.
* Add delay (`time.sleep()`) to avoid rate-limiting or blocks.
* This scraper does **not use headless mode by default** for debug visibility. You can switch it by changing:

  ```python
  browser = p.chromium.launch(headless=True)
  ```

---

## 📌 License

MIT License © 2025 Fatih Etlik

---

## 🤝 Contributing

Pull requests are welcome! Feel free to suggest improvements or open issues.

```

---

Let me know if you'd like:
- Bash script to automate login
- Conversion to Excel (`.xlsx`)
- Data schema JSON for API use

I can help generate those too.
```
