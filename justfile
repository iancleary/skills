# Repository Python commands use managed Python, independent of ambient python3.
check:
    uv run --no-project --managed-python --python 3.11 python -B scripts/check_curation.py
    uv run --no-project --managed-python --python 3.11 python -B -m unittest discover -s scripts -p 'test_curation.py'
    uv run --no-project --managed-python --python 3.11 python -B -m unittest discover -s plugins/bulk-read-routing/scripts -p 'test_*.py'
    uv run --no-project --managed-python --python 3.11 python -B scripts/test_managed_python.py
    git diff --check

install-skills:
    npx skills add iancleary/skills -g

install-plugin:
    #!/usr/bin/env bash
    set -euo pipefail
    if codex plugin marketplace list --json | uv run --no-project --managed-python --python 3.11 python -c 'import json, sys; data = json.load(sys.stdin); raise SystemExit(not any(item.get("name") == "iancleary-skills" for item in data.get("marketplaces", [])))'; then
        codex plugin marketplace upgrade iancleary-skills
    else
        codex plugin marketplace add iancleary/skills
    fi
    codex plugin add bulk-read-routing@iancleary-skills

[positional-arguments]
install-agent-roles *args:
    uv run --no-project --managed-python --python 3.11 python plugins/bulk-read-routing/scripts/install_agent_roles.py "$@"

[positional-arguments]
test-live-delegation *args:
    uv run --no-project --managed-python --python 3.11 python plugins/bulk-read-routing/scripts/test_live_delegation.py "$@"
