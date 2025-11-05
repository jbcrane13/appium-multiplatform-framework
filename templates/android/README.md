# Android Support - Coming Soon

Android automation support is planned for future implementation.

## Current Status

The framework architecture is designed to support both iOS and Android platforms. Android implementation is **in progress** and will be added in a future release.

## Planned Android Features

When implemented, Android support will include:

### Platform Support
- ✅ UIAutomator2 driver integration
- ✅ Android Emulator support
- ✅ Real Android device support
- ✅ APK and AAB handling
- ✅ Multiple Android versions

### Locator Strategies
- ✅ Accessibility ID (content-desc)
- ✅ Resource ID (android:id/)
- ✅ UIAutomator selectors
- ✅ XPath (with caution)
- ✅ Class name

### Features
- ✅ Same Page Object Model as iOS
- ✅ Shared base classes
- ✅ Android-specific gestures
- ✅ Screenshot on failure
- ✅ Same reporting as iOS
- ✅ Parallel execution

## Using This Framework for Android

Once Android support is added, you'll be able to:

```bash
# Deploy Android automation
python deploy/deploy_android.py --app-path ~/Projects/YourAndroidApp

# This will create YourAndroidApp-Automation/ with Android support

# Deploy both platforms
python deploy/deploy_both.py \
  --ios-path ~/Projects/YourApp-iOS \
  --android-path ~/Projects/YourApp-Android
```

## Timeline

Android implementation is targeted for the next framework release.

In the meantime, you can:
1. Use the iOS implementation as a reference
2. Review the platform-agnostic `base_page.py`
3. Prepare your Android app for testing

## Contributing

If you'd like to contribute Android support, see the framework's contributing guide.

---

**This folder will contain Android-specific templates once implementation is complete.**
