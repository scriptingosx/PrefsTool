#!/usr/bin/python

import os
import sys
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

def get_config_level(bundle_id, pref_name, value):
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
         'domain': '.GlobalPreferences',
         'user': kCFPreferencesCurrentUser,
         'host': kCFPreferencesCurrentHost
        },
        {'location': 'User/Global',
         'file': os.path.join(home_dir, 'Library/Preferences',
                              '.GlobalPreferences.plist'),
         'domain': '.GlobalPreferences',
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
         'domain': '.GlobalPreferences',
         'user': kCFPreferencesAnyUser,
         'host': kCFPreferencesCurrentHost
        },
    ]
    for level in levels:
        if (value == CFPreferencesCopyValue(
                pref_name, level['domain'], level['user'], level['host'])):
            return level['location']
    if value == DEFAULT_PREFS.get(pref_name):
        return 'default'
    return 'unknown'


def main():
    try:
        app_id = sys.argv[1]
    except IndexError:
        print >> sys.stderr, "Usage: %s <domain>" % sys.argv[0]
        sys.exit(-1)
    
    app_defaults = NSUserDefaults.alloc().initWithSuiteName_(app_id)
    app_keys = app_defaults.dictionaryRepresentation().keys()
    
    for key in app_keys:
        value = get_pref_value(app_id, key)
        type = get_type(value)
        domain = get_config_level(app_id, key, value)
        #if "Global" not in domain:
        print "%s <%s>: (%s) %r" % (key, type, domain, value)


if __name__ == '__main__':
    main()