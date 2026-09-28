"""Render representative PyVis HTML files in Chrome and save browser screenshots."""

from __future__ import annotations

import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


ROOT = Path(__file__).resolve().parents[1]
cases = {
    ROOT / "out/input5_pyvis/network_styled.html": ROOT / "out/input5_pyvis/network_styled_screenshot.png",
    ROOT / "out/input9_directed_pyvis/network_styled.html": ROOT / "out/input9_directed_pyvis/network_styled_screenshot.png",
}
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1400,900")
driver = webdriver.Chrome(options=options)
try:
    for source, target in cases.items():
        driver.get(source.as_uri())
        time.sleep(3)
        ok = driver.save_screenshot(str(target))
        if not ok or target.stat().st_size < 2000:
            raise RuntimeError(f"Screenshot failed: {target}")
        print(target, target.stat().st_size)
finally:
    driver.quit()
