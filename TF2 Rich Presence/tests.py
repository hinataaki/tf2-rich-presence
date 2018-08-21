import os
import shutil
import unittest

import requests

import configs
import custom_maps
import logger as log
import main
import updater


class TestTF2RichPresense(unittest.TestCase):
    def setUp(self):
        log.enabled = False
        log.to_stderr = False
        log.sentry_enabled = False

        if not os.path.exists('main.py'):
            os.chdir(os.path.abspath('TF2 Rich Presence'))

        self.console_lines = 10000

    def test_get_idle_duration(self):
        idle_duration = main.get_idle_duration()
        self.assertTrue(10.0 > idle_duration >= 0.0)

    def test_console_log_in_menus(self):
        self.assertEqual(main.interpret_console_log('test_resources\\console_in_menus.log', ['Kataiser'], self.console_lines), ('In menus', 'Not queued'))

    def test_console_queued_casual(self):
        self.assertEqual(main.interpret_console_log('test_resources\\console_queued_casual.log', ['Kataiser'], self.console_lines), ('In menus', 'Queued for Casual'))

    def test_console_badwater(self):
        self.assertEqual(main.interpret_console_log('test_resources\\console_badwater.log', ['Kataiser'], self.console_lines), ('pl_badwater', 'Pyro'))

    def test_console_custom_map(self):
        self.assertEqual(main.interpret_console_log('test_resources\\console_custom_map.log', ['Kataiser'], self.console_lines), ('cp_catwalk_a5c', 'Soldier'))

    def test_steam_config_file(self):
        self.assertEqual(configs.steam_config_file('test_resources\\'), ['Kataiser'])

    def test_find_custom_map_gamemode(self):
        self.assertEqual(tuple(custom_maps.find_custom_map_gamemode('cp_catwalk_a5c')), ('control-point', 'Control Point'))
        self.assertEqual(tuple(custom_maps.find_custom_map_gamemode('koth_wubwubwub_remix_vip')), ('koth', 'King of the Hill'))
        self.assertEqual(tuple(custom_maps.find_custom_map_gamemode('surf_air_arena_v4')), ('surfing', 'Surfing'))

    def test_logger(self):
        log.enabled = True
        log.filename = 'test_resources\\test_log.log'
        log.info("Test.")

        with open(log.filename, 'r') as current_log_file:
            self.assertTrue(current_log_file.read().endswith('] INFO: Test.\n'))

        os.remove(log.filename)
        log.enabled = False

    def test_log_cleanup(self):
        old_dir = os.getcwd()
        os.chdir(os.path.abspath('test_resources'))

        shutil.copytree('empty_logs', 'logs')
        log.cleanup(4)
        self.assertEqual(os.listdir('logs'), ['267d4853.log', '46b087ff.log', '898ff621.log', 'da0d028a.log'])
        shutil.rmtree('logs')

        os.chdir(old_dir)

    def test_generate_hash(self):
        old_dir = os.getcwd()
        os.chdir(os.path.abspath('test_resources\\hash_targets'))

        self.assertEqual(log.generate_hash(), 'c9311b6e')

        os.chdir(old_dir)

    def test_read_truncated_file(self):
        with open('test_resources\\correct_file_ending.txt', 'r') as correct_file_ending_file:
            correct_file_ending_text = correct_file_ending_file.read()

        self.assertTrue(log.read_truncated_file('test_resources\\console_queued_casual.log', limit=1000) == correct_file_ending_text)

    def test_access_github_api(self):
        newest_version, downloads_url, changelog = updater.access_github_api(10)
        self.assertTrue(newest_version.startswith('v') and '.' in newest_version)
        self.assertTrue(downloads_url.startswith('https://github.com/Kataiser/tf2-rich-presence/releases/tag/v'))
        self.assertTrue(len(changelog) > 0)

        with self.assertRaises(requests.exceptions.Timeout):
            updater.access_github_api(0.01)


if __name__ == '__main__':
    unittest.main()
