#!/usr/bin/env python3
"""Structural check (no ansible needed): YAML parses, tasks use FQCN modules, notify targets exist, template vars have defaults."""
import re, sys, pathlib, yaml
role = pathlib.Path("roles/jvm")
tasks = yaml.safe_load((role / "tasks/main.yml").read_text())
handlers = {h["name"] for h in yaml.safe_load((role / "handlers/main.yml").read_text())}
defaults = yaml.safe_load((role / "defaults/main.yml").read_text())
yaml.safe_load(pathlib.Path("site.yml").read_text())
errs = []
for t in tasks:
    mod = next(k for k in t if k not in ("name", "notify", "become", "when"))
    if not mod.startswith("ansible.builtin."):
        errs.append(f"{t['name']}: non-FQCN module {mod}")
    if t.get("notify") and t["notify"] not in handlers:
        errs.append(f"{t['name']}: unknown handler")
for v in set(re.findall(r"\{\{\s*(\w+)", (role / "templates/orders.service.j2").read_text())):
    if v not in defaults:
        errs.append(f"template var {v} lacks a default")
print("\n".join(errs) or "ok: role structure valid")
sys.exit(1 if errs else 0)
