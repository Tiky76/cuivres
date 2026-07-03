[app]

title = cuivre app
package.name = capitaine
package.domain = org.capitaine

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

# ✅ IMPORTANT FIX CI
requirements = python3,kivy,pillow

orientation = portrait
fullscreen = 0

# Android settings
android.api = 33
android.minapi = 21
android.ndk_api = 21

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

# ❌ NE PAS METTRE sqlite3 (il est déjà inclus)
# ❌ NE PAS METTRE android.ndk_path (cassé en CI)

# Permissions (si besoin)
# android.permissions = INTERNET

[buildozer]

log_level = 2
warn_on_root = 1
