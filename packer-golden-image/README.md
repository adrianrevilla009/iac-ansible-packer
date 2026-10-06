# packer-golden-image

A Packer template, `orders.pkr.hcl`, that builds an `orders-golden:local` Docker image by running the `ansible-roles-jvm` playbook inside an Ubuntu 24.04 container.

## Goal

Show how a golden image reuses the same Ansible role as a live host, so the image and the running servers cannot drift apart.

## Run it

```
python3 verify.py
```
Expected: `ok: packer template looks valid`.

To build the image (not run here: Packer and Ansible are not installed, so the build has never been executed):

```
packer init .
packer build orders.pkr.hcl
```

## What it proves

- Both plugins are pinned exactly: `docker` `= 1.1.1` and `ansible` `= 1.1.2`; the check rejects any version that does not start with `= `.
- The `ansible` provisioner points to `../ansible-roles-jvm/site.yml`, and the check fails if that file is missing.
- The build passes `jvm_manage_service=false`, so the role skips the systemd restart handler inside a container, and a `docker-tag` post-processor names the result `orders-golden:local`.

## Trade-offs

- The check only counts braces and looks for the `packer`, `source` and `build` blocks; it is not `packer validate`.
- A Docker image is a local stand-in for a VM image such as an AMI; a cloud build would use a different source block.
- The base image is `ubuntu:24.04`, a moving tag, and the shell step installs Python with `apt-get`, so builds are not fully reproducible.
- Systemd does not run in the container, so the unit file is installed but never started.

## When not to use it

- When you only run containers, a Dockerfile is simpler than Packer plus Ansible.
- When hosts are configured after boot and rarely replaced, baking images adds a build step with little benefit.
