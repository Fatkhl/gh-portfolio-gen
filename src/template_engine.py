"""
Template Engine
Generates portfolio HTML from templates and data.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


class TemplateEngine:
    """Generate portfolio HTML from data and templates."""
    
    def __init__(self, theme: str = "cream"):
        self.theme = theme
        self.template_dir = Path(__file__).parent.parent / "templates"
        self.static_dir = Path(__file__).parent.parent / "static"
    
    def generate(self, data: dict, output_path: Path):
        """Generate the complete portfolio site."""
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Copy static assets
        self._copy_static(output_path)
        
        # Generate index.html
        html = self._render_index(data)
        (output_path / "index.html").write_text(html, encoding="utf-8")
        
        # Generate .nojekyll for GitHub Pages
        (output_path / ".nojekyll").touch()
    
    def _copy_static(self, output_path: Path):
        """Copy CSS/JS/fonts to output."""
        static_out = output_path / "static"
        if static_out.exists():
            shutil.rmtree(static_out)
        if self.static_dir.exists():
            shutil.copytree(self.static_dir, static_out)
    
    def _render_index(self, data: dict) -> str:
        """Render the main index.html."""
        profile = data["profile"]
        repos = data["repos"]
        languages = data["languages"]
        contributions = data["contributions"]
        
        # Build repo cards HTML
        repo_cards = self._build_repo_cards(repos[:12])
        
        # Build language bar HTML
        lang_bar = self._build_language_bar(languages)
        
        # Build language list HTML
        lang_list = self._build_language_list(languages)
        
        # Build recent activity HTML
        activity_html = self._build_activity(contributions.get("recent_activity", []))
        
        # Profile data
        name = profile.get("name", profile.get("username", ""))
        username = profile.get("username", "")
        bio = profile.get("bio", "") or "Developer"
        avatar = profile.get("avatar_url", "")
        location = profile.get("location", "") or ""
        company = profile.get("company", "") or ""
        blog = profile.get("blog", "") or ""
        twitter = profile.get("twitter", "") or ""
        github_url = profile.get("github_url", "")
        followers = profile.get("followers", 0)
        following = profile.get("following", 0)
        public_repos = profile.get("public_repos", 0)
        
        # Social links
        social_links = f'<a href="{github_url}" target="_blank" class="social-link" title="GitHub">GitHub</a>'
        if blog:
            social_links += f'\n            <a href="{blog}" target="_blank" class="social-link" title="Website">Website</a>'
        if twitter:
            social_links += f'\n            <a href="https://twitter.com/{twitter}" target="_blank" class="social-link" title="Twitter">Twitter</a>'
        
        # Location/Company info
        info_parts = []
        if company:
            info_parts.append(f'<span class="info-item">🏢 {company}</span>')
        if location:
            info_parts.append(f'<span class="info-item">📍 {location}</span>')
        info_html = "\n            ".join(info_parts)
        
        # Stats
        total_stars = sum(r.get("stars", 0) for r in repos)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — Developer Portfolio</title>
    <meta name="description" content="{name} — {bio}">
    <meta name="theme-color" content="#f5f0e8">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{name} — Developer Portfolio">
    <meta property="og:description" content="{bio}">
    <meta property="og:image" content="{avatar}">
    <meta property="og:type" content="website">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <style>
        /* ═══════════════════════════════════════════════════
           CSS Variables — Cream/Warm Theme
           ═══════════════════════════════════════════════════ */
        :root {{
            --bg-primary: #f5f0e8;
            --bg-secondary: #ede8df;
            --bg-card: #ffffff;
            --bg-card-hover: #faf8f4;
            --text-primary: #1a1714;
            --text-secondary: #5c564a;
            --text-muted: #8a8478;
            --accent: #c4956a;
            --accent-hover: #b3844d;
            --accent-light: rgba(196, 149, 106, 0.15);
            --border: #e0dbd2;
            --border-light: #eae5dc;
            --shadow: 0 2px 12px rgba(26, 23, 20, 0.06);
            --shadow-hover: 0 8px 30px rgba(26, 23, 20, 0.12);
            --radius: 16px;
            --radius-sm: 10px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* ═══ Reset & Base ═══ */
        *, *::before, *::after {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html {{
            scroll-behavior: smooth;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        /* ═══ Subtle Background Pattern ═══ */
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(196, 149, 106, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(196, 149, 106, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 50% 80%, rgba(196, 149, 106, 0.03) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }}
        
        /* ═══ Container ═══ */
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 24px;
        }}
        
        /* ═══ Hero Section ═══ */
        .hero {{
            padding: 80px 0 60px;
            text-align: center;
        }}
        
        .avatar {{
            width: 140px;
            height: 140px;
            border-radius: 50%;
            border: 4px solid var(--bg-card);
            box-shadow: var(--shadow);
            margin-bottom: 24px;
            transition: var(--transition);
        }}
        
        .avatar:hover {{
            transform: scale(1.05);
            box-shadow: var(--shadow-hover);
        }}
        
        .hero-name {{
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 8px;
            color: var(--text-primary);
        }}
        
        .hero-username {{
            font-size: 1.1rem;
            color: var(--text-muted);
            font-weight: 400;
            margin-bottom: 16px;
        }}
        
        .hero-bio {{
            font-size: 1.15rem;
            color: var(--text-secondary);
            max-width: 500px;
            margin: 0 auto 20px;
            line-height: 1.7;
        }}
        
        .hero-info {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 24px;
        }}
        
        .info-item {{
            font-size: 0.9rem;
            color: var(--text-muted);
        }}
        
        .social-links {{
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 32px;
        }}
        
        .social-link {{
            display: inline-flex;
            align-items: center;
            padding: 10px 20px;
            background: var(--bg-card);
            color: var(--text-primary);
            text-decoration: none;
            border-radius: var(--radius-sm);
            font-size: 0.9rem;
            font-weight: 500;
            border: 1px solid var(--border);
            transition: var(--transition);
        }}
        
        .social-link:hover {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }}
        
        /* ═══ Stats ═══ */
        .stats {{
            display: flex;
            gap: 32px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--accent);
        }}
        
        .stat-label {{
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        /* ═══ Section ═══ */
        .section {{
            padding: 60px 0;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-title::before {{
            content: '';
            width: 4px;
            height: 24px;
            background: var(--accent);
            border-radius: 2px;
        }}
        
        .section-subtitle {{
            font-size: 0.95rem;
            color: var(--text-muted);
            margin-bottom: 32px;
        }}
        
        /* ═══ Language Bar ═══ */
        .lang-bar {{
            display: flex;
            height: 12px;
            border-radius: 6px;
            overflow: hidden;
            margin-bottom: 16px;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
        }}
        
        .lang-bar-segment {{
            height: 100%;
            transition: var(--transition);
        }}
        
        .lang-bar-segment:hover {{
            opacity: 0.8;
            transform: scaleY(1.2);
        }}
        
        .lang-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
        }}
        
        .lang-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        
        .lang-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            flex-shrink: 0;
        }}
        
        .lang-name {{
            font-weight: 500;
        }}
        
        .lang-percent {{
            color: var(--text-muted);
        }}
        
        /* ═══ Repo Cards ═══ */
        .repo-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
        }}
        
        .repo-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: var(--radius);
            padding: 24px;
            transition: var(--transition);
            display: flex;
            flex-direction: column;
            text-decoration: none;
            color: inherit;
        }}
        
        .repo-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-hover);
            border-color: var(--accent);
            background: var(--bg-card-hover);
        }}
        
        .repo-name {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--accent);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .repo-name::before {{
            content: '⬡';
            font-size: 0.8em;
        }}
        
        .repo-desc {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 16px;
            flex: 1;
            line-height: 1.6;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .repo-meta {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}
        
        .repo-meta-item {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .repo-lang-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }}
        
        .repo-topics {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 12px;
        }}
        
        .topic-tag {{
            padding: 3px 10px;
            background: var(--accent-light);
            color: var(--accent);
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        
        /* ═══ Activity ═══ */
        .activity-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        
        .activity-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 18px;
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-sm);
            transition: var(--transition);
        }}
        
        .activity-item:hover {{
            border-color: var(--accent);
        }}
        
        .activity-icon {{
            width: 36px;
            height: 36px;
            background: var(--accent-light);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            flex-shrink: 0;
        }}
        
        .activity-content {{
            flex: 1;
        }}
        
        .activity-type {{
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--text-primary);
        }}
        
        .activity-repo {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        
        .activity-date {{
            font-size: 0.8rem;
            color: var(--text-muted);
        }}
        
        /* ═══ Footer ═══ */
        .footer {{
            padding: 40px 0;
            text-align: center;
            border-top: 1px solid var(--border-light);
            margin-top: 40px;
        }}
        
        .footer-text {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        
        .footer-link {{
            color: var(--accent);
            text-decoration: none;
        }}
        
        .footer-link:hover {{
            text-decoration: underline;
        }}
        
        /* ═══ Animations ═══ */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .animate-in {{
            animation: fadeIn 0.6s ease forwards;
        }}
        
        /* ═══ Responsive ═══ */
        @media (max-width: 768px) {{
            .hero {{
                padding: 50px 0 40px;
            }}
            
            .hero-name {{
                font-size: 1.8rem;
            }}
            
            .avatar {{
                width: 100px;
                height: 100px;
            }}
            
            .repo-grid {{
                grid-template-columns: 1fr;
            }}
            
            .stats {{
                gap: 20px;
            }}
            
            .stat-value {{
                font-size: 1.4rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- ═══ Hero ═══ -->
    <section class="hero">
        <div class="container">
            <img src="{avatar}" alt="{name}" class="avatar animate-in">
            <h1 class="hero-name animate-in">{name}</h1>
            <p class="hero-username animate-in">@{username}</p>
            <p class="hero-bio animate-in">{bio}</p>
            
            <div class="hero-info animate-in">
                {info_html}
            </div>
            
            <div class="social-links animate-in">
                {social_links}
            </div>
            
            <div class="stats animate-in">
                <div class="stat">
                    <div class="stat-value">{public_repos}</div>
                    <div class="stat-label">Repositories</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{total_stars}</div>
                    <div class="stat-label">Stars</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{followers}</div>
                    <div class="stat-label">Followers</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{following}</div>
                    <div class="stat-label">Following</div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- ═══ Languages ═══ -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Tech Stack</h2>
            <p class="section-subtitle">Languages used across repositories</p>
            
            {lang_bar}
            
            <div class="lang-list">
                {lang_list}
            </div>
        </div>
    </section>
    
    <!-- ═══ Repositories ═══ -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Featured Projects</h2>
            <p class="section-subtitle">Top repositories by stars</p>
            
            <div class="repo-grid">
                {repo_cards}
            </div>
        </div>
    </section>
    
    <!-- ═══ Activity ═══ -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Recent Activity</h2>
            <p class="section-subtitle">Latest public contributions</p>
            
            <div class="activity-list">
                {activity_html}
            </div>
        </div>
    </section>
    
    <!-- ═══ Footer ═══ -->
    <footer class="footer">
        <div class="container">
            <p class="footer-text">
                Generated with ❤️ by <a href="https://github.com/Fatkhl/gh-portfolio-gen" class="footer-link">GH Portfolio Generator</a>
                · Updated {data.get('generated_at', '')}
            </p>
        </div>
    </footer>
    
    <!-- ═══ Scripts ═══ -->
    <script>
        // Intersection Observer for scroll animations
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, {{ threshold: 0.1 }});
        
        document.querySelectorAll('.repo-card, .activity-item, .lang-item').forEach(el => {{
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(el);
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def _build_repo_cards(self, repos: list) -> str:
        """Build HTML for repository cards."""
        cards = []
        lang_colors = {
            "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Python": "#3572A5",
            "Java": "#b07219", "C++": "#f34b7d", "Go": "#00ADD8", "Rust": "#dea584",
            "Ruby": "#701516", "PHP": "#4F5D95", "Shell": "#89e051", "HTML": "#e34c26",
            "CSS": "#563d7c", "Solidity": "#AA6746", "Dart": "#00B4AB",
        }
        
        for r in repos:
            topics_html = ""
            if r.get("topics"):
                tags = "".join(f'<span class="topic-tag">{t}</span>' for t in r["topics"][:5])
                topics_html = f'<div class="repo-topics">{tags}</div>'
            
            lang_color = lang_colors.get(r.get("language", ""), "#8b8b8b")
            lang_html = ""
            if r.get("language"):
                lang_html = f'<span class="repo-meta-item"><span class="repo-lang-dot" style="background:{lang_color}"></span> {r["language"]}</span>'
            
            stars_html = f'<span class="repo-meta-item">⭐ {r["stars"]}</span>' if r.get("stars", 0) > 0 else ""
            forks_html = f'<span class="repo-meta-item">🔀 {r["forks"]}</span>' if r.get("forks", 0) > 0 else ""
            
            desc = r.get("description", "") or "No description"
            
            cards.append(f'''
                <a href="{r['url']}" target="_blank" class="repo-card">
                    <div class="repo-name">{r['name']}</div>
                    {topics_html}
                    <div class="repo-desc">{desc}</div>
                    <div class="repo-meta">
                        {lang_html}
                        {stars_html}
                        {forks_html}
                    </div>
                </a>''')
        
        return "\n".join(cards)
    
    def _build_language_bar(self, languages: list) -> str:
        """Build the language progress bar."""
        if not languages:
            return ""
        
        segments = []
        for lang in languages[:8]:
            segments.append(
                f'<div class="lang-bar-segment" style="width:{lang["percentage"]}%;background:{lang["color"]}" title="{lang["name"]}: {lang["percentage"]}%"></div>'
            )
        
        return f'<div class="lang-bar">{"".join(segments)}</div>'
    
    def _build_language_list(self, languages: list) -> str:
        """Build the language list below the bar."""
        items = []
        for lang in languages[:12]:
            items.append(f'''
                <div class="lang-item">
                    <span class="lang-dot" style="background:{lang['color']}"></span>
                    <span class="lang-name">{lang['name']}</span>
                    <span class="lang-percent">{lang['percentage']}%</span>
                </div>''')
        
        return "\n".join(items)
    
    def _build_activity(self, activities: list) -> str:
        """Build recent activity list."""
        if not activities:
            return '<p style="color:var(--text-muted)">No recent public activity</p>'
        
        icons = {
            "Push": "📤", "Create": "✨", "Delete": "🗑️", "Fork": "🔀",
            "Issues": "🐛", "PullRequest": "🔀", "Watch": "⭐", "Release": "📦",
            "Public": "🌍", "Member": "👤", "Gollum": "📝",
        }
        
        items = []
        for a in activities:
            event_type = a.get("type", "Event")
            icon = icons.get(event_type, "📌")
            repo = a.get("repo", "")
            date = a.get("date", "")
            
            items.append(f'''
                <div class="activity-item">
                    <div class="activity-icon">{icon}</div>
                    <div class="activity-content">
                        <div class="activity-type">{event_type}</div>
                        <div class="activity-repo">{repo}</div>
                    </div>
                    <div class="activity-date">{date}</div>
                </div>''')
        
        return "\n".join(items)
