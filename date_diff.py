"""
DateDiff - Sublime Text Plugin

Inserts formatted `datetime.now() + timedelta(days=<days>)`.
"""

import sublime, sublime_plugin

from datetime import datetime, timedelta

settings_filename = "DateDiff.sublime-settings"


class PromptDateDiffDaysCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Days:', '', self.on_done, None, None)

    def on_done(self, text):
        try:
            days = int(text)
            if self.window.active_view():
                self.window.active_view().run_command('date_diff', {'days': days})
        except ValueError:
            pass


class DateDiffCommand(sublime_plugin.TextCommand):
    FMT = '%a %Y-%m-%d'

    def run(self, edit, days=0):
        settings = sublime.load_settings(settings_filename)
        fmt = settings.get("fmt") or self.FORMAT

        view = self.view
        sel = view.sel()
        dt = datetime.now() + timedelta(days=days)
        for region in sel: # handle multiple selection regions
            view.insert(edit, region.begin(), dt.strftime(fmt))
