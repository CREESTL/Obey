# Obey

Personal [opencode](https://opencode.ai) configuration, synced across machines via Git.

## Setup on a new machine

Clone anywhere, then deploy files to the locations opencode reads them from.

### 1. Global config → `~/.config/opencode/`

Copy these into your opencode config directory:

- `AGENTS.md`
- `opencode.jsonc`

```sh
cp AGENTS.md opencode.jsonc ~/.config/opencode/
```

### 2. Skills → home directory

Copy the `.agents/` folder into your home directory so skills load globally:

```sh
cp -r .agents ~/
```

### 3. Secrets → `~/.config/opencode/.secrets/`

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
