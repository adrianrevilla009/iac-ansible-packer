# ansible-roles-jvm

An Ansible `jvm` role and a one-play `site.yml` that prepare a host to run the Orders service as a systemd unit.

## Goal

Show how a small role is split into tasks, defaults, a template and a handler, so the same code can configure a laptop, a VM or an image build.

## Run it

```
python3 verify.py
```
Expected: `ok: role structure valid`.

To apply the role (not run here, because Ansible is not installed on the machine this was written on):

```
ansible-playbook site.yml
```

## What it proves

- `roles/jvm/tasks/main.yml` has four tasks (install `openjdk-21-jre-headless`, create the `orders` user, create `/opt/orders`, template the unit), all with fully qualified `ansible.builtin.*` module names.
- The template task notifies `Restart orders`, and that handler exists in `handlers/main.yml`; the check fails if the name is wrong.
- Every variable used in `templates/orders.service.j2` has a default in `defaults/main.yml` (heap 256 MB, port 8080, and so on).

## Trade-offs

- The check is structural only. It does not run Ansible, so apt behaviour, privilege escalation and the systemd calls are untested.
- `inventory.ini` targets `orders-1` with `ansible_connection=local` and `site.yml` uses `become: true`, so applying it changes the machine you run it on.
- The role does not deploy `orders.jar`; the unit points to `/opt/orders/orders.jar`, which you must supply.
- `jvm_manage_service` (default `true`) switches the restart handler off, which the Packer folder uses during image builds.

## When not to use it

- For a single host that never changes, a shell script is shorter.
- When the target has no systemd (for example a plain container at runtime), the unit and handler do not apply.
