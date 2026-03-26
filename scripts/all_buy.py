#!/usr/bin/env python3
"""Print product name and ordering URL for each product."""
import re, yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent

for md in sorted(ROOT.glob("products/*.md")):
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        continue
    front = yaml.safe_load(m.group(1))
    model = front.get("model", "?")
    slug = front.get("slug", md.stem)

    if front.get("discontinued"):
        print(f"{model:30s}  (discontinued)")
        continue
    if front.get("future"):
        print(f"{model:30s}  (future - simulator)")
        continue

    buy_url = front.get("buy_url")
    if not buy_url:
        clean = model.split("/")[0].strip().replace(" ", "")
        buy_url = f"https://orders.thinksrs.com/OnlineOrders/SRSOrders.html?EPrdGrp={clean}"

    print(f"{model:30s}  {buy_url}")
