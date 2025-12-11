# Browser Configuration for Eel

Eel allows you to specify which browser to use when launching your desktop application. This guide explains how to configure different browsers.

## Quick Start: Using Edge

To use Microsoft Edge instead of Chrome, add `mode='edge'` to your `eel.start()` call:

```python
eel.start('index.html', size=(900, 700), port=0, mode='edge')
```

## Available Browser Modes

### 1. **Chrome (Default)**
```python
eel.start('index.html', mode='chrome')
```
- Uses Google Chrome browser
- Default if no mode is specified
- Works on Windows, macOS, and Linux (if Chrome is installed)

### 2. **Microsoft Edge**
```python
eel.start('index.html', mode='edge')
```
- Uses Microsoft Edge browser
- **Best for Windows 10/11** where Edge is pre-installed
- On macOS, requires Edge to be installed separately
- Uses Chromium-based Edge (not the old Internet Explorer-based version)

### 3. **Chrome App Mode**
```python
eel.start('index.html', mode='chrome-app')
```
- Launches Chrome in app mode (no browser UI)
- More desktop-like experience
- Hides address bar and browser controls

### 4. **System Default**
```python
eel.start('index.html', mode=None)
```
- Uses the system's default browser
- Could be Chrome, Edge, Firefox, Safari, etc.
- Less predictable but works on any system

### 5. **Custom Browser Path**
```python
eel.start('index.html', mode='path/to/browser.exe')
```
- Specify a custom path to any browser executable
- Useful for portable browsers or non-standard installations

## Platform-Specific Considerations

### Windows
- **Edge**: Pre-installed on Windows 10/11, works out of the box
- **Chrome**: Must be installed separately
- **Recommendation**: Use `mode='edge'` for best compatibility

### macOS
- **Chrome**: Must be installed separately
- **Edge**: Must be installed separately (download from Microsoft)
- **Safari**: Not directly supported by Eel (uses WebKit, not Chromium)
- **Recommendation**: Use `mode='chrome'` or install Edge first

### Linux
- **Chrome/Chromium**: Usually available via package manager
- **Edge**: Available but less common
- **Recommendation**: Use `mode='chrome'` or `mode='chrome-app'`

## Finding Browser Paths

If you need to use a custom path, here are common locations:

### Windows
- Chrome: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- Edge: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`

### macOS
- Chrome: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Edge: `/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge`

### Linux
- Chrome: `/usr/bin/google-chrome` or `/usr/bin/chromium-browser`
- Edge: `/usr/bin/microsoft-edge`

## Example: Platform Detection

You can make your app choose the best browser automatically:

```python
import platform
import eel

eel.init('web')

# Choose browser based on platform
system = platform.system()
if system == 'Windows':
    browser_mode = 'edge'  # Edge is pre-installed on Windows
elif system == 'Darwin':  # macOS
    browser_mode = 'chrome'  # Chrome is more common on macOS
else:  # Linux
    browser_mode = 'chrome-app'  # App mode works well on Linux

eel.start('index.html', size=(900, 700), port=0, mode=browser_mode)
```

## Troubleshooting

### "Browser not found" Error

If Eel can't find the specified browser:

1. **Check if browser is installed**: Make sure the browser exists on your system
2. **Use system default**: Try `mode=None` to use whatever browser is available
3. **Specify full path**: Use `mode='full/path/to/browser.exe'` if browser is in non-standard location

### Edge Not Working on macOS

If `mode='edge'` doesn't work on macOS:

1. **Install Edge**: Download from [Microsoft Edge website](https://www.microsoft.com/edge)
2. **Use Chrome instead**: Change to `mode='chrome'`
3. **Use custom path**: Specify the full path to Edge executable

### Performance Differences

- **Chrome**: Generally fastest, most features
- **Edge**: Very similar to Chrome (both Chromium-based), good performance
- **Chrome App Mode**: Slightly faster, more desktop-like
- **System Default**: Performance depends on which browser is default

## Current Configuration

In this project, Edge is configured:

```python
eel.start('index.html', size=(900, 700), port=0, mode='edge')
```

To change it, simply modify the `mode` parameter in `main.py`.

