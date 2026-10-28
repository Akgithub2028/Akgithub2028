"""Refresh the contribution card using GitHub's API and the standard library.

GITHUB_TOKEN is the workflow's built-in, read-only API credential. The artwork
is replaced only after a complete, valid API response. A failed request leaves
the last good card untouched.
"""

from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = os.environ.get("PROFILE_OWNER", "Akgithub2028")
QUERY = """query($login:String!) {
  user(login:$login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel weekday } }
      }
    }
  }
}"""


def render(calendar, mobile=False):
    weeks = calendar["weeks"]
    if not 50 <= len(weeks) <= 54 or not all(w["contributionDays"] for w in weeks):
        raise ValueError("Incomplete contribution calendar")
    colors = {"NONE":"#131d2d", "FIRST_QUARTILE":"#164b5b",
              "SECOND_QUARTILE":"#247c8c", "THIRD_QUARTILE":"#43b7c7",
              "FOURTH_QUARTILE":"#a8f3fa"}
    updated = datetime.now(timezone.utc).strftime("%d %b %Y").upper()
    width,height = (600,400) if mobile else (1200,230)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
         f'<title>{escape(OWNER)}: {calendar["totalContributions"]} contributions in the last year; updated {updated} UTC</title>',
         f'<rect width="{width}" height="{height}" rx="14" fill="#080c16"/>',
         '<g font-family="DejaVu Sans Mono,monospace">',
         f'<text x="28" y="35" fill="#67e8f9" font-size="{14 if mobile else 12}">CONTRIBUTIONS / LAST 12 MONTHS</text>']
    if not mobile:
        s.append(f'<text x="1172" y="35" fill="#a0b2ca" font-size="11" text-anchor="end">UPDATED {updated} UTC</text>')
    step = 20 if mobile else min(21, 1138 / len(weeks))
    seen = set()
    for i,week in enumerate(weeks):
        for day in week["contributionDays"]:
            x = 28+(i%27 if mobile else i)*step
            row_offset = (i//27)*145 if mobile else 0
            month = day["date"][:7]
            if month not in seen and int(day["date"][-2:]) <= 7:
                seen.add(month)
                label = datetime.fromisoformat(day["date"]).strftime("%b").upper()
                s.append(f'<text x="{x:.1f}" y="{65+row_offset}" fill="#a0b2ca" font-size="{12 if mobile else 9}">{label}</text>')
            y = 77+row_offset+day["weekday"]*16
            color = colors[day["contributionLevel"]]
            caption = f'{day["date"]}: {day["contributionCount"]} contributions'
            s.append(f'<rect x="{x:.1f}" y="{y}" width="{step-4:.1f}" height="12" rx="2" fill="{color}"><title>{caption}</title></rect>')
    s.append(f'<text x="28" y="{360 if mobile else 212}" fill="#edf4ff" font-size="{18 if mobile else 12}">{calendar["totalContributions"]:,} CONTRIBUTIONS</text>')
    if mobile:
        s.append(f'<text x="28" y="385" fill="#a0b2ca" font-size="12">UPDATED {updated} UTC / GITHUB CALENDAR</text>')
    else:
        s.append('<text x="1172" y="212" fill="#a0b2ca" font-size="11" text-anchor="end">SOURCE / GITHUB CONTRIBUTION CALENDAR</text>')
    s.append('</g></svg>\n')
    return "".join(s)


def main():
    token = os.environ["GITHUB_TOKEN"]
    req = Request("https://api.github.com/graphql",
                  data=json.dumps({"query":QUERY,"variables":{"login":OWNER}}).encode(),
                  headers={"Authorization":f"Bearer {token}",
                           "Content-Type":"application/json","User-Agent":"profile-signal"})
    with urlopen(req, timeout=30) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError("GitHub rejected the contribution query")
    calendar = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    outputs = [("signal.svg",render(calendar)),("signal-mobile.svg",render(calendar,mobile=True))]
    for name,output in outputs:
        target = ROOT / "profile" / name
        target.parent.mkdir(exist_ok=True)
        staging = target.with_suffix(".tmp")
        staging.write_text(output)
        staging.replace(target)
    print(f'Updated contribution signal for {OWNER}: {calendar["totalContributions"]} contributions')


if __name__ == "__main__":
    main()
