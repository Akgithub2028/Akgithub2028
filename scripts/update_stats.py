"""Generate theme-aware profile stats from GitHub; keep the last cards on API failure."""
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = os.environ.get('PROFILE_OWNER', 'Akgithub2028')
QUERY = '''query($login:String!, $cursor:String) {
 user(login:$login) {
  createdAt
  followers { totalCount }
  contributionsCollection { contributionCalendar { totalContributions } }
  repositories(first:100, after:$cursor, ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false) {
   pageInfo { hasNextPage endCursor }
   nodes { stargazerCount languages(first:100, orderBy:{field:SIZE,direction:DESC}) {
    totalSize edges { size node { name color } }
   } }
  }
 }
}'''


def fetch():
    repos, cursor, user = [], None, None
    while True:
        req = Request('https://api.github.com/graphql',
            data=json.dumps({'query':QUERY, 'variables':{'login':OWNER, 'cursor':cursor}}).encode(),
            headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],
                     'Content-Type':'application/json', 'User-Agent':'profile-stats'})
        with urlopen(req, timeout=30) as response:
            data = json.load(response)
        if data.get('errors') or not data.get('data', {}).get('user'):
            raise RuntimeError('GitHub did not return complete profile statistics')
        user = data['data']['user']
        page = user['repositories']
        repos.extend(page['nodes'])
        if not page['pageInfo']['hasNextPage']:
            return user, repos
        cursor = page['pageInfo']['endCursor']


def card(title, desc, light, height):
    bg, ink, muted, border = ('#ffffff','#172235','#576778','#dce3ec') if light else ('#0d1117','#edf3fc','#9baec5','#293544')
    accent = '#7545c7' if light else '#c1a1ff'
    start = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="{height}" viewBox="0 0 600 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<rect x=".5" y=".5" width="599" height="{height-1}" rx="12" fill="{bg}" stroke="{border}"/>
<g font-family="DejaVu Sans,Arial,sans-serif" fill="{ink}">
<rect x="24" y="25" width="3" height="21" rx="1.5" fill="{accent}"/>
<text x="38" y="42" font-size="18" font-weight="600">{escape(title)}</text>'''
    return [start], ink, muted, accent, border


def render(user, repos, light=False):
    updated = datetime.now(timezone.utc).strftime('%d %b %Y')
    stats = [('Contributions · last 12 months', user['contributionsCollection']['contributionCalendar']['totalContributions']),
             ('Stars · public original repos', sum(r['stargazerCount'] for r in repos)),
             ('Public original repositories', len(repos)), ('Followers', user['followers']['totalCount'])]
    description = '; '.join(f'{label}: {value:,}' for label,value in stats)
    s, ink, muted, accent, border = card('GitHub stats', description, light, 250)
    for i,(label,value) in enumerate(stats):
        x, y = 26+(i%2)*300, 99+(i//2)*77
        color = (['#7545c7','#087c83','#315bd9','#b45b0a'] if light else ['#c1a1ff','#6eddd1','#83b5ff','#ffba70'])[i]
        s.append(f'<text x="{x}" y="{y}" font-size="30" font-weight="700" fill="{color}">{value:,}</text>')
        s.append(f'<text x="{x}" y="{y+22}" font-size="12" fill="{muted}">{escape(label)}</text>')
    s.append(f'<text x="26" y="231" font-size="10" fill="{muted}">GITHUB API · UPDATED {updated.upper()} UTC</text></g></svg>\n')

    totals, colors = Counter(), {}
    for repo in repos:
        for edge in repo['languages']['edges']:
            name = edge['node']['name']
            totals[name] += edge['size']
            colors[name] = edge['node']['color'] or '#a1a1aa'
    if not totals:
        raise ValueError('No repository language data returned')
    total = sum(totals.values())
    top = totals.most_common(6)
    detail = '; '.join(f'{name}: {size/total:.1%}' for name,size in top)
    t, ink, muted, accent, border = card('Most-used languages', detail+'. By code bytes in public original repositories.', light, 310)
    # A segmented ring uses true code-byte proportions, including an Other segment.
    segments = [(name, size, colors[name]) for name,size in top]
    remainder = total-sum(size for _,size in top)
    if remainder:
        segments.append(('Other', remainder, '#64748b'))
    offset = 0
    t.append(f'<circle cx="133" cy="160" r="78" fill="none" stroke="{border}" stroke-width="20"/>')
    for name,size,color in segments:
        pct = size/total*100
        t.append(f'<circle cx="133" cy="160" r="78" pathLength="100" fill="none" stroke="{color}" stroke-width="20" stroke-dasharray="{pct:.5f} {100-pct:.5f}" stroke-dashoffset="{-offset:.5f}" transform="rotate(-90 133 160)"/>')
        offset += pct
    t.append(f'<text x="133" y="157" text-anchor="middle" font-size="30" font-weight="700">{len(totals)}</text><text x="133" y="180" text-anchor="middle" font-size="12" fill="{muted}">LANGUAGES</text>')
    for i,(name,size,color) in enumerate(segments):
        y = 83+i*25
        t.append(f'<circle cx="272" cy="{y-4}" r="4" fill="{color}"/><text x="286" y="{y}" font-size="14">{escape(name)}</text>')
        t.append(f'<text x="572" y="{y}" text-anchor="end" font-size="14" fill="{muted}">{size/total:.1%}</text>')
    t.append(f'<text x="26" y="282" font-size="10" fill="{muted}">CODE BYTES · PUBLIC ORIGINAL REPOSITORIES · {updated.upper()} UTC</text></g></svg>\n')
    return ''.join(s), ''.join(t)


def fetch_history(created_at):
    """Fetch every account year, rather than treating a one-year calendar as all-time."""
    first = date.fromisoformat(created_at[:10])
    today = datetime.now(timezone.utc).date()
    days = {}
    query = """query($login:String!, $from:DateTime!, $to:DateTime!) {
      user(login:$login) { contributionsCollection(from:$from,to:$to) {
        contributionCalendar { weeks { contributionDays { date contributionCount } } }
      } }
    }"""
    for year in range(first.year, today.year+1):
        begin, end = max(first,date(year,1,1)), min(today,date(year,12,31))
        variables = {'login':OWNER, 'from':str(begin)+'T00:00:00Z', 'to':str(end)+'T23:59:59Z'}
        req = Request('https://api.github.com/graphql',
            data=json.dumps({'query':query,'variables':variables}).encode(),
            headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],
                     'Content-Type':'application/json','User-Agent':'profile-stats'})
        with urlopen(req, timeout=30) as response:
            result = json.load(response)
        if result.get('errors'):
            raise RuntimeError('GitHub rejected the contribution-history query')
        weeks = result['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
        for week in weeks:
            for day in week['contributionDays']:
                d = date.fromisoformat(day['date'])
                if begin <= d <= end:
                    days[d] = day['contributionCount']
    expected = (today-first).days+1
    if len(days) != expected:
        raise ValueError('Incomplete contribution history; keeping existing streak cards')
    return days, first, today


def streak_summary(days, today):
    longest, best_start, best_end, run, run_start = 0, None, None, 0, None
    for d,count in sorted(days.items()):
        if count:
            if not run:
                run_start = d
            run += 1
            if run > longest:
                longest, best_start, best_end = run, run_start, d
        else:
            run = 0
    end = today if days.get(today,0) else today-timedelta(days=1)
    start, current = end, 0
    while days.get(start,0):
        current += 1
        start -= timedelta(days=1)
    current_range = (start+timedelta(days=1),end) if current else (None,None)
    return sum(days.values()), current, longest, current_range, (best_start,best_end)


def date_range(pair):
    start,end = pair
    if start is None:
        return 'No active streak'
    if start == end:
        return start.strftime('%b %d, %Y').replace(' 0',' ')
    # Include both years when the run crosses a year boundary.
    fmt = '%b %d, %Y' if start.year != end.year else '%b %d'
    return (start.strftime(fmt)+' – '+end.strftime(fmt)).replace(' 0',' ')


def render_streak(history, light=False, mobile=False):
    days, first, today = history
    total,current,longest,current_dates,best_dates = streak_summary(days,today)
    w,h = (420,226) if mobile else (900,300)
    bg,ink,muted,border = ('#ffffff','#172235','#667085','#dce3ec') if light else ('#11151d','#f0f4fc','#9ba7ba','#394354')
    orange = '#ba5600' if light else '#ff9b2f'
    blue = '#315bd9' if light else '#83b5ff'
    purple = '#7545c7' if light else '#c1a1ff'
    centers = [w/6,w/2,w*5/6]
    cy,r = (78,39) if mobile else (115,65)
    number_y = cy+12
    label_y = 150 if mobile else 221
    dates_y = 174 if mobile else 251
    title = f'{OWNER}: {total:,} total contributions, {current} day current streak, {longest} day longest streak'
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">Contribution history since {first}. Current streak uses today or yesterday so an unfinished UTC day does not break it.</desc>',
         f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="{bg}" stroke="{border}"/>',
         f'<path d="M{w/3} 36V{h-45} M{w*2/3} 36V{h-45}" stroke="{border}"/>',
         f'<g font-family="DejaVu Sans,Arial,sans-serif" text-anchor="middle" fill="{ink}">',
         f'<circle cx="{w/2}" cy="{cy}" r="{r}" fill="none" stroke="{border}" stroke-width="6"/>',
         f'<circle cx="{w/2}" cy="{cy}" r="{r}" fill="none" stroke="{orange}" stroke-width="6" stroke-dasharray="{2*3.141593*r*.9:.2f} {2*3.141593*r*.1:.2f}" transform="rotate(-72 {w/2} {cy})"/>']
    # Native vector flame, with no dependency on emoji fonts or image services.
    fx,fy,scale = w/2,cy-r-8,(.65 if mobile else 1)
    s.append(f'<g transform="translate({fx} {fy}) scale({scale})"><rect x="-17" y="-23" width="34" height="45" fill="{bg}"/><path d="M2 -21C10 -9 4 -7 6 -2C13 -5 15 3 14 8C13 23 -12 25 -14 9C-15 2 -10 -5 -7 -9C-9 3 0 4 2 -2C5 -9 3 -15 2 -21Z" fill="{orange}"/></g>')
    for x,value,color in zip(centers,(total,current,longest),(blue,ink,purple)):
        s.append(f'<text x="{x}" y="{number_y}" font-size="{30 if mobile else 47}" font-weight="700" fill="{color}">{value:,}</text>')
    for x,label,caption,color in zip(centers,('Total contributions','Current streak','Longest streak'),
            (first.strftime('%b %Y')+' – present',date_range(current_dates),date_range(best_dates)),(muted,orange,muted)):
        s.append(f'<text x="{x}" y="{label_y}" font-size="{12 if mobile else 20}" font-weight="{700 if label == "Current streak" else 400}" fill="{color}">{label}</text>')
        s.append(f'<text x="{x}" y="{dates_y}" font-size="{9 if mobile else 13}" fill="{muted}">{escape(caption)}</text>')
    s.append(f'<text x="{w/2}" y="{h-15}" font-size="{8 if mobile else 10}" fill="{muted}">GITHUB CONTRIBUTIONS · UPDATED {today} UTC</text></g></svg>\n')
    return ''.join(s)


def main():
    user, repos = fetch()
    history = fetch_history(user['createdAt'])
    outputs = {}
    for light in (False, True):
        stats, langs = render(user, repos, light)
        suffix = '-light' if light else ''
        outputs[f'stats{suffix}.svg'] = stats
        outputs[f'top-langs{suffix}.svg'] = langs
        outputs[f'streak{suffix}.svg'] = render_streak(history,light)
        outputs[f'streak-mobile{suffix}.svg'] = render_streak(history,light,mobile=True)
    for name,content in outputs.items():
        target = ROOT/'profile'/name
        staging = target.with_suffix('.tmp')
        staging.write_text(content)
        staging.replace(target)
    print(f'Updated stats and languages from {len(repos)} public original repositories.')


if __name__ == '__main__':
    main()
