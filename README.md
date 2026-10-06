# iac-ansible-packer

Four small configuration-as-code examples that provision the same Orders JVM host with Ansible, Ansible Vault, Packer and cloud-init, each with an offline check you can run without any of those tools installed.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`ansible-roles-jvm`](./ansible-roles-jvm) | A `jvm` role that installs a JRE, creates a service user and installs a systemd unit | `python3 verify.py` |
| [`inventories-vault`](./inventories-vault) | Separate dev and prod inventories with secrets kept behind `vault_` variables | `python3 verify.py` |
| [`packer-golden-image`](./packer-golden-image) | A Packer template that builds a Docker image by running the Ansible role | `python3 verify.py` |
| [`cloud-init`](./cloud-init) | A `user-data.yml` that configures the same host on first boot | `python3 verify.py` |

Run each command from inside its folder. All four checks are structural: none of them runs Ansible, Packer or cloud-init, and each folder README says what was not run end to end. The shared example domain is Orders.

## Prerequisites

- Python 3 with PyYAML (for the checks).
- To actually apply the code: Ansible, Packer 1.x with the pinned `docker` 1.1.1 and `ansible` 1.1.2 plugins, Docker, and a cloud-init capable VM image.

## How to read it

Start with `ansible-roles-jvm`, because `packer-golden-image` reuses its playbook. Then read `inventories-vault`, and finish with `cloud-init`, which reaches the same result without Ansible.
