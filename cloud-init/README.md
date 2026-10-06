# cloud-init

A `user-data.yml` cloud-config file that sets up the Orders JVM host on first boot, without Ansible.

## Goal

Show what a stock cloud image can configure for itself at first boot: hostname, packages, a service user, a config file and a directory.

## Run it

```
python3 verify.py
```
Expected: `ok: user-data valid`.

Booting it for real (not run here, because no VM or cloud-init tooling was used): pass `user-data.yml` as the user-data of an Ubuntu cloud image.


## What it proves

- The file starts with `#cloud-config` and parses as YAML.
- It uses only a known set of keys: `hostname`, `package_update`, `packages`, `users`, `write_files`, `runcmd` and `final_message`. It installs `openjdk-21-jre-headless`, creates the `orders` user with `/usr/sbin/nologin`, and writes `/etc/orders/orders.env` with `SERVER_PORT=8080` and `JAVA_OPTS=-Xmx256m`.
- File permissions are the quoted string `"0644"`, which the check requires to avoid YAML reading the number as octal by accident.

## Trade-offs

- The check is a hand-written key allow-list, not the official cloud-init schema validator, so a typo inside a valid key can pass.
- Unlike `ansible-roles-jvm`, this runs once at first boot. Later changes need a new instance or manual work.
- It writes the environment file but no systemd unit and no `orders.jar`, so the service itself is not set up.
- `orders.env` is world-readable (`0644`); do not put secrets in it.

## When not to use it

- For hosts that change over time, use a configuration tool such as the Ansible role.
- When the logic needs conditions or loops, cloud-config becomes hard to read.
