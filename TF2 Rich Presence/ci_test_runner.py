# Copyright (C) 2019 Kataiser & https://github.com/Kataiser/tf2-rich-presence/contributors
# https://github.com/Kataiser/tf2-rich-presence/blob/master/LICENSE

import os

import tests

# for https://travis-ci.org/Kataiser/tf2-rich-presence
if __name__ == '__main__':
    print(os.listdir(os.getcwd()))

    f_tests = tests.TestTF2RichPresenseFunctions
    ci_tests = [f_tests.test_interpret_console_log, f_tests.test_steam_config_file, f_tests.test_logger, f_tests.test_settings_check_int, f_tests.test_settings_access,
                f_tests.test_get_api_key, f_tests.test_compact_file, f_tests.test_generate_delta, f_tests.test_process_scanning, f_tests.test_settings_gui, f_tests.test_localization,
                f_tests.test_main_simple]

    for ci_test in ci_tests:
        # this is probably broken in some way
        f_test_runner = tests.TestTF2RichPresenseFunctions()
        f_tests.setUp(f_test_runner)
        ci_test(f_test_runner)
        f_tests.tearDown(f_test_runner)
