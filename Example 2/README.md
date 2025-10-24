# Workspace Name & its Dataset Name Extraction 🚀🧩✨

## 🚦 Usage

```ps1
# Force close msedge threads running on task-manager

taskkill /F /IM msedge.exe
taskkill /F /IM msedgedriver.exe

# Force-update already populated rows:

python Fabric_Dataset_RPA.py `
  --out "$env:USERPROFILE\Desktop\Python Script\RPA Connection Link\workspaces_datasets.csv" `
  --edge-user-data-dir "$env:USERPROFILE\AppData\Local\Microsoft\Edge\User Data" `
  --profile-name "Power Bi Dev"

```


- Use `--profile-dir` to specify a profile folder instead of display name.
- Add `--headless` for background scraping.

**Output:**  
- Scraped workspaces and their dataset names, exported as CSV.

---

## 🏁 Example Output

| PBI Index | Workspace Name         | Dataset Name                            |
|-----------|-----------------------|------------------------------------------|
| 0         | "Finance Team"        | Revenue Dataset                          |
| 1         | "Operations & Sales"  | Operational_Lead_Time_Dataset            |

---
