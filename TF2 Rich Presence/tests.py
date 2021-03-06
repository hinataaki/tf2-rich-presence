# Copyright (C) 2019 Kataiser & https://github.com/Kataiser/tf2-rich-presence/contributors
# https://github.com/Kataiser/tf2-rich-presence/blob/master/LICENSE

import io
import os
import shutil
import sys
import time
import tkinter as tk
import unittest
import webbrowser

import keyboard
import requests
from discoIPC import ipc

import configs
import custom_maps
import launcher
import localization
import logger
import main
import processes
import settings
import updater


class TestTF2RichPresenseFunctions(unittest.TestCase):
    def setUp(self):
        self.old_settings = settings.access_registry()
        if self.old_settings != settings.get_setting_default(return_all=True):
            settings.access_registry(save_dict=settings.get_setting_default(return_all=True))

        self.log = logger.Log()
        self.log.enabled = False
        self.log.to_stderr = False
        self.log.sentry_enabled = False
        self.log.log_levels_allowed = self.log.log_levels

    def tearDown(self):
        self.log.log_file.close()
        settings.access_registry(save_dict=self.old_settings)

    def test_interpret_console_log(self):
        app = main.TF2RichPresense(self.log)
        self.assertEqual(app.interpret_console_log('test_resources\\console_in_menus.log', ['Kataiser'], float('inf')), ('In menus', 'Not queued'))
        self.assertEqual(app.interpret_console_log('test_resources\\console_queued_casual.log', ['Kataiser'], float('inf')), ('In menus', 'Queued for Casual'))
        self.assertEqual(app.interpret_console_log('test_resources\\console_badwater.log', ['Kataiser'], float('inf')), ('pl_badwater', 'Pyro'))
        self.assertEqual(app.interpret_console_log('test_resources\\console_custom_map.log', ['Kataiser'], float('inf')), ('cp_catwalk_a5c', 'Soldier'))
        self.assertEqual(app.interpret_console_log('test_resources\\console_empty.log', ['Kataiser'], float('inf')), ('', ''))

    def test_steam_config_file(self):
        self.assertEqual(configs.steam_config_file(self.log, 'test_resources\\'), ['Kataiser'])

    def test_find_custom_map_gamemode(self):
        self.assertEqual(tuple(custom_maps.find_custom_map_gamemode(self.log, 'cp_catwalk_a5c', 5)), ('control-point', 'Control Point'))
        self.assertEqual(tuple(custom_maps.find_custom_map_gamemode(self.log, 'koth_wubwubwub_remix_vip', 5)), ('koth', 'King of the Hill'))
        self.assertEqual(tuple(custom_maps.find_custom_map_gamemode(self.log, 'surf_air_arena_v4', 5)), ('surfing', 'Surfing'))
        self.assertEqual(tuple(custom_maps.find_custom_map_gamemode(self.log, 'ph_kakariko_b1', 5)), ('prophunt', 'Prop Hunt'))  # Prop Hunt? Prophunt? idk
        self.assertEqual(tuple(custom_maps.find_custom_map_gamemode(self.log, 'ytsb8eitybw', 5)), ('unknown_map', 'Unknown gamemode'))

    def test_logger(self):
        self.log.log_file.close()
        try:
            os.remove(self.log.filename)
        except (FileNotFoundError, PermissionError):
            pass

        self.log.enabled = True
        self.log.filename = 'test_resources\\test_self.log'

        try:
            os.remove(self.log.filename)
        except (FileNotFoundError, PermissionError):
            pass

        self.log.log_file = open(self.log.filename, 'a')
        self.log.info("Test.")
        self.log.log_file.close()

        with open(self.log.filename, 'r') as current_log_file:
            self.assertTrue(' +0.0000] INFO: Test.\n' in current_log_file.read())

        os.remove(self.log.filename)

    def test_log_cleanup(self):
        old_dir = os.getcwd()
        os.chdir(os.path.abspath('test_resources'))

        try:
            shutil.rmtree('logs')
        except FileNotFoundError:
            pass

        shutil.copytree('empty_logs', 'logs')
        self.log.cleanup(4)
        self.assertEqual(os.listdir('logs'), ['267d4853.log', '46b087ff.log', '898ff621.log', 'da0d028a.log'])
        shutil.rmtree('logs')

        os.chdir(old_dir)

    def test_generate_hash(self):
        old_dir = os.getcwd()
        os.chdir(os.path.abspath('test_resources\\hash_targets'))

        self.assertEqual(logger.generate_hash(), '46e4b3f2')

        os.chdir(old_dir)

    def test_access_github_api(self):
        newest_version, downloads_url, changelog = updater.access_github_api(10)
        self.assertTrue(newest_version.startswith('v') and '.' in newest_version)
        self.assertTrue(downloads_url.startswith('https://github.com/Kataiser/tf2-rich-presence/releases/tag/v'))
        self.assertTrue(len(changelog) > 0)

        with self.assertRaises(requests.exceptions.Timeout):
            updater.access_github_api(0.01)

    def test_settings_check_int(self):
        self.assertTrue(settings.check_int('', 1000))
        self.assertTrue(settings.check_int('1', 1000))
        self.assertTrue(settings.check_int('1000', 1000))
        self.assertTrue(settings.check_int('60', 60))

        self.assertFalse(settings.check_int('1001', 1000))
        self.assertFalse(settings.check_int('61', 60))
        self.assertFalse(settings.check_int('a', 1000))
        self.assertFalse(settings.check_int('abc123qwe098', 1000))

    def test_settings_access(self):
        default_settings = settings.get_setting_default(return_all=True)

        for setting in default_settings:
            self.assertEqual(type(default_settings[setting]), type(settings.get(setting)))

    def test_get_api_key(self):
        self.assertEqual(len(launcher.get_api_key('discord')), 18)
        self.assertEqual(len(launcher.get_api_key('teamwork')), 32)
        self.assertEqual(len(launcher.get_api_key('pastebin')), 32)
        self.assertEqual(len(launcher.get_api_key('sentry')), 91)

    def test_discoipc(self):
        # this test fails if Discord isn't running
        activity = {'details': 'In menus',
                    'timestamps': {'start': int(time.time())},
                    'assets': {'small_image': 'tf2_icon_small', 'small_text': 'Team Fortress 2', 'large_image': 'main_menu',
                               'large_text': 'In menus'},
                    'state': ''}

        client = ipc.DiscordIPC('429389143756374017')
        time.sleep(0.1)  # this fix works? seriously?
        client.connect()
        client.update_activity(activity)
        client_state = (client.client_id, client.connected, client.ipc_path, isinstance(client.pid, int), client.platform, isinstance(client.socket, io.BufferedRandom), client.socket.name)
        self.assertEqual(client_state, ('429389143756374017', True, '\\\\?\\pipe\\discord-ipc-0', True, 'windows', True, '\\\\?\\pipe\\discord-ipc-0'))

        client.disconnect()
        client_state = (client.client_id, client.connected, client.ipc_path, isinstance(client.pid, int), client.platform, client.socket)
        self.assertEqual(client_state, ('429389143756374017', False, '\\\\?\\pipe\\discord-ipc-0', True, 'windows', None))

    def test_compact_file(self):
        compact_file_out = logger.compact_file('test_resources\\console_badwater.log', guarantee=True)

        try:
            self.assertTrue(compact_file_out.startswith("Compacted file test_resources\\console_badwater.log (took "))
            self.assertTrue(compact_file_out.endswith("console_badwater.log 9309970 : 2490368 = 3.7 to 1 [OK] 1 files within 1 directories were compressed. 9,309,970 total bytes of data are "
                                                      "stored in 2,490,368 bytes. The compression ratio is 3.7 to 1."))
        except self.failureException:
            print(compact_file_out, file=sys.stderr)
            raise

    def test_generate_delta(self):
        app = main.TF2RichPresense(self.log)

        self.assertEqual(app.generate_delta(time.time() - 1), ' (+1 second)')
        self.assertEqual(app.generate_delta(time.time() - 10), ' (+10 seconds)')
        self.assertEqual(app.generate_delta(time.time() - 100), ' (+1.7 minutes)')
        self.assertEqual(app.generate_delta(time.time() - 1000), ' (+16.7 minutes)')
        self.assertEqual(app.generate_delta(time.time() - 10000), ' (+2.8 hours)')
        self.assertEqual(app.generate_delta(time.time() - 100000), ' (+1.2 days)')

    def test_process_scanning(self):
        process_scanner = processes.ProcessScanner(self.log)

        self.assertEqual(len(process_scanner.scan()), 3)
        p_info = process_scanner.get_info_from_pid(os.getpid(), ('path', 'time'))

        self.assertEqual(p_info['running'], False)
        self.assertTrue('python' in p_info['path'].lower())  # hope your Python installation is sane
        self.assertTrue(isinstance(p_info['time'], int))

    def test_settings_gui(self):
        root = tk.Tk()
        settings_gui = settings.GUI(root)
        dimensions = settings_gui.window_dimensions

        self.assertGreaterEqual(dimensions[0], 200)
        self.assertGreaterEqual(dimensions[1], 200)

    def test_localization(self):
        all_keys = localization.access_localization_file().keys()
        english_lines = [localization.access_localization_file()[key]['English'] for key in all_keys]
        num_lines_total = len(english_lines)
        incorrect_hashes = []

        for key in all_keys:
            test_key = localization.hash_text(localization.access_localization_file()[key]['English'])

            if key != test_key:
                incorrect_hashes.append((key, test_key, localization.access_localization_file()[key]['English']))

        self.assertEqual(incorrect_hashes, [])

        for language in ['English', 'German', 'French', 'Spanish', 'Portuguese', 'Italian', 'Dutch', 'Polish', 'Russian', 'Korean', 'Chinese', 'Japanese']:
            localizer = localization.Localizer(language=language)
            num_equal_lines = 0

            for line_english in english_lines:
                line_localized = localizer.text(line_english)
                self.assertNotEqual(line_localized, "")
                self.assertEqual(line_localized.count('{0}'), line_english.count('{0}'))
                self.assertEqual(line_localized.count('{1}'), line_english.count('{1}'))

                if line_localized == line_english:
                    num_equal_lines += 1

            if language == 'English':
                self.assertEqual(num_equal_lines, num_lines_total)
            else:
                self.assertLess(num_equal_lines, num_lines_total / 2)

    def test_main_simple(self):
        log = logger.Log()
        app = main.TF2RichPresense(log)
        self.assertEqual(app.test_state, 'init')
        self.assertEqual(fix_activity_dict(app.activity),
                         {'details': 'In menus', 'timestamps': {'start': 0}, 'assets': {'small_image': 'tf2_icon_small', 'small_text': 'Team Fortress 2',
                                                                                        'large_image': 'main_menu', 'large_text': 'Main menu'}, 'state': ''})
        app.loop_body()
        self.assertEqual(app.test_state, 'no tf2')
        self.assertEqual(fix_activity_dict(app.activity),
                         {'details': 'In menus', 'timestamps': {'start': 0}, 'assets': {'small_image': 'tf2_icon_small', 'small_text': 'Team Fortress 2',
                                                                                        'large_image': 'main_menu', 'large_text': 'Main menu'}, 'state': ''})


class TestTF2RichPresenseSimulated(unittest.TestCase):
    def test_main(self):
        # this one is seperate due to the long run time (over 1.5 minutes)
        # this opens TF2 and simulates keypresses, so it needs Steam and Discord to be running
        # requires the custom map cp_catwalk_a5c to be installed (https://tf2maps.net/downloads/catwalk.1393/)

        log = logger.Log()
        app = main.TF2RichPresense(log)
        self.assertEqual(app.test_state, 'init')
        self.assertEqual(fix_activity_dict(app.activity),
                         {'details': 'In menus', 'timestamps': {'start': 0}, 'assets': {'small_image': 'tf2_icon_small', 'small_text': 'Team Fortress 2',
                                                                                        'large_image': 'main_menu', 'large_text': 'In menus'}, 'state': ''})
        app.loop_body()
        self.assertEqual(app.test_state, 'no tf2')
        self.assertEqual(fix_activity_dict(app.activity),
                         {'details': 'In menus', 'timestamps': {'start': 0}, 'assets': {'small_image': 'tf2_icon_small', 'small_text': 'Team Fortress 2',
                                                                                        'large_image': 'main_menu', 'large_text': 'In menus'}, 'state': ''})

        print("Launching TF2 via default browser")
        webbrowser.open('steam://rungameid/440')
        input("Press enter when TF2 has finished loading (will send an alt-tab)")
        keyboard.press('alt')
        keyboard.press_and_release('tab')
        keyboard.release('alt')
        app.loop_body()
        self.assertEqual(app.test_state, 'menus')
        self.assertEqual(fix_activity_dict(app.activity),
                         {'details': 'In menus', 'timestamps': {'start': 0}, 'assets': {'small_image': 'tf2_icon_small', 'small_text': 'Team Fortress 2',
                                                                                        'large_image': 'main_menu', 'large_text': 'Main menu'}, 'state': 'Not queued'})

        print("Loading in to map \"itemtest\"")
        keyboard.press_and_release('~')
        time.sleep(0.5)
        keyboard.write('map itemtest')
        time.sleep(0.2)
        keyboard.press_and_release('enter')
        input("Press enter when itemtest has finished loading (will send an alt-tab)")
        keyboard.press('alt')
        keyboard.press_and_release('tab')
        keyboard.release('alt')
        time.sleep(0.2)
        for _ in range(3):
            keyboard.press_and_release('d')
            time.sleep(0.2)
        keyboard.press_and_release('1')
        time.sleep(0.5)
        app.loop_body()
        self.assertEqual(app.test_state, 'in game')
        self.assertEqual(fix_activity_dict(app.activity),
                         {'details': 'Map: Itemtest', 'timestamps': {'start': 0}, 'assets': {'small_image': 'scout_icon', 'small_text': 'Scout',
                                                                                             'large_image': 'unknown_map', 'large_text': 'No gamemode'}, 'state': 'Class: Scout'})

        print("Changing map to \"cp_catwalk_a5c\"")
        keyboard.press_and_release('~')
        time.sleep(0.5)
        keyboard.write('map cp_catwalk_a5c')
        time.sleep(0.2)
        keyboard.press_and_release('enter')
        input("Press enter when cp_catwalk has finished loading (will send an alt-tab)")
        keyboard.press('alt')
        keyboard.press_and_release('tab')
        keyboard.release('alt')
        time.sleep(0.2)
        for _ in range(3):
            keyboard.press_and_release('d')
            time.sleep(0.2)
        keyboard.press_and_release('2')
        time.sleep(0.5)
        app.loop_body()
        self.assertEqual(app.test_state, 'in game')
        self.assertEqual(fix_activity_dict(app.activity),
                         {'details': 'Map: cp_catwalk_a5c', 'timestamps': {'start': 0},
                          'assets': {'small_image': 'soldier_icon', 'small_text': 'Soldier',
                                     'large_image': 'control-point', 'large_text': 'Control Point [custom/community map]'}, 'state': 'Class: Soldier'})

        print("Quitting to main menu")
        keyboard.press_and_release('~')
        time.sleep(0.5)
        keyboard.write('disconnect')
        time.sleep(0.2)
        keyboard.press_and_release('enter')
        time.sleep(0.2)
        app.loop_body()
        self.assertEqual(app.test_state, 'menus')
        self.assertEqual(fix_activity_dict(app.activity),
                         {'details': 'In menus', 'timestamps': {'start': 0}, 'assets': {'small_image': 'tf2_icon_small', 'small_text': 'Team Fortress 2',
                                                                                        'large_image': 'main_menu', 'large_text': 'Main menu'}, 'state': 'Not queued'})

        keyboard.write('quit')
        time.sleep(0.2)
        keyboard.press_and_release('enter')
        print("Waiting 15 seconds for TF2 to fully close")
        time.sleep(15)  # TF2's process takes forever to finally end after the game is closed

        try:
            app.loop_body()
        except SystemExit:
            pass
        self.assertEqual(app.test_state, 'no tf2')
        self.assertEqual(fix_activity_dict(app.activity),
                         {'details': 'In menus', 'timestamps': {'start': 0}, 'assets': {'small_image': 'tf2_icon_small', 'small_text': 'Team Fortress 2',
                                                                                        'large_image': 'main_menu', 'large_text': 'Main menu'}, 'state': 'Not queued'})
        log.log_file.close()


def fix_activity_dict(activity):
    try:
        activity['timestamps']['start'] = int(activity['timestamps']['start'] * 0)
    except KeyError:
        pass

    return activity


if __name__ == '__main__':
    unittest.main()
