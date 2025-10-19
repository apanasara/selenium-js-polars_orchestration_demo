from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService

edge_options = Options()
edge_options.add_argument(r'--user-data-dir=%USERPROFILE%\AppData\Local\Microsoft\Edge\User Data')
edge_options.add_argument('--profile-directory=Default')   # or Profile 3 (folder), not the display name
edge_options.add_argument('--start-maximized')
# edge_options.add_argument('--headless=new')  # try only if your Edge is new enough

service = EdgeService()  # or EdgeService(executable_path=r"C:\Tools\msedgedriver\msedgedriver.exe")
driver = webdriver.Edge(service=service, options=edge_options)

driver.get("edge://version")
print("Edge started; current URL:", driver.current_url)
driver.quit()