from pathlib import Path

import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

src_path = Path("task2_data/dem/study_area_dem.tif")
out_dir = Path("land_pipeline_output/terrain")
out_dir.mkdir(parents=True, exist_ok=True)

if not src_path.exists():
    raise FileNotFoundError(f"DEM not found: {src_path}")

# Allikulam, Thoothukudi: UTM Zone 44N, metres
target_crs = "EPSG:32644"
nodata = -9999.0

# Reproject elevation into a metric CRS
with rasterio.open(src_path) as src:
    transform, width, height = calculate_default_transform(
        src.crs, target_crs, src.width, src.height, *src.bounds
    )

    profile = src.profile.copy()
    profile.update(
        driver="GTiff",
        crs=target_crs,
        transform=transform,
        width=width,
        height=height,
        count=1,
        dtype="float32",
        nodata=nodata,
        compress="deflate"
    )

    elevation = np.full((height, width), nodata, dtype=np.float32)

    reproject(
        source=rasterio.band(src, 1),
        destination=elevation,
        src_transform=src.transform,
        src_crs=src.crs,
        src_nodata=src.nodata,
        dst_transform=transform,
        dst_crs=target_crs,
        dst_nodata=nodata,
        resampling=Resampling.bilinear
    )

elev_path = out_dir / "elevation_utm.tif"
with rasterio.open(elev_path, "w", **profile) as dst:
    dst.write(elevation, 1)

# Calculate slope in degrees using the metric pixel dimensions
valid = np.isfinite(elevation) & (elevation != nodata)

# Fill invalid cells temporarily to avoid contaminating neighbouring gradients
filled = elevation.astype(np.float64)
if not valid.all():
    # Nearest valid fill is used only for gradient calculation
    from scipy.ndimage import distance_transform_edt
    if not valid.any():
        raise ValueError("DEM contains no valid elevation pixels")
    nearest = distance_transform_edt(
        ~valid, return_distances=False, return_indices=True
    )
    filled[~valid] = filled[tuple(nearest)][~valid]

pixel_x = abs(transform.a)
pixel_y = abs(transform.e)

gradient_y, gradient_x = np.gradient(filled, pixel_y, pixel_x)
slope = np.degrees(np.arctan(np.sqrt(gradient_x**2 + gradient_y**2)))
slope = slope.astype(np.float32)
slope[~valid] = nodata

slope_path = out_dir / "slope_degrees.tif"
with rasterio.open(slope_path, "w", **profile) as dst:
    dst.write(slope, 1)

print("Terrain processing complete.")
print("Elevation raster:", elev_path)
print("Slope raster:", slope_path)
print("CRS:", target_crs)
print("Pixel size (m):", round(pixel_x, 2), "x", round(pixel_y, 2))
print("Valid elevation pixels:", int(valid.sum()))
print("Elevation range (m):", round(float(elevation[valid].min()), 2),
      "to", round(float(elevation[valid].max()), 2))
print("Slope range (degrees):", round(float(slope[valid].min()), 2),
      "to", round(float(slope[valid].max()), 2))
