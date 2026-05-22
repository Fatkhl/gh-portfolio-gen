"""
GitHub API Fetcher
Fetches user profile, repos, languages, and contribution data.
"""

import json
import os
import re
import urllib.request
import urllib.error
from typing import Optional


class GitHubFetcher:
    """Fetch GitHub profile data via REST API (no external deps)."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GH-Portfolio-Generator",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request to GitHub API."""
        url = f"{self.BASE_URL}{endpoint}"
        if params:
            query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
            url = f"{url}?{query}"
        
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ValueError(f"User not found: {endpoint}")
            elif e.code == 403:
                print(f"   ⚠ Rate limited. Set GITHUB_TOKEN for higher limits.")
                return {}
            raise
    
    def _get_all_pages(self, endpoint: str, params: dict = None, max_pages: int = 10) -> list:
        """Fetch all pages of a paginated endpoint."""
        all_items = []
        for page in range(1, max_pages + 1):
            p = {**(params or {}), "page": str(page), "per_page": "100"}
            items = self._get(endpoint, p)
            if not items or not isinstance(items, list):
                break
            all_items.extend(items)
            if len(items) < 100:
                break
        return all_items
    
    def fetch_profile(self, username: str) -> dict:
        """Fetch user profile information."""
        data = self._get(f"/users/{username}")
        
        return {
            "username": data.get("login", username),
            "name": data.get("name", username),
            "bio": data.get("bio", ""),
            "avatar_url": data.get("avatar_url", ""),
            "location": data.get("location", ""),
            "company": data.get("company", ""),
            "blog": data.get("blog", ""),
            "twitter": data.get("twitter_username", ""),
            "github_url": data.get("html_url", f"https://github.com/{username}"),
            "public_repos": data.get("public_repos", 0),
            "followers": data.get("followers", 0),
            "following": data.get("following", 0),
            "created_at": data.get("created_at", ""),
        }
    
    def fetch_repos(self, username: str, max_repos: int = 50, skip_forks: bool = False) -> list:
        """Fetch user repositories."""
        raw_repos = self._get_all_pages(f"/users/{username}/repos", {"sort": "updated"})
        
        repos = []
        for r in raw_repos[:max_repos]:
            if skip_forks and r.get("fork", False):
                continue
            
            repos.append({
                "name": r.get("name", ""),
                "description": r.get("description", "") or "",
                "url": r.get("html_url", ""),
                "homepage": r.get("homepage", "") or "",
                "language": r.get("language", ""),
                "stars": r.get("stargazers_count", 0),
                "forks": r.get("forks_count", 0),
                "watchers": r.get("watchers_count", 0),
                "topics": r.get("topics", []),
                "created_at": r.get("created_at", ""),
                "updated_at": r.get("updated_at", ""),
                "pushed_at": r.get("pushed_at", ""),
                "size": r.get("size", 0),
                "archived": r.get("archived", False),
                "fork": r.get("fork", False),
                "license": (r.get("license") or {}).get("spdx_id", ""),
            })
        
        return repos
    
    def fetch_language_stats(self, repos: list) -> list:
        """Aggregate language statistics from repos."""
        lang_counts = {}
        for r in repos:
            lang = r.get("language")
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        # Sort by count
        sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Color map for common languages
        colors = {
            "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Python": "#3572A5",
            "Java": "#b07219", "C++": "#f34b7d", "C": "#555555", "C#": "#178600",
            "Go": "#00ADD8", "Rust": "#dea584", "Ruby": "#701516", "PHP": "#4F5D95",
            "Swift": "#F05138", "Kotlin": "#A97BFF", "Dart": "#00B4AB",
            "Shell": "#89e051", "HTML": "#e34c26", "CSS": "#563d7c",
            "SCSS": "#c6538c", "Vue": "#41b883", "Svelte": "#ff3e00",
            "Lua": "#000080", "Perl": "#0298c3", "R": "#198CE7",
            "Scala": "#c22d40", "Elixir": "#6e4a7e", "Haskell": "#5e5086",
            "Jupyter Notebook": "#DA5B0B", "Solidity": "#AA6746",
        }
        
        total = sum(c for _, c in sorted_langs)
        
        return [
            {
                "name": lang,
                "count": count,
                "percentage": round(count / total * 100, 1) if total else 0,
                "color": colors.get(lang, "#8b8b8b"),
            }
            for lang, count in sorted_langs[:12]  # Top 12
        ]
    
    def fetch_contributions(self, username: str) -> dict:
        """Fetch contribution data (public activity)."""
        # GitHub doesn't have a direct API for contributions graph
        # We'll use the events API as an approximation
        events = self._get(f"/users/{username}/events/public", {"per_page": "100"})
        
        # Count events by type
        event_counts = {}
        recent_activity = []
        
        for event in (events or [])[:100]:
            event_type = event.get("type", "")
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            
            # Recent activity (last 10)
            if len(recent_activity) < 10:
                repo = event.get("repo", {}).get("name", "")
                created = event.get("created_at", "")
                recent_activity.append({
                    "type": event_type.replace("Event", ""),
                    "repo": repo,
                    "date": created[:10] if created else "",
                })
        
        return {
            "total_events": len(events or []),
            "event_counts": event_counts,
            "recent_activity": recent_activity,
        }
