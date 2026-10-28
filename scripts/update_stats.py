"""Generate theme-aware profile stats from GitHub; keep the last cards on API failure."""
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = os.environ.get('PROFILE_OWNER', 'Akgithub2028')
QUERY = '''query($login:String!, $cursor:String) {
 user(login:$login) {
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
        s.append(f'<text x="{x}" y="{y}" font-size="30" font-weight="700" fill="{accent}">{value:,}</text>')
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
    t, ink, muted, accent, border = card('Most-used languages', detail+'. By code bytes in public original repositories.', light, 340)
    for i,(name,size) in enumerate(top):
        y = 77+i*37
        pct = size/total
        t.append(f'<circle cx="29" cy="{y-4}" r="4" fill="{colors[name]}"/><text x="41" y="{y}" font-size="12">{escape(name)}</text>')
        t.append(f'<text x="574" y="{y}" text-anchor="end" font-size="12" fill="{muted}">{pct:.1%}</text>')
        t.append(f'<rect x="26" y="{y+8}" width="548" height="5" rx="2.5" fill="{border}"/><rect x="26" y="{y+8}" width="{548*pct:.2f}" height="5" rx="2.5" fill="{colors[name]}"/>')
    t.append(f'<text x="26" y="316" font-size="10" fill="{muted}">CODE BYTES · PUBLIC ORIGINAL REPOSITORIES · {updated.upper()} UTC</text></g></svg>\n')
    return ''.join(s), ''.join(t)


def main():
    user, repos = fetch()
    outputs = {}
    for light in (False, True):
        stats, langs = render(user, repos, light)
        suffix = '-light' if light else ''
        outputs[f'stats{suffix}.svg'] = stats
        outputs[f'top-langs{suffix}.svg'] = langs
    for name,content in outputs.items():
        target = ROOT/'profile'/name
        staging = target.with_suffix('.tmp')
        staging.write_text(content)
        staging.replace(target)
    print(f'Updated stats and languages from {len(repos)} public original repositories.')


if __name__ == '__main__':
    main()
