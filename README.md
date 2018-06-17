# `prefs` Tools

This tool is an extension of [Greg Neagle's `fancy_defaults_read.py`](https://gist.github.com/gregneagle/010b369e86410a2f279ff8e980585c68).

In the simplest use case you can just pass the app identifier:

```
$ ./prefs.py com.apple.screensaver
idleTime <int>: 0L (User/ByHost)
CleanExit <string>: u'YES' (User/ByHost)
askForPassword <bool>: True (Managed)
askForPasswordDelay <int>: 0L (Managed)
moduleDict <dict>: {
    moduleName = iLifeSlideshows;
    path = "/System/Library/Frameworks/ScreenSaver.framework/Resources/iLifeSlideshows.saver";
    type = 0;
} (User/ByHost)
showClock <bool>: True (User/ByHost)
PayloadUUID <string>: u'AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE' (Managed)
tokenRemovalAction <int>: 0L (User/ByHost)
PrefsVersion <int>: 100L (User/ByHost)
```

The tool will print _all_ composited preferences keys and their type and value, with the preference domain where the value was set. The output format is:

```
prefKey <type>: value (domain)
```

A preference domain of `Managed` means the value is set with a configuration profile.

While preference values set in `.GlobalPreferences.plist` in the different domains are composited into the the application defaults, they are _not_ shown by default, since there are many of them and they will make the output fairly unreadable. If you want to see them add the `--globals` (or `-g` option):

```
$ ./prefs.py --globals com.apple.screensaver
```

You can also add one or more keys after the app identifier to get just specific values:

```
$ ./prefs.py com.apple.screensaver askForPassword askForPasswordDelay AppleLocale
askForPassword <bool>: True (Managed)
askForPasswordDelay <int>: 0L (Managed)
AppleLocale <string>: u'en_NL' (User/Global)
```

You can also add the `--value` (or `-V`) option to show just the value in the output (might be useful when you want to get the composited value for another script.

```
$ ./prefs.py -V com.apple.screensaver askForPassword
True
```

## To do:

- determine the configuration profile a setting came from
- set or delete values in a certain domain
- read keys or values in nested arrays or dicts

(inherited from `fancy_defaults_read.py`)
- Instead of '/Library/Preferences/ByHost/com.apple.screensaver.xxxx.plist', print the actual filename.
- Add support for sandboxed applications that store their preferences in ~/Library/Containers/<identifier>/Data/Library/Preferences/<identifier>.plist
