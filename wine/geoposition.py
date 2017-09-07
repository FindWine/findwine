

def geoposition_to_dms_string(geoposition):
    return '{} {}'.format(
        format_dms(*decimal_to_dms(geoposition.latitude), is_latitude=True),
        format_dms(*decimal_to_dms(geoposition.longitude), is_latitude=False),
    )


def decimal_to_dms(deg):
    # from http://en.proft.me/2015/09/20/converting-latitude-and-longitude-decimal-values-p/
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]


def format_dms(degrees, minutes, seconds, is_latitude):
    if is_latitude:
        prefix = 'N' if degrees > 0 else 'S'
    else:
        prefix = 'E' if degrees > 0 else 'W'
    return '{} {}° {}\' {:.2f}"'.format(prefix, abs(degrees), minutes, seconds)
