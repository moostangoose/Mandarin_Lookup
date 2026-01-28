file dict.db is in line with CC-CEDIT as of 28/01/2026

place dict.db and clipboard_lookup.py in chosen (the same) location;
place chinese-lookup-wrapper.sh in ~/bin (create ~/bin if doesn't exist);

Ubuntu/Ubuntu-Studio wayland tested (should work on most debian based distros)

**install any missing dependencies if prompted:**

# Database and data processing
python3-sqlite3  # Usually pre-installed

# Pinyin tone mark generation
python3-pypinyin

# Alternative (if using venv):
pip install pypinyin

# For Wayland (Ubuntu Studio default):
wl-clipboard      # Clipboard access
python3-notify2   # Desktop notifications

# For X11 systems (non-Wayland):
xclip             # Clipboard access
python3-notify2   # Desktop notifications

# DBus support (usually pre-installed)
libnotify-bin     # Notification daemon
dbus              # Message bus system

sudo apt install python3-pypinyin xclip python3-notify2 libnotify-bin

(for troubleshooting - optional)
python3-dbus      # DBus Python bindings
gir1.2-gtk-3.0    # GTK/GObject introspection (for alternative clipboard)

Most Ubuntu/Debian systems already have python3-sqlite3, dbus, and libnotify-bin installed by default.
