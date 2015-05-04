# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2015 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <http://weblate.org/>
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
from weblate import appsettings


class OverrideSettings(object):
    """
    makes a context manager also act as decorator
    """
    def __init__(self, **values):
        self._values = values
        self._backup = {}

    def __enter__(self):
        for name, value in self._values.items():
            self._backup[name] = getattr(appsettings, name)
            setattr(appsettings, name, value)
        return self

    def __exit__(self, *args, **kwds):
        for name in self._values.keys():
            setattr(appsettings, name, self._backup[name])

    def __call__(self, func):
        def wrapper(*args, **kwds):
            with self:
                return func(*args, **kwds)
        return wrapper