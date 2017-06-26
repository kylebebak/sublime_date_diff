"""
DateDiff - Sublime Text Plugin

Inserts formatted `datetime.now() + timedelta(days=<days>)`.
"""

import sublime, sublime_plugin

from datetime import datetime, timedelta

settings_filename = "DateDiff.sublime-settings"


class PromptDateDiffFmt(sublime_plugin.WindowCommand):
    def run(self): # invoked before `on_done`, which makes passing args via `self` very convenient
        self.fmts = sublime.load_settings(settings_filename).get('fmts')
        self.window.show_quick_panel([f.get('label') for f in self.fmts], self.on_done)

    def on_done(self, index):
        if index < 0:  # e.g. user presses escape
            return
        fmt = self.fmts[index].get('fmt')
        self.window.run_command('prompt_date_diff_days', {'fmt': fmt})


class PromptDateDiffDaysCommand(sublime_plugin.WindowCommand):
    def run(self, fmt=None):
        self.fmt = fmt
        self.window.show_input_panel('Days:', '', self.on_done, None, None)

    def on_done(self, text):
        try:
            days = int(text)
            if self.window.active_view():
                self.window.active_view().run_command('date_diff', {'fmt': self.fmt, 'days': days})
        except ValueError:
            pass


class DateDiffCommand(sublime_plugin.TextCommand):
    FMT = '%a %Y-%m-%d'

    def run(self, edit, fmt=None, days=0):
        settings = sublime.load_settings(settings_filename)
        try:
            default_fmt = settings.get('fmts')[0].get('fmt')
        except:
            default_fmt = None
        fmt = fmt or default_fmt or self.FMT

        view = self.view
        sel = view.sel()
        dt = datetime.now() + timedelta(days=days)
        for region in sel: # handle multiple selection regions
            view.insert(edit, region.begin(), dt.strftime(fmt))
