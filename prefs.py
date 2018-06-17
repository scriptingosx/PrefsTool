#!/usr/bin/python

import os
import sys
import argparse
from Foundation import (NSUserDefaults,
                       CFPreferencesAppValueIsForced,
                       CFPreferencesCopyAppValue,
                       CFPreferencesCopyValue,
                       kCFPreferencesAnyUser,
                       kCFPreferencesAnyHost,
                       kCFPreferencesCurrentUser,
                       kCFPreferencesCurrentHost,
                       kCFPreferencesAnyApplication)

def get_type(value):
    '''Returns type of pref value'''
    if value is None:
        return 'null'
    type_name = type(value).__name__
    if type_name == '__NSCFDictionary':
        return 'dict'
    if type_name == '__NSCFArray':
        return 'array'
    if type_name in ('pyobjc_unicode', '__NSCFString'):
        return 'string'
    if type_name in ('bool', '__NSCFBoolean'):
        return 'bool'
    if type_name == '__NSCFData':
        return 'data'
    if type_name == '__NSDate':
        return 'date'
    if type_name == 'OC_PythonLong':
        return 'int'
    if type_name == 'OC_PythonFloat':
        return 'real'
    return type(value).__name__

def get_pref_value(bundle_id, pref_name):
    '''Returns the effective value of a preference'''
    return CFPreferencesCopyAppValue(pref_name, bundle_id)

def get_config_level(bundle_id, pref_name, value, showPath):
    '''Returns a string indicating where the given preference is defined'''
    if value is None:
        return 'not set'
    if CFPreferencesAppValueIsForced(pref_name, bundle_id):
        return 'Managed'
    home_dir = os.path.expanduser('~')
    # define all the places we need to search, in priority order
    levels = [
        {'location': 'User/ByHost',
         'file': os.path.join(home_dir, 'Library/Preferences/ByHost',
                              bundle_id + '.xxxx.plist'),
         'domain': bundle_id,
         'user': kCFPreferencesCurrentUser,
         'host': kCFPreferencesCurrentHost
        },
        {'location': 'User',
         'file': os.path.join(home_dir, 'Library/Preferences/',
                              bundle_id + '.plist'),
         'domain': bundle_id,
         'user': kCFPreferencesCurrentUser,
         'host': kCFPreferencesAnyHost
        },
        {'location': 'User/ByHost/Global',
         'file': os.path.join(home_dir, 'Library/Preferences/ByHost',
                              '.GlobalPreferences.xxxx.plist'),
         'domain': kCFPreferencesAnyApplication,
         'user': kCFPreferencesCurrentUser,
         'host': kCFPreferencesCurrentHost
        },
        {'location': 'User/Global',
         'file': os.path.join(home_dir, 'Library/Preferences',
                              '.GlobalPreferences.plist'),
         'domain': kCFPreferencesAnyApplication,
         'user': kCFPreferencesCurrentUser,
         'host': kCFPreferencesAnyHost
        },
        {'location': 'Computer',
         'file': os.path.join('/Library/Preferences', bundle_id +'.plist'),
         'domain': bundle_id,
         'user': kCFPreferencesAnyUser,
         'host': kCFPreferencesCurrentHost
        },
        {'location': 'Computer/Global',
         'file': '/Library/Preferences/.GlobalPreferences.plist',
         'domain': kCFPreferencesAnyApplication,
         'user': kCFPreferencesAnyUser,
         'host': kCFPreferencesCurrentHost
        },
    ]
    for level in levels:
        if (value == CFPreferencesCopyValue(
                pref_name, level['domain'], level['user'], level['host'])):
            if showPath:
                return level['file']
            else:
                return level['location']
    if value == DEFAULT_PREFS.get(pref_name):
        return 'default'
    return 'unknown'

def print_detail(app_id, key, showGlobals, showPath):
    value = get_pref_value(app_id, key)
    type = get_type(value)
    location = get_config_level(app_id, key, value, showPath)
    if (showGlobals or "Global" not in location):
        print "%s <%s>: %r (%s)" % (key, type, value, location)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("app_id", metavar="APP_ID", help="the app identifier or preference domain")
    parser.add_argument("keys", nargs="*", metavar="KEY", help="preference keys to show. When no key is given all values will be shown")
    parser.add_argument("-g", "--globals", action="store_true", help="show values from GlobalPreferences files as well")
    parser.add_argument("-V", "--value", action="store_true", help="show only the value, no other information")
    parser.add_argument("-p", "--path", action="store_true", help="print path to plist file instead of domain")
    args = parser.parse_args()

    app_id = args.app_id
    showGlobals = args.globals
    
    if len(args.keys) == 0:
        app_defaults = NSUserDefaults.alloc().initWithSuiteName_(app_id)
        keys = app_defaults.dictionaryRepresentation().keys()
    else:
        keys = args.keys
        # set showGlobals regardless so all keys will be shown
        showGlobals = True
    
    for key in keys:
        if args.value:
            print repr(get_pref_value(app_id, key))
        else:
            print_detail(app_id, key, showGlobals, args.path)


if __name__ == '__main__':
    main()