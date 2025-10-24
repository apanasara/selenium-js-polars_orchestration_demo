import argparse
import os
import sys
import time
import json
import glob
import urllib.parse
import polars as pl

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# -------------------- Selenium helpers --------------------

def resolve_edge_profile_dir(user_data_dir, display_name):
    """
    Given the Edge user data root and a display name (e.g., 'Power Bi Dev'),
    find the actual profile folder (e.g., 'Profile 3') by reading each Profile*/Preferences.
    Returns the folder name (not full path). Raises if not found.
    """
    candidates = sorted(glob.glob(os.path.join(user_data_dir, "Profile *"))) + \
                 ([os.path.join(user_data_dir, "Default")] if os.path.isdir(os.path.join(user_data_dir, "Default")) else [])

    found = []
    for p in candidates:
        pref_path = os.path.join(p, "Preferences")
        try:
            with open(pref_path, "r", encoding="utf-8") as f:
                prefs = json.load(f)
            name = prefs.get("profile", {}).get("name")
            if name:
                found.append((os.path.basename(p), name))
                if name.strip().lower() == display_name.strip().lower():
                    return os.path.basename(p)
        except Exception:
            continue

    msg_lines = [
        f"Edge profile with display name '{display_name}' was not found.",
        "Available profiles I could read:"
    ] + [f"  - Folder: {folder} | Name: {name}" for folder, name in found]
    raise RuntimeError("\n".join(msg_lines))

#  ------------------- getting scrolling viewport -----------------

def _get_viewport(driver, timeout=20):

    driver.get("https://app.powerbi.com/home?experience=power-bi")
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Workspaces']")))
    
    workspace_button = driver.find_element(By.XPATH, "//button[@aria-label='Workspaces']")
    workspace_button.click()
    
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Workspace search']")))

    wait = WebDriverWait(driver, timeout)
    # Either by tag name or class (both are common)
    try:
        return wait.until(EC.presence_of_element_located((By.TAG_NAME, "cdk-virtual-scroll-viewport")))
    except Exception:
        # Fallback: by class
        return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cdk-virtual-scroll-viewport")))

# ------------------- extracting all workspace -----------------

def _extract_workspaces(driver, workspace_handle):

    [workspaces, last_index] = workspace_handle

    if last_index == -1:
        cssSelectorStart = 'tri-workspace-button:not(.pinned-workspace)'
    else:
        cssSelectorStart = f'tri-workspace-button[data-idx="workspace-button-{last_index}"] ~ tri-workspace-button'

    cssSelector = f'{cssSelectorStart} ~ tri-workspace-button'
    idx = driver.execute_script(f"""
                                return Array.from(
                                    document.querySelectorAll('{cssSelector}')
                                )
                                .map(
                                    el => +(el.getAttribute('data-idx').match(/\d+$/)[0])
                                );
                                """)

    no_of_idx = len(idx)

    if no_of_idx>0:
        cssSelector = f'{cssSelector} > button.workspace-button-left'
        names = driver.execute_script(f"""
                                    return Array.from(
                                        document.querySelectorAll('{cssSelector}')
                                    )
                                    .map(
                                        el => el.getAttribute('title')
                                    );
                                    """)

        cssSelector = f'{cssSelector} > tri-svg-icon.diamond'
        Icones = driver.execute_script(f"""
                                    return Array.from(
                                        document.querySelectorAll('{cssSelector}')
                                    )
                                    .map(
                                        el => el.getAttribute('style')!='display: none;'
                                    );
                                    """)

        
        temp_df = pl.DataFrame({
            "PBI Index": idx,
            "Workspace Name": names,
            "Is Connectable": Icones
        })
        
        # Append efficiently
        workspaces = pl.concat([workspaces, temp_df], how="vertical")

    return [workspaces, last_index + no_of_idx]

# ------------ Scroller---------------------
def collect_workspaces_with_virtual_scroll(
    driver,
    workspaces,
    pause=0.35,
    timeout_viewport=20
):
    viewport = _get_viewport(driver, timeout=timeout_viewport)

    # Ensure we start at the top of the list
    driver.execute_script("arguments[0].scrollTop = 0;", viewport)
    time.sleep(pause)

    last_index = -1
    previous_last_index = last_index

    # Initial page
    [workspaces, last_index] = _extract_workspaces(driver, [workspaces, last_index])
    print(f'Extracted Workspace range : (    {previous_last_index}    ,     {last_index}    ]')

    while True:
        
        if previous_last_index < last_index:
            driver.execute_script("arguments[0].scrollBy(0, 3000);", viewport)
            time.sleep(pause)
            previous_last_index = last_index
            [workspaces, last_index] = _extract_workspaces(driver, [workspaces, last_index])
            print(f'Extracted Workspace range : (    {previous_last_index}    ,     {last_index}    ]')
        else:
            break
    
    return workspaces

# -------------------- Main --------------------

def main():
    parser = argparse.ArgumentParser(description="Bulk fetch Power BI Workspace connections (XMLA endpoints) from a PBI service using Selenium on Edge.")
    parser.add_argument("--out", default=None, help="Output CSV path., '_out' will be added to the filename.")
    parser.add_argument("--edge-user-data-dir", default=None,
                        help="Edge user data root, e.g., %USERPROFILE%\\AppData\\Local\\Microsoft\\Edge\\User Data")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--profile-name", help="Edge profile DISPLAY name, e.g., 'Power Bi Dev'")
    group.add_argument("--profile-dir", help="Edge profile FOLDER name, e.g., 'Profile 3' or 'Default'")

    parser.add_argument("--headless", action="store_true", help="Run Edge headless.")
    parser.add_argument("--timeout", type=int, default=30, help="Explicit wait timeout.")
    args = parser.parse_args()

    # Resolve user data dir default (Windows typical)
    if not args.edge_user_data_dir:
        home = os.path.expanduser("~")
        default_ud = os.path.join(home, "AppData", "Local", "Microsoft", "Edge", "User Data")
        if os.path.isdir(default_ud):
            args.edge_user_data_dir = default_ud
        else:
            print("[error] Please supply --edge-user-data-dir (Edge user data root).", file=sys.stderr)
            sys.exit(1)

    # Resolve profile dir from display name if needed
    profile_dir = args.profile_dir
    if args.profile_name:
        profile_dir = resolve_edge_profile_dir(args.edge_user_data_dir, args.profile_name)
        print(f"[info] Resolved display name '{args.profile_name}' -> folder '{profile_dir}'")

    # Setup Edge driver
    edge_options = Options()
    edge_options.add_argument(f"--user-data-dir={args.edge_user_data_dir}")
    edge_options.add_argument(f"--profile-directory={profile_dir}")
    if args.headless:
        edge_options.add_argument("--headless=new")
    edge_options.add_argument("--start-maximized")

    service = EdgeService()  # or EdgeService(executable_path=r"C:\Tools\msedgedriver\msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.set_page_load_timeout(args.timeout)

    try:
        # Ensure we land in the service once (allow SSO/MFA if needed)
        driver.get("https://app.powerbi.com/home?experience=power-bi")
        try:
            WebDriverWait(driver, args.timeout).until(
                EC.any_of(
                    EC.url_contains("powerbi.com"),
                    EC.url_contains("fabric.microsoft.com")
                )
            )
        except Exception:
            pass

        workspaces = pl.DataFrame(schema={
            "PBI Index": pl.Int64,
            "Workspace Name": pl.Utf8,
            "Is Connectable": pl.Boolean
        })
        workspaces = collect_workspaces_with_virtual_scroll(driver, workspaces)
        print(f"Found {len(workspaces)} premium/PPU workspaces")
       
        workspaces = workspaces.with_columns([
                        pl.when(pl.col("Is Connectable"))
                        .then(
                            "powerbi://api.powerbi.com/v1.0/myorg/"
                            + pl.col("Workspace Name").map_elements(urllib.parse.quote, return_dtype=pl.Utf8)
                        )
                        .otherwise(pl.lit(None))
                        .alias("Connection String")
        ])
        workspaces = workspaces.drop("Is Connectable")
        
        # Ensure out path always defined
        out_path = args.out or "workspaces_out.csv"
        workspaces.write_csv(out_path)
        print(f"\n[done] Wrote results to: {out_path}")

    finally:
        if not args.headless:
            time.sleep(1.5)
        driver.quit()


if __name__ == "__main__":
    main()
