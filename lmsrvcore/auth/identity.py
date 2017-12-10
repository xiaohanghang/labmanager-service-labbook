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
from lmcommon.auth.identity import AuthenticationError
import time


def get_identity_manager_instance():
    """Method to retrieve the id manager from the flask application"""
    if "LABMGR_ID_MGR" not in current_app.config:
        raise AuthenticationError("Application mis-configured. Missing identity manager instance.", 401)

    return current_app.config["LABMGR_ID_MGR"]


class AuthorizationMiddleware(object):
    """Middlewere to enforce authentication requirements and parse JWT"""

    def _extract_token(self, headers: dict):
        """Helper method to extract the token from the request

        Args:
            headers:

        Returns:

        """
        # Pull the token out of the header if available
        token = None
        if "Authorization" in headers:
            if "Bearer" in headers["Authorization"]:
                _, token = headers["Authorization"].split("Bearer ")
                if not token:
                    raise AuthenticationError("Could not parse JWT from Authorization Header. Should be `Bearer XXX`", 401)
            else:
                raise AuthenticationError("Could not parse JWT from Authorization Header. Should be `Bearer XXX`", 401)

        return token

    def resolve(self, next, root, args, context, info, **kwargs):
        # Get the identity manager class
        id_mgr = get_identity_manager_instance()

        # Pull the token out of the request, if available
        token = self._extract_token(context.headers)

        # If a token is set, check if token has been validated within the last 8 seconds
        try:
            if token:
                token_key = token[:20]
                if hasattr(current_app, 'last_token_validate'):
                    if type(current_app.last_token_validate) == dict:
                        if token_key in current_app.last_token_validate:
                            # Previously checked this token. Use time based cache
                            if (time.time() - current_app.last_token_validate[token_key]) < 8:
                                # Skip token eval
                                return next(root, args, context, info, **kwargs)
                            else:
                                # Re-validate token
                                current_app.current_user = id_mgr.authenticate(token)
                                current_app.last_token_validate[token_key] = time.time()

                        else:
                            # No previous checks for THIS token, validate token
                            current_app.current_user = id_mgr.authenticate(token)
                            current_app.last_token_validate[token_key] = time.time()

                # No previous checks, validate token
                current_app.current_user = id_mgr.authenticate(token)
                current_app.last_token_validate = {token_key: time.time()}

            else:
                # No token is set, so the frontend doesn't have a valid session.
                # Process auth class to deal with this case.
                # If running with the local auth class, it will load from disk.
                current_app.current_user = id_mgr.authenticate(token)

        except AuthenticationError:
            # If an AuthenticationError is raised here, it means the token was invalid, so remove user data
            current_app.current_user = None

        return next(root, args, context, info, **kwargs)
