from __future__ import annotations

import ssl

import certifi

from maxgram.certs import RUSSIAN_TRUSTED_CA

__all__ = ["RUSSIAN_TRUSTED_CA", "create_ssl_context"]


def create_ssl_context(trust_russian_ca: bool = True) -> ssl.SSLContext:
    """Build the default client SSL context for MAX API requests.

    Starts from the standard :mod:`certifi` trust store and, when
    ``trust_russian_ca`` is ``True`` (the default), additionally trusts the
    Минцифры *Russian Trusted Root CA* / *Sub CA*. The MAX API host
    ``platform-api2.max.ru`` presents a certificate chained to that root, which
    is not part of the public certifi bundle, so it must be added explicitly.

    ``load_verify_locations`` *accumulates* CAs rather than replacing them, so
    verification of ordinary public HTTPS endpoints keeps working.

    :param trust_russian_ca: also trust the bundled Минцифры CA (default ``True``).
    """
    context = ssl.create_default_context(cafile=certifi.where())
    if trust_russian_ca:
        context.load_verify_locations(cafile=str(RUSSIAN_TRUSTED_CA))
    return context
