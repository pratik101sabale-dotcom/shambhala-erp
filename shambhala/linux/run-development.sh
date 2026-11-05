#!/usr/bin/env bash
set -eo pipefail
export PATH="$HOME/.local/bin:$PATH"
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"
nvm use 24 >/dev/null
cd /opt/erpnext-dev/frappe-bench
exec bench start
