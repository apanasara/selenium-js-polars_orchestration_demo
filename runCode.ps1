taskkill /F /IM msedge.exe
taskkill /F /IM msedgedriver.exe

# Force-update already populated rows:

python PowerBI_Service_RPA.py `
  --out "$env:USERPROFILE\Desktop\Python Script\RPA Connection Link\workspaces.csv" `
  --edge-user-data-dir "$env:USERPROFILE\AppData\Local\Microsoft\Edge\User Data" `
  --profile-name "Power Bi Dev"

<#
# for headless add following arfument
 .... --headless

 #>