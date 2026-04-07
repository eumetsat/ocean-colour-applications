import numpy as np
from shapely.geometry import MultiPoint, Polygon

def points_mask_in_box(lat, lon, box):
    """
    Create a 2D mask array matching lat/lon shape.
    1 where point is inside box, np.nan elsewhere.
    """
    lat_min, lat_max, lon_min, lon_max = box
    mask = np.ones_like(lat, dtype=float) * np.nan
    inside = (lat >= lat_min) & (lat <= lat_max) & (lon >= lon_min) & (lon <= lon_max)
    mask[inside] = 1.0
    return mask

def largest_common_box_and_masks(grids, num_scanlines=500):
    """
    Parameters
    ----------
    grids : list of (lat, lon)
        Each entry is a pair of 2D arrays (lat_grid, lon_grid)

    Returns
    -------
    box : (lat_min, lat_max, lon_min, lon_max)
    masks : list of 2D arrays (same shapes as input grids)
        mask[i] = 1 inside box, np.nan outside
    """

    # ---- Build convex hull polygons for each grid ----
    def grid_polygon(lat, lon):
        points = np.vstack([
            np.column_stack([lon[0, :], lat[0, :]]),
            np.column_stack([lon[-1, :], lat[-1, :]]),
            np.column_stack([lon[:, 0], lat[:, 0]]),
            np.column_stack([lon[:, -1], lat[:, -1]])
        ])
        return MultiPoint(points).convex_hull

    polygons = [grid_polygon(lat, lon) for lat, lon in grids]

    # ---- Compute intersection of all polygons ----
    inter = polygons[0]
    for p in polygons[1:]:
        inter = inter.intersection(p)
        if inter.is_empty:
            raise RuntimeError("No overlapping region between all grids.")

    # ---- Largest axis-aligned rectangle search ----
    def largest_rectangle_in_intersection(poly, num_scanlines):
        minx, miny, maxx, maxy = poly.bounds
        ys = np.linspace(miny, maxy, num_scanlines)

        xmins = np.zeros_like(ys)
        xmaxs = np.zeros_like(ys)

        for i, y in enumerate(ys):
            # Narrow horizontal band
            band = Polygon([
                (minx, y - 1e-12), (maxx, y - 1e-12),
                (maxx, y + 1e-12), (minx, y + 1e-12)
            ])
            inter_slice = poly.intersection(band)
            if inter_slice.is_empty:
                xmins[i] = np.nan
                xmaxs[i] = np.nan
                continue

            if inter_slice.geom_type == 'Polygon':
                xs = np.array(inter_slice.exterior.xy[0])
            elif inter_slice.geom_type == 'MultiPolygon':
                xs = np.hstack([p.exterior.xy[0] for p in inter_slice.geoms])
            else:
                xmins[i] = xmaxs[i] = np.nan
                continue

            xmins[i] = np.min(xs)
            xmaxs[i] = np.max(xs)

        # Keep only rows where polygon overlaps the scanline
        valid = ~np.isnan(xmins)
        ys_valid = ys[valid]
        xmins = xmins[valid]
        xmaxs = xmaxs[valid]

        # Brute-force search for best rectangle
        best_area = -1
        best_box = None
        n = len(ys_valid)

        for i in range(n):
            for j in range(i + 1, n):
                lat_min = ys_valid[i]
                lat_max = ys_valid[j]
                lon_min_allowed = np.max(xmins[i:j + 1])
                lon_max_allowed = np.min(xmaxs[i:j + 1])
                if lon_max_allowed <= lon_min_allowed:
                    continue

                area = (lat_max - lat_min) * (lon_max_allowed - lon_min_allowed)
                if area > best_area:
                    best_area = area
                    best_box = (lat_min, lat_max, lon_min_allowed, lon_max_allowed)

        return best_box

    box = largest_rectangle_in_intersection(inter, num_scanlines=num_scanlines)

    # ---- Compute masks for each grid ----
    masks = []
    for lat, lon in grids:
        masks.append(points_mask_in_box(lat, lon, box))

    return box, masks
