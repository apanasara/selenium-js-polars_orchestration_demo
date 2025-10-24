# Workspace Name & Connection String Extraction 🚀🧩✨

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

## 🏁 Example Output

| PBI Index | Workspace Name         | Connection String                                                        |
|-----------|-----------------------|--------------------------------------------------------------------------|
| 0         | "Finance Team"        | powerbi://api.powerbi.com/v1.0/myorg/Finance%20Team                      |
| 1         | "Operations & Sales"  | powerbi://api.powerbi.com/v1.0/myorg/Operations%20%26%20Sales            |

---
