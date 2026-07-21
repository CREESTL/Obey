# Obey

Personal [opencode](https://opencode.ai) configuration, synced across machines via Git.

## File layout

Where each repo path lands on the target machine:

```
repo/
├── AGENTS.md            →  ~/.config/opencode/AGENTS.md
├── opencode.jsonc       →  ~/.config/opencode/opencode.jsonc
├── opencode/
│   ├── agents/          →  ~/.config/opencode/agents/
│   └── commands/        →  ~/.config/opencode/commands/
├── tui.json             →  ~/.config/opencode/tui.json
├── .agents/             →  ~/.agents/                     (skills, installed via skills.sh)
└── .secrets/            →  ~/.config/opencode/.secrets/   (gitignored — recreate locally)
```

## Setup on a new machine

Clone anywhere, then deploy files to the locations opencode reads them from.

### Quick install (automated)

Run the deploy script — it copies everything to the right places:

```sh
python install.py
```

### Manual install

If you prefer to copy files by hand:

### 1. Global config → `~/.config/opencode/`

Copy these into your opencode config directory:

- `AGENTS.md`
- `opencode.jsonc`

```sh
cp AGENTS.md opencode.jsonc ~/.config/opencode/
```

### 2. Agents & commands → `~/.config/opencode/`

Custom [agents](opencode/agents/) and [commands](opencode/commands/) live in the `opencode/` directory.

Copy the entire `opencode/` folder so opencode picks them up:

```sh
cp -r opencode ~/.config/opencode/
```

### 3. Skills → home directory

Skills live in `.agents/skills` (not `~/.config/opencode/skills`) because they are installed from [skills.sh](https://skills.sh), which installs to `~/.agents/skills` and offers no option to change the directory.

Copy the `.agents/` folder into your home directory so skills load globally:

```sh
cp -r .agents ~/
```

### 4. TUI config → `~/.config/opencode/`

`tui.json` holds keybinds and TUI preferences (theme, scroll, etc.). Copy it next to `opencode.jsonc`:

```sh
cp tui.json ~/.config/opencode/
```

### 5. Secrets → `~/.config/opencode/.secrets/`

`opencode.jsonc` reads credentials via `{file:...}`:

```jsonc
"baseURL": "{file:.secrets/base_url}",
"apiKey":  "{file:.secrets/api_key}"
```

Paths are relative to the config file, so create the folder next to `opencode.jsonc`:

```sh
mkdir -p ~/.config/opencode/.secrets
# One value per file, no trailing newline:
echo -n "https://your-endpoint" > ~/.config/opencode/.secrets/base_url
echo -n "your-api-key"         > ~/.config/opencode/.secrets/api_key
```

`.secrets/` is gitignored — recreate it on every machine. Do not commit real keys.

## Updating skills

Installed skills are tracked by `.skill-lock.json` (sources + hashes). To add or update a skill, use opencode's skill install command; commit the updated `.skill-lock.json` and any new `SKILL.md` files so other machines pull the same versions.
