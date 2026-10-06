#!/usr/bin/env python3
"""Lightweight HCL check (no packer needed): braces balance, versions pinned, playbook path exists."""
import pathlib, re, sys
src = pathlib.Path("orders.pkr.hcl").read_text()
errs = []
if src.count("{") != src.count("}"):
    errs.append("unbalanced braces")
for blk in ("packer", "source", "build"):
    if not re.search(rf"^{blk}\b", src, re.M):
        errs.append(f"missing {blk} block")
for v in re.findall(r'version\s*=\s*"([^"]+)"', src):
    if not v.startswith("= "):
        errs.append(f"plugin version not pinned exactly: {v}")
pb = re.search(r'playbook_file\s*=\s*"([^"]+)"', src).group(1)
if not pathlib.Path(pb).exists():
    errs.append(f"playbook not found: {pb}")
print("\n".join(errs) or "ok: packer template looks valid")
sys.exit(1 if errs else 0)
