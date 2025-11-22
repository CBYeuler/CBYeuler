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

    rows = []
    for repo in repos:
        name = repo["name"]
        url = repo["html_url"]
        card = f"""
<td align="center">
  <a href="{url}">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={name}&theme=gruvbox&hide_border=true" />
  </a>
</td>
"""
        rows.append(card)

    # Eğer 2 repo değilse doldur
    while len(rows) < 2:
        rows.append("<td></td>")

    table = f"<table><tr>{''.join(rows)}</tr></table>"
    return table


def main():
    with open("README.md", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- PROJECTS:START -->"
    end_marker = "<!-- PROJECTS:END -->"

    block = fetch_latest_repos()

    replacement = f"{start_marker}\n{block}\n{end_marker}"

    pattern = re.compile(
        rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}",
        re.DOTALL,
    )

    new_content, count = pattern.subn(replacement, content)

    if count == 0:
        print("Markers not found!")
        return

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README updated.")


if __name__ == "__main__":
    main()
