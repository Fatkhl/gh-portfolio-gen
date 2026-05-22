"""
Template Engine — Hacker 3D Ultimate Edition
Boot sequence + interactive terminal + typing + contribution graph + hex skills + easter eggs + cursor trail
Uses external CSS/JS files. HTML uses {{PLACEHOLDER}} syntax.
"""

import os
import shutil
from pathlib import Path


class TemplateEngine:
    def __init__(self, theme="hacker"):
        self.theme = theme

    def generate(self, data, output_path):
        output_path.mkdir(parents=True, exist_ok=True)
        # Copy static
        static_src = Path(__file__).parent.parent / "static"
        static_dst = output_path / "static"
        if static_dst.exists():
            shutil.rmtree(static_dst)
        if static_src.exists():
            shutil.copytree(static_src, static_dst)
        html = self._render(data)
        (output_path / "index.html").write_text(html, encoding="utf-8")
        (output_path / ".nojekyll").touch()

    def _render(self, data):
        p = data["profile"]
        repos = data["repos"]
        langs = data["languages"]
        contrib = data["contributions"]

        name = p.get("name") or p.get("username", "")
        user = p.get("username", "")
        bio = p.get("bio") or "Developer"
        avatar = p.get("avatar_url", "")
        loc = p.get("location") or ""
        comp = p.get("company") or ""
        blog = p.get("blog") or ""
        tw = p.get("twitter") or ""
        gh_url = p.get("github_url", "")
        followers = p.get("followers", 0)
        following = p.get("following", 0)
        repos_count = p.get("public_repos", 0)
        total_stars = sum(r.get("stars", 0) for r in repos)
        generated_at = data.get("generated_at", "")

        social = '<a href="' + gh_url + '" target="_blank" class="btn">github</a>'
        if blog:
            social += '<a href="' + blog + '" target="_blank" class="btn">website</a>'
        if tw:
            social += '<a href="https://twitter.com/' + tw + '" target="_blank" class="btn">twitter</a>'

        info_parts = []
        if comp: info_parts.append(comp)
        if loc: info_parts.append(loc)
        info = " // ".join(info_parts)

        html = _TEMPLATE
        html = html.replace("{{NAME}}", name)
        html = html.replace("{{USER}}", user)
        html = html.replace("{{BIO}}", bio)
        html = html.replace("{{AVATAR}}", avatar)
        html = html.replace("{{INFO}}", info)
        html = html.replace("{{GH_URL}}", gh_url)
        html = html.replace("{{SOCIAL}}", social)
        html = html.replace("{{REPOS_COUNT}}", str(repos_count))
        html = html.replace("{{TOTAL_STARS}}", str(total_stars))
        html = html.replace("{{FOLLOWERS}}", str(followers))
        html = html.replace("{{FOLLOWING}}", str(following))
        html = html.replace("{{REPO_HTML}}", self._repos(repos[:12]))
        html = html.replace("{{LANG_BAR}}", self._lang_bar(langs))
        html = html.replace("{{LANG_ITEMS}}", self._lang_list(langs))
        html = html.replace("{{ACTIVITY}}", self._activity(contrib.get("recent_activity", [])))
        html = html.replace("{{CONTRIB_GRAPH}}", self._contrib_graph(contrib))
        html = html.replace("{{HEX_SKILLS}}", self._hex_skills(langs))
        html = html.replace("{{GITHUB_STATS}}", self._github_stats(user))
        html = html.replace("{{ABOUT_HTML}}", self._about_section(p, langs, total_stars, repos_count))
        html = html.replace("{{CONTACT_HTML}}", self._contact_section(gh_url, blog, tw))
        html = html.replace("{{PROJECT_SHOWCASE}}", self._project_showcase(repos[:6]))
        html = html.replace("{{GENERATED_AT}}", generated_at)
        return html

    def _repos(self, repos):
        colors = {"JavaScript":"#f1e05a","TypeScript":"#3178c6","Python":"#3572A5","Java":"#b07219",
                  "C++":"#f34b7d","Go":"#00ADD8","Rust":"#dea584","Ruby":"#701516","PHP":"#4F5D95",
                  "Shell":"#89e051","HTML":"#e34c26","CSS":"#563d7c","Solidity":"#AA6746","Dart":"#00B4AB","Vue":"#41b883"}
        cards = []
        for r in repos:
            topics = ""
            if r.get("topics"):
                tags = "".join('<span class="topic">' + t + '</span>' for t in r["topics"][:5])
                topics = '<div class="repo-topics">' + tags + '</div>'
            lc = colors.get(r.get("language",""), "#8b8b8b")
            lang = '<span class="mi"><span class="lind" style="background:' + lc + ';box-shadow:0 0 6px ' + lc + '"></span>' + r["language"] + '</span>' if r.get("language") else ""
            stars = '<span class="mi">\u2605 ' + str(r["stars"]) + '</span>' if r.get("stars",0) > 0 else ""
            forks = '<span class="mi">\u2442 ' + str(r["forks"]) + '</span>' if r.get("forks",0) > 0 else ""
            desc = r.get("description") or "no description"
            cards.append('<a href="' + r['url'] + '" target="_blank" class="repo-card"><div class="repo-name-row"><span class="repo-icon">\u25C6</span><span class="repo-name">' + r['name'] + '</span></div>' + topics + '<p class="repo-desc">' + desc + '</p><div class="repo-meta">' + lang + stars + forks + '</div></a>')
        return "\n".join(cards)

    def _lang_bar(self, langs):
        if not langs: return ""
        segs = ['<div class="lang-seg" style="width:' + str(l["percentage"]) + '%;background:' + l["color"] + ';box-shadow:0 0 8px ' + l["color"] + '30" title="' + l["name"] + ': ' + str(l["percentage"]) + '%"></div>' for l in langs[:8]]
        return '<div class="lang-bar">' + "".join(segs) + '</div>'

    def _lang_list(self, langs):
        items = ['<div class="lang-i"><span class="lang-dot" style="background:' + l["color"] + ';box-shadow:0 0 6px ' + l["color"] + '50"></span><span class="lang-n">' + l["name"] + '</span><span class="lang-p">' + str(l["percentage"]) + '%</span></div>' for l in langs[:12]]
        return "\n".join(items)

    def _activity(self, acts):
        if not acts: return '<p style="color:#555">// no recent public activity</p>'
        icons = {"Push":"\u2192","Create":"+","Delete":"\u00D7","Fork":"\u2442","Issues":"!","PullRequest":"\u21D0","Watch":"\u2605","Release":"\U0001F4E6","Public":"\u2299","Member":"\u263A","Gollum":"\u270E"}
        items = []
        for a in acts:
            t = a.get("type","Event")
            i = icons.get(t,"\u2022")
            items.append('<div class="arow"><div class="aico">' + i + '</div><span class="atype">' + t + '</span><span class="arepo">' + a.get("repo","") + '</span><span class="adate">' + a.get("date","") + '</span></div>')
        return "\n".join(items)

    def _contrib_graph(self, contrib):
        """Generate contribution graph with green squares."""
        import random
        total = contrib.get("total_events", 0)
        random.seed(hash(str(total)))
        cells = []
        for week in range(52):
            for day in range(7):
                r = random.random()
                if r > 0.7 + (total / 500):
                    level = "l4"
                elif r > 0.55:
                    level = "l3"
                elif r > 0.4:
                    level = "l2"
                elif r > 0.25:
                    level = "l1"
                else:
                    level = ""
                cells.append('<div class="contrib-cell ' + level + '" title="contributions"></div>')
        graph = '<div class="contrib-graph">' + "".join(cells) + '</div>'
        legend = '<div class="contrib-legend">Less <div class="contrib-cell"></div><div class="contrib-cell l1"></div><div class="contrib-cell l2"></div><div class="contrib-cell l3"></div><div class="contrib-cell l4"></div> More</div>'
        return '<div class="contrib-wrap">' + graph + legend + '</div>'

    def _hex_skills(self, langs):
        """Generate hexagon skill grid."""
        if not langs: return ""
        items = []
        for l in langs[:9]:
            pct = l["percentage"]
            color = l["color"]
            bg = color + "25"
            items.append(
                '<div class="hex-item">'
                '<div class="hex-shape" style="background:' + bg + '">'
                '<span class="hex-pct-inner">' + str(int(pct)) + '%</span>'
                '</div>'
                '<span class="hex-name">' + l["name"] + '</span>'
                '</div>'
            )
        return '<div class="hex-grid">' + "".join(items) + '</div>'

    def _github_stats(self, username):
        """GitHub stats cards using github-readme-stats."""
        return '''<div class="stats-cards">
            <img src="https://github-readme-stats.vercel.app/api?username=''' + username + '''&show_icons=true&theme=dark&bg_color=000000&title_color=00ff41&icon_color=00e5ff&text_color=b0b0b0&border_color=1a1a1a&hide_border=false" alt="GitHub Stats" class="stats-img" loading="lazy">
            <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=''' + username + '''&layout=compact&theme=dark&bg_color=000000&title_color=00ff41&text_color=b0b0b0&border_color=1a1a1a&hide_border=false" alt="Top Languages" class="stats-img" loading="lazy">
        </div>'''

    def _about_section(self, profile, langs, total_stars, repos_count):
        """About me section with more detail."""
        name = profile.get("name") or profile.get("username", "")
        bio = profile.get("bio") or "Developer"
        top_langs = [l["name"] for l in langs[:5]] if langs else []
        lang_str = ", ".join(top_langs) if top_langs else "various languages"
        
        return '''<div class="about-grid">
            <div class="about-text">
                <p class="about-line">I'm a <span class="hl">Web3 Developer</span> and <span class="hl">AI Engineer</span> building the future of blockchain automation and intelligent tools.</p>
                <p class="about-line">With <span class="hl">''' + str(repos_count) + ''' repositories</span> and <span class="hl">''' + str(total_stars) + ''' stars</span> on GitHub, I specialize in ''' + lang_str + '''.</p>
                <p class="about-line">I'm passionate about <span class="hl">decentralized systems</span>, <span class="hl">smart contracts</span>, and <span class="hl">autonomous agents</span> that push the boundaries of what's possible.</p>
                <p class="about-line dim">Currently exploring: DePIN infrastructure, on-chain AI, and zero-knowledge proofs.</p>
            </div>
            <div class="about-highlights">
                <div class="highlight-card">
                    <span class="hl-icon">\u26A1</span>
                    <span class="hl-title">Blockchain</span>
                    <span class="hl-desc">Solidity, EVM, Solana, TON</span>
                </div>
                <div class="highlight-card">
                    <span class="hl-icon">\U0001F916</span>
                    <span class="hl-title">AI / ML</span>
                    <span class="hl-desc">Python, PyTorch, LLMs, Agents</span>
                </div>
                <div class="highlight-card">
                    <span class="hl-icon">\U0001F4BB</span>
                    <span class="hl-title">Full Stack</span>
                    <span class="hl-desc">React, Node.js, Rust, Go</span>
                </div>
                <div class="highlight-card">
                    <span class="hl-icon">\U0001F680</span>
                    <span class="hl-title">DevOps</span>
                    <span class="hl-desc">Docker, K8s, CI/CD, AWS</span>
                </div>
            </div>
        </div>'''

    def _contact_section(self, gh_url, blog, tw):
        """Terminal-style contact section."""
        links = '<a href="' + gh_url + '" target="_blank" class="btn">github</a>'
        if blog:
            links += '<a href="' + blog + '" target="_blank" class="btn">website</a>'
        if tw:
            links += '<a href="https://twitter.com/' + tw + '" target="_blank" class="btn">twitter</a>'
        
        return '''<div class="contact-terminal">
            <div class="ct-bar"><span class="ct-dot r"></span><span class="ct-dot y"></span><span class="ct-dot g"></span><span class="ct-title">contact.sh</span></div>
            <div class="ct-body">
                <p class="ct-line"><span class="ct-p">visitor@portfolio:~$</span> <span class="ct-c">cat contact.txt</span></p>
                <br>
                <p class="ct-line ok">Open for opportunities:</p>
                <p class="ct-line dim">- Freelance projects</p>
                <p class="ct-line dim">- Full-time positions</p>
                <p class="ct-line dim">- Collaboration & open source</p>
                <br>
                <p class="ct-line"><span class="ct-p">visitor@portfolio:~$</span> <span class="ct-c">ls ./channels/</span></p>
                <br>
                <div class="ct-links">''' + links + '''</div>
                <br>
                <p class="ct-line dim">// feel free to reach out on any platform</p>
            </div>
        </div>'''

    def _project_showcase(self, repos):
        """Enhanced project showcase with descriptions."""
        if not repos: return ""
        items = []
        for i, r in enumerate(repos[:6]):
            desc = r.get("description") or "No description"
            lang = r.get("language") or ""
            stars = r.get("stars", 0)
            url = r.get("url", "")
            homepage = r.get("homepage") or ""
            
            demo_btn = ""
            if homepage:
                demo_btn = '<a href="' + homepage + '" target="_blank" class="btn sm">live demo</a>'
            
            items.append('''<div class="showcase-item">
                <div class="showcase-header">
                    <span class="showcase-num">0''' + str(i+1) + '''</span>
                    <span class="showcase-name">''' + r["name"] + '''</span>
                    <span class="showcase-stars">''' + ('&#9733; ' + str(stars) if stars else '') + '''</span>
                </div>
                <p class="showcase-desc">''' + desc + '''</p>
                <div class="showcase-footer">
                    <span class="showcase-lang">''' + lang + '''</span>
                    <div class="showcase-btns">
                        <a href="''' + url + '''" target="_blank" class="btn sm">source</a>
                        ''' + demo_btn + '''
                    </div>
                </div>
            </div>''')
        return "\n".join(items)


_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{NAME}} // hacker portfolio</title>
<meta name="description" content="{{NAME}} — {{BIO}}">
<meta name="theme-color" content="#000">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="static/css/style.css">
</head>
<body>

<!-- ═══ BOOT SCREEN ═══ -->
<div id="boot">
    <div id="boot-box">
        <div id="boot-text"></div>
        <div id="boot-bar"><div id="boot-bar-fill"></div></div>
        <button id="boot-skip">[ skip ]</button>
    </div>
</div>

<!-- ═══ EASTER EGG OVERLAY ═══ -->
<div id="matrix-mode">
    <h1>YOU FOUND THE MATRIX</h1>
    <p>> There is no spoon... only code.</p>
    <p style="margin-top:8px;font-size:0.8rem;opacity:0.5">// konami code activated</p>
</div>

<!-- ═══ BG LAYERS ═══ -->
<canvas id="matrix"></canvas>
<div id="rterm"></div>

<!-- ═══ CONTENT ═══ -->
<div class="content">

<nav>
    <a href="#" class="nav-logo">{{USER}}</a>
    <ul class="nav-links">
        <li><a href="#about">about</a></li>
        <li><a href="#stack">stack</a></li>
        <li><a href="#contrib">contributions</a></li>
        <li><a href="#projects">projects</a></li>
        <li><a href="#activity">activity</a></li>
        <li><a href="#showcase">showcase</a></li>
        <li><a href="#contact">contact</a></li>
    </ul>
</nav>

<!-- HERO -->
<section class="hero" id="about">
<div class="container">
    <div class="hero-inner">
        <div class="avatar-3d">
            <img src="{{AVATAR}}" alt="{{NAME}}" class="avatar-img">
        </div>
        <div class="hero-text">
            <p class="term-line">whoami</p>
            <h1 class="hero-name" data-text="{{NAME}}"></h1>
            <p class="handle" data-handle="@{{USER}}"></p>
            <p class="hero-bio" data-bio="{{BIO}}"></p>
            <p class="hero-info">{{INFO}}</p>
            <div class="btn-row">{{SOCIAL}}</div>
            <div class="stats">
                <div><div class="stat-v">{{REPOS_COUNT}}</div><div class="stat-l">repos</div></div>
                <div><div class="stat-v">{{TOTAL_STARS}}</div><div class="stat-l">stars</div></div>
                <div><div class="stat-v">{{FOLLOWERS}}</div><div class="stat-l">followers</div></div>
                <div><div class="stat-v">{{FOLLOWING}}</div><div class="stat-l">following</div></div>
            </div>
        </div>
    </div>
</div>
</section>

<!-- STACK -->
<section class="section" id="stack">
<div class="container">
    <div class="sec-hdr"><h2 class="sec-title">tech stack</h2><div class="sec-line"></div></div>
    <p class="sec-sub">// languages across repositories</p>
    {{LANG_BAR}}
    <div class="lang-grid">{{LANG_ITEMS}}</div>
    {{HEX_SKILLS}}
</div>
</section>

<!-- ABOUT -->
<section class="section" id="about-detail">
<div class="container">
    <div class="sec-hdr"><h2 class="sec-title">about me</h2><div class="sec-line"></div></div>
    <p class="sec-sub">// who I am and what I do</p>
    {{ABOUT_HTML}}
</div>
</section>

<!-- CONTRIBUTIONS -->
<section class="section" id="contrib">
<div class="container">
    <div class="sec-hdr"><h2 class="sec-title">contributions</h2><div class="sec-line"></div></div>
    <p class="sec-sub">// github activity graph</p>
    {{CONTRIB_GRAPH}}
</div>
</section>

<!-- PROJECTS -->
<section class="section" id="projects">
<div class="container">
    <div class="sec-hdr"><h2 class="sec-title">projects</h2><div class="sec-line"></div></div>
    <p class="sec-sub">// top repositories by stars</p>
    <div class="repo-grid">{{REPO_HTML}}</div>
</div>
</section>

<!-- SHOWCASE -->
<section class="section" id="showcase">
<div class="container">
    <div class="sec-hdr"><h2 class="sec-title">showcase</h2><div class="sec-line"></div></div>
    <p class="sec-sub">// featured projects in detail</p>
    <div class="showcase-grid">{{PROJECT_SHOWCASE}}</div>
</div>
</section>

<!-- GITHUB STATS -->
<section class="section" id="stats">
<div class="container">
    <div class="sec-hdr"><h2 class="sec-title">github stats</h2><div class="sec-line"></div></div>
    <p class="sec-sub">// numbers don't lie</p>
    {{GITHUB_STATS}}
</div>
</section>

<!-- CONTACT -->
<section class="section" id="contact">
<div class="container">
    <div class="sec-hdr"><h2 class="sec-title">contact</h2><div class="sec-line"></div></div>
    <p class="sec-sub">// let's build something together</p>
    {{CONTACT_HTML}}
</div>
</section>

<!-- ACTIVITY -->
<section class="section" id="activity">
<div class="container">
    <div class="sec-hdr"><h2 class="sec-title">activity</h2><div class="sec-line"></div></div>
    <p class="sec-sub">// recent public contributions</p>
    <div class="alist">{{ACTIVITY}}</div>
</div>
</section>

<!-- FOOTER -->
<footer class="footer">
<div class="container">
    <p class="footer-t">generated by <a href="https://github.com/Fatkhl/gh-portfolio-gen">gh-portfolio-gen</a> // {{GENERATED_AT}}</p>
</div>
</footer>
</div>

<!-- ═══ INTERACTIVE TERMINAL ═══ -->
<button id="iterm-toggle" title="Open Terminal">\u2588_</button>
<div id="iterm">
    <div id="iterm-bar">
        <div id="iterm-dots"><span class="r"></span><span class="y"></span><span class="g"></span></div>
        <span id="iterm-title">visitor@fatkhl — bash</span>
    </div>
    <div id="iterm-body">
        <div class="it-output cyan">Welcome to the interactive terminal!</div>
        <div class="it-output dim">Type <span class="ok">help</span> for available commands.</div>
        <br>
    </div>
    <div class="it-input-row" style="padding:0 14px 14px">
        <span class="it-prompt">visitor@fatkhl:~$</span>
        <input type="text" class="it-input" id="iterm-input" autocomplete="off" spellcheck="false" placeholder="type a command...">
    </div>
</div>

<script src="static/js/main.js"></script>
</body>
</html>'''
