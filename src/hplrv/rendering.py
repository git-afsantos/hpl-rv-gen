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

    def render_rospy_node(self, hpl_properties, topic_types):
        class_names = []
        topics = {}
        callbacks = {}
        monitor_classes = []
        for p in hpl_properties:
            builder, template_file = self._template(p, True)
            i = len(class_names)
            builder.class_name = 'Property{}Monitor'.format(i)
            class_names.append(builder.class_name)
            for name in builder.on_msg:
                topics[name] = topic_types[name]
                if name not in callbacks:
                    callbacks[name] = set()
                callbacks[name].add(i)
            data = {'state_machine': builder}
            monitor_classes.append(self._render_template(template_file, data))
        ros_imports = {'std_msgs'}
        for name in topics.values():
            pkg, msg = name.split('/')
            ros_imports.add(pkg)
        data = {
            'class_names': class_names,
            'monitor_classes': monitor_classes,
            'topics': topics,
            'ros_imports': ros_imports,
            'callbacks': callbacks,
        }
        return self._render_template('node.python.jinja', data)

    def render_monitor(self, hpl_property, id_as_class=True):
        builder, template_file = self._template(hpl_property, id_as_class)
        data = {'state_machine': builder}
        return self._render_template(template_file, data)

    def _template(self, hpl_property, id_as_class):
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
        if id_as_class:
            name = hpl_property.metadata.get('id', 'Property')
            name = ''.join(word.title() for word in name.split("_") if word)
            builder.class_name = name + 'Monitor'
        return (builder, template_file)

    def _render_template(self, template_file, data, strip=True):
        template = self.jinja_env.get_template(template_file)
        text = template.render(**data).encode('utf-8')
        if strip:
            text = text.strip()
        return text
