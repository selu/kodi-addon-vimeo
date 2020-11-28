#! /usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
from . import GrantFailed

class ClientTokenMixin(object):
    """Provide core logic to the authentication mixins."""

    def verify_token(self):
        """Check the logged in user."""

        resp = self.get('/oauth/verify')

        if not resp.status_code == 200:
            raise GrantFailed

        resp = resp.json()
        res = {
            'scope': resp['scope'].split(),
            'logged_in': 'user' in resp
        }
        if res['logged_in']:
            res['user_uri'] = resp['user']['uri']
            res['user_name'] = resp['user']['name']

        return res

    def delete_token(self):
        """Log out for authenticated user."""

        resp = self.delete('/tokens')

        return resp.status_code
