# icp.py
import re, random, pathlib, csv
from dataclasses import dataclass

@dataclass
class Company:
    name: str
    website: str
    country: str
    industry: str

ANIMALS = ["Labs", "Studios", "Works", "Interactive", "Dynamics", "Omni", "Forge", "Factory", "Hub"]
TLDS_BY_REGION = {
    "US": [".com", ".io"],
    "EU": [".eu", ".com"],
    "JP": [".jp", ".com"],
    "KR": [".kr", ".com"],
    "SG": [".sg", ".com"],
}

def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def parse_icp(text: str):
    t = text.lower()
    # 超簡易抽出（MVP）
    keywords = re.findall(r"[a-zA-Z0-9\-/+]+", t)
    regions = []
    for k, tag in [("us","US"),("eu","EU"),("japan","JP"),("jp","JP"),("korea","KR"),("kr","KR"),("singapore","SG"),("sg","SG")]:
        if k in t: regions.append(tag)
    if not regions: regions = ["US","EU","JP"]
    return {
        "industry_keywords": [k for k in keywords if len(k) > 2][:4] or ["tech","entertainment"],
        "regions": regions[:3]
    }

def generate_companies(filters: dict, n: int = 10):
    kws = filters["industry_keywords"]
    regions = filters["regions"]
    out = []
    for i in range(n):
        base = random.choice(kws).capitalize()
        suffix = random.choice(ANIMALS)
        name = f"{base} {suffix}"
        region = random.choice(regions)
        tld = random.choice(TLDS_BY_REGION.get(region, [".com"]))
        domain = _slug(f"{base}-{suffix}") + tld
        industry = " / ".join(list(dict.fromkeys([k.capitalize() for k in kws]))[:2])
        out.append(Company(name=name, website=f"https://{domain}", country=region, industry=industry))
    return out

def save_companies_csv(companies, path="data/companies.csv"):
    pathlib.Path("data").mkdir(exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name","title","company","website","email","country"])
        for c in companies:
            # email は未取得なので空。後でApollo連携で埋める。
            w.writerow(["", "", c.name, c.website, "", c.country])
