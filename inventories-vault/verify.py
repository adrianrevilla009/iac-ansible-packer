#!/usr/bin/env python3
"""Check each inventory parses, every vars.yml indirection (vault_*) has a matching key in vault.yml.example,
and no committed vault.yml is plaintext."""
import pathlib, re, sys, yaml
errs = []
for inv in sorted(pathlib.Path("inventories").iterdir()):
    hosts = yaml.safe_load((inv / "hosts.yml").read_text())
    if not hosts["all"]["children"]["orders"]["hosts"]:
        errs.append(f"{inv.name}: no hosts")
    gv = inv / "group_vars/all"
    refs = set(re.findall(r"\{\{\s*(vault_\w+)", (gv / "vars.yml").read_text()))
    have = set(yaml.safe_load((gv / "vault.yml.example").read_text()))
    for r in refs - have:
        errs.append(f"{inv.name}: {r} missing from vault.yml.example")
    real = gv / "vault.yml"
    if real.exists() and not real.read_text().startswith("$ANSIBLE_VAULT;"):
        errs.append(f"{inv.name}: vault.yml is not encrypted")
print("\n".join(errs) or "ok: inventories and vault indirection valid")
sys.exit(1 if errs else 0)
