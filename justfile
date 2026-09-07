install-skills:
    npx skills add iancleary/skills -g

install-plugin:
    #!/usr/bin/env bash
    set -euo pipefail
    if codex plugin marketplace list --json | python3 -c 'import json, sys; data = json.load(sys.stdin); raise SystemExit(not any(item.get("name") == "iancleary-skills" for item in data.get("marketplaces", [])))'; then
        codex plugin marketplace upgrade iancleary-skills
    else
        codex plugin marketplace add iancleary/skills
    fi
    codex plugin add bulk-read-routing@iancleary-skills

install-agent-roles:
    python3 plugins/bulk-read-routing/scripts/install_agent_roles.py
