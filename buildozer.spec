[app]
# Application metadata
title = Manim Android
package.name = manimandroid
package.domain = org.manimanim

# Source files and assets
source.dir = .
# Include all necessary file types for rendering and media
source.include_exts = py,png,jpg,kv,atlas,ttf,ttc,mp4,mp3,txt,json

# Versioning
version = 0.1.0

# ============================================
# CRITICAL: Python Requirements for Manim
# ============================================
# Format: package_name or package_name==version
# For C-extensions: use recipe names if available (e.g., numpy, kivy, pycairo)
# Note: ffmpeg-python won't work on Android; we use ffmpeg binary instead
requirements = \
    python3,\
    kivy==2.3.0,\
    numpy,\
    scipy,\
    matplotlib,\
    pillow,\
    sympy,\
    pydub,\
    requests,\
    watchdog,\
    cython==0.29.33,\
    buildozer,\
    android,\
    pycairo,\
    opencv-python,\
    scikit-image,\
    imageio

# ============================================
# APPLICATION ORIENTATION & WINDOW
# ============================================
orientation = portrait
fullscreen = 0
# Allow landscape for better animation viewing
android.features = android.hardware.screen.landscape

# Icon and presplash (optional)
#icon.filename = %(source.dir)s/data/icon.png
#presplash.filename = %(source.dir)s/data/presplash.png
#presplash.loglevel = 2

# ============================================
# ANDROID PERMISSIONS
# ============================================
# Essential permissions for Manim (video/audio processing and file I/O)
android.permissions = \
    INTERNET,\
    WRITE_EXTERNAL_STORAGE,\
    READ_EXTERNAL_STORAGE,\
    RECORD_AUDIO,\
    MODIFY_AUDIO_SETTINGS

# ============================================
# ANDROID BUILD CONFIGURATION
# ============================================
# API levels
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# CPU architecture - ARM64 for best compatibility and performance
android.archs = arm64-v8a
# Uncomment for multi-architecture build (slower build but more device support)
#android.archs = arm64-v8a,armeabi-v7a

# Gradle and additional build config
android.allow_backup = True
android.gradle_dependencies = \
    androidx.appcompat:appcompat:1.6.1,\
    androidx.constraintlayout:constraintlayout:2.1.4

# ============================================
# BUILDOZER / P4A (Python-for-Android) CONFIG
# ============================================
# Python-for-Android fork and versioning
p4a.branch = develop

# Use develop branch for latest features and fixes
# You can pin to specific commits if needed:
# p4a.branch = develop
# p4a.commit = abc123def456

# Bootstrap to use (sdl2 is default and works well)
# p4a.bootstrap = sdl2

# Custom recipes directory (for building system libraries from source)
# This is where custom recipes for Cairo, Pango, HarfBuzz would go
# Uncomment if you have custom p4a recipes
# p4a.local_recipes = ./recipes/

# Enable detailed logging to help debug build issues
log_level = 2

# ============================================
# JAVA / GRADLE CONFIGURATION
# ============================================
# Java version compatibility
android.gradle_options = org.gradle.jvmargs=-Xmx4096m

# Manifest entries for camera/audio permission handling
# android.entrypoint = org.kivy.android.PythonActivity

# ============================================
# STORAGE & CACHING
# ============================================
# Use app-specific directories
android.use_legacy_toolchain = False

# ============================================
# BUILDOZER GLOBAL CONFIG
# ============================================
[buildozer]
# Logging
log_level = 2
warn_on_root = 1

# Build directory cleanup (set to 0 to keep intermediate files for debugging)
# buildozer.gradle_dependencies =

# ============================================
# DEPLOYMENT SETTINGS
# ============================================
# Android studio path (if you have it installed locally)
# android.studio_dir = /path/to/android-studio

# Custom Java options for larger builds
# android.gradle_options = org.gradle.jvmargs=-Xmx8g
