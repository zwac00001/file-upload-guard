from __future__ import annotations

import sys
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_ROOT))

from file_upload_guard.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
