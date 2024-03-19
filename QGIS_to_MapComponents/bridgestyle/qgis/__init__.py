
from .. import mapboxgl
from . import togeostyler


def layerStyleAsMapbox(layer):
    geostyler, icons, sprites, warnings = togeostyler.convert(layer)
    mbox, mbWarnings = mapboxgl.fromgeostyler.convert(geostyler)
    warnings.extend(mbWarnings)
    return mbox, icons, warnings