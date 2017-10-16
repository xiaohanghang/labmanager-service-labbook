# Copyright (c) 2017 FlashX, LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THEt
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from flask import g

from lmcommon.auth.identity import get_identity_manager, AuthenticationError
from lmcommon.configuration import Configuration


# TODO: Store user identity in a cache or the session to reduce overhead between requests
def get_identity_manager_instance():
    id_mrg = getattr(g, '_identity_mgr', None)
    if id_mrg is None:
        id_mrg = g._identity_mgr = get_identity_manager(Configuration())
    return id_mrg


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, context, **args):

        id_mgr = get_identity_manager_instance()

        token = None
        if "Authorization" in info.headers:
            _, token = info.headers["Authorization"].split("Bearer ")
            if not token:
                raise AuthenticationError("Could not parse JWT from Authorization Header. Should be `Bearer XXX`", 401)

        id_mgr.authenticate(token)

        return next(root, info, context, **args)
