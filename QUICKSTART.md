# Quick Start Guide

Get your iOS automation project deployed in 5 minutes!

## Prerequisites

Ensure you have:
- ✅ Python 3.8+
- ✅ Xcode 14.0+
- ✅ Node.js & npm
- ✅ Appium: `npm install -g appium`
- ✅ XCUITest driver: `appium driver install xcuitest`

## Deploy to Your iOS App

### 1. Run Deployment Script

```bash
cd ~/Projects/appium-multiplatform-framework

python deploy/deploy_ios.py --app-path ~/Projects/YourApp
```

This creates: `~/Projects/YourApp-Automation/`

### 2. Navigate to Project

```bash
cd ~/Projects/YourApp-Automation
```

### 3. Set Up Virtual Environment

```bash
# Create and activate venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Start Appium

In a separate terminal:

```bash
appium
```

### 5. Update Locators (Important!)

Edit `pages/ios/home_page.py` and update the placeholder locators with actual accessibility IDs from your app.

Use Appium Inspector to find elements:
```bash
# Install Appium Inspector
npm install -g appium-inspector

# Or download from:
# https://github.com/appium/appium-inspector/releases
```

### 6. Run Tests

```bash
# Run smoke tests
pytest tests/ios/ -m smoke -v

# Run all tests
pytest tests/ios/ -v

# Generate HTML report
pytest tests/ios/ --html=reports/ios/report.html
```

---

## Deploy Another App

The framework is reusable! Deploy to as many apps as you want:

```bash
cd ~/Projects/appium-multiplatform-framework

# Deploy to App #2
python deploy/deploy_ios.py --app-path ~/Projects/AnotherApp

# This creates: ~/Projects/AnotherApp-Automation/
```

Each automation project is independent!

---

## Command Options

```bash
# Basic
python deploy/deploy_ios.py --app-path ~/Projects/MyApp

# Custom output directory
python deploy/deploy_ios.py \
  --app-path ~/Projects/MyApp \
  --output-dir ~/Automation

# Override app name
python deploy/deploy_ios.py \
  --app-path ~/Projects/MyApp \
  --app-name "CoolApp"

# Skip building (if you already have .app)
python deploy/deploy_ios.py \
  --app-path ~/Projects/MyApp \
  --skip-build

# Skip virtual environment setup
python deploy/deploy_ios.py \
  --app-path ~/Projects/MyApp \
  --skip-venv

# Verbose output
python deploy/deploy_ios.py \
  --app-path ~/Projects/MyApp \
  --verbose
```

---

## Troubleshooting

### "Appium not found"
```bash
npm install -g appium
appium driver install xcuitest
```

### "XCUITest driver not installed"
```bash
appium driver install xcuitest
appium driver list  # Verify
```

### "Build failed"
- Open project in Xcode and build manually first
- Or use `--skip-build` and provide .app path in config

### "Tests fail to run"
- Ensure Appium server is running: `appium`
- Check app path in `config/ios/capabilities.json`
- Update locators in page objects

---

## Next Steps

1. **Customize Page Objects** - Add your app's screens
2. **Write More Tests** - Expand test coverage
3. **Add to CI/CD** - See examples in `examples/`
4. **Deploy to More Apps** - Reuse the framework!

---

## Example: AppJubilee Deployment

```bash
# 1. Deploy
cd ~/Projects/appium-multiplatform-framework
python deploy/deploy_ios.py --app-path ~/Projects/AppJubilee

# 2. Set up
cd ~/Projects/AppJubilee-Automation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Start Appium (separate terminal)
appium

# 4. Run tests
pytest tests/ios/ -m smoke -v
```

---

**You're ready to automate!** 🚀

See [README.md](README.md) for complete documentation.
