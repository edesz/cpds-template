#!/usr/bin/env python3


"""Define copier context updater."""

from datetime import datetime

from copier_template_extensions import ContextHook


class ContextUpdater(ContextHook):
    def hook(self, context):
        context["current_year"] = datetime.now().year
