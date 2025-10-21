# imgpv - Image Previewer

## Installation
- Requirements: `uv`.
- Init, activate and install packages for venv.
- Install `ccache` and `patchelf` system packages (e.g. with `pacman`)
- Build and install:
    ```bash
    nuitka --onefile --standalone --enable-plugin=pyside6 src/main.py -o imgpv 
    ```

## Usage
```bash
imgpv -h                             
usage: imgpv [-h] [--dir DIR] [--config CONFIG] [--theme THEME] [--ext EXT]
             [--no-live-theme]
             [items ...]

positional arguments:
  items                Items to preview

options:
  -h, --help           show this help message and exit
  --dir, -d DIR
  --config, -c CONFIG
  --theme, -t THEME
  --ext, -x EXT
  --no-live-theme
```

- Default config file: `$HOME/.config/imgpv/imgpv.toml`
    - To add custom keybinds, add an entry `[[keybinds]]`, for example:
        ```bash
        [[keybinds]]
        keys = "ctrl+shift+y"
        command = "wl-copy --type image/png < {{path}}"
        description = "copy image"
        ```
    - Placeholders supported: `{{path}}` (file path (absolute)), `{{ext}}` (file extension, e.g. `.png`)

- Default theme file: `$HOME/.config/imgpv/theme.toml`.
