# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos


###############################################################################
# Imports
###############################################################################

from __future__ import unicode_literals
from builtins import object, str

from jinja2 import Environment, PackageLoader

from .monitors import (
    AbsenceBuilder, ExistenceBuilder, RequirementBuilder, ResponseBuilder,
    PreventionBuilder,
)


###############################################################################
# Public Interface
###############################################################################

class TemplateRenderer(object):
    def __init__(self):
        self.jinja_env = Environment(
            loader=PackageLoader('hplrv', 'templates'),
            line_statement_prefix=None,
            line_comment_prefix=None,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=False
        )

    def render_monitor(self, hpl_property):
        if hpl_property.pattern.is_absence:
            builder = AbsenceBuilder(hpl_property)
            template_file = 'absence.python.jinja'
        elif hpl_property.pattern.is_existence:
            builder = ExistenceBuilder(hpl_property)
            template_file = 'existence.python.jinja'
        elif hpl_property.pattern.is_requirement:
            builder = RequirementBuilder(hpl_property)
            if not builder.has_trigger_refs:
                template_file = 'requirement-simple.python.jinja'
            else:
                template_file = 'requirement-refs.python.jinja'
        elif hpl_property.pattern.is_response:
            builder = ResponseBuilder(hpl_property)
            template_file = 'response.python.jinja'
        elif hpl_property.pattern.is_prevention:
            builder = PreventionBuilder(hpl_property)
            template_file = 'prevention.python.jinja'
        else:
            raise ValueError('unknown pattern: ' + str(hpl_property.pattern))
        data = {'state_machine': builder}
        return self._render_template(template_file, data)

    def _render_template(self, template_file, data, strip=True):
        template = self.jinja_env.get_template(template_file)
        text = template.render(**data).encode('utf-8')
        if strip:
            text = text.strip()
        return text
