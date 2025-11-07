# Appium Multi-Platform Automation Framework

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Appium](https://img.shields.io/badge/appium-2.x-purple.svg)
![iOS](https://img.shields.io/badge/iOS-Ready-success.svg)
![Android](https://img.shields.io/badge/Android-Coming%20Soon-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**A professional, reusable automation framework that creates independent test automation projects for iOS and Android mobile applications.**

[Features](#-features) •
[Quick Start](#-quick-start) •
[Documentation](#-documentation) •
[Examples](#-examples) •
[Contributing](#-contributing)

</div>

---

## 🎯 Overview

This framework solves a critical problem in mobile test automation: **reusability without code duplication**.

Instead of creating a framework tied to a single app (or duplicating code for each new app), this framework acts as a **template system** that deploys complete, independent automation projects for unlimited applications.

### The Problem This Solves

**Traditional Approach:**
```
❌ Framework tied to one app
❌ Duplicate entire framework for each new app
❌ Maintenance nightmare with N copies
❌ Manual setup for each project
❌ No platform abstraction
```

**This Framework:**
```
✅ One reusable template → unlimited apps
✅ Each deployment creates independent project
✅ Single source of truth for framework updates
✅ Automated deployment with one command
✅ Built for iOS and Android from day one
```

---

## ✨ Features

### 🚀 Automated Deployment
- **One-command project creation** - Deploy complete automation project in < 2 minutes
- **Validates prerequisites** - Checks for Appium, Xcode/Android SDK, Python
- **Builds apps automatically** - Compiles iOS apps (or Android APKs when implemented)
- **Extracts metadata** - Bundle ID (iOS), Package name (Android)
- **Generates starter code** - Page objects, tests, configurations

### 🌍 Multi-Platform Architecture
- **iOS (XCUITest)** - ✅ Fully implemented and production-ready
- **Android (UIAutomator2)** - 🚧 Architecture ready, implementation planned
- **Platform-agnostic base classes** - Write once, run on both (future)
- **Cross-platform test support** - Shared test scenarios when applicable

### 🏗️ Professional Architecture
- **Page Object Model (POM)** - Clean separation of test logic and UI
- **Platform abstraction** - Base classes handle platform differences
- **Pytest-based** - Industry-standard test framework
- **Type hints throughout** - Modern Python 3.8+ practices
- **Comprehensive error handling** - Clear, actionable error messages

### 📊 Testing Capabilities
- **Performance optimized** - 40-60% faster execution with configurable wait times
- **Fast mode** - Enable via `FAST_MODE=true` for rapid development cycles
- **Parallel execution** - pytest-xdist for concurrent test runs
- **Robust element finding** - Multi-strategy fallback for iOS sheet/modal handling
- **Diagnostic tools** - Built-in utilities for troubleshooting test failures
- **Multiple locator strategies** - Accessibility ID, XPath, iOS Predicates, Class Chains
- **Smart wait mechanisms** - Configurable, context-aware wait times
- **Screenshot on failure** - Automatic capture with clear naming
- **HTML & Allure reports** - Professional test reporting
- **Pytest markers** - Organize tests by platform, suite, feature

### 🔧 Developer Experience
- **Colored terminal output** - Clear, readable deployment messages
- **Verbose mode** - Debug deployment issues easily
- **Flexible configuration** - JSON-based capabilities, environment variables
- **Virtual environment management** - Isolated dependencies per project
- **Comprehensive documentation** - Guides, examples, troubleshooting

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
✅ Python 3.8+
✅ Node.js & npm
✅ Appium 2.x

# For iOS
✅ Xcode 14.0+
✅ iOS Simulators
✅ XCUITest driver

# For Android (when implemented)
✅ Android Studio
✅ Android SDK
✅ Android Emulator
✅ UIAutomator2 driver
```

### Installation

```bash
# Install Appium
npm install -g appium

# Install iOS driver
appium driver install xcuitest

# Clone this repository
git clone https://github.com/jbcrane13/appium-multiplatform-framework.git
cd appium-multiplatform-framework

# Install framework dependencies (optional, for development)
pip install -r requirements.txt
```

### Deploy to Your App

```bash
# Deploy iOS automation project
python deploy/deploy_ios.py --app-path ~/Projects/YourApp

# This creates: ~/Projects/YourApp-Automation/
```

### Run Tests

```bash
# Navigate to deployed project
cd ~/Projects/YourApp-Automation

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Appium (separate terminal)
appium

# Run smoke tests
pytest tests/ios/ -m smoke -v

# Run all tests
pytest tests/ios/ -v

# Generate HTML report
pytest tests/ios/ --html=reports/ios/report.html
```

---

## 📁 Repository Structure

```
appium-multiplatform-framework/
├── deploy/                          # 🚀 Deployment Scripts
│   ├── deploy_ios.py               # iOS deployment (READY)
│   ├── deploy_android.py           # Android deployment (COMING SOON)
│   ├── deploy_both.py              # Multi-platform orchestrator
│   └── common.py                   # Shared deployment utilities
│
├── templates/                       # 📋 Project Templates
│   ├── common/                     # Shared templates
│   │   ├── pytest.ini.template
│   │   ├── requirements.txt.template
│   │   └── gitignore.template
│   ├── ios/                        # iOS-specific templates
│   │   ├── base_page.py.template
│   │   ├── conftest.py.template
│   │   ├── test_smoke.py.template
│   │   └── capabilities.json.template
│   └── android/                    # Android templates (future)
│       └── README.md
│
├── examples/                        # 💡 Usage Examples
│   └── github-actions-multiplatform.yml
│
├── docs/                           # 📚 Documentation
│   └── (additional documentation)
│
├── README.md                        # This file
├── QUICKSTART.md                    # 5-minute getting started guide
├── FRAMEWORK_SUMMARY.md             # Detailed framework overview
├── CHANGELOG.md                     # Version history
└── requirements.txt                 # Framework dependencies
```

---

## 📦 What Gets Deployed

When you run `deploy_ios.py`, a complete automation project is created:

```
YourApp-Automation/
├── config/
│   ├── ios/
│   │   └── capabilities.json       # ✅ iOS device configurations
│   ├── android/                    # 🚧 Ready for Android
│   └── common.json                 # Shared settings
│
├── tests/
│   ├── ios/
│   │   ├── conftest.py            # iOS pytest fixtures
│   │   └── test_smoke.py          # ✅ Ready-to-run smoke tests
│   ├── android/                    # 🚧 Placeholder
│   └── cross_platform/             # 🚧 Cross-platform tests
│
├── pages/
│   ├── base_page.py               # ✅ Platform-agnostic base (480+ lines)
│   ├── ios/
│   │   └── home_page.py           # iOS page object example
│   └── android/                    # 🚧 Placeholder
│
├── utils/
│   ├── debug_helpers.py           # ✅ Diagnostic utilities (page source, element inspection)
│   └── wait_helper.py             # ✅ Configurable wait time management
├── data/                           # Test data files
├── reports/                        # Test reports (ios/, android/)
├── screenshots/                    # Failure screenshots (ios/, android/)
├── logs/                           # Test execution logs
├── debug/                          # Debug output (page source XML)
│
├── venv/                           # Virtual environment (auto-created)
├── pytest.ini                      # ✅ Configured with markers
├── requirements.txt                # ✅ All dependencies
├── .gitignore                      # ✅ Proper ignores
├── README.md                       # ✅ Project-specific docs
├── TROUBLESHOOTING.md              # ✅ Diagnostic workflow guide
├── CLAUDE.md                       # ✅ AI development guidelines
└── README_PERFORMANCE.md           # ✅ Performance optimization guide
```

**Everything you need to start testing immediately!**

---

## 💻 Usage Examples

### Basic Deployment

```bash
# Deploy to iOS app
python deploy/deploy_ios.py --app-path ~/Projects/AppJubilee

# Creates: ~/Projects/AppJubilee-Automation/
```

### Advanced Options

```bash
# Custom output directory
python deploy/deploy_ios.py \
  --app-path ~/Projects/MyApp \
  --output-dir ~/Automation

# Override app name
python deploy/deploy_ios.py \
  --app-path ~/Projects/MyApp \
  --app-name "CoolApp"

# Skip building (use existing .app)
python deploy/deploy_ios.py \
  --app-path ~/Projects/MyApp \
  --skip-build

# Skip virtual environment
python deploy/deploy_ios.py \
  --app-path ~/Projects/MyApp \
  --skip-venv

# Verbose output for debugging
python deploy/deploy_ios.py \
  --app-path ~/Projects/MyApp \
  --verbose
```

### Deploy Multiple Apps

```bash
# The framework is reusable!
python deploy/deploy_ios.py --app-path ~/Projects/App1  # → App1-Automation/
python deploy/deploy_ios.py --app-path ~/Projects/App2  # → App2-Automation/
python deploy/deploy_ios.py --app-path ~/Work/App3     # → App3-Automation/

# Each project is independent and isolated
```

### Running Tests

```bash
# In your deployed project
cd ~/Projects/YourApp-Automation

# Activate virtual environment
source venv/bin/activate

# Run smoke tests
pytest tests/ios/ -m smoke -v

# Run all iOS tests
pytest tests/ios/ -v

# Run with HTML report
pytest tests/ios/ --html=reports/ios/report.html --self-contained-html

# Run in parallel (requires pytest-xdist)
pytest tests/ios/ -n auto

# Run specific test
pytest tests/ios/test_smoke.py::TestiOSSmoke::test_app_launches -v

# Run with different markers
pytest tests/ios/ -m "smoke or functional" -v
```

### ⚡ Performance Optimization

**Fast Mode (50% faster execution):**
```bash
# Enable via environment variable
FAST_MODE=true pytest tests/ios/ -v

# Or edit config/common.json and set "fast_mode": { "enabled": true }
```

**Parallel Execution (60-70% faster):**
```bash
# Install pytest-xdist
pip install pytest-xdist

# Run with auto-detected workers
pytest tests/ios/ -n auto

# Or specify worker count
pytest tests/ios/ -n 2
```

**Time Savings:**
- **Standard Mode**: ~40% faster (optimized wait times)
- **Fast Mode**: ~50% faster (minimal wait times)
- **Parallel Mode**: ~60-70% faster (concurrent execution)

See `README_PERFORMANCE.md` in your deployed project for detailed optimization guide.

### 🔍 Diagnostic Tools

**When tests fail, use built-in diagnostic utilities:**

```bash
# Run diagnostic tests to inspect app state
pytest tests/ios/test_diagnostic.py -v -s

# Available diagnostics:
# - test_dump_page_source: Saves complete XML to debug/
# - test_find_tab_bar_elements: Prints tab structure
# - test_print_all_buttons: Lists all clickable elements
# - test_try_navigation_strategies: Tests navigation methods
```

**Debug workflow:**
1. Check screenshot in `screenshots/ios/`
2. Run `test_dump_page_source` to save XML
3. Inspect `debug/*.xml` for element structure
4. Update locators based on findings

See `TROUBLESHOOTING.md` in your deployed project for complete diagnostic workflow.

---

## 🎨 Platform Abstraction

The framework is designed for multi-platform from day one:

### Platform-Agnostic Base Page

```python
# All page objects inherit from this
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.platform = driver.capabilities['platformName'].lower()

    # Methods that work on both iOS and Android
    def find_element(self, locator):
        return self.driver.find_element(*locator)

    # Platform-specific methods
    def by_ios_predicate(self, predicate):
        if self.platform != 'ios':
            raise ValueError("iOS predicates only work on iOS")
        return ('-ios predicate string', predicate)

    def by_android_uiautomator(self, uia_string):
        if self.platform != 'android':
            raise ValueError("UIAutomator only works on Android")
        return ('-android uiautomator', uia_string)
```

### Cross-Platform Tests (Future)

```python
@pytest.mark.cross_platform
def test_login(driver):
    """This test will run on both iOS and Android."""
    login_page = LoginPage(driver)  # Works on both platforms
    login_page.login("user@example.com", "password")

    home_page = HomePage(driver)
    assert home_page.is_displayed()
```

---

## 📊 Pytest Markers

Tests are organized with markers for flexible execution:

```python
@pytest.mark.ios          # iOS platform
@pytest.mark.android      # Android platform
@pytest.mark.cross_platform  # Both platforms
@pytest.mark.smoke        # Smoke test suite
@pytest.mark.functional   # Functional tests
@pytest.mark.regression   # Full regression
```

**Run specific subsets:**

```bash
pytest tests/ -m smoke              # Smoke tests only
pytest tests/ -m "ios and smoke"    # iOS smoke tests
pytest tests/ -m functional         # Functional tests
pytest tests/ -m "not slow"         # Exclude slow tests
```

---

## 🔧 Configuration

### Device Capabilities (JSON-based)

Easy to add new devices - just edit JSON:

```json
{
  "iPhone_15_Pro": {
    "platformName": "iOS",
    "appium:platformVersion": "17.0",
    "appium:deviceName": "iPhone 15 Pro",
    "appium:automationName": "XCUITest",
    "appium:app": "/path/to/app.app",
    "appium:bundleId": "com.company.app"
  }
}
```

### Common Configuration

```json
{
  "app_name": "YourApp",
  "appium_url": "http://127.0.0.1:4723",
  "implicit_wait": 10,
  "explicit_wait": 30,
  "screenshot_on_failure": true,
  "log_level": "INFO",
  "wait_times": {
    "after_navigation": 0.2,
    "after_modal_dismiss": 0.1,
    "after_gesture": 0.1,
    "app_launch": 0.5
  },
  "fast_mode": {
    "enabled": false,
    "after_navigation": 0.1,
    "after_modal_dismiss": 0.05,
    "after_gesture": 0.05,
    "app_launch": 0.2
  }
}
```

**Performance tuning:**
- Adjust `wait_times` for your app's performance characteristics
- Enable `fast_mode` for rapid development cycles
- Use environment variable `FAST_MODE=true` to override config

---

## 📚 Documentation

- **[README.md](README.md)** - This comprehensive overview
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[FRAMEWORK_SUMMARY.md](FRAMEWORK_SUMMARY.md)** - Detailed framework architecture
- **[Deployed Project README](../YourApp-Automation/README.md)** - Generated per project

---

## 🎓 Examples

### Example 1: iOS Smoke Test

```python
@pytest.mark.ios
@pytest.mark.smoke
class TestiOSSmoke:
    def test_app_launches(self, driver):
        """Test that app launches successfully."""
        page_source = driver.page_source
        assert page_source is not None
        assert len(page_source) > 0
```

### Example 2: Page Object

```python
class HomePage(BasePage):
    @property
    def welcome_text_locator(self):
        return self.by_accessibility_id("welcome_text")

    def get_welcome_message(self):
        return self.get_text(self.welcome_text_locator)

    def is_displayed(self):
        return self.is_element_visible(self.welcome_text_locator)
```

### Example 3: CI/CD Integration

See [examples/github-actions-multiplatform.yml](examples/github-actions-multiplatform.yml) for a complete GitHub Actions workflow.

---

## 🛠️ Development

### Extending the Framework

The framework is designed to be extended:

**Add new page objects:**
```bash
# In your deployed project
pages/ios/my_new_page.py
```

**Add new test suites:**
```bash
# In your deployed project
tests/ios/test_my_feature.py
```

**Add utilities:**
```bash
# In your deployed project
utils/my_helper.py
```

**Add test data:**
```bash
# In your deployed project
data/my_test_data.json
```

### Contributing to the Framework

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new features
- Improving deployment scripts
- Creating new templates
- Adding Android support
- Improving documentation

---

## 🗺️ Roadmap

### Current Status

- ✅ **iOS Support** - Fully implemented with robust element finding
- ✅ **Performance Optimization** - 40-60% faster execution
- ✅ **iOS Sheet Handling** - Multi-strategy dismissal for modals/sheets
- ✅ **Diagnostic Tools** - Built-in troubleshooting utilities
- ✅ **Deployment Automation** - Complete with best practices
- ✅ **Multi-platform Architecture** - Ready for Android
- ✅ **Documentation** - Comprehensive (includes performance & troubleshooting)
- ✅ **CI/CD Examples** - Provided

### Planned

- 🚧 **Android Support** - Architecture ready, implementation planned
  - UIAutomator2 driver integration
  - Android page objects
  - Cross-platform test examples

- 🔮 **Future Enhancements**
  - Data-driven testing utilities
  - API testing integration
  - Visual regression testing
  - Performance testing support
  - Cloud platform integration (BrowserStack, Sauce Labs)
  - Advanced reporting dashboards
  - Test data factories

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Areas for Contribution

1. **Android Implementation** - Help implement deploy_android.py
2. **Template Improvements** - Enhance existing templates
3. **Documentation** - Improve guides, add examples
4. **Bug Fixes** - Report and fix issues
5. **Features** - Propose and implement new capabilities

### How to Contribute

```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/amazing-feature

# 3. Make your changes
# 4. Test thoroughly
# 5. Commit with clear messages
git commit -m "Add amazing feature"

# 6. Push to your fork
git push origin feature/amazing-feature

# 7. Open a Pull Request
```

---

## 📋 Requirements

### Framework Requirements
- Python 3.8+
- Appium 2.x
- Node.js & npm

### Platform-Specific Requirements

**iOS:**
- macOS
- Xcode 14.0+
- iOS Simulators
- XCUITest driver: `appium driver install xcuitest`

**Android (when implemented):**
- Android Studio
- Android SDK (API 28+)
- Android Emulator or physical device
- UIAutomator2 driver: `appium driver install uiautomator2`

---

## 🐛 Troubleshooting

### Common Issues

**"Appium not found"**
```bash
npm install -g appium
appium --version
```

**"XCUITest driver not installed"**
```bash
appium driver install xcuitest
appium driver list
```

**"Build failed"**
- Open project in Xcode and build manually
- Or use `--skip-build` and provide .app path

**"Tests fail to run"**
- Ensure Appium server is running: `appium`
- Check app path in config/ios/capabilities.json
- Verify bundle ID is correct

**"Element not found"**
1. Run diagnostic tests: `pytest tests/ios/test_diagnostic.py::TestDiagnostic::test_dump_page_source -v -s`
2. Check XML in `debug/` folder for actual element structure
3. Update locators to match actual app state
4. Use robust multi-strategy element finding (see `CLAUDE.md`)

**"iOS sheet/modal blocking navigation"**
- Framework includes automatic sheet dismissal via swipe-down gesture
- Use `dismiss_modal_if_present()`, `dismiss_sheet_by_swipe()`, or `tap_outside_sheet()`
- See `TROUBLESHOOTING.md` for complete diagnostic workflow

**"Tests are too slow"**
- Enable Fast Mode: `FAST_MODE=true pytest tests/ios/ -v`
- Use parallel execution: `pytest tests/ios/ -n auto`
- See `README_PERFORMANCE.md` for optimization strategies

For complete troubleshooting workflow, see `TROUBLESHOOTING.md` in deployed projects.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Appium** - For the excellent mobile automation framework
- **Pytest** - For the robust testing framework
- **Python Community** - For amazing tools and libraries

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/appium-multiplatform-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/appium-multiplatform-framework/discussions)
- **Documentation**: See [docs/](docs/) directory

---

## 🌟 Star History

If you find this framework useful, please consider giving it a star! ⭐

---

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/appium-multiplatform-framework?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/appium-multiplatform-framework?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/appium-multiplatform-framework)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/appium-multiplatform-framework)

---

<div align="center">

**Built with ❤️ for the mobile test automation community**

[⬆ back to top](#appium-multi-platform-automation-framework)

</div>
