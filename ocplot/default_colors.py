from em_reconstruction.plotting_utils.color_utils import get_n_colors
from matplotlib.colors import ListedColormap

COLS = dict(
    phase=ListedColormap(get_n_colors(1000, lum=45, sat=70, hshift=90) / 255),
    phase_light=ListedColormap(get_n_colors(1000, lum=60, sat=45, hshift=90) / 255),
    isoluminant=[
        "#bf3f76",
        "#577b34",
        "#9d6620",
        "#c54238",
        "#925b84",
        "#546dae",
        "#976a61",
        "#397b74",
        "#5981a3",
    ],
    qualitative=[
        "#1b9e77",
        "#d95f02",
        "#7570b3",
        "#e7298a",
        "#66a61e",
        "#e6ab02",
        "#a6761d",
    ],
)
