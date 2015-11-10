# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2015 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
'''
Wrapper to include useful information in error mails.
'''

from django.views.debug import SafeExceptionReporterFilter
from weblate import get_versions_list


class WeblateExceptionReporterFilter(SafeExceptionReporterFilter):
    def get_post_parameters(self, request):
        if hasattr(request, 'META'):
            meta = request.META
            if (hasattr(request, 'user') and
                    request.user.is_authenticated()):
                meta['WEBLATE_USER'] = repr(request.user.username)
            if (hasattr(request, 'session') and
                    'django_language' in request.session):
                meta['WEBLATE_LANGUAGE'] = request.session['django_language']

            for version in get_versions_list():
                meta['WEBLATE_VERSION:{0}'.format(version[0])] = version[2]

        return super(WeblateExceptionReporterFilter, self).get_post_parameters(
            request
        )
