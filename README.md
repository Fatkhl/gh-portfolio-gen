# 🚀 GitHub Portfolio Generator

> Auto-generate a beautiful developer portfolio from your GitHub profile

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![GitHub](https://img.shields.io/badge/GitHub-API-181717?style=for-the-badge&logo=github)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

One command. Beautiful portfolio. Auto-deploy to GitHub Pages.

---

## ✨ Features

- 🔌 **Zero dependencies** — pure Python, no pip install needed
- 🎨 **Cream/warm theme** — clean, premium design (dark & ocean themes too)
- 📊 **Auto-detect** tech stack from repos
- ⭐ **Sort by stars** — best projects first
- 📱 **Fully responsive** — works on mobile
- 🚀 **One-command deploy** to GitHub Pages
- 🔄 **Auto-update** — run again to refresh data

---

## ⚡ Quick Start

```bash
# Clone
git clone https://github.com/Fatkhl/gh-portfolio-gen.git
cd gh-portfolio-gen

# Generate (no dependencies needed!)
python generate.py YOUR_GITHUB_USERNAME

# Open in browser
open output/index.html
```

---

## 🎨 Themes

```bash
# Cream (default — warm & clean)
python generate.py YOUR_USERNAME --theme cream

# Dark theme
python generate.py YOUR_USERNAME --theme dark

# Ocean theme
python generate.py YOUR_USERNAME --theme ocean
```

---

## 🚀 Deploy to GitHub Pages

```bash
# Generate + auto-deploy
python generate.py YOUR_USERNAME --deploy

# Your portfolio is now live at:
# https://YOUR_USERNAME.github.io
```

### Manual Deploy

```bash
# 1. Create repo YOUR_USERNAME.github.io on GitHub

# 2. Generate
python generate.py YOUR_USERNAME --output ./portfolio

# 3. Push
cd portfolio
git init
git add -A
git commit -m "🚀 Deploy portfolio"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_USERNAME.github.io.git
git push -u origin master --force
```

---

## 📖 Full Usage

```
python generate.py <username> [options]

Arguments:
  username                GitHub username

Options:
  --theme {cream,dark,ocean}  Theme (default: cream)
  --output, -o PATH           Output directory (default: ./output)
  --deploy                    Deploy to GitHub Pages
  --repo-name NAME            Repo for deployment (default: username.github.io)
  --token TOKEN               GitHub token (or set GITHUB_TOKEN)
  --max-repos N               Max repos to fetch (default: 50)
  --skip-forks                Skip forked repos
  --no-stars                  Hide star counts
  --no-contributions          Hide contribution graph
```

---

## 🔑 GitHub Token (Optional)

For higher API rate limits and private repos:

```bash
# Set environment variable
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Or pass directly
python generate.py YOUR_USERNAME --token ghp_xxxxxxxxxxxx
```

Get a token at: https://github.com/settings/tokens

---

## 📁 Project Structure

```
gh-portfolio-gen/
├── generate.py              # Main CLI entry point
├── src/
│   ├── github_fetcher.py    # GitHub API client
│   └── template_engine.py   # HTML generator
├── templates/               # (future: custom templates)
├── static/                  # (future: static assets)
├── output/                  # Generated portfolio
│   ├── index.html
│   └── .nojekyll
└── README.md
```

---

## 🎯 What Gets Generated

Your portfolio includes:

- **Profile section** — avatar, name, bio, location, social links
- **Stats** — repos count, total stars, followers
- **Tech stack** — language bar with percentages
- **Featured projects** — top repos sorted by stars
- **Recent activity** — latest public contributions
- **Responsive design** — works on all devices

---

## 🔧 Customization

### Edit the template

The HTML template is in `src/template_engine.py`. You can:
- Change colors via CSS variables (`:root` section)
- Modify layout in `_render_index()`
- Add new sections

### CSS Variables

```css
:root {
    --bg-primary: #f5f0e8;      /* Page background */
    --bg-card: #ffffff;          /* Card background */
    --text-primary: #1a1714;     /* Main text */
    --text-secondary: #5c564a;   /* Secondary text */
    --accent: #c4956a;           /* Accent color */
    --border: #e0dbd2;           /* Borders */
}
```

---

## 📝 License

MIT — free to use, modify, and distribute.

---

*Built with ❤️ by [AER](https://github.com/Fatkhl) — ARRAYYAN Jr*
