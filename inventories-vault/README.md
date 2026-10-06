# inventories-vault

Dev and prod Ansible inventories with per-environment `group_vars` and an Ansible Vault indirection for the database password.

## Goal

Show how to keep environment differences in inventories and keep secrets out of plain variables, so only an encrypted file ever needs to be committed.

## Run it

```
python3 verify.py
```
Expected: `ok: inventories and vault indirection valid`.

Creating a real vault file (not run here, because Ansible is not installed):

```
cp inventories/dev/group_vars/all/vault.yml.example inventories/dev/group_vars/all/vault.yml
ansible-vault encrypt inventories/dev/group_vars/all/vault.yml
```

## What it proves

- `inventories/dev/hosts.yml` has one local host; `inventories/prod/hosts.yml` has two hosts (`10.0.0.11`, `10.0.0.12`).
- Heap differs per environment (`orders_heap_mb` is 256 in dev and 2048 in prod), set in each `vars.yml`.
- `vars.yml` only refers to `{{ vault_orders_db_password }}`; the check confirms each such reference has a key in `vault.yml.example` and fails if a `vault.yml` exists that does not start with `$ANSIBLE_VAULT;`.

## Trade-offs

- The `.example` files contain the placeholder value `change-me`, so the lab holds no real secret, but you must create and encrypt `vault.yml` yourself.
- The check does not decrypt anything; it only looks at the file header.
- The prod hosts are example addresses, so `ansible-playbook -i inventories/prod` would not reach anything real.
- These inventories are not wired to the `jvm` role's variable names (`jvm_heap_mb`); they show the pattern only.

## When not to use it

- When secrets already live in a managed store such as a cloud secret manager, vault files add a second place to rotate.
- For one environment with one host, a single inventory file is enough.
