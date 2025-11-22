import json
import re
import urllib.request

USERNAME = "CBYeuler"
API_URL = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=10"


def fetch_latest_repos(n=2):
    req = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "github-profile-bot"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)

    # fork olmayanlardan en son güncellenen N tanesini al
    repos = [r for r in data if not r.get("fork", False)][:n]

    lines = []
    for repo in repos:
        name = repo["name"]
        url = repo["html_url"]
        desc = repo.get("description") or ""
        # description çok uzunsa kısalt
        if len(desc) > 80:
            desc = desc[:77] + "..."
        if desc:
            line = f"- [{name}]({url}) — {desc}"
        else:
            line = f"- [{name}]({url})"
        lines.append(line)

    return "\n".join(lines) if lines else "- (no recent projects found)"


def main():
    with open("README.md", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- PROJECTS:START -->"
    end_marker = "<!-- PROJECTS:END -->"

    latest_block = fetch_latest_repos(2)

    replacement = f"{start_marker}\n{latest_block}\n{end_marker}"

    pattern = re.compile(
        rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}",
        re.DOTALL,
    )

    new_content, count = pattern.subn(replacement, content)

    if count == 0:
        print("Markers not found in README.md")
        return

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README.md updated with latest projects.")


if __name__ == "__main__":
    main()
