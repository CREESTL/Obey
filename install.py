#!/usr/bin/env python3
"""
Deploy this repo's opencode configuration to the user's machine.

Copies files and directories to their dedicated locations:

    AGENTS.md            -> ~/.config/opencode/AGENTS.md
    opencode.jsonc       -> ~/.config/opencode/opencode.jsonc
    tui.json             -> ~/.config/opencode/tui.json
    opencode/agents/     -> ~/.config/opencode/agents/
    opencode/commands/   -> ~/.config/opencode/commands/
    .agents/             -> ~/.agents/

.secrets/ is intentionally skipped (gitignored; recreate locally per README).

Works on Windows, macOS, and Linux. Requires Python 3.8+.
"""

from pathlib import Path
import shutil
import sys

REPO = Path(__file__).resolve().parent
HOME = Path.home()
OPENCODE_DIR = HOME / ".config" / "opencode"
AGENTS_DIR = HOME / ".agents"

TARGETS = [
    (REPO / "AGENTS.md",             OPENCODE_DIR / "AGENTS.md",            "global rules"),
    (REPO / "opencode.jsonc",        OPENCODE_DIR / "opencode.jsonc",       "providers, models, permissions"),
    (REPO / "tui.json",              OPENCODE_DIR / "tui.json",             "keybinds & TUI prefs"),
    (REPO / "opencode" / "agents",   OPENCODE_DIR / "agents",               "subagents (reviewer, tester, ...)"),
    (REPO / "opencode" / "commands", OPENCODE_DIR / "commands",             "slash commands (/test, /review)"),
    (REPO / ".agents",               AGENTS_DIR,                            "skills (from skills.sh)"),
]

GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"
CYAN   = "\033[36m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def supports_color() -> bool:
    return sys.stdout.isatty() and sys.platform != "win32"


def paint(text: str, color: str) -> str:
    return f"{color}{text}{RESET}" if supports_color() else text


def banner(title: str) -> None:
    bar = "=" * 64
    print(paint(f"\n{bar}", DIM))
    print(paint(f"  {title}", BOLD))
    print(paint(f"{bar}\n", DIM))


def header(src: Path, dst: Path, label: str) -> str:
    rel = src.relative_to(REPO) if src.is_absolute() and src.is_relative_to(REPO) else src
    return f"{paint(str(rel), CYAN)} {paint(f'({label})', DIM)}\n      {paint('~>', DIM)} {dst}"


def copy(src: Path, dst: Path, label: str) -> str:
    if not src.exists():
        return f"  {paint('SKIP', YELLOW)}  {header(src, dst, label)} {paint('[missing in repo]', YELLOW)}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        n_files = sum(1 for _ in src.rglob("*") if _.is_file())
        shutil.copytree(src, dst, dirs_exist_ok=True)
        kind = "DIR "
        detail = f"({n_files} files)"
    else:
        shutil.copy2(src, dst)
        kind = "FILE"
        detail = ""
    return f"  {paint('OK', GREEN)}  {header(src, dst, label)} {paint(detail, DIM)}"


def main() -> int:
    banner("opencode config deployment")
    print(f"  {paint('repo', DIM)}       {REPO}")
    print(f"  {paint('opencode', DIM)}   {OPENCODE_DIR}")
    print(f"  {paint('agents', DIM)}     {AGENTS_DIR}")

    banner("copying")
    for src, dst, label in TARGETS:
        print(copy(src, dst, label))

    banner("summary")
    print(f"  {paint('NOTE', YELLOW)}  {paint('.secrets/', CYAN)} skipped — recreate locally (see README step 5).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(paint("\nAborted.", RED))
        sys.exit(130)