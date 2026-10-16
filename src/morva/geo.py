"""Geodesy helpers.

Distances use the haversine formula on a sphere (error < 0.5% vs. the WGS84 ellipsoid,
negligible at the 20-minute horizons studied). Short-range motion models work in a local
equirectangular tangent plane centred on the anchor point (x east, y north, metres),
which is accurate to well under 1 m over the ~10 km a ship covers in 20 minutes.
"""

import numpy as np

EARTH_RADIUS_M = 6_371_008.8
KNOT_MS = 1852.0 / 3600.0


def haversine_m(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = (np.radians(np.asarray(a, dtype=float)) for a in (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * EARTH_RADIUS_M * np.arcsin(np.sqrt(np.clip(a, 0.0, 1.0)))


def to_local_xy(lat, lon, lat0, lon0):
    """Project lat/lon (deg) to metres in a tangent plane at (lat0, lon0). Broadcasts."""
    x = np.radians(np.asarray(lon) - lon0) * EARTH_RADIUS_M * np.cos(np.radians(lat0))
    y = np.radians(np.asarray(lat) - lat0) * EARTH_RADIUS_M
    return x, y


def from_local_xy(x, y, lat0, lon0):
    lat = lat0 + np.degrees(np.asarray(y) / EARTH_RADIUS_M)
    lon = lon0 + np.degrees(np.asarray(x) / (EARTH_RADIUS_M * np.cos(np.radians(lat0))))
    return lat, lon


def velocity_from_sog_cog(sog_kn, cog_deg):
    """Nautical course (clockwise from north) -> (vx east, vy north) in m/s."""
    speed = np.asarray(sog_kn, dtype=float) * KNOT_MS
    theta = np.radians(cog_deg)
    return speed * np.sin(theta), speed * np.cos(theta)
