#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import re

SETTINGS_FILE = 'esprima.sublime-settings'

class EsprimaCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    settings = sublime.load_settings(SETTINGS_FILE)
    cmd = settings.get('esvalidator', 'esvalidator')

    filepath = self.view.file_name()
    args = {
      "cmd": [
        cmd,
        "--format=sublime",
        filepath
      ],
      'line_regex': settings.get('line_regex', r"(\d+),(\d+): (.*)$"),
      'file_regex': settings.get('file_regex', r"esvalidator (.+)\]")
    }

    if sublime.platform() == "windows":
      args['cmd'][0] += ".cmd"
    elif sublime.platform() == "osx":
      args['path'] = "/usr/local/share/npm/bin:/usr/local/bin:/opt/local/bin:$PATH"

    self.view.window().run_command('exec', args)

class EsprimaOnSave(sublime_plugin.EventListener):
  def on_post_save(self, view):
    settings = sublime.load_settings(SETTINGS_FILE)
    if settings.get('run_on_save', False) == False:
      return
    if re.search(settings.get('filename_filter'), view.file_name()):
      view.window().run_command("esvalidator")
      return
