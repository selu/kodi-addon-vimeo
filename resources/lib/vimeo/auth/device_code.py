#! /usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from .base import AuthenticationMixinBase
from . import GrantFailed


class DeviceCodeMixin(AuthenticationMixinBase):
    """
    Implement the device code grant for Vimeo.

    This class should never be inited on it's own.
    """

    def initiate_device_authentication(self, scope=[]):
        """Initiate the device code grant process."""

        params = {
            "grant_type": "device_grant"
        }

        if (scope):
            scope = ' '.join(scope)
            params['scope'] = scope

        code, headers, resp = self.call_grant(
            '/oauth/device',
            params
        )

        if not code == 200:
            raise GrantFailed()

        return resp

    def device_authorization(self, authorize_url, device_code, user_code):
        """Check whether the user authorized this device."""

        params = {
            "user_code": user_code,
            "device_code": device_code
        }

        code, headers, resp = self.call_grant(
            authorize_url,
            params
        )

        if not code == 200:
            raise GrantFailed()

        self.token = resp['access_token']

        return self.token
