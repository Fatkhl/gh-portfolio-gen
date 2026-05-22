#!/usr/bin/env python3
"""
GitHub Portfolio Generator
Auto-generate a developer portfolio from GitHub data.

Usage:
    python generate.py <github_username> [--theme dark|light|cream] [--output ./output]
    python generate.py Fatkhl --deploy
"""

import argparse
import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from github_fetcher import GitHubFetcher
from template_engine import TemplateEngine


def main():
    parser = argparse.ArgumentParser(
        description="🚀 GitHub Portfolio Generator — Auto-create developer portfolio from GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate.py Fatkhl                     # Generate with cream theme
  python generate.py Fatkhl --theme dark        # Dark theme
  python generate.py Fatkhl --deploy            # Generate + deploy to GitHub Pages
  python generate.py Fatkhl --output ./mysite   # Custom output directory
        """
    )
    
    parser.add_argument("username", help="GitHub username")
    parser.add_argument("--theme", choices=["cream", "dark", "ocean", "hacker"], default="hacker",
                       help="Portfolio theme (default: cream)")
    parser.add_argument("--output", "-o", default="./output",
                       help="Output directory (default: ./output)")
    parser.add_argument("--deploy", action="store_true",
                       help="Deploy to GitHub Pages after generation")
    parser.add_argument("--repo-name", default=None,
                       help="Repo name for deployment (default: <username>.github.io)")
    parser.add_argument("--token", default=None,
                       help="GitHub token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--max-repos", type=int, default=50,
                       help="Maximum repos to fetch (default: 50)")
    parser.add_argument("--skip-forks", action="store_true",
                       help="Skip forked repositories")
    parser.add_argument("--show-stars", action="store_true", default=True,
                       help="Show star count on repos")
    parser.add_argument("--contribution-graph", action="store_true", default=True,
                       help="Include contribution graph")
    
    args = parser.parse_args()
    
    print(f"""
╔═══════════════════════════════════════════════════════╗
║         🚀 GitHub Portfolio Generator                 ║
║         by AER — ARRAYYAN Jr                          ║
╚═══════════════════════════════════════════════════════╝
    """)
    
    # Get token
    token = args.token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    
    # Step 1: Fetch GitHub data
    print(f"📡 Fetching data for @{args.username}...")
    fetcher = GitHubFetcher(token=token)
    profile = fetcher.fetch_profile(args.username)
    repos = fetcher.fetch_repos(
        args.username, 
        max_repos=args.max_repos,
        skip_forks=args.skip_forks
    )
    languages = fetcher.fetch_language_stats(repos)
    contributions = fetcher.fetch_contributions(args.username)
    
    print(f"   ✓ Found {len(repos)} repositories")
    print(f"   ✓ Found {len(languages)} languages")
    print(f"   ✓ Profile: {profile.get('name', args.username)}")
    
    # Step 2: Prepare template data
    data = {
        "profile": profile,
        "repos": sorted(repos, key=lambda r: r.get("stars", 0), reverse=True),
        "languages": languages,
        "contributions": contributions,
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "theme": args.theme,
        "show_stars": args.show_stars,
        "show_contributions": args.contribution_graph,
    }
    
    # Step 3: Generate portfolio
    print(f"\n🎨 Generating portfolio with '{args.theme}' theme...")
    engine = TemplateEngine(theme=args.theme)
    output_path = Path(args.output)
    engine.generate(data, output_path)
    
    print(f"   ✓ Portfolio generated at: {output_path.absolute()}")
    
    # Step 4: Deploy if requested
    if args.deploy:
        repo_name = args.repo_name or f"{args.username}.github.io"
        print(f"\n🚀 Deploying to {repo_name}...")
        deploy_to_github(output_path, repo_name, token)
        print(f"   ✓ Live at: https://{repo_name}")
    
    print(f"""
╔═══════════════════════════════════════════════════════╗
║  ✅ Done! Portfolio generated successfully            ║
║                                                       ║
║  📁 Output: {str(output_path.absolute()):<38s}║
║  🌐 Open:   {str(output_path.absolute() / 'index.html'):<38s}║
╚═══════════════════════════════════════════════════════╝
    """)
    
    if not args.deploy:
        print("💡 To deploy to GitHub Pages, run:")
        print(f"   python generate.py {args.username} --deploy")


def deploy_to_github(output_path: Path, repo_name: str, token: str = None):
    """Deploy generated portfolio to GitHub Pages."""
    import subprocess
    
    os.chdir(output_path)
    
    # Init git if not already
    if not (output_path / ".git").exists():
        run("git init")
        run("git checkout -b master")
    
    # Create .nojekyll
    (output_path / ".nojekyll").touch()
    
    # Add and commit
    run("git add -A")
    run(f'git commit -m "🚀 Auto-update portfolio {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}"')
    
    # Set remote
    github_url = f"https://github.com/Fatkhl/{repo_name}.git"
    if token:
        github_url = f"https://{token}@github.com/Fatkhl/{repo_name}.git"
    
    run(f"git remote remove origin 2>/dev/null; git remote add origin {github_url}")
    run("git push -u origin master --force")
    
    print(f"   ✓ Deployed to https://Fatkhl.github.io/{repo_name.replace('.github.io', '')}")


def run(cmd: str):
    """Run a shell command."""
    subprocess.run(cmd, shell=True, capture_output=True, text=True)


if __name__ == "__main__":
    main()
