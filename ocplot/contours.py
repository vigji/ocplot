import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from skimage.measure import find_contours


def smooth(coords, wnd=7):
    padded = np.concatenate([coords[-wnd:, :], coords, coords[:wnd, :]])
    return pd.DataFrame(padded).rolling(wnd, center=True).mean().values[wnd:-wnd]


def projection_contours(img, smooth_wnd=7, thr=0.5, size_threshold=40):
    """Find contours in a 2D image and smooth them. Returns a list of smoothed contours."""
    padded = np.zeros([(s + 2) for s in img.shape])
    padded[1:-1, 1:-1] = img
    contours = find_contours(padded, thr)
    return [
        smooth(c, wnd=smooth_wnd) - 1 for c in contours if c.shape[0] > size_threshold
    ]


def plot_projection(mask, i, smooth_wnd=7, resolution=0.5, ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()
    contours = projection_contours(mask.max(i), smooth_wnd=smooth_wnd)
    for contour in contours:
        contour *= resolution
        ax.fill(contour[:, 1], contour[:, 0], **kwargs)
