"""Bundled CA certificates shipped with maxgram.

Currently contains the Минцифры (Russian Ministry of Digital Development)
*Russian Trusted Root CA* and *Sub CA*, required to verify the TLS certificate
of ``platform-api2.max.ru``.
"""

from __future__ import annotations

from pathlib import Path

#: Path to the bundled Минцифры Root + Sub CA PEM bundle.
RUSSIAN_TRUSTED_CA: Path = Path(__file__).parent / "russian_trusted_ca.pem"

__all__ = ["RUSSIAN_TRUSTED_CA"]
