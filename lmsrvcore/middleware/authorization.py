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
from flask import current_app
from lmsrvcore.auth.identity import get_identity_manager_instance, parse_token


class AuthorizationMiddleware(object):
    """Middlewere to enforce authentication requirements and parse JWT"""
    id_mgr = None

    def resolve(self, next, root, info, **args):
        if not self.id_mgr:
            # Load ID manager instance on first run
            self.id_mgr = get_identity_manager_instance()

        # On first field processed in request, authenticate
        if not hasattr(info.context, "auth_middleware_complete"):
            # Pull the token out of the header if available
            token = None
            if "Authorization" in info.context.headers:
                token = parse_token(info.context.headers["Authorization"])

            # Authenticate and set current user context on each request
            current_app.current_user = self.id_mgr.authenticate(token)
            info.context.auth_middleware_complete = True

        return next(root, info, **args)
