#! /usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
import xbmc

class AuthenticationMixinBase(object):
    """Provide core logic to the authentication mixins."""

    def call_grant(self, path, data):
        """Perform the calls to the grant endpoints.

        These endpoints handle the echange to get the information from the API.
        """
        assert self.app_info[0] is not None and self.app_info[1] is not None

        xbmc.log("app_info0: %s" % self.app_info[0], xbmc.LOGERROR)
        xbmc.log("app_info1: %s" % self.app_info[1], xbmc.LOGERROR)
        resp = self.post(path, auth=self.app_info, jsonify=False, data=data)

        return resp.status_code, resp.headers, resp.json()
