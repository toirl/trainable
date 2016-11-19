#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pkg_resources
from mako.lookup import TemplateLookup
from formbar.renderer import FieldRenderer
from ringo.lib.renderer.form import renderers
import ringo.lib.helpers

base_dir = pkg_resources.get_distribution("trainable").location
template_dir = os.path.join(base_dir, 'trainable', 'templates')
template_lookup = TemplateLookup(directories=[template_dir],
                                 default_filters=['h'])


class InfoboxRenderer(FieldRenderer):
    """Custom renderer to render digrams which are synced to the map"""
    def __init__(self, field, translate):
        """@todo: to be defined"""
        FieldRenderer.__init__(self, field, translate)
        self.template = template_lookup.get_template("internal/infoboxfield.mako")

    def _render_label(self):
        return ""

    def _get_template_values(self):
        values = FieldRenderer._get_template_values(self)
        values['request'] = self._field._form._request
        values['h'] = ringo.lib.helpers
        return values

renderers['infobox'] = InfoboxRenderer
