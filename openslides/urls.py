#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    openslides.urls
    ~~~~~~~~~~~~~~~

    Global URL list for OpenSlides.

    :copyright: 2011 by the OpenSlides team, see AUTHORS.
    :license: GNU GPL, see LICENSE for more details.
"""

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
from django.utils.importlib import import_module
import settings

handler500 = 'openslides.utils.views.server_error'

urlpatterns = patterns('',

    # frontpage
    (r'^$', RedirectView.as_view(
        url='projector/control',
        permanent = False,
    )),

    (r'^agenda/', include('agenda.urls')),
    (r'', include('application.urls')),
    (r'', include('participant.urls')),
    (r'', include('assignment.urls')),
    (r'config/', include('system.urls')),
    (r'projector/', include('projector.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^i18n/', include('django.conf.urls.i18n')),
)

for plugin in settings.INSTALLED_PLUGINS:
    try:
        mod = import_module(plugin + '.urls')
    except (ImportError):
        continue

    plugin_name = mod.__name__.split('.')[0]
    urlpatterns += patterns('', (r'^%s/' % plugin_name, include('%s.urls' % plugin_name)))


urlpatterns += patterns('',
    (r'^500/$', 'openslides.utils.views.server_error'),
)
