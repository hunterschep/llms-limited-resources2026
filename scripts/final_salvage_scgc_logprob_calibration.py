#!/usr/bin/env python3
from __future__ import annotations

import json


def main() -> int:
    print(json.dumps({"status": "not_run", "reason": "log-probability calibration is diagnostic-only until organizer inference rules are clarified"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
