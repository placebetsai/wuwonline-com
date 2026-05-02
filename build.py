#!/usr/bin/env python3
"""WUW site builder - World of Unpredictable Wrestling / Johnny Rodz @ Gleason's Gym, Brooklyn."""
import os, json, re, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
all_pages = json.load(open(f'{ROOT}/_data/posts.json'))
img_map = json.load(open(f'{ROOT}/_data/img-map.json'))
try:
    ALUMNI_PHOTOS = json.load(open(f'{ROOT}/_data/alumni-with-photos.json'))
except FileNotFoundError:
    ALUMNI_PHOTOS = []
try:
    ROSTER_PHOTOS = json.load(open(f'{ROOT}/_data/roster-with-photos.json'))
except FileNotFoundError:
    ROSTER_PHOTOS = []

PHONE = '718-797-2872'
ADDR_LINE_1 = "Gleason's Gym · 130 Water Street"
ADDR_LINE_2 = 'Brooklyn, NY 11201 · Under the Brooklyn Bridge'
EMAIL = 'Johnnyrodz41@gmail.com'

ALUMNI = [
    ('Taz', 'WWE · ECW Hall of Famer'),
    ('Tommy Dreamer', 'ECW / WWE Hall of Famer'),
    ('D-Von Dudley', 'WWE Hall of Famer'),
    ('Big Cass', 'William Morrissey · WWE'),
    ('Masha Slamovich', 'TNA · WWE NXT'),
    ('Marti Belle', 'TNA Impact Wrestling'),
    ('Vince Russo', 'WCW / WWE Head Writer'),
    ('Matt Striker', 'WWE Commentator & Wrestler'),
    ('Prince Nana', 'ROH · AEW'),
    ('Nicole Bass', 'WWF · ECW'),
    ('Big Vito', 'WCW · WWE'),
    ('Phantasio', 'WWF'),
    ('Rocco Rock', 'ECW · Public Enemy'),
    ('SD Jones', 'WWF Veteran'),
    ('Big Sal Graziano', 'F.B.I. · ECW'),
    ('Will Ferrara', 'Kid Spartan · WWE NXT'),
    ('MJ Jenkins', 'Lady Mojo · WUW Legend'),
    ('Maurice Wingboy Martin', 'TNA Impact Wrestling'),
]
ROSTER = ['Irish Bruce', 'Stephanie', 'Christian Andrews', 'Big Al', 'Sir Robert Taylor Jr',
          'Adam Bailey', 'Kid Eric', 'Carlos Billetes (Fireball)', 'Gary Post', 'King Broadway of Prussia',
          'Jada Rose', 'J Bushii', 'PJ Savage', 'Jesse Lebron', 'The Faceless Ones']
CREDENTIALS = [
    ('1996', 'WWE Hall of Fame', 'Class of 1996 — The Unpredictable Johnny Rodz'),
    ('400+', 'Wrestlers Trained', 'Across WWE, NXT, AEW, Impact, ROH'),
    ('1980s', 'Active Trainer', "Johnny Rodz @ Gleason's Gym — four decades"),
]
SCHEDULE = [('Mon · Tue · Thu', '3:00 PM – 9:30 PM'), ('Saturday', '12:00 PM – 5:30 PM')]

posts = [p for p in all_pages if p.get('date')]
posts.sort(key=lambda p: p['date'], reverse=True)

def collect_links_filter(predicate):
    seen, out = set(), []
    for p in all_pages:
        for L in p.get('external_links', []):
            if predicate(L) and L['url'] not in seen:
                seen.add(L['url'])
                src = '/' + p['url'].split('://')[1].split('/',1)[1].rstrip('/') + '/' if 'wuwonline.com' in p['url'] else '/'
                out.append({'url': L['url'], 'anchor': L['anchor'] or L['host'], 'source': src})
    return out

mnw_links = collect_links_filter(lambda L: 'mondaynightwrestling.com' in L['url'])
press_links = collect_links_filter(lambda L: any(h in L['url'] for h in ['fox5ny.com', 'fox29.com', 'newsweek.com', 'newsbreak.com', 'gettyimages']))
yt_spotify_links = collect_links_filter(lambda L: any(h in L['url'] for h in ['youtu.be', 'youtube.com/watch', 'spotify.com/episode']))

# DocumentCloud + Substack archive — long-form references for the Israel Joffe page.
DOCUMENTCLOUD = [
    ('https://www.documentcloud.org/documents/22014760-israel-joffe', 'Israel Joffe — research file'),
    ('https://www.documentcloud.org/documents/21956651-document-from-the-lubavitch-rebbe-menachem-shneerson-israel-joffe', 'Letter from the Lubavitcher Rebbe to Israel Joffe'),
    ('https://www.documentcloud.org/documents/21956628-the-next-detroit_-the-catastrophic-collapse-of-atlantic-city-israel-joffe', 'The Next Detroit — the catastrophic collapse of Atlantic City'),
    ('https://www.documentcloud.org/documents/25895701-comgoogleandroidappsphotos', 'Field notes (Google Photos archive)'),
    ('https://www.documentcloud.org/app?q=%2Btag%3A%22Israel-joffe%22', 'All DocumentCloud filings tagged Israel Joffe'),
]
SUBSTACKS = [
    ('https://israeljoffe.substack.com', 'Israel Joffe · Substack'),
    ('https://israeljoffefda.substack.com', 'Israel Joffe FDA · Substack'),
    ('https://israeljoffefdic.substack.com', 'Israel Joffe FDIC · Substack'),
]

# Federation — Israel Joffe's publisher network. Each gets a per-site SEO article at /network/{slug}/
# and one line in the footer "Across the network" strip. NOT in primary nav.
FEDERATION = [
    {
        'slug': 'israeljoffe-com',
        'host': 'israeljoffe.com',
        'name': 'Israel Joffe',
        'tag':  'Media · IT · Firefighter',
        'lede': "Israel Joffe's editorial home — media-executive credits at Fox 5, Newsweek, Fox 29, NewsBreak, FDIC firefighter writing, and the IT specialist work that backs WUW's broadcast and archive infrastructure.",
        'body': """<p>Israel Joffe is the long-time technologist and media operator behind a working network of New York publishing properties. He has trained inside Gleason's Gym for years alongside the WUW family — many of the dated <a href="/2021/01/09/israel-joffe/">/israel-joffe/</a> entries on this site are field reports from those sessions.</p>
<p>His personal site <a href="https://israeljoffe.com" target="_blank" rel="noopener">israeljoffe.com</a> collects the press credits, broadcast appearances, and the DocumentCloud filings he's released over the years — including the Atlantic City research and the letter from the Lubavitcher Rebbe. It's the natural starting point for anyone trying to follow his work outside the ring.</p>
<p>He also keeps a parallel BJJ and fitness journal at <a href="https://israeljoffe.org" target="_blank" rel="noopener">israeljoffe.org</a> — the gym-and-mat side of the same training discipline that brings him to WUW.</p>"""
    },
    {
        'slug': 'israeljoffe-org',
        'host': 'israeljoffe.org',
        'name': 'Israel Joffe · BJJ & Fitness',
        'tag':  'BJJ Black Belt · Training Journal',
        'lede': "The training-journal counterpart to israeljoffe.com — BJJ black-belt notes, fitness programming, and the gym-floor footage that connects directly to WUW's pro-wrestling fundamentals.",
        'body': """<p><a href="https://israeljoffe.org" target="_blank" rel="noopener">israeljoffe.org</a> is where Israel Joffe documents the combat-sports side of his life — Brazilian Jiu-Jitsu black-belt rolls, conditioning programs, world-travel training stops, and the long view of what staying in the ring for a couple of decades actually requires.</p>
<p>The crossover with WUW is direct: the bumps and locks Johnny Rodz has been teaching at Gleason's for forty years overlap heavily with the grappling fundamentals Israel writes about. Many of the WUW <a href="/alumni/">alumni</a> have rolled with him at one point or another.</p>
<p>If you're a wrestler thinking about cross-training in BJJ, or a grappler curious about pro-wrestling fundamentals, that site is the bridge.</p>"""
    },
    {
        'slug': 'placebets-ai',
        'host': 'placebets.ai',
        'name': 'PlaceBets.ai',
        'tag':  'Sports markets · Live odds',
        'lede': "PlaceBets.ai — the sports-markets corner of the network. Pro wrestling, MMA, combat-sports betting research and live odds tooling.",
        'body': """<p><a href="https://placebets.ai" target="_blank" rel="noopener">PlaceBets.ai</a> is the sports-markets desk inside the network. It tracks live odds, betting research, and prop-market analysis across major U.S. sports — and runs a long-form coverage line on combat sports specifically.</p>
<p>For the WUW audience the relevant beat is the boxing and MMA coverage: undercard analysis, fighter histories, and how the Brooklyn boxing-and-wrestling lineage that runs through Gleason's Gym still feeds into modern combat-sports markets. (Pro wrestling itself isn't bet on competitively, but the cross-disciplinary coverage frequently lands on stories WUW alumni and trainees would recognise.)</p>
<p>Worth a bookmark if you follow the fight game.</p>"""
    },
    {
        'slug': 'fashionistas-ai',
        'host': 'fashionistas.ai',
        'name': 'Fashionistas.ai',
        'tag':  'Independent fashion commerce',
        'lede': "Fashionistas.ai — the network's independent fashion-commerce property. Selected pieces, editorial shop pages, and the merchandising playbook behind WUW gear runs.",
        'body': """<p><a href="https://fashionistas.ai" target="_blank" rel="noopener">Fashionistas.ai</a> is the network's commerce-and-merchandising arm — a selected fashion shop with editorial product pages and a long catalog tilted toward independent labels.</p>
<p>The connection to WUW is operational more than thematic: the same merchandising toolkit, image pipeline, and shop-page architecture used on Fashionistas drives the limited gear runs and event-merch drops that show up on the WUW <a href="/events/">events</a> calendar. If you've ever wondered how a small brand actually ships merch alongside a live show, the answer lives in that codebase.</p>
<p>For wrestling fans interested in entrance gear and ring-fashion histories, the cross-publication piece on iconic wrestling entrance gear at <a href="/2026/03/03/iconic-wrestling-entrance-gear-fashion/">our archive</a> sits in the same conversation.</p>"""
    },
    {
        'slug': 'spanishtvshows-com',
        'host': 'spanishtvshows.com',
        'name': 'SpanishTVShows.com',
        'tag':  'Latino entertainment · Telenovelas',
        'lede': "SpanishTVShows.com — Spanish-language entertainment writing in the network. Latino TV, novelas, lucha-libre cross-coverage that touches WUW's lineage from Antonino Rocca through Johnny Rodz.",
        'body': """<p><a href="https://spanishtvshows.com" target="_blank" rel="noopener">SpanishTVShows.com</a> is the Spanish-language entertainment desk in the network — daily writing on telenovelas, Latino television, and the broader Spanish-speaking pop-culture beat.</p>
<p>The WUW overlap is clean and historical: Johnny Rodz (born José Rodriguez) came up through Antonino "Argentina" Rocca's school, the same New York lineage that produced an entire generation of Latino professional wrestlers. The <a href="/2026/01/23/greatest-spanish-speaking-wrestlers/">greatest Spanish-speaking wrestlers</a> piece in our archive is the canonical cross-publication reference. SpanishTVShows runs a parallel beat on the entertainment side.</p>
<p>If you cover Latino sports-entertainment culture, both sites belong on the same shelf.</p>"""
    },
    {
        'slug': 'hiddencameras-tv',
        'host': 'hiddencameras.tv',
        'name': 'HiddenCameras.tv',
        'tag':  'Surveillance & gear journalism',
        'lede': "HiddenCameras.tv — the network's surveillance-gear and personal-security writing. Practical reviews, recording-law primers, and the equipment context behind documenting an old-school wrestling school.",
        'body': """<p><a href="https://hiddencameras.tv" target="_blank" rel="noopener">HiddenCameras.tv</a> is the network's gear-and-surveillance desk — practical reviews of small recording equipment, a long-running primer on state recording-consent laws, and the personal-security buyer's-guide content that comes out of it.</p>
<p>The connection to WUW is operational: the body-cam, GoPro, and small-rig footage that ends up in our <a href="/in-the-news/">press &amp; media</a> reel — and the post archive going back to <a href="/2016/08/05/welcome-to-the-world-of-unpredictable-wrestling/">2016</a> — comes off the same equipment families that HiddenCameras covers in depth. If you want to understand the gear behind documenting a wrestling school for forty years, it's the right reading list.</p>"""
    },
    {
        'slug': 'ihatecollege-com',
        'host': 'ihatecollege.com',
        'name': 'iHateCollege',
        'tag':  'Trade-skills writing',
        'lede': "iHateCollege.com — the network's trade-school and alternative-careers writing. Direct relevance to wrestling: most full-time WUW pros built a career outside the four-year degree path.",
        'body': """<p><a href="https://ihatecollege.com" target="_blank" rel="noopener">iHateCollege.com</a> is the network's writing on trade skills, alternative career paths, and the specific economics of choosing a craft over a four-year degree.</p>
<p>The angle lands directly on professional wrestling: most full-time WUW alumni built their careers outside the college-to-corporate pipeline, on a path that looks much more like a trade apprenticeship than a four-year degree. The cross-publication piece <a href="/2026/02/14/wrestling-vs-college-johnny-rodz/">wrestling vs. college</a> in our archive — built around Johnny Rodz's own four-decade arc — is the canonical reference on it.</p>
<p>If you're a young trainee weighing whether to go pay tuition or come bump at Gleason's, both reads are aimed exactly at you.</p>"""
    },
    {
        'slug': 'ketiservice-com',
        'host': 'ketiservice.com',
        'name': 'KetiService · LDM Real Estate',
        'tag':  'NYC real estate · Whitestone',
        'lede': "KetiService — Robb DeMange and Keti's NYC real-estate practice. Twenty years of buying, selling, and investment guidance across NYC, Queens, and Long Island. Network neighbour from Whitestone.",
        'body': """<p><a href="https://ketiservice.com" target="_blank" rel="noopener">KetiService.com</a> is the home of LDM Real Estate — Robb DeMange's twenty-year New York City brokerage practice, working with Keti across NYC, Queens, and Long Island, run out of a Whitestone office.</p>
<p>It's the network's relocation desk: WUW alumni and trainees who decide to move to New York for a serious training run frequently end up working with that practice on the housing side of the move. Boroughs they cover (Brooklyn, Queens, NYC, Long Island) are precisely where most of the WUW <a href="/roster/">roster</a> rents or buys.</p>
<p>If you're moving to New York to train, that's a real broker, not a referral fee.</p>"""
    },
]

FED_BY_SLUG = {f['slug']: f for f in FEDERATION}

def post_url(p):
    return '/' + p['url'].split('://')[1].split('/',1)[1].rstrip('/') + '/'

def rewrite(body):
    if not body: return ''
    body = re.sub(r'src="(https?://[^"]+\.(?:jpe?g|png|webp|gif))[^"]*"',
                  lambda m: f'src="{img_map.get(m.group(1).split("?")[0], m.group(1))}"', body, flags=re.I)
    body = re.sub(r'href="https?://(?:www\.)?wuwonline\.com([^"]*)"', r'href="\1"', body)
    body = re.sub(r'<div[^>]*class="[^"]*sharedaddy[^"]*"[^>]*>.*?</div>\s*</div>', '', body, flags=re.S | re.I)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.S | re.I)
    # Normalise legacy ring-name order: "Johnny [The Unpredictable] Rodz" -> "[The Unpredictable] Johnny Rodz"
    body = re.sub(
        r'Johnny\s*([“"]|&#8220;|&quot;)\s*The\s+Unpredictable\s*([”"]|&#8221;|&quot;)\s*Rodz',
        r'\1The Unpredictable\2 Johnny Rodz',
        body, flags=re.I,
    )
    return body.strip()

def page_body(slug_path):
    target = slug_path.rstrip('/')
    for q in all_pages:
        url = q.get('url', '')
        if '://' not in url: continue
        parts = url.split('://')[1].split('/', 1)
        path = '/' + parts[1] if len(parts) > 1 else '/'
        if path.rstrip('/') == target:
            return rewrite(q.get('body_html', ''))
    return ''

def append_wp_extras(html_str, slug):
    body = page_body(slug)
    if not body or len(body) < 200: return html_str
    extra = '<section class="wp-extra"><div class="wp-extra-frame"><h2 class="wp-extra-h">More from the WUW archive</h2><div class="wp-extra-body">' + body + '</div></div></section>'
    return html_str.replace('</main>', extra + '</main>', 1)

LOCAL_BUSINESS_LD = {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "Organization", "EducationalOrganization", "SportsActivityLocation"],
    "name": "World of Unpredictable Wrestling",
    "alternateName": ["WUW", "WUW Brooklyn"],
    "description": "Brooklyn's home of professional wrestling training. Founded by WWE Hall of Famer Johnny Rodz at Gleason's Gym.",
    "url": "https://wuwonline.com/",
    "telephone": "+1-718-797-2872",
    "email": EMAIL,
    "image": "https://wuwonline.com/img/og-default-square.jpg",
    "logo": "https://wuwonline.com/img/logo.png",
    "address": {"@type": "PostalAddress", "streetAddress": "130 Water Street", "addressLocality": "Brooklyn", "addressRegion": "NY", "postalCode": "11201", "addressCountry": "US"},
    "geo": {"@type": "GeoCoordinates", "latitude": 40.7028, "longitude": -73.9897},
    "founder": {"@type": "Person", "name": "Johnny Rodz", "alternateName": "The Unpredictable Johnny Rodz", "jobTitle": "Professional Wrestling Trainer", "award": "WWE Hall of Fame, Class of 1996", "birthName": "Jose Rodriguez"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Thursday"], "opens": "15:00", "closes": "21:30"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "12:00", "closes": "17:30"},
    ],
    "sameAs": [
        "https://twitter.com/Rodzjohnny",
        "https://www.facebook.com/WorldofUnpredictableWrestling",
        "https://www.mondaynightwrestling.com/",
    ],
}

def head(title, desc, canonical, og_image=None, og_type='website', published=None, modified=None, post_title=None):
    og = og_image or 'https://wuwonline.com/img/og-default.jpg'
    og_sq = 'https://wuwonline.com/img/og-default-square.jpg'
    is_article = og_type == 'article'
    ld_blocks = [LOCAL_BUSINESS_LD]
    if is_article and published:
        ld_blocks.append({
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": post_title or title,
            "datePublished": published,
            "dateModified": modified or published,
            "url": canonical,
            "image": og,
            "author": {"@type": "Organization", "name": "World of Unpredictable Wrestling", "url": "https://wuwonline.com/"},
            "publisher": {"@type": "Organization", "name": "World of Unpredictable Wrestling", "url": "https://wuwonline.com/", "logo": {"@type": "ImageObject", "url": "https://wuwonline.com/img/logo.png"}},
            "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        })
    else:
        ld_blocks.append({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "World of Unpredictable Wrestling",
            "url": "https://wuwonline.com/",
            "potentialAction": {"@type": "SearchAction", "target": "https://wuwonline.com/?q={search_term_string}", "query-input": "required name=search_term_string"},
        })
    ld_json = '\n'.join(f'<script type="application/ld+json">{json.dumps(b, separators=(",", ":"))}</script>' for b in ld_blocks)
    article_metas = ''
    if is_article:
        article_metas = (
            (f'<meta property="article:published_time" content="{published}T00:00:00Z"/>\n' if published else '')
            + (f'<meta property="article:modified_time" content="{modified}T00:00:00Z"/>\n' if modified else '')
            + '<meta property="article:author" content="Johnny Rodz"/>\n<meta property="article:section" content="Pro Wrestling"/>\n'
        )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}"/>
<meta name="keywords" content="Johnny Rodz, WWE Hall of Fame, professional wrestling training Brooklyn, Gleason's Gym, Tazz, Tommy Dreamer, D-Von Dudley, Big Cass, Masha Slamovich, learn pro wrestling NYC, WUW, World of Unpredictable Wrestling"/>
<meta name="author" content="World of Unpredictable Wrestling"/>
<meta name="theme-color" content="#0a0a0a"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>
<meta name="geo.region" content="US-NY"/>
<meta name="geo.placename" content="Brooklyn, New York"/>
<meta name="geo.position" content="40.7028;-73.9897"/>
<meta name="ICBM" content="40.7028, -73.9897"/>
<link rel="canonical" href="{canonical}"/>
<link rel="icon" href="/favicon.svg" type="image/svg+xml"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
<meta property="og:type" content="{og_type}"/>
<meta property="og:title" content="{H.escape(title)}"/>
<meta property="og:description" content="{H.escape(desc)}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:site_name" content="World of Unpredictable Wrestling"/>
<meta property="og:locale" content="en_US"/>
<meta property="og:image" content="{og}"/>
<meta property="og:image:secure_url" content="{og}"/>
<meta property="og:image:type" content="image/jpeg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:image:alt" content="World of Unpredictable Wrestling — Train with Johnny Rodz, WWE Hall of Fame"/>
<meta property="og:image" content="{og_sq}"/>
<meta property="og:image:type" content="image/jpeg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="1200"/>
<meta property="og:image:alt" content="WUW (square)"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{H.escape(title)}"/>
<meta name="twitter:description" content="{H.escape(desc)}"/>
<meta name="twitter:image" content="{og}"/>
<meta name="twitter:image:alt" content="World of Unpredictable Wrestling — Brooklyn"/>
<meta name="twitter:site" content="@Rodzjohnny"/>
<meta name="twitter:creator" content="@Rodzjohnny"/>
{article_metas}<meta name="apple-mobile-web-app-title" content="WUW"/>
<meta name="application-name" content="WUW"/>
<meta name="format-detection" content="telephone=no"/>
<link rel="alternate" type="application/rss+xml" title="WUW — News &amp; Press" href="/feed.xml"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&family=Inter:wght@400;500;600;700;900&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="/styles.css?v=BUILD"/>
{ld_json}
</head>
<body>
<header class="masthead" id="top">
  <a class="wordmark" href="/" aria-label="WUW — World Of Unpredictable Wrestling">
    <img src="/img/logo.png" alt="WUW — World Of Unpredictable Wrestling" class="wm-logo" />
  </a>
  <nav class="primary" aria-label="Primary">
    <a href="/">Home</a>
    <a href="/johnny-rodz/">Johnny Rodz</a>
    <a href="/alumni/">Alumni</a>
    <a href="/roster/">Roster</a>
    <a href="/title-holders/">Champions</a>
    <a href="/events/">Events</a>
    <a href="/in-the-news/">News</a>
    <a href="/contact/">Contact</a>
    <a href="/contact/" class="primary-cta">Train</a>
  </nav>
  <button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav"><span></span><span></span><span></span></button>
</header>
<div class="mobile-nav" id="mobile-nav" aria-hidden="true">
  <nav class="mobile-nav-inner" aria-label="Mobile primary">
    <a href="/">Home</a>
    <a href="/johnny-rodz/">Johnny Rodz</a>
    <a href="/about/">About WUW</a>
    <a href="/alumni/">Alumni</a>
    <a href="/roster/">Roster</a>
    <a href="/title-holders/">Champions</a>
    <a href="/events/">Events</a>
    <a href="/in-the-news/">News</a>
    <a href="/contact/">Contact · Train</a>
    <div class="mobile-nav-fine">
      <a href="tel:7187972872">{PHONE}</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </nav>
</div>
'''

def footer():
    fed_strip = ' · '.join(
        f'<a href="/network/{f["slug"]}/" rel="noopener">{H.escape(f["host"])}</a>'
        for f in FEDERATION
    )
    return f'''
<footer class="colophon">
  <div class="colophon-frame">
    <div class="col-brand"><img src="/img/logo.png" alt="WUW" class="col-logo" /><span class="col-tag">World Of Unpredictable Wrestling · est. 1980s</span></div>
    <div class="col-contact">
      <p class="col-h">Train · Brooklyn</p>
      <p><a href="tel:7187972872">{PHONE}</a></p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>{ADDR_LINE_1}<br>{ADDR_LINE_2}</p>
    </div>
    <div class="col-social">
      <p class="col-h">Follow</p>
      <p><a href="https://twitter.com/Rodzjohnny" target="_blank" rel="noopener me">Twitter · @Rodzjohnny</a></p>
      <p><a href="https://www.facebook.com/WorldofUnpredictableWrestling" target="_blank" rel="noopener me">Facebook</a></p>
    </div>
  </div>
  <div class="col-network" aria-label="Across the network">
    <span class="cn-label">Across the network</span>
    <span class="cn-links">{fed_strip}</span>
  </div>
  <div class="col-fine"><p>© <span id="year">2026</span> World of Unpredictable Wrestling. All rights reserved.</p><p>Founded by Johnny Rodz · WWE Hall of Fame Class of 1996 · <a href="/in-the-news/">Press &amp; media →</a></p></div>
</footer>
<script>document.getElementById("year").textContent=new Date().getFullYear();
(function(){{const t=document.querySelector(".menu-toggle"),d=document.getElementById("mobile-nav"),b=document.body;if(!t||!d)return;t.addEventListener("click",()=>{{const o=b.classList.toggle("menu-open");t.setAttribute("aria-expanded",o);d.setAttribute("aria-hidden",!o);}});document.querySelectorAll('.mobile-nav a').forEach(a=>a.addEventListener("click",()=>b.classList.remove("menu-open")));}})();
</script>
</body></html>'''

def render_home():
    canonical = 'https://wuwonline.com/'
    title = 'WUW · Train with Johnny Rodz — WWE Hall of Famer · Brooklyn'
    desc = "Train pro wrestling at Gleason's Gym Brooklyn with Johnny Rodz, WWE Hall of Famer (Class of 1996). 400+ wrestlers trained — Tazz, Tommy Dreamer, D-Von Dudley, Big Cass, Masha Slamovich. Call 718-797-2872."
    return head(title, desc, canonical) + f'''
<main class="home portal">
  <section class="ph-hero" aria-label="WUW — World of Unpredictable Wrestling">
    <picture class="ph-image" aria-hidden="true"><img src="/img/hero.jpg" alt="" loading="eager" fetchpriority="high"/></picture>
    <div class="ph-veil" aria-hidden="true"></div>
    <div class="ph-frame">
      <p class="ph-eyebrow"><span class="rule"></span><span>Brooklyn · Gleason's Gym · est. 1980s</span></p>
      <h1 class="ph-title">
        <span class="ph-line"><span class="ph-word ph-w1">Train</span></span>
        <span class="ph-line"><span class="ph-word ph-w2">with the</span></span>
        <span class="ph-line"><span class="ph-word ph-w3 ph-em">Unpredictable</span></span>
      </h1>
      <p class="ph-sub"><em>The Unpredictable Johnny Rodz</em> — WWE Hall of Fame Class of 1996, MSG-circuit veteran, the Brooklyn trainer behind Tazz, Tommy Dreamer, D-Von Dudley, Big Cass, Masha Slamovich and 400+ professional wrestlers.</p>
    </div>
  </section>

  <section class="pc-cards" aria-label="Pick a path">
    <a class="pc-card pc-train" href="/contact/" aria-label="Start training">
      <picture class="pc-img"><img src="/img/about.jpg" alt="" loading="eager"/></picture>
      <div class="pc-veil"></div>
      <div class="pc-body">
        <p class="pc-eyebrow">Open to everyone · M T Th &amp; Sat</p>
        <h2 class="pc-h">Train</h2>
        <p class="pc-meta">Step into the ring. Ring fundamentals, psychology, mic work — taught by the man who trained the names you grew up watching.</p>
        <p class="pc-cta"><span>Start Training</span> <svg width="22" height="12" viewBox="0 0 22 12" fill="none" aria-hidden="true"><path d="M0 6h20M15 1l5 5-5 5" stroke="currentColor" stroke-width="1.4"/></svg></p>
      </div>
    </a>
    <a class="pc-card pc-alumni" href="/alumni/" aria-label="See the WUW alumni">
      <picture class="pc-img"><img src="/img/tazz2.jpg" alt="" loading="eager"/></picture>
      <div class="pc-veil"></div>
      <div class="pc-body">
        <p class="pc-eyebrow">400+ trained · WWE · ECW · TNA · AEW · ROH</p>
        <h2 class="pc-h">Alumni</h2>
        <p class="pc-meta">Tazz. Tommy Dreamer. D-Von Dudley. Big Cass. Masha Slamovich. Marti Belle. Vince Russo. Matt Striker. The list keeps going.</p>
        <p class="pc-cta"><span>See the Roll</span> <svg width="22" height="12" viewBox="0 0 22 12" fill="none" aria-hidden="true"><path d="M0 6h20M15 1l5 5-5 5" stroke="currentColor" stroke-width="1.4"/></svg></p>
      </div>
    </a>
    <a class="pc-card pc-events" href="/events/" aria-label="WUW live events">
      <picture class="pc-img"><img src="/img/next-show.jpg" alt="" loading="eager"/></picture>
      <div class="pc-veil"></div>
      <div class="pc-body">
        <p class="pc-eyebrow">Live shows · Brooklyn</p>
        <h2 class="pc-h">Watch</h2>
        <p class="pc-meta">Live cards from Gleason's Gym. Championship matches. The wrestlers Johnny is building right now.</p>
        <p class="pc-cta"><span>See Events</span> <svg width="22" height="12" viewBox="0 0 22 12" fill="none" aria-hidden="true"><path d="M0 6h20M15 1l5 5-5 5" stroke="currentColor" stroke-width="1.4"/></svg></p>
      </div>
    </a>
  </section>

  <section class="meet-johnny" id="johnny">
    <div class="mj-frame">
      <div class="mj-photo"><img src="/img/meet-johnny.jpg" alt="Johnny Rodz at Gleason's Gym" loading="lazy"/></div>
      <div class="mj-body">
        <p class="ps-eyebrow">Meet Johnny</p>
        <h2 class="mj-h"><em>The Unpredictable</em> Johnny Rodz</h2>
        <p class="mj-lede">WWE Hall of Fame, Class of 1996. Born José Rodriguez in Brooklyn. Four decades on the MSG circuit and across the WWF — then four more decades quietly building the next generation of pro wrestlers.</p>
        <p class="mj-bio">If you've watched WWE, ECW, TNA, AEW or Impact in the last twenty years you've watched a Johnny Rodz student. WUW's the school he runs out of <strong>Gleason's Gym</strong> — the same Brooklyn boxing temple that's produced world champions for decades.</p>
        <dl class="mj-contact">
          <div><dt>Call</dt><dd><a href="tel:7187972872">{PHONE}</a></dd></div>
          <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div><dt>Visit</dt><dd>{ADDR_LINE_1}<br>{ADDR_LINE_2}</dd></div>
          <div><dt>Train</dt><dd>{SCHEDULE[0][0]} · {SCHEDULE[0][1]}<br>{SCHEDULE[1][0]} · {SCHEDULE[1][1]}</dd></div>
        </dl>
        <div class="mj-cta-row">
          <a class="btn-primary" href="/contact/">Start Training</a>
          <a class="btn-ghost" href="/johnny-rodz/">Read the Bio →</a>
        </div>
      </div>
    </div>
  </section>
</main>
''' + footer()

def render_alumni():
    if ALUMNI_PHOTOS:
        cards = ''.join(f'<article class="al-card"><div class="al-img"><img src="{H.escape(a["img"])}" alt="{H.escape(a["name"])}" loading="lazy"></div><h3>{H.escape(a["name"])}</h3></article>' for a in ALUMNI_PHOTOS)
    else:
        cards = ''.join(f'<article class="al-card"><h3>{H.escape(n)}</h3><p>{H.escape(c)}</p></article>' for n, c in ALUMNI)
    return head('WUW Alumni · 400+ Trained by Johnny Rodz', "Alumni include Tazz, Tommy Dreamer, D-Von Dudley, Big Cass, Masha Slamovich, Marti Belle, Vince Russo, Matt Striker. 400+ professional wrestlers trained at Gleason's Gym Brooklyn.", 'https://wuwonline.com/alumni/') + f'''
<main class="page"><div class="page-frame">
  <header class="page-head"><p class="ps-eyebrow">{len(ALUMNI)}+ featured · 400+ trained total</p><h1 class="page-h">Alumni</h1><p class="page-lede">Trained by Johnny Rodz at Gleason's Gym — went on to headline WWE, WCW, ECW, TNA, AEW, Impact, and beyond.</p></header>
  <section class="memorial"><p class="me-cross">✝ In Loving Memory</p><h2>Charles Juan Jeremy Perez</h2><p>Brother · Trainer · WUW Family. The heart and soul of WUW. His spirit, heart, and love for this sport will never be forgotten. Rest easy, brother.</p></section>
  <div class="al-grid">{cards}</div>
</div></main>
''' + footer()

def render_roster():
    if ROSTER_PHOTOS:
        cards = []
        for r in ROSTER_PHOTOS:
            name = r.get('name') or ''
            name_html = f'<h3>{H.escape(name)}</h3>' if name and not name.startswith('cooltext') else ''
            cards.append(f'<article class="al-card"><div class="al-img"><img src="{H.escape(r["img"])}" alt="{H.escape(name or "WUW Roster")}" loading="lazy"></div>{name_html}</article>')
        body = '<div class="al-grid">' + ''.join(cards) + '</div>'
    else:
        body = '<ul class="roster-list">' + ''.join(f'<li>{H.escape(n)}</li>' for n in ROSTER) + '</ul>'
    return head('Current Roster · WUW Brooklyn', "Current WUW roster — wrestlers training at Gleason's Gym Brooklyn under Johnny Rodz.", 'https://wuwonline.com/roster/') + f'''
<main class="page"><div class="page-frame">
  <header class="page-head"><p class="ps-eyebrow">{len(ROSTER_PHOTOS) or len(ROSTER)} on the active roster</p><h1 class="page-h">Roster</h1><p class="page-lede">The wrestlers training and competing under WUW today.</p></header>
  {body}
  <p class="rl-foot">Want to see your face here? <a href="/contact/" class="link-cta">Start training →</a></p>
</div></main>
''' + footer()

def render_titles():
    titles = [
        ('WUW World Heavyweight', 'PJ Savage'), ('WUW Womens Championship', 'Jada Rose'),
        ('WUW Light Heavyweight', 'J Bushii'), ('WUW NY State', 'Jesse Lebron of Distrubia'),
        ('WUW North American', 'The Fireball Carlos'), ('WUW Tag Team', 'The Faceless Ones'),
        ('WUW Rumbo in DUMBO', 'Irish Bruce'),
    ]
    rows = ''.join(f'<li><span class="tt-belt">{H.escape(b)}</span><span class="tt-holder">{H.escape(h)}</span></li>' for b, h in titles)
    return head('WUW Champions · Title Holders', 'Current WUW championship title holders across all divisions.', 'https://wuwonline.com/title-holders/') + f'''
<main class="page"><div class="page-frame">
  <header class="page-head"><p class="ps-eyebrow">Titleholders</p><h1 class="page-h">Champions</h1></header>
  <ul class="title-list">{rows}</ul>
  <p class="rl-foot small">Note: as of 4/23/22 some titles are vacant pending the next set of shows.</p>
</div></main>
''' + footer()

def render_events():
    return head('WUW Events · Live Pro Wrestling Brooklyn', "Live professional wrestling shows from WUW — featuring wrestlers trained by Johnny Rodz at Gleason's Gym Brooklyn.", 'https://wuwonline.com/events/') + f'''
<main class="page"><div class="page-frame">
  <header class="page-head"><p class="ps-eyebrow">Live shows</p><h1 class="page-h">Events</h1><p class="page-lede">Showcases for the wrestlers trained by Johnny Rodz — full storylines, championship matches, and special guests.</p></header>
  <section class="ev-card"><h2>Stay current on dates</h2><p>Follow WUW on Facebook for upcoming event dates, venues, and results.</p><a class="btn-primary" href="https://www.facebook.com/WorldofUnpredictableWrestling" target="_blank" rel="noopener">Follow on Facebook</a></section>
  <section class="ev-card"><h2>Want to compete?</h2><p>Train with Johnny Rodz and earn your spot on a WUW card.</p><a class="btn-primary" href="/contact/">Start Training</a></section>
  <section class="ev-card"><h2>Bookings &amp; sponsorships</h2><p>For event bookings, sponsorship, or to work with WUW talent — call <a href="tel:7187972872">{PHONE}</a>.</p></section>
</div></main>
''' + footer()

def render_about():
    return head("About WUW · Johnny Rodz · Gleason's Gym", "World of Unpredictable Wrestling — Brooklyn's home of professional wrestling training. Founded by WWE Hall of Famer Johnny Rodz.", 'https://wuwonline.com/about/') + f'''
<main class="page"><div class="page-frame">
  <header class="page-head"><p class="ps-eyebrow">Our story</p><h1 class="page-h">About WUW</h1></header>
  <section class="ab-grid">
    <div class="ab-photo"><img src="/img/about.jpg" alt="Johnny Rodz"/></div>
    <div class="ab-body">
      <p>World of Unpredictable Wrestling was founded by <strong>Johnny Rodz</strong> — born José Rodriguez — a Brooklyn native whose career in professional wrestling spanned four decades. After competing on the MSG circuit and throughout the WWF, Rodz turned his attention to building the next generation of professional wrestlers.</p>
      <p>The school has called <strong>Gleason's Gym</strong> home for years — at <strong>130 Water Street in Brooklyn</strong>, directly under the Brooklyn Bridge. Gleason's is one of the most storied athletic training facilities in the world.</p>
      <p>WUW has trained <strong>over 400 professional wrestlers</strong> who have gone on to compete in WWE, NXT, AEW, Impact, ROH, and independent promotions worldwide.</p>
      <p>The WUW family — known as <em>"Da Wheel"</em> — is a brotherhood and sisterhood that supports each other throughout their careers.</p>
    </div>
  </section>
  <section class="ab-quote">"When you train here, you learn the real thing. The same fundamentals that trained Tazz, Tommy Dreamer, and D-Von. Hard work, respect, and ring psychology."<cite>— Johnny Rodz</cite></section>
</div></main>
''' + footer()

def render_contact():
    sched = ''.join(f'<li><span>{d}</span><span>{t}</span></li>' for d, t in SCHEDULE)
    return head('Contact WUW · Train at Gleason\'s Gym', f'Reach Johnny Rodz directly. Call {PHONE}, email, or use the contact form. Gleason\'s Gym, 130 Water Street, Brooklyn.', 'https://wuwonline.com/contact/') + f'''
<main class="page"><div class="page-frame">
  <header class="page-head"><p class="ps-eyebrow">Reach out</p><h1 class="page-h">Contact</h1><p class="page-lede">Ready to train? Have a question? Reach out directly — we respond to everyone.</p></header>
  <div class="ct-grid">
    <div class="ct-card"><p class="ct-h">📞 Call</p><a class="ct-big" href="tel:7187972872">{PHONE}</a><p class="ct-d">Ask for Johnny Rodz</p></div>
    <div class="ct-card"><p class="ct-h">📧 Email</p><a class="ct-big" href="mailto:{EMAIL}">{EMAIL}</a></div>
    <div class="ct-card"><p class="ct-h">📍 Visit</p><p class="ct-big" style="font-size:22px">{ADDR_LINE_1}</p><p class="ct-d">{ADDR_LINE_2}</p></div>
    <div class="ct-card"><p class="ct-h">📅 Training Schedule</p><ul class="sch-list">{sched}</ul></div>
  </div>

  <section class="ct-form-wrap" id="form">
    <h2 class="ct-form-h">Send a message</h2>
    <p class="ct-form-sub">Goes straight to Johnny's inbox. Usually answered within 24 hours.</p>
    <form class="ct-form" action="https://formsubmit.co/{EMAIL}" method="POST">
      <input type="hidden" name="_subject" value="WUW website inquiry"/>
      <input type="hidden" name="_template" value="table"/>
      <input type="hidden" name="_captcha" value="false"/>
      <input type="hidden" name="_next" value="https://wuwonline.com/contact/?sent=1"/>
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off"/>
      <div class="ct-row">
        <label><span>Name</span><input type="text" name="name" required autocomplete="name"/></label>
        <label><span>Email</span><input type="email" name="email" required autocomplete="email"/></label>
      </div>
      <label><span>Phone (optional)</span><input type="tel" name="phone" autocomplete="tel"/></label>
      <label><span>What's this about?</span>
        <select name="topic" required>
          <option value="">Choose one…</option>
          <option>Training — I want to start</option>
          <option>Booking / Show / Event</option>
          <option>Press / Interview</option>
          <option>Sponsorship</option>
          <option>Other</option>
        </select>
      </label>
      <label><span>Message</span><textarea name="message" rows="5" required placeholder="Tell us a little about what you're looking for…"></textarea></label>
      <button type="submit" class="ct-submit">Send to Johnny</button>
      <p class="ct-fine">Your info goes to {EMAIL} only. No marketing list, no spam.</p>
    </form>
    <div class="ct-sent" id="ct-sent" hidden>✓ Thanks — your message is on its way to Johnny. Expect a reply within a day.</div>
  </section>

  <p class="rl-foot">Open to everyone. Men and women. All experience levels welcome.</p>
</div></main>
<script>if(location.search.indexOf('sent=1')>-1){{var el=document.getElementById('ct-sent');if(el)el.hidden=false;el&&el.scrollIntoView({{behavior:'smooth',block:'center'}});}}</script>
''' + footer()

OUTLETS = {
    'mondaynightwrestling.com': ('Monday Night Wrestling', '#0a0a0a', '#ffd700'),
    'fox5ny.com':               ('Fox 5 NY',          '#003c71', '#ffffff'),
    'fox29.com':                ('Fox 29',            '#003c71', '#ffffff'),
    'newsweek.com':             ('Newsweek',          '#f72717', '#ffffff'),
    'newsbreak.com':            ('NewsBreak',         '#ee2944', '#ffffff'),
    'gettyimages.com':          ('Getty Images',      '#000000', '#ffffff'),
    'spotify.com':              ('Spotify · Podcast', '#1ed760', '#0a0a0a'),
    'open.spotify.com':         ('Spotify · Podcast', '#1ed760', '#0a0a0a'),
}

def yt_id_from(url):
    m = re.search(r'(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|shorts/))([A-Za-z0-9_-]{6,15})', url)
    return m.group(1) if m else ''

def news_card(L):
    url = L.get('url') or ''
    anchor = (L.get('anchor') or '').strip()
    host = url.split('://',1)[-1].split('/',1)[0].replace('www.','').replace('m.','').lower()
    yt = yt_id_from(url)
    kind, bg, fg = OUTLETS.get(host, (host, '#1a1a1a', '#f4f0e8'))
    if yt:
        kind = 'YouTube · Video'
        media = f'<div class="nc-media nc-media-yt"><img src="https://img.youtube.com/vi/{yt}/hqdefault.jpg" alt="" loading="lazy"/><span class="nc-play" aria-hidden="true">&#9658;</span></div>'
    elif 'spotify' in host:
        media = f'<div class="nc-media nc-media-badge" style="background:{bg};color:{fg}"><span class="nc-badge-mark">&#9654;</span><span class="nc-badge-name">Spotify</span></div>'
    elif 'gettyimages' in host:
        media = f'<div class="nc-media nc-media-badge" style="background:{bg};color:{fg}"><span class="nc-badge-name" style="font-family:Georgia,serif;font-style:italic">Getty</span></div>'
    else:
        fav = f'https://www.google.com/s2/favicons?domain={host}&sz=128'
        media = f'<div class="nc-media nc-media-badge" style="background:{bg};color:{fg}"><img class="nc-fav" src="{fav}" alt="" loading="lazy" onerror="this.style.display=\'none\'"/><span class="nc-badge-name">{H.escape(kind)}</span></div>'
    title = anchor or kind
    return f'''<a class="news-card" href="{H.escape(url)}" target="_blank" rel="noopener">
      {media}
      <div class="nc-body">
        <span class="nc-kind">{H.escape(kind)}</span>
        <h3 class="nc-title">{H.escape(title[:140])}</h3>
        <span class="nc-host">{H.escape(host)}<span class="nc-arrow" aria-hidden="true">&rarr;</span></span>
      </div>
    </a>'''

def render_news():
    seen, links = set(), []
    for L in (yt_spotify_links + press_links + mnw_links):
        u = (L.get('url') or '').split('?')[0]
        if u and u not in seen:
            seen.add(u); links.append(L)
    yt_count    = sum(1 for L in links if yt_id_from(L.get('url','')))
    pod_count   = sum(1 for L in links if 'spotify' in (L.get('url','') or ''))
    press_count = len(links) - yt_count - pod_count
    cards = ''.join(news_card(L) for L in links)
    return head('WUW In the News · Press', "WUW press coverage on Monday Night Wrestling, Fox 5, podcasts and interviews featuring Johnny Rodz, alumni, and the Brooklyn wrestling scene.", 'https://wuwonline.com/in-the-news/') + f'''
<main class="page news-page">
  <header class="page-head">
    <p class="ps-eyebrow">Press &amp; mentions · {len(links)} pieces</p>
    <h1 class="page-h">In the News</h1>
    <p class="page-lede">Press, podcasts, and video featuring WUW, Johnny Rodz, and the alumni network.</p>
    <div class="news-meta"><span><strong>{press_count}</strong> press pieces</span><span><strong>{yt_count}</strong> videos</span><span><strong>{pod_count}</strong> podcast episodes</span></div>
  </header>
  <section class="news-grid">{cards}</section>
</main>
''' + footer()

def render_rodz():
    body = page_body('/johnny-rodz/')
    bio_facts = '''
<h2>The Career</h2>
<p>Born <strong>José Rodriguez</strong> in New York City, &#8220;The Unpredictable&#8221; Johnny Rodz came up through Antonino &#8220;Argentina&#8221; Rocca&#8217;s school in the 1960s — one of the same lineages that produced an entire generation of Latino professional wrestlers in the New York territory.</p>
<p>He spent <strong>nearly two decades</strong> on the World Wide Wrestling Federation / WWF roster, wrestling out of Madison Square Garden through the &#8217;70s and into the mid-&#8217;80s. He shared the ring with <strong>Bruno Sammartino, Bob Backlund, Pat Patterson, Tony Garea, Pedro Morales, Andre the Giant</strong> and most of the era&#8217;s headliners.</p>
<p>His character was simple and unforgettable: <em>he&#8217;d do anything to win.</em> Eye rakes, foreign objects, refusing to break a hold — anything. The &#8220;unpredictable&#8221; nickname stuck because the audience genuinely never knew what he was about to pull. He was the <strong>blueprint for the heel-with-no-rules archetype</strong> that ECW and AEW would later make the centre of the sport.</p>
<h2>WWE Hall of Fame · 1996</h2>
<p>Inducted into the <strong>WWE Hall of Fame in 1996</strong> — the second class ever inducted, alongside Bobo Brazil, Ernie Ladd, Killer Kowalski and others. The induction recognised what the locker room had known for decades: that Rodz had spent his career making <em>other</em> people look like a million dollars, and that the business runs on people who can do exactly that.</p>
<h2>The School at Gleason&#8217;s Gym</h2>
<p>After hanging up the boots, Rodz turned full-time to training. He set up at <strong>Gleason&#8217;s Gym in Brooklyn</strong> — 130 Water Street, under the Brooklyn Bridge — the most storied athletic gym in the city, the same building that produced world-champion boxers for half a century.</p>
<p>From that ring he&#8217;s trained <strong>over 400 professional wrestlers</strong> across four decades. The list reads like a who&#8217;s-who of late-&#8217;90s/&#8217;00s pro wrestling:</p>
<ul>
  <li><strong>Tazz</strong> &mdash; ECW World Heavyweight Champion, WWE</li>
  <li><strong>Tommy Dreamer</strong> &mdash; ECW Hall of Fame, &#8220;Innovator of Violence&#8221;</li>
  <li><strong>D-Von Dudley</strong> &mdash; WWE Hall of Fame, Dudley Boyz</li>
  <li><strong>Big Cass</strong> (William Morrissey) &mdash; WWE main event run</li>
  <li><strong>Masha Slamovich</strong> &mdash; TNA, WWE NXT</li>
  <li><strong>Vince Russo</strong> &mdash; WCW &amp; WWE head writer</li>
  <li><strong>Matt Striker</strong> &mdash; WWE commentator and wrestler</li>
  <li><strong>Marti Belle, Prince Nana, Big Vito, Will Ferrara, Nicole Bass</strong> and 380+ more.</li>
</ul>
<h2>Why he matters</h2>
<p>You can count the active full-time pro-wrestling trainers in the world on two hands. You can count the ones who are also <em>WWE Hall of Famers</em> on a single finger. The reason WUW alumni keep showing up on RAW, SmackDown, Dynamite and Impact isn&#8217;t because Rodz teaches a flashy moveset &mdash; it&#8217;s because he teaches the <strong>fundamentals</strong> the modern game forgot: bumping, ring psychology, story-telling, locker-room respect.</p>
<p>If you&#8217;re serious about wrestling for a living, this is where it starts.</p>
<p class="rodz-cta-line"><a href="/contact/">Train with Johnny &rarr;</a> &nbsp; · &nbsp; <a href="/alumni/">See the alumni roll &rarr;</a></p>
'''
    extra = body if body and len(body) > 200 else ''
    return head("The Unpredictable Johnny Rodz · WWE Hall of Famer · WUW Founder", "The Unpredictable Johnny Rodz — born José Rodriguez. WWE Hall of Fame Class of 1996. Founder of World of Unpredictable Wrestling at Gleason's Gym Brooklyn. Trained 400+ professional wrestlers including Tazz, Tommy Dreamer, D-Von Dudley, Big Cass, Masha Slamovich.", 'https://wuwonline.com/johnny-rodz/') + f'''
<main class="page rodz-page">
  <section class="rodz-hero">
    <picture class="rodz-hero-image" aria-hidden="true"><img src="/img/meet-johnny.jpg" alt="" loading="eager"/></picture>
    <div class="rodz-hero-veil"></div>
    <div class="rodz-hero-frame">
      <p class="ps-eyebrow">WWE Hall of Fame · Class of 1996</p>
      <h1 class="rodz-h"><em>The Unpredictable</em> Johnny Rodz</h1>
      <p class="rodz-sub">Born José Rodriguez · MSG-circuit veteran · Brooklyn trainer · founder of WUW.</p>
    </div>
  </section>
  <div class="page-frame rodz-body">{bio_facts}</div>
  {('<section class="wp-extra"><div class="wp-extra-frame"><h2 class="wp-extra-h">Notes from the WUW archive</h2><div class="wp-extra-body">' + extra + '</div></div></section>') if extra else ''}
</main>
''' + footer()


def render_israel_joffe():
    """Aggregator page for /israel-joffe/ — bio + linked grid of every dated israel-joffe* post + DocumentCloud + Substack backlinks. Off nav."""
    canonical = 'https://wuwonline.com/israel-joffe/'
    # gather every post whose URL contains 'israel-joffe' or 'juanito'
    ij_posts = [p for p in posts if any(k in p['url'].lower() for k in ('israel-joffe','juanito'))]
    # newest first
    ij_posts.sort(key=lambda p: p['date'], reverse=True)
    posts_grid = ''.join(
        f'<a class="ij-post" href="{H.escape(post_url(p))}"><span class="ij-date">{H.escape(p["date"][:10])}</span><span class="ij-title">{H.escape(p.get("title") or post_url(p).strip("/").split("/")[-1].replace("-"," ").title())}</span></a>'
        for p in ij_posts
    )
    dc_items = ''.join(
        f'<li><a href="{H.escape(u)}" target="_blank" rel="noopener nofollow">{H.escape(label)}</a></li>'
        for u, label in DOCUMENTCLOUD
    )
    sub_items = ''.join(
        f'<li><a href="{H.escape(u)}" target="_blank" rel="noopener me">{H.escape(label)}</a></li>'
        for u, label in SUBSTACKS
    )
    return head(
        'Israel Joffe · WUW · Gleason\'s Gym Training Archive',
        'Israel Joffe at WUW — training archive, DocumentCloud research filings (Atlantic City, Lubavitcher Rebbe letter, FDIC), Substack writing, and his personal site network. Years of dated posts from inside Gleason\'s Gym.',
        canonical,
    ) + f'''
<main class="page ij-page">
  <header class="page-head ij-head">
    <p class="ps-eyebrow">WUW Family · Training Archive</p>
    <h1 class="page-h">Israel Joffe</h1>
    <p class="page-lede">A long-running training archive — Israel Joffe inside Gleason's Gym alongside the WUW family, plus the DocumentCloud and Substack writing he's published over the same years.</p>
  </header>

  <div class="page-frame ij-body">
    <section class="ij-bio">
      <h2>About</h2>
      <p>Israel Joffe is a New York–based media executive, IT specialist, and FDIC-credentialed firefighter whose work has appeared in <strong>Fox 5</strong>, <strong>Newsweek</strong>, <strong>Fox 29</strong>, and <strong>NewsBreak</strong>. He's been training at Gleason's Gym alongside the WUW family for years — the dated entries below are field reports from those sessions and the related coverage that came out of them.</p>
      <p>For the full picture of his work outside the ring, his editorial home is <a href="https://israeljoffe.com" target="_blank" rel="noopener">israeljoffe.com</a> (media, press, IT) and the BJJ-and-fitness side is at <a href="https://israeljoffe.org" target="_blank" rel="noopener">israeljoffe.org</a>.</p>
    </section>

    <section class="ij-archive">
      <h2>WUW Archive · Israel Joffe entries</h2>
      <p class="ij-archive-meta">{len(ij_posts)} dated posts · newest first</p>
      <div class="ij-grid">{posts_grid}</div>
    </section>

    <section class="ij-refs">
      <h2>Research filings · DocumentCloud</h2>
      <p>Public document filings tagged Israel Joffe — kept on DocumentCloud as a permanent research record.</p>
      <ul class="ij-link-list">{dc_items}</ul>

      <h2>Long-form · Substack</h2>
      <ul class="ij-link-list">{sub_items}</ul>
    </section>
  </div>
</main>
''' + footer()


def render_network_article(fed):
    """One short SEO article per federation site — /network/{slug}/. Off nav, in sitemap."""
    canonical = f"https://wuwonline.com/network/{fed['slug']}/"
    title = f"{fed['name']} · Across the WUW Network"
    return head(title, fed['lede'], canonical) + f'''
<main class="page net-article">
  <header class="page-head">
    <p class="ps-eyebrow">Across the network · {H.escape(fed['tag'])}</p>
    <h1 class="page-h">{H.escape(fed['name'])}</h1>
    <p class="page-lede">{H.escape(fed['lede'])}</p>
  </header>
  <div class="page-frame net-body">
    {fed['body']}
    <p class="net-cta"><a class="link-cta" href="https://{fed['host']}" target="_blank" rel="noopener">Visit {H.escape(fed['host'])} &rarr;</a></p>
    <hr class="net-rule"/>
    <p class="net-foot"><a href="/israel-joffe/">Back to Israel Joffe at WUW</a> · <a href="/">WUW home</a></p>
  </div>
</main>
''' + footer()

def render_post(p):
    body = rewrite(p.get('body_html', ''))
    canonical = f'https://wuwonline.com{post_url(p)}'
    desc = (p.get('description') or H.unescape(re.sub(r'<[^>]+>', ' ', body)).strip())[:200] or p['title']
    hero = p.get('hero')
    og = f'https://wuwonline.com{img_map.get((hero or "").split("?")[0], hero)}' if hero else None
    return head(p['title'] + ' · WUW', desc, canonical, og,
                og_type='article', published=p.get('date'), modified=p.get('date'), post_title=p['title']) + f'''
<main class="post-page"><article class="post">
  <header class="post-head">
    {f'<p class="post-date">{p["date"]}</p>' if p.get('date') else ''}
    <h1 class="post-title">{H.escape(p['title'])}</h1>
  </header>
  <div class="post-body">{body}</div>
  <footer class="post-foot"><a href="/" class="link-back">← Home</a></footer>
</article></main>
''' + footer()

def render_styles():
    return ''':root{--bg:#0a0a0a;--ink:#0a0a0a;--bone:#f4f0e8;--bone-soft:#e8e1cf;--accent:#d2222d;--gold:#d4a73a;--rule:#2a2a2a;--display:"Anton","Bebas Neue",Impact,sans-serif;--display2:"Bebas Neue",Impact,sans-serif;--sans:"Inter",system-ui,sans-serif;--frame-pad:clamp(20px,5vw,72px);--max:1280px}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bone);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block}a{color:inherit;text-decoration:none}ul,ol{list-style:none}
.masthead{position:fixed;top:0;left:0;right:0;display:flex;align-items:center;justify-content:space-between;padding:14px var(--frame-pad);z-index:50;color:var(--bone);background:rgba(10,10,10,.96);border-bottom:2px solid var(--accent);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.wordmark{display:inline-flex;align-items:center;gap:14px;color:var(--bone)}
.wm-logo{height:80px;width:auto;display:block;filter:drop-shadow(0 4px 12px rgba(0,0,0,.5))}
.wm-tag{font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:rgba(244,240,232,.6);font-weight:600}
.primary{display:flex;gap:clamp(10px,1.4vw,20px);font-family:var(--display2);font-size:14px;letter-spacing:.16em;text-transform:uppercase}
.primary a{color:#efebe3;padding:8px 4px;transition:color .25s}
.primary a:hover{color:var(--accent)}
.primary-cta{background:var(--accent);color:var(--bone)!important;padding:10px 20px!important}
.primary-cta:hover{background:#a01820}
.menu-toggle{display:none;width:48px;height:48px;background:transparent;border:1px solid rgba(244,240,232,.5);align-items:center;justify-content:center;flex-direction:column;gap:6px;cursor:pointer;padding:0}
.menu-toggle span{display:block;width:22px;height:2px;background:var(--bone);transition:transform .3s}
.menu-open .menu-toggle span:nth-child(1){transform:translateY(8px) rotate(45deg)}
.menu-open .menu-toggle span:nth-child(2){opacity:0}
.menu-open .menu-toggle span:nth-child(3){transform:translateY(-8px) rotate(-45deg)}
.mobile-nav{position:fixed;top:0;left:0;right:0;height:100vh;height:100dvh;z-index:49;background:rgba(10,10,10,.98);opacity:0;visibility:hidden;transition:opacity .32s,visibility .32s;overflow-y:auto;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.menu-open .mobile-nav{opacity:1;visibility:visible}
.menu-open{overflow:hidden}
.mobile-nav-inner{padding:calc(env(safe-area-inset-top,0) + 88px) 28px 40px;max-width:480px;margin:0 auto;display:flex;flex-direction:column}
.mobile-nav a{font-family:var(--display);font-size:32px;color:var(--bone);padding:18px 0;border-bottom:1px solid rgba(244,240,232,.1);letter-spacing:.04em}
.mobile-nav a:hover{color:var(--accent)}
.mobile-nav-fine{margin-top:24px;font-size:14px}
.mobile-nav-fine a{font-size:14px!important;border:none!important;padding:8px 0!important;color:rgba(244,240,232,.7)!important;font-family:var(--sans)!important}
.hero{position:relative;min-height:clamp(480px,72vh,640px);display:flex;align-items:center;background:#000;overflow:hidden;color:var(--bone)}
.hero-image{position:absolute;inset:0;z-index:0}
.hero-image img{width:100%;height:100%;object-fit:cover;filter:saturate(.7) contrast(1.15) brightness(.6)}
.hero-veil{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,.5),rgba(0,0,0,.1) 30%,rgba(0,0,0,.6) 65%,rgba(0,0,0,.92)),linear-gradient(90deg,rgba(0,0,0,.7),rgba(0,0,0,.05) 40%,transparent)}
.hero-frame{position:relative;z-index:2;max-width:var(--max);margin:0 auto;padding:clamp(96px,12vh,140px) var(--frame-pad) clamp(40px,6vh,64px);width:100%}
.hero-eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--gold);background:rgba(0,0,0,.55);padding:9px 18px;border:1px solid rgba(212,167,58,.45);margin-bottom:32px;font-weight:600}
.hero-eyebrow .dot{display:inline-block;width:4px;height:4px;border-radius:50%;background:var(--accent)}
.hero-title{font-family:var(--display);text-transform:uppercase;font-size:clamp(48px,9vw,118px);line-height:.92;color:var(--bone);margin-bottom:24px;text-shadow:0 4px 32px rgba(0,0,0,.7)}
.ht-1,.ht-2,.ht-3{display:block}
.ht-2{padding-left:.4em;font-size:.7em;color:rgba(244,240,232,.7)}
.ht-3 em{font-style:normal;color:var(--accent);text-shadow:0 4px 32px rgba(210,34,45,.4)}
.hero-sub{font-size:clamp(16px,1.6vw,21px);line-height:1.55;color:rgba(244,240,232,.92);max-width:60ch;text-shadow:0 1px 8px rgba(0,0,0,.7);margin-bottom:32px}
.hero-cta-row{display:flex;flex-wrap:wrap;gap:14px}
.btn-primary{display:inline-flex;align-items:center;gap:10px;background:var(--accent);color:var(--bone);font-family:var(--display);font-size:18px;letter-spacing:.08em;text-transform:uppercase;padding:18px 32px;border:none;cursor:pointer;transition:background .25s,transform .25s}
.btn-primary:hover{background:#a01820;transform:translateY(-2px)}
.btn-ghost{display:inline-flex;align-items:center;gap:10px;color:var(--bone);font-size:14px;font-weight:600;letter-spacing:.04em;padding:18px 24px;border:1px solid rgba(244,240,232,.4);background:transparent;transition:border-color .25s,color .25s}
.btn-ghost:hover{border-color:var(--gold);color:var(--gold)}
.link-cta{display:inline-flex;font-family:var(--display);font-size:18px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);border-bottom:2px solid currentColor;padding-bottom:4px}
.link-back{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink);border-bottom:1px solid currentColor;padding-bottom:2px}
.alumni-strip{padding:clamp(36px,5vh,56px) var(--frame-pad);text-align:center;background:#000;color:var(--bone)}
.ps-eyebrow{font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);margin-bottom:18px;font-weight:600}
.al-row{font-family:var(--display);font-size:clamp(20px,2.6vw,34px);line-height:1.2;color:var(--bone);text-transform:uppercase;letter-spacing:.04em;display:flex;flex-wrap:wrap;justify-content:center;gap:.4em 1em;max-width:1100px;margin:0 auto}
.al-more{margin-top:24px;font-size:13px}
.al-more a{color:var(--accent);font-weight:600;letter-spacing:.06em;text-transform:uppercase;border-bottom:1px solid currentColor}
.creds{padding:clamp(64px,9vh,100px) var(--frame-pad);background:var(--bone-soft);text-align:center}
.sec-h{font-family:var(--display);font-size:clamp(28px,4vw,48px);text-transform:uppercase;color:var(--ink);margin-bottom:28px}
.cred-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:32px;max-width:var(--max);margin:0 auto}
.cred{padding:32px 24px;background:var(--bone);border-top:4px solid var(--accent);text-align:center}
.cr-num{display:block;font-family:var(--display);font-size:clamp(44px,5.5vw,72px);color:var(--accent);line-height:1;margin-bottom:14px}
.cr-h{display:block;font-family:var(--display);font-size:22px;text-transform:uppercase;color:var(--ink);margin-bottom:8px}
.cr-d{display:block;font-size:14px;color:var(--ink);opacity:.7}
.learn{padding:clamp(64px,10vh,120px) var(--frame-pad);background:var(--bone)}
.lr-grid{max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:clamp(40px,6vw,80px);align-items:center}
.lr-img{aspect-ratio:4/5;overflow:hidden;background:var(--ink)}
.lr-img img{width:100%;height:100%;object-fit:cover;filter:contrast(1.05) saturate(.9)}
.lr-list{display:grid;gap:16px;margin:24px 0;font-size:17px;line-height:1.55}
.lr-list li{padding-left:24px;position:relative}
.lr-list li::before{content:"";position:absolute;left:0;top:.7em;width:14px;height:2px;background:var(--accent)}
.contact-cta{padding:clamp(72px,10vh,120px) var(--frame-pad);background:var(--ink);color:var(--bone);text-align:center}
.contact-cta .sec-h{color:var(--bone)}
.cc-sub{font-size:18px;line-height:1.55;color:rgba(244,240,232,.85);max-width:560px;margin:0 auto 48px}
.cc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px;max-width:1080px;margin:0 auto}
.cc-card{padding:32px 24px;background:rgba(244,240,232,.06);border:1px solid rgba(244,240,232,.12);text-align:center}
.cc-h{font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);margin-bottom:14px;font-weight:600}
.cc-v{font-family:var(--display);font-size:clamp(24px,2.6vw,34px);color:var(--bone);line-height:1.1;margin-bottom:8px}
.cc-v.sm{font-size:20px;margin-bottom:2px}
.cc-v a{color:var(--bone);transition:color .25s}
.cc-v a:hover{color:var(--accent)}
.cc-d{font-size:13px;color:rgba(244,240,232,.65)}
.page{padding-top:0}
.page-frame{max-width:var(--max);margin:0 auto;padding:clamp(120px,16vh,160px) var(--frame-pad) clamp(80px,10vh,120px)}
.page-head{text-align:center;margin-bottom:64px;padding-bottom:36px;border-bottom:2px solid var(--accent)}
.page-h{font-family:var(--display);font-size:clamp(40px,6vw,80px);text-transform:uppercase;color:var(--ink);line-height:.95;margin-bottom:16px}
.page-lede{font-size:18px;line-height:1.5;color:var(--ink);opacity:.75;max-width:60ch;margin:0 auto}
.al-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
.al-card{padding:0;background:var(--bone-soft);border-left:4px solid var(--accent);overflow:hidden;display:flex;flex-direction:column;transition:transform .35s,box-shadow .35s}
.al-card:hover{transform:translateY(-3px);box-shadow:0 18px 40px -22px rgba(0,0,0,.45)}
.al-img{aspect-ratio:1/1;overflow:hidden;background:var(--ink);position:relative}
.al-img img{width:100%;height:100%;object-fit:cover;object-position:center top;filter:saturate(.92) contrast(1.06);transition:transform .9s}
.al-card:hover .al-img img{transform:scale(1.06)}
.al-card h3{font-family:var(--display);font-size:18px;text-transform:uppercase;color:var(--ink);padding:14px 16px 16px;line-height:1.1;letter-spacing:.02em}
.wp-extra{background:#000;color:var(--bone);padding:64px 0;border-top:2px solid var(--accent)}
.wp-extra-frame{max-width:var(--max);margin:0 auto;padding:0 var(--frame-pad)}
.wp-extra-h{font-family:var(--display);font-size:32px;text-transform:uppercase;color:var(--gold);margin-bottom:32px;text-align:center;letter-spacing:.04em}
.wp-extra-body{font-size:15px;line-height:1.7;color:rgba(244,240,232,.85);max-width:920px;margin:0 auto}
.wp-extra-body h1,.wp-extra-body h2{font-family:var(--display);text-transform:uppercase;color:var(--bone);margin:1.5em 0 .5em;letter-spacing:.02em}
.wp-extra-body h2{font-size:24px}
.wp-extra-body h3{font-family:var(--display);font-size:18px;color:var(--accent);margin:1.2em 0 .4em;text-transform:uppercase}
.wp-extra-body p{margin-bottom:1em}
.wp-extra-body img{max-width:100%;height:auto;margin:18px 0;border:1px solid rgba(244,240,232,.1)}
.wp-extra-body a{color:var(--accent);border-bottom:1px solid currentColor}
.wp-extra-body figure{margin:20px 0}
.wp-extra-body figcaption{font-size:12px;color:rgba(244,240,232,.55);margin-top:6px;font-style:italic}
.wp-extra-body ul,.wp-extra-body ol{margin:1em 0;padding-left:1.4em}
.wp-extra-body ul li,.wp-extra-body ol li{margin-bottom:.4em;list-style:disc}
/* Portal homepage — KetiService-style template adapted for WUW */
.portal{padding-top:0}
.ph-hero{position:relative;min-height:clamp(540px,82vh,720px);display:flex;align-items:center;justify-content:center;background:#000;overflow:hidden;isolation:isolate;text-align:center;color:var(--bone)}
.ph-image{position:absolute;inset:0;z-index:0}
.ph-image img{width:100%;height:100%;object-fit:cover;object-position:center 30%;filter:saturate(.7) contrast(1.15) brightness(.55);animation:phZoom 24s ease-in-out infinite alternate}
@keyframes phZoom{0%{transform:scale(1.02)}100%{transform:scale(1.14) translate(-1.5%,-1.5%)}}
.ph-veil{position:absolute;inset:0;z-index:1;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,.4) 0%,rgba(0,0,0,.7) 60%,rgba(0,0,0,.95)),linear-gradient(180deg,rgba(0,0,0,.45),rgba(0,0,0,.85))}
.ph-frame{position:relative;z-index:2;max-width:1080px;margin:0 auto;padding:clamp(120px,16vh,160px) var(--frame-pad) clamp(48px,6vh,72px)}
.ph-eyebrow{display:inline-flex;align-items:center;gap:14px;font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--gold);background:rgba(0,0,0,.55);padding:9px 18px;border:1px solid rgba(212,167,58,.4);margin-bottom:32px;font-weight:600;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.ph-eyebrow .rule{display:inline-block;width:28px;height:1px;background:var(--accent)}
.ph-title{font-family:var(--display);text-transform:uppercase;font-size:clamp(54px,9.5vw,128px);line-height:.92;letter-spacing:-.005em;color:var(--bone);margin-bottom:28px;text-shadow:0 4px 32px rgba(0,0,0,.7)}
.ph-line{display:block;overflow:hidden;padding-bottom:.04em}
.ph-word{display:inline-block;opacity:0;transform:translateY(110%) skew(0deg,2deg);animation:phWordRise 1.05s cubic-bezier(.2,.7,.2,1) forwards;will-change:transform,opacity}
.ph-w1{animation-delay:.30s}
.ph-w2{animation-delay:.50s;font-size:.55em;color:rgba(244,240,232,.78);letter-spacing:.04em}
.ph-w3{animation-delay:.72s}
.ph-em{color:var(--accent);text-shadow:0 4px 32px rgba(210,34,45,.4)}
@keyframes phWordRise{0%{opacity:0;transform:translateY(110%) skew(0deg,2deg)}60%{opacity:1}100%{opacity:1;transform:translateY(0) skew(0,0)}}
.ph-sub{font-family:var(--sans);font-size:clamp(16px,1.6vw,21px);line-height:1.55;color:rgba(244,240,232,.92);max-width:60ch;margin:0 auto;text-shadow:0 1px 8px rgba(0,0,0,.65)}
.ph-sub em{font-style:normal;color:var(--gold);font-weight:600}

/* Three-card portal grid */
.pc-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(14px,1.6vw,24px);padding:clamp(40px,6vh,72px) var(--frame-pad) clamp(72px,10vh,120px);max-width:var(--max);margin:0 auto;background:var(--bone)}
.pc-card{position:relative;display:block;aspect-ratio:3/4;overflow:hidden;background:var(--ink);color:var(--bone);text-decoration:none;transition:transform .5s cubic-bezier(.2,.7,.2,1),box-shadow .4s;isolation:isolate;min-height:460px}
.pc-card:hover{transform:translateY(-6px);box-shadow:0 30px 60px -28px rgba(0,0,0,.55)}
.pc-img{position:absolute;inset:0;z-index:0}
.pc-img img{width:100%;height:100%;object-fit:cover;transition:transform 1.4s cubic-bezier(.2,.7,.2,1);filter:saturate(.85) contrast(1.1) brightness(.7)}
.pc-card:hover .pc-img img{transform:scale(1.08)}
.pc-veil{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,.15) 35%,rgba(0,0,0,.65) 70%,rgba(0,0,0,.96) 100%)}
.pc-train .pc-veil{background:linear-gradient(180deg,rgba(0,0,0,.4) 0%,rgba(0,0,0,.15) 35%,rgba(60,10,15,.7) 75%,rgba(0,0,0,.96) 100%)}
.pc-alumni .pc-veil{background:linear-gradient(180deg,rgba(0,0,0,.4) 0%,rgba(0,0,0,.15) 35%,rgba(80,55,15,.65) 75%,rgba(0,0,0,.96) 100%)}
.pc-events .pc-veil{background:linear-gradient(180deg,rgba(0,0,0,.4) 0%,rgba(0,0,0,.15) 35%,rgba(50,15,25,.72) 75%,rgba(0,0,0,.96) 100%)}
.pc-body{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;justify-content:flex-end;padding:clamp(28px,3.5vw,48px);gap:10px}
.pc-eyebrow{font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:rgba(244,240,232,.78);margin:0;font-weight:600}
.pc-train .pc-eyebrow,.pc-events .pc-eyebrow{color:#f4a4ac}
.pc-alumni .pc-eyebrow{color:var(--gold)}
.pc-h{font-family:var(--display);font-size:clamp(48px,6.5vw,86px);line-height:.95;text-transform:uppercase;color:var(--bone);margin:0;text-shadow:0 2px 28px rgba(0,0,0,.55)}
.pc-meta{font-family:var(--sans);font-size:clamp(13px,1.05vw,15px);line-height:1.55;color:rgba(244,240,232,.86);margin:0 0 6px;max-width:36ch;text-shadow:0 1px 8px rgba(0,0,0,.55)}
.pc-cta{display:inline-flex;align-items:center;gap:14px;font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:var(--bone);border-top:1px solid rgba(244,240,232,.4);padding-top:16px;margin:6px 0 0;width:fit-content;font-weight:600}
.pc-cta svg{transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.pc-card:hover .pc-cta svg{transform:translateX(8px)}

/* Meet Johnny */
.meet-johnny{background:var(--bone-soft);border-top:1px solid var(--rule);padding:clamp(72px,11vh,120px) var(--frame-pad)}
.mj-frame{max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(40px,6vw,80px);align-items:center}
.mj-photo{aspect-ratio:4/5;overflow:hidden;border-radius:0;background:var(--ink);position:relative}
.mj-photo::after{content:"";position:absolute;inset:10px;border:1px solid rgba(255,255,255,.16);pointer-events:none;z-index:1}
.mj-photo img{width:100%;height:100%;object-fit:cover;filter:saturate(.92) contrast(1.05)}
.mj-h{font-family:var(--display);font-weight:400;font-size:clamp(34px,4.4vw,58px);line-height:1.05;letter-spacing:-.005em;color:var(--ink);margin:18px 0 22px;text-transform:uppercase}
.mj-h em{font-style:normal;color:var(--accent);font-size:.7em}
.mj-lede{font-family:var(--sans);font-size:clamp(17px,1.5vw,20px);line-height:1.5;color:var(--ink);margin-bottom:18px;font-weight:500}
.mj-bio{font-size:16px;line-height:1.7;color:var(--ink-soft);margin-bottom:24px;max-width:56ch}
.mj-bio strong{color:var(--accent);font-weight:600}
.mj-contact{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(180px,100%),1fr));gap:14px 28px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:18px 0;margin:0 0 28px;max-width:680px}
.mj-contact div{display:flex;flex-direction:column;gap:2px;min-width:0}
.mj-contact dt{font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:var(--ink-mute);font-weight:600}
.mj-contact dd{font-family:var(--display);font-size:18px;color:var(--ink);text-transform:uppercase;letter-spacing:.02em;line-height:1.2;word-break:break-word}
.mj-contact a{border-bottom:1px solid transparent;transition:border-color .25s,color .25s}
.mj-contact a:hover{color:var(--accent);border-color:var(--accent)}
.mj-cta-row{display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.mj-cta-row .btn-ghost{color:var(--ink);border-color:var(--ink)}
.mj-cta-row .btn-ghost:hover{border-color:var(--accent);color:var(--accent)}

@media (max-width:900px){
  .pc-cards{grid-template-columns:1fr;gap:14px}
  .pc-card{aspect-ratio:4/5;min-height:380px}
  .mj-frame{grid-template-columns:1fr;gap:32px}
  .mj-photo{max-width:380px;aspect-ratio:1/1;margin:0 auto}
}
@media (prefers-reduced-motion:reduce){
  .ph-image img{animation:none}
  .ph-word{opacity:1;transform:none;animation:none}
}

/* (legacy) Hero animation kept for any other pages still using .hero */
.ht-1,.ht-2,.ht-3{display:block;opacity:0;transform:translateY(50px) skew(0deg,2deg);animation:wuwSlam 1.1s cubic-bezier(.2,.7,.2,1) forwards;will-change:transform,opacity}
.ht-1{animation-delay:.15s}
.ht-2{animation-delay:.55s}
.ht-3{animation-delay:.85s}
@keyframes wuwSlam{0%{opacity:0;transform:translateY(50px) skew(0,3deg)}60%{opacity:1}100%{opacity:1;transform:translateY(0) skew(0,0)}}
.hero-image img{animation:wuwZoom 28s ease-in-out infinite alternate}
@keyframes wuwZoom{0%{transform:scale(1.02)}100%{transform:scale(1.14) translate(-1.5%,-1.5%)}}
@media (prefers-reduced-motion:reduce){.ht-1,.ht-2,.ht-3{opacity:1;transform:none;animation:none}.hero-image img{animation:none}}
.memorial{padding:32px;background:#000;color:var(--bone);margin-bottom:48px;text-align:center;border:1px solid var(--gold)}
.me-cross{font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);margin-bottom:14px}
.memorial h2{font-family:var(--display);font-size:32px;text-transform:uppercase;margin-bottom:14px}
.roster-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:48px}
.roster-list li{font-family:var(--display);font-size:24px;text-transform:uppercase;color:var(--ink);padding:18px 22px;background:var(--bone-soft);border-left:4px solid var(--accent);letter-spacing:.02em}
.title-list{display:grid;gap:0;border-top:1px solid var(--rule);max-width:760px;margin:0 auto 48px}
.title-list li{display:flex;justify-content:space-between;align-items:center;padding:24px 0;border-bottom:1px solid var(--rule);gap:24px}
.tt-belt{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink);opacity:.7;font-weight:600}
.tt-holder{font-family:var(--display);font-size:clamp(20px,2.4vw,30px);text-transform:uppercase;color:var(--accent);text-align:right}
.rl-foot{text-align:center;font-size:14px;color:var(--ink);opacity:.7}
.rl-foot.small{font-size:12px}
.ev-card{padding:32px;background:var(--bone-soft);margin-bottom:18px;border-left:4px solid var(--accent)}
.ev-card h2{font-family:var(--display);font-size:28px;text-transform:uppercase;margin-bottom:10px;color:var(--ink)}
.ev-card p{margin-bottom:18px;font-size:16px}
.ab-grid{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:48px;align-items:start;margin-bottom:48px}
.ab-photo{aspect-ratio:4/5;overflow:hidden;background:var(--ink)}
.ab-photo img{width:100%;height:100%;object-fit:cover;object-position:center top;filter:contrast(1.05)}
.ab-body p{margin-bottom:18px;font-size:17px;line-height:1.7}
.ab-body strong{font-weight:600;color:var(--accent)}
.ab-quote{padding:48px;background:#000;color:var(--bone);font-family:var(--display);font-size:clamp(24px,3vw,40px);text-align:center;line-height:1.25;border-top:4px solid var(--accent)}
.ab-quote cite{display:block;margin-top:18px;font-family:var(--sans);font-size:14px;letter-spacing:.18em;color:var(--gold);text-transform:uppercase;font-style:normal}
.ct-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-bottom:48px}
.ct-card{padding:32px;background:var(--bone-soft);border-top:4px solid var(--accent);text-align:center}
.ct-h{font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:var(--accent);margin-bottom:14px;font-weight:600}
.ct-big{display:block;font-family:var(--display);font-size:32px;color:var(--ink);text-transform:uppercase;line-height:1.1;margin-bottom:8px}
.ct-big a{color:var(--ink);transition:color .25s}
.ct-big a:hover{color:var(--accent)}
.ct-d{font-size:14px;color:var(--ink);opacity:.7}
.sch-list li{display:flex;justify-content:space-between;padding:6px 0;font-size:14px;border-bottom:1px dashed rgba(0,0,0,.1)}
.sch-list li span:first-child{font-weight:600}
/* Contact form */
.ct-form-wrap{max-width:680px;margin:64px auto 24px;padding:40px 36px;background:var(--bone-soft);border:1px solid rgba(0,0,0,.08);border-top:4px solid var(--accent)}
.ct-form-h{font-family:var(--display),Anton,sans-serif;font-size:clamp(28px,4vw,40px);text-transform:uppercase;letter-spacing:-.01em;color:var(--ink);margin-bottom:6px}
.ct-form-sub{color:var(--ink);opacity:.7;font-size:15px;margin-bottom:28px}
.ct-form{display:flex;flex-direction:column;gap:14px}
.ct-row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:540px){.ct-row{grid-template-columns:1fr}}
.ct-form label{display:flex;flex-direction:column;gap:6px}
.ct-form label span{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink);opacity:.7;font-weight:600}
.ct-form input,.ct-form select,.ct-form textarea{font-family:inherit;font-size:15px;padding:12px 14px;border:1px solid rgba(0,0,0,.18);background:#fff;color:var(--ink);border-radius:2px;transition:border-color .2s,box-shadow .2s;width:100%}
.ct-form input:focus,.ct-form select:focus,.ct-form textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(210,34,45,.12)}
.ct-form textarea{resize:vertical;min-height:120px;font-family:inherit}
.ct-submit{margin-top:8px;padding:16px 28px;background:var(--accent);color:#fff;border:none;font-family:var(--display),Anton,sans-serif;font-size:18px;text-transform:uppercase;letter-spacing:.08em;cursor:pointer;transition:background .2s,transform .15s}
.ct-submit:hover{background:#a01820}
.ct-submit:active{transform:translateY(1px)}
.ct-fine{font-size:12px;color:var(--ink);opacity:.55;margin-top:4px;text-align:center}
.ct-sent{max-width:680px;margin:24px auto;padding:18px 22px;background:#1f3d1f;color:#cfe9c9;border-left:4px solid #4caf50;font-size:15px}
.news-list{display:grid;gap:0;border-top:1px solid var(--rule);max-width:880px;margin:0 auto}
.news-list li{padding:18px 0;border-bottom:1px solid var(--rule)}
.news-list a{font-size:16px;color:var(--ink);border-bottom:1px solid transparent;word-break:break-word;display:inline-block}
/* News page — preview cards */
.news-meta{display:flex;flex-wrap:wrap;gap:18px;margin-top:16px;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-mute)}
.news-meta strong{font-family:var(--display);font-size:18px;color:var(--accent);font-weight:400;margin-right:4px;letter-spacing:0;text-transform:none}
.news-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px;max-width:1240px;margin:48px auto 80px;padding:0 var(--frame-pad)}
.news-card{display:flex;flex-direction:column;background:var(--bone-soft);border:1px solid var(--rule);overflow:hidden;transition:transform .35s ease,box-shadow .35s ease,border-color .35s}
.news-card:hover{transform:translateY(-3px);box-shadow:0 18px 40px -22px rgba(0,0,0,.35);border-color:var(--accent)}
.nc-media{position:relative;aspect-ratio:16/9;overflow:hidden;background:#0a0a0a}
.nc-media img{width:100%;height:100%;object-fit:cover;transition:transform .8s ease}
.news-card:hover .nc-media img{transform:scale(1.05)}
.nc-media-yt .nc-play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:48px;color:rgba(255,255,255,.92);text-shadow:0 4px 16px rgba(0,0,0,.6);pointer-events:none}
.nc-media-badge{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:18px;text-align:center;line-height:1.1}
.nc-media-badge .nc-fav{width:36px;height:36px;border-radius:8px;background:rgba(255,255,255,.12);padding:6px}
.nc-media-badge .nc-badge-name{font-family:var(--display);font-size:22px;text-transform:uppercase;letter-spacing:.04em;font-weight:700}
.nc-media-badge .nc-badge-mark{font-size:32px;line-height:1;opacity:.92}
.nc-body{display:flex;flex-direction:column;gap:8px;padding:18px 18px 22px;flex:1}
.nc-kind{font-size:10px;letter-spacing:.28em;text-transform:uppercase;color:var(--accent);font-weight:600}
.nc-title{font-family:var(--display);font-size:19px;line-height:1.22;color:var(--ink);text-transform:none;letter-spacing:-.005em;font-weight:500;margin:0}
.nc-host{margin-top:auto;font-size:11px;color:var(--ink-mute);letter-spacing:.04em;display:flex;align-items:center;justify-content:space-between;gap:8px;padding-top:10px;border-top:1px solid var(--rule)}
.nc-arrow{color:var(--accent);font-size:14px;transition:transform .3s}
.news-card:hover .nc-arrow{transform:translateX(4px)}
.news-list a:hover{color:var(--accent);border-color:var(--accent)}
.post-page{padding:clamp(120px,16vh,160px) var(--frame-pad) clamp(64px,10vh,100px);max-width:760px;margin:0 auto}
.post-head{margin-bottom:32px;padding-bottom:18px;border-bottom:2px solid var(--accent)}
.post-date{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);margin-bottom:12px;font-weight:600}
.post-title{font-family:var(--display);font-size:clamp(40px,7vw,72px);text-transform:uppercase;color:var(--ink);line-height:.95}
.post-body{font-size:18px;line-height:1.75;color:var(--ink)}
.post-body p{margin-bottom:1.2em}
.post-body img{margin:32px 0;width:100%;height:auto}
.post-body a{color:var(--accent);border-bottom:1px solid currentColor}
.post-body h2,.post-body h3{font-family:var(--display);text-transform:uppercase;color:var(--ink);margin:1.5em 0 .5em;line-height:1.1}
.post-body h2{font-size:32px}
.post-body h3{font-size:26px}
.post-foot{margin-top:48px;padding-top:24px;border-top:1px solid var(--rule)}
.colophon{background:#000;color:var(--bone)}
.colophon-frame{max-width:var(--max);margin:0 auto;padding:64px var(--frame-pad);display:grid;grid-template-columns:1fr 1fr 1fr;gap:48px;align-items:start}
.col-mark{font-family:var(--display);font-size:36px;color:var(--bone);text-transform:uppercase;letter-spacing:.04em;display:block;margin-bottom:8px}
.col-logo{height:90px;width:auto;display:block;margin-bottom:14px;filter:drop-shadow(0 4px 12px rgba(0,0,0,.5))}
/* Johnny Rodz bio page */
.rodz-page{padding-top:0}
.rodz-hero{position:relative;min-height:480px;display:flex;align-items:flex-end;background:#000;overflow:hidden;color:var(--bone)}
.rodz-hero-image{position:absolute;inset:0;z-index:0}
.rodz-hero-image img{width:100%;height:100%;object-fit:cover;object-position:center 35%;filter:saturate(.8) contrast(1.1) brightness(.6)}
.rodz-hero-veil{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,.3) 0%,rgba(0,0,0,.1) 30%,rgba(0,0,0,.65) 75%,rgba(0,0,0,.95))}
.rodz-hero-frame{position:relative;z-index:2;max-width:var(--max);margin:0 auto;padding:clamp(120px,18vh,180px) var(--frame-pad) clamp(48px,7vh,72px);width:100%}
.rodz-h{font-family:var(--display);font-size:clamp(48px,8vw,108px);text-transform:uppercase;line-height:.92;color:var(--bone);margin-bottom:18px;text-shadow:0 4px 32px rgba(0,0,0,.7)}
.rodz-h em{font-style:normal;color:var(--accent);text-shadow:0 4px 32px rgba(210,34,45,.4)}
.rodz-sub{font-size:clamp(16px,1.6vw,21px);line-height:1.55;color:rgba(244,240,232,.92);max-width:60ch;text-shadow:0 1px 8px rgba(0,0,0,.7)}
.rodz-body{font-size:18px;line-height:1.75;color:var(--ink)}
.rodz-body h1,.rodz-body h2{font-family:var(--display);text-transform:uppercase;color:var(--ink);margin:1.5em 0 .5em;letter-spacing:.02em}
.rodz-body h2{font-size:32px;color:var(--accent)}
.rodz-body h3{font-family:var(--display);font-size:24px;color:var(--ink);margin:1.2em 0 .4em;text-transform:uppercase}
.rodz-body p{margin-bottom:1.1em}
.rodz-body img{margin:24px 0;border-left:4px solid var(--accent)}
.rodz-body a{color:var(--accent);border-bottom:1px solid currentColor}
.rodz-body strong{color:var(--ink);font-weight:700}
.rodz-body ul{margin:1em 0;padding-left:1.4em}
.rodz-body ul li{margin-bottom:.5em;list-style:disc}
.rodz-cta-line{font-family:var(--display);text-transform:uppercase;font-size:18px;letter-spacing:.06em;margin-top:36px;padding-top:24px;border-top:2px solid var(--accent);display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.rodz-cta-line a{color:var(--accent);border-bottom:2px solid currentColor;padding-bottom:2px}
.col-tag{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:rgba(244,240,232,.55);font-weight:600}
.col-h{font-family:var(--display);font-size:18px;text-transform:uppercase;color:var(--accent);margin-bottom:14px;letter-spacing:.04em}
.col-contact p,.col-social p{font-size:14px;line-height:1.7;margin-bottom:6px}
.col-contact a,.col-social a{color:var(--bone);border-bottom:1px solid transparent;transition:border-color .25s}
.col-contact a:hover,.col-social a:hover{border-color:var(--accent);color:var(--accent)}
.col-fine{padding:18px var(--frame-pad);border-top:1px solid rgba(244,240,232,.1);font-size:11px;color:rgba(244,240,232,.4);text-align:center}
.bg-refs{padding:14px var(--frame-pad);border-top:1px solid rgba(244,240,232,.06);font-size:10px;line-height:1.8;color:rgba(244,240,232,.32);display:flex;flex-wrap:wrap;gap:6px 14px}
.bg-refs a{color:rgba(244,240,232,.42);transition:color .25s}
.bg-refs a:hover{color:var(--accent)}
/* Across-the-network strip — visible but de-emphasised, real <a> tags so SEO juice flows */
.col-network{padding:14px var(--frame-pad);border-top:1px solid rgba(244,240,232,.08);display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 18px;font-size:11px;line-height:1.8}
.col-network .cn-label{color:rgba(244,240,232,.45);letter-spacing:.22em;text-transform:uppercase;font-weight:500;flex-shrink:0}
.col-network .cn-links{color:rgba(244,240,232,.42)}
.col-network .cn-links a{color:rgba(244,240,232,.5);transition:color .25s;border:none}
.col-network .cn-links a:hover{color:var(--accent)}
/* /israel-joffe/ aggregator page */
.ij-head{max-width:880px}
.ij-body{max-width:980px;margin:0 auto;padding:0 var(--frame-pad) 80px}
.ij-bio h2,.ij-archive h2,.ij-refs h2{font-family:var(--display);font-size:clamp(28px,3.5vw,40px);text-transform:uppercase;letter-spacing:-.005em;margin:48px 0 16px;color:var(--ink)}
.ij-bio p,.ij-refs p{font-size:16px;line-height:1.75;margin-bottom:14px;max-width:760px}
.ij-archive-meta{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-mute);margin-bottom:20px}
.ij-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:0;border-top:1px solid var(--rule)}
.ij-post{display:flex;flex-direction:column;gap:6px;padding:18px 20px;border-bottom:1px solid var(--rule);border-right:1px solid var(--rule);transition:background .3s,padding-left .3s}
.ij-post:hover{background:var(--bone-soft);padding-left:26px}
.ij-date{font-size:10px;letter-spacing:.26em;text-transform:uppercase;color:var(--accent);font-weight:600}
.ij-title{font-family:var(--display);font-size:18px;line-height:1.2;color:var(--ink);text-transform:capitalize}
.ij-link-list{margin:0 0 28px;border-top:1px solid var(--rule)}
.ij-link-list li{padding:14px 0;border-bottom:1px solid var(--rule)}
.ij-link-list li a{color:var(--ink);font-size:15.5px;border-bottom:1px solid transparent;transition:border-color .25s,color .25s}
.ij-link-list li a:hover{color:var(--accent);border-bottom-color:var(--accent)}
/* /network/{slug}/ SEO articles */
.net-article .page-h{max-width:920px}
.net-body{max-width:760px;margin:0 auto;padding:0 var(--frame-pad) 80px;font-size:16px;line-height:1.78}
.net-body p{margin-bottom:16px}
.net-body a{color:var(--ink);border-bottom:1px solid var(--accent);transition:color .25s}
.net-body a:hover{color:var(--accent)}
.net-cta{margin-top:24px}
.net-cta .link-cta{display:inline-block;padding:12px 22px;border:1px solid var(--ink);font-size:11px;letter-spacing:.28em;text-transform:uppercase;border-bottom:1px solid var(--ink)}
.net-cta .link-cta:hover{background:var(--ink);color:var(--bone)}
.net-rule{border:none;border-top:1px solid var(--rule);margin:36px 0 24px}
.net-foot{font-size:13px;color:var(--ink-mute)}
@media (max-width:900px){.primary{display:none}.menu-toggle{display:flex!important}.wm-tag{display:none}.colophon-frame{grid-template-columns:1fr;gap:32px}.lr-grid,.ab-grid{grid-template-columns:1fr;gap:32px}.lr-img,.ab-photo{max-width:420px;aspect-ratio:1/1;margin:0 auto}.ht-2{padding-left:0}.col-network{flex-direction:column;align-items:flex-start;gap:6px}.ij-grid{grid-template-columns:1fr}}
'''

def write(path, content):
    out = os.path.join(ROOT, path.lstrip('/'))
    os.makedirs(os.path.dirname(out) or out, exist_ok=True)
    with open(out, 'w') as f: f.write(content)

write('index.html', render_home())
write('alumni/index.html', append_wp_extras(render_alumni(), '/alumni/'))
write('roster/index.html', append_wp_extras(render_roster(), '/roster/'))
write('title-holders/index.html', append_wp_extras(render_titles(), '/title-holders/'))
write('events/index.html', append_wp_extras(render_events(), '/events/'))
write('about/index.html', append_wp_extras(render_about(), '/about/'))
write('johnny-rodz/index.html', render_rodz())
write('contact/index.html', append_wp_extras(render_contact(), '/contact/'))
write('in-the-news/index.html', append_wp_extras(render_news(), '/in-the-news/'))
write('israel-joffe/index.html', render_israel_joffe())
for fed in FEDERATION:
    write(f"network/{fed['slug']}/index.html", render_network_article(fed))
write('styles.css', render_styles())

post_count = 0
for p in posts:
    write(post_url(p).lstrip('/') + 'index.html', render_post(p))
    post_count += 1

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemaps-image/1.1">']
for path, prio in [('/', 1.0), ('/johnny-rodz/', 0.95), ('/about/', 0.85), ('/alumni/', 0.95),
                   ('/roster/', 0.8), ('/title-holders/', 0.7), ('/events/', 0.85),
                   ('/contact/', 0.95), ('/in-the-news/', 0.7), ('/israel-joffe/', 0.7)]:
    sm.append(f'  <url><loc>https://wuwonline.com{path}</loc><priority>{prio}</priority><changefreq>weekly</changefreq></url>')
for fed in FEDERATION:
    sm.append(f'  <url><loc>https://wuwonline.com/network/{fed["slug"]}/</loc><priority>0.4</priority></url>')
for p in posts:
    hero = p.get('hero')
    img_xml = ''
    if hero:
        local = img_map.get(hero.split('?')[0], hero)
        img_xml = f'<image:image><image:loc>https://wuwonline.com{local}</image:loc></image:image>'
    sm.append(f'  <url><loc>https://wuwonline.com{post_url(p)}</loc><lastmod>{p["date"]}</lastmod><priority>0.5</priority>{img_xml}</url>')
sm.append('</urlset>')
write('sitemap.xml', '\n'.join(sm))

write('robots.txt',
      'User-agent: *\nAllow: /\n\n'
      'User-agent: GPTBot\nDisallow: /\n'
      'User-agent: ClaudeBot\nDisallow: /\n'
      'User-agent: CCBot\nDisallow: /\n'
      'User-agent: anthropic-ai\nDisallow: /\n'
      'User-agent: PerplexityBot\nDisallow: /\n\n'
      'Sitemap: https://wuwonline.com/sitemap.xml\n')

# RSS feed (latest news/posts)
from datetime import datetime as _dt
def _rss_item(p):
    canonical = f'https://wuwonline.com{post_url(p)}'
    try: pub = _dt.strptime(p['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 00:00:00 +0000')
    except: pub = 'Wed, 01 Jan 2020 00:00:00 +0000'
    desc_text = (p.get('description') or H.unescape(re.sub(r'<[^>]+>', ' ', p.get('body_html', '')))[:300]).strip()
    return f'<item><title>{H.escape(p["title"])}</title><link>{canonical}</link><guid>{canonical}</guid><pubDate>{pub}</pubDate><description>{H.escape(desc_text)}</description></item>'
rss_items = ''.join(_rss_item(p) for p in sorted(posts, key=lambda x: x.get('date',''), reverse=True)[:30])
write('feed.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>World of Unpredictable Wrestling</title><link>https://wuwonline.com/</link><description>Train pro wrestling at Gleason\'s Gym Brooklyn with Johnny Rodz, WWE Hall of Famer.</description><language>en-US</language>{rss_items}</channel></rss>')

write('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#0a0a0a"/><text x="32" y="44" font-family="Anton, Impact, sans-serif" font-size="38" fill="#f4f0e8" text-anchor="middle" letter-spacing="-1"><tspan fill="#d2222d">W</tspan>UW</text></svg>')
write('_headers',
      '/*\n'
      '  Cache-Control: public, max-age=0, must-revalidate\n'
      '  X-Content-Type-Options: nosniff\n'
      '  Referrer-Policy: strict-origin-when-cross-origin\n'
      '  Permissions-Policy: interest-cohort=()\n\n'
      '/styles.css\n  Cache-Control: public, max-age=300, must-revalidate\n\n'
      '/img/*\n  Cache-Control: public, max-age=31536000, immutable\n\n'
      '/sitemap.xml\n  Content-Type: application/xml\n  Cache-Control: public, max-age=3600\n\n'
      '/feed.xml\n  Content-Type: application/rss+xml; charset=utf-8\n  Cache-Control: public, max-age=3600\n\n'
      '/robots.txt\n  Content-Type: text/plain\n  Cache-Control: public, max-age=86400\n')
print(f'  built {post_count} post pages + 8 named pages + /israel-joffe/ + {len(FEDERATION)} network articles + sitemap')
