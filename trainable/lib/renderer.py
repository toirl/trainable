#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pkg_resources
from mako.lookup import TemplateLookup
from formbar.renderer import FieldRenderer
from ringo.lib.renderer.form import renderers
from ringo.lib.helpers import literal
import ringo.lib.helpers

base_dir = pkg_resources.get_distribution("trainable").location
template_dir = os.path.join(base_dir, 'trainable', 'templates')
template_lookup = TemplateLookup(directories=[template_dir],
                                 default_filters=['h'])


def plan_renderer(request, item, column, tableconfig):
    # Depending where where this method is called the item is
    # either a tuple or the item. If it is called from the
    # ListfieldRenderer the item is a tuple
    if isinstance(item, tuple):
        item = item[0]

    # Do the renderering. In case you return HTML do not forget to
    # escape all values properly and finally return a literal.
    if item.category != 0:
        return item.get_value("category", expand=True)
    else:
        return item.plan


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


class MapRenderer(FieldRenderer):
    """Maprenderer for the map on the activity page"""
    def __init__(self, field, translate):
        """@todo: to be defined"""
        FieldRenderer.__init__(self, field, translate)
        self.template = template_lookup.get_template("internal/mapfield.mako")

    def _get_template_values(self):
        values = FieldRenderer._get_template_values(self)
        values['request'] = self._field._form._request
        values['h'] = ringo.lib.helpers
        return values


class ActivityDiagramRenderer(FieldRenderer):
    """Custom renderer to render digrams which are synced to the map"""
    def __init__(self, field, translate):
        """@todo: to be defined"""
        FieldRenderer.__init__(self, field, translate)
        self.template = template_lookup.get_template("internal/diagramfield.mako")

    def _render_label(self):
        return ""

    def _get_template_values(self):
        values = FieldRenderer._get_template_values(self)
        values['request'] = self._field._form._request
        values['h'] = ringo.lib.helpers
        return values

renderers['synceddiagram'] = ActivityDiagramRenderer
renderers['map'] = MapRenderer
renderers['infobox'] = InfoboxRenderer
