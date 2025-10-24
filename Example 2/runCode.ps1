taskkill /F /IM msedge.exe
taskkill /F /IM msedgedriver.exe

# Force-update already populated rows:

python Fabric_Dataset_RPA.py `
  --out "$env:USERPROFILE\Desktop\workspaces_datasets.csv" `
  --edge-user-data-dir "$env:USERPROFILE\AppData\Local\Microsoft\Edge\User Data" `
  --profile-name "Power Bi Dev"

<#
# for headless add following arfument
 .... --headless

 #>
