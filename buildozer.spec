[app]
# Title of your application
title = Manim Animation

# Package name (lowercase, alphanumeric only)
package.name = manimanim

# Package domain (use reverse domain notation)
package.domain = org.manim

# Source code location
source.dir = .

# Include patterns
source.include_exts = py,png,jpg,kv,atlas,ttf,json,txt

# Exclude patterns (to reduce APK size)
source.exclude_patterns = tests/*,docs/*,.git/*,.github/*

# Version
version = 0.1.0

# Application requirements (dependencies)
requirements = \
    python3, \
    kivy, \
    numpy, \
    scipy, \
    matplotlib, \
    pillow, \
    sympy, \
    pydub, \
    requests, \
    watchdog, \
    opencv, \
    scikit-image, \
    imageio, \
    imageio-ffmpeg

# Orientation (portrait/landscape/sensor)
orientation = portrait

# Allow fullscreen
fullscreen = 0

# Icon (optional - 512x512 PNG)
#icon.filename = %(source.dir)s/data/icon.png

# Presplash image (optional - loading screen)
#presplash.filename = %(source.dir)s/data/presplash.png

# Android permissions
android.permissions = \
    INTERNET, \
    ACCESS_NETWORK_STATE, \
    WRITE_EXTERNAL_STORAGE, \
    READ_EXTERNAL_STORAGE

# Android features
android.features = android.hardware.screen.landscape

# Android API version
android.api = 31

# Minimum Android API version
android.minapi = 21

# Android NDK version
android.ndk = 25b

# Accept Android SDK licenses
android.accept_sdk_license = True

# Architecture (arm64-v8a for modern devices)
android.arch = arm64-v8a

# Allow backup
android.allow_backup = True

# Gradle dependencies
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

# Log level
android.logcat_filters = *:S python:D

# Buildozer options
[buildozer]

# Log level (0=error, 1=info, 2=debug)
log_level = 2

# Warn on root
warn_on_root = 1
