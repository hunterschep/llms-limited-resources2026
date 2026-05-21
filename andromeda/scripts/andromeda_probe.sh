#!/usr/bin/env bash
set -euo pipefail

hostname
whoami
pwd
test -f "${HOME}/ANDROMEDA_MAP.md" && sed -n '1,120p' "${HOME}/ANDROMEDA_MAP.md"
sinfo --version
sinfo -h -o "%P|%a|%l|%D|%C|%G" | sort
squeue -u "$USER" -o "%i|%j|%P|%t|%M|%l|%D|%C|%m|%b|%R"
acct-chk "$USER"
