# Packaging Guide: Creating a Mac Application

This guide explains how to package your Eel application as a standalone Mac `.app` bundle that can run without Python installed.

## Quick Start

### Option 1: PyInstaller (Recommended - Cross-platform)

```bash
# Install PyInstaller
pip install pyinstaller

# Build the app
python build_app.py

# Or use PyInstaller directly
pyinstaller --name=IntelligentToDoList --windowed --onedir --add-data=web:web main.py
```

### Option 2: py2app (Mac-specific)

```bash
# Install py2app
pip install py2app

# Build the app
python setup.py py2app
```

## Detailed Instructions

### Method 1: PyInstaller (Recommended)

**Why PyInstaller?**
- ✅ Works on Mac, Windows, and Linux
- ✅ Creates standalone executables
- ✅ No Python installation required for end users
- ✅ Well-documented and widely used

#### Step 1: Install PyInstaller

```bash
# Activate your virtual environment
source venv/bin/activate  # or .venv/bin/activate

# Install PyInstaller
pip install pyinstaller
```

#### Step 2: Build the Application

**Option A: Use the build script (easiest)**
```bash
python build_app.py
```

**Option B: Use PyInstaller directly**
```bash
pyinstaller --name=IntelligentToDoList \
    --windowed \
    --onedir \
    --add-data=web:web \
    --hidden-import=eel \
    --hidden-import=setuptools \
    --collect-all=eel \
    main.py
```

#### Step 3: Find Your App

After building, you'll find:
- `dist/IntelligentToDoList/` - The application folder
- `dist/IntelligentToDoList/IntelligentToDoList.app` - The Mac app bundle

**To run**: Double-click `IntelligentToDoList.app` or drag it to Applications.

#### Step 4: Test the App

```bash
# Test from command line
open dist/IntelligentToDoList/IntelligentToDoList.app

# Or navigate and double-click
cd dist/IntelligentToDoList
open IntelligentToDoList.app
```

### Method 2: py2app (Mac-specific)

**Why py2app?**
- ✅ Creates native Mac .app bundles
- ✅ Better Mac integration
- ✅ Can create DMG installers easily

#### Step 1: Install py2app

```bash
pip install py2app
```

#### Step 2: Create setup.py

I'll create this file for you (see below).

#### Step 3: Build

```bash
python setup.py py2app
```

## Configuration Files

### PyInstaller Spec File (Advanced)

For more control, create a spec file:

```bash
pyinstaller --name=IntelligentToDoList main.py
# This creates IntelligentToDoList.spec - edit it for customization
```

### py2app setup.py

See `setup.py` file (created below) for py2app configuration.

## Troubleshooting

### Issue: "Module not found" errors

**Solution**: Add hidden imports
```bash
--hidden-import=module_name
```

### Issue: Web files not included

**Solution**: Ensure `--add-data=web:web` is included

### Issue: App is too large

**Solution**: Use `--onedir` instead of `--onefile` (already in build script)

### Issue: App won't start

**Solution**: Check console for errors:
```bash
# Run from terminal to see errors
./dist/IntelligentToDoList/IntelligentToDoList.app/Contents/MacOS/IntelligentToDoList
```

## Distribution

### Creating a DMG (Disk Image)

1. **Using create-dmg** (recommended):
```bash
npm install -g create-dmg
create-dmg dist/IntelligentToDoList/IntelligentToDoList.app dist/
```

2. **Manually**:
   - Open Disk Utility
   - Create new image
   - Drag app into it
   - Convert to read-only DMG

### Code Signing (Optional)

For distribution outside the App Store:
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" IntelligentToDoList.app
```

### Notarization (For Gatekeeper)

Required for distribution:
```bash
xcrun altool --notarize-app \
    --primary-bundle-id "com.intelligenttodolist.app" \
    --username "your@email.com" \
    --password "@keychain:AC_PASSWORD" \
    --file IntelligentToDoList.dmg
```

## File Structure After Building

```
intelligent_to-do_list/
├── build/                    # Build files (can be deleted)
├── dist/
│   └── IntelligentToDoList/
│       └── IntelligentToDoList.app  # Your Mac app!
├── IntelligentToDoList.spec  # PyInstaller spec (optional)
└── ...
```

## What Gets Included?

- ✅ All Python modules (todo.py, goals.py, etc.)
- ✅ Eel framework
- ✅ Web files (HTML, CSS, JavaScript)
- ✅ Python interpreter
- ✅ All dependencies

## What Doesn't Get Included?

- ❌ Virtual environment
- ❌ Source code (compiled to bytecode)
- ❌ Development files (.git, etc.)

## App Size

Expect the app to be:
- **50-100 MB** (includes Python interpreter)
- Larger than source code, but standalone

## Updating the App

To rebuild after changes:
1. Make your code changes
2. Run `python build_app.py` again
3. New app will be in `dist/`

## Best Practices

1. **Test thoroughly** before distributing
2. **Create an icon** for your app (see Icon Creation below)
3. **Version your builds** (update app name with version)
4. **Test on clean Mac** (without Python installed)
5. **Keep build script** for easy rebuilding

## Icon Creation

1. Create a 512x512 PNG icon
2. Use `iconutil` or online converters to create .icns
3. Add to PyInstaller: `--icon=icon.icns`

## Next Steps

1. Build the app using one of the methods above
2. Test it on your Mac
3. Test on a Mac without Python installed
4. Create a DMG for distribution
5. (Optional) Code sign and notarize for wider distribution

