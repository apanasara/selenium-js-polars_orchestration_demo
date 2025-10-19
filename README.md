# selenium-js-polars_orchestration_demo 🚀🧩✨

**Efficient end-to-end web scraping demonstration leveraging Selenium (Edge) 🕸️, live JavaScript execution 🧑‍💻, and Polars DataFrames 📊 for high-performance extraction. Example target: Power BI Service 🟡. Reusable for other dynamic web data engineering tasks.**

---

## 🌟 Features

- 🤖 Orchestrates browser automation with Selenium and advanced JavaScript injection
- 🪄 Dynamically scrolls, scrapes, and extracts structured content
- ⚡ Uses Polars DataFrames for ultra-fast data batching, transformation, and CSV output
- 🔁 Easily adaptable to similar UI-driven cloud apps
- 🗂 Robust profile management (Edge user-data-dir & profile detection)

---

## 🚦 Usage

```ps1
# Force close msedge threads running on task-manager

taskkill /F /IM msedge.exe
taskkill /F /IM msedgedriver.exe

# Force-update already populated rows:

python PowerBI_Service_RPA.py `
  --out "$env:USERPROFILE\Desktop\Python Script\RPA Connection Link\workspaces.csv" `
  --edge-user-data-dir "$env:USERPROFILE\AppData\Local\Microsoft\Edge\User Data" `
  --profile-name "Power Bi Dev"

```


- Use `--profile-dir` to specify a profile folder instead of display name.
- Add `--headless` for background scraping.

**Output:**  
- Scraped workspaces and their connection strings, exported as CSV.

---

## 📚 Documentation Outline

**1. Introduction**  
🌈 Orchestration approach  
🛠 Technologies used (Selenium, JS injection, Polars)

**2. Installation**  
📦 Python dependencies (`Utils\prerequisites.ps1`)  
🧭 Edge browser + Edge WebDriver testing  
🚀 Polars install notes

**3. Configuration**  
🔑 User data directory and profile selection  
🎛 CLI argument reference (`--profile-name`, `--profile-dir`, `--out`, `--headless`, etc.)

**4. How It Works**  
🕹 How Selenium controls the browser  
⚙️ Use of JavaScript to extract UI elements  
🧮 Data collation via Polars  
📤 CSV output flow

**5. License & Contributions**  
📜 Licensing terms  
🤝 Contributor guidelines

---

## 🏁 Example Output

| PBI Index | Workspace Name         | Connection String                                                        |
|-----------|-----------------------|--------------------------------------------------------------------------|
| 0         | "Finance Team"        | powerbi://api.powerbi.com/v1.0/myorg/Finance%20Team                      |
| 1         | "Operations & Sales"  | powerbi://api.powerbi.com/v1.0/myorg/Operations%20%26%20Sales            |

---

---

## 🧩 Extending To Other Sites

✏️ **Adapting selectors and JS snippets**  
- 🔍 Every site uses unique HTML tags, classes, or IDs. Use browser DevTools to inspect elements you want to scrape.
- 💡 Update Selenium locators (`By.XPATH`, `By.CSS_SELECTOR`, etc.) and tweak JavaScript snippets for the new site’s structure.
- ↕️ Handle infinite scroll, popups, or pagination by modifying scroll logic and Selenium wait conditions.

🔌 **Data pipeline adaptation tips**  
- 🎯 Adjust your data collection and batching steps for the new site’s data fields.
- 🧮 Edit your Polars DataFrame structure to match the incoming data.
- 🧪 Test as you build to catch mapping or formatting bugs early.

---

## 🛠️ Troubleshooting

🤔 **Common Selenium/Edge/JS errors**  
- ❗ *Element not found/timeout*: Double-check selectors; increase timeouts; confirm element is visible in the actual page.
- 🧑‍💻 *Browser won’t start or quit*: Install correct driver; set proper browser paths.
- 🪟 *Unexpected popups/redirects*: Add extra waits; handle popups/alerts in Selenium.

💡 **Profile location issues**  
- 📁 Make sure your user data folder and profile are correctly set; needed for accessing login sessions and configs.
- 🔑 If login fails, check you’re using the right profile name or directory.

🗃 **Output file handling**  
- 📄 Empty CSV or missing columns? Confirm all scraped variables are set and DataFrame columns match expected output.
- 🔀 For large jobs, break up output files or write incrementally to avoid slowing down or crashing.

---
