#!/usr/bin/env bash
set -euo pipefail
exec 9>/opt/erpnext-dev/keepalive.lock
flock -n 9 || exit 0
while [ -f /opt/erpnext-dev/.installing ] || systemctl is-active --quiet erpnext-dev; do
  sleep 10
done
