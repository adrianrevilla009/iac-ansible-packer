#!/usr/bin/env python3
"""Check user-data starts with #cloud-config, parses, and uses only known top-level keys with sane types."""
import pathlib, sys, yaml
text = pathlib.Path("user-data.yml").read_text()
KNOWN = {"hostname", "package_update", "packages", "users", "write_files", "runcmd", "final_message"}
errs = []
if not text.startswith("#cloud-config\n"):
    errs.append("first line must be #cloud-config")
doc = yaml.safe_load(text)
for k in set(doc) - KNOWN:
    errs.append(f"unexpected key {k}")
for f in doc.get("write_files", []):
    if not str(f.get("permissions", "")).startswith("0"):
        errs.append(f"{f.get('path')}: permissions must be a quoted octal string")
if not isinstance(doc.get("packages"), list):
    errs.append("packages must be a list")
print("\n".join(errs) or "ok: user-data valid")
sys.exit(1 if errs else 0)
