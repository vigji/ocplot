import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from skimage import measure


def add_cbar(
    ref_plot,
    ax,
    inset_loc=None,
    title="",
    ticks=None,
    ticklabels=None,
    tick_visible=False,
    labelsize=8,
    titlesize=10,
    **kwargs,
):
    """Add properly edited colorbar to a plot.

    Parameters
    ----------
    ref_plot : matplotlib object accepting a colormap.
        The imshow/scatterplot to add the cmap to.
    ax : Axis
        Either the axes to be used for plotting (if no inset_loc passed), or the axes
        relative to which to compute the position of the inset plot.
    inset_loc : tuple (optional)
        Position of the colormap inset, relative to ref_axis (default=None).
    title : str (optional)
        Title (label) of the colormap (default=None).
    ticks : list (optional)
         List of ticks positions (default=matplotlib default).
    ticklabels : list (optional)
        List of ticks labels (default=matplotlib default).
    tick_visible : bool (optional)
        Specify if ticks are visible. If not, remove box as well (default=False).
    labelsize : int (optional)
        Specify fontsize of tick labels (default=8).
    titlesize : int (optional)
        Specify fontsize of title (default=10).
    kwargs

    Returns
    -------
        matplotlib Colorbar obj

    """
    if inset_loc is not None:
        col_ax = inset_axes(
            ax,
            width="100%",
            height="100%",
            bbox_to_anchor=inset_loc,
            bbox_transform=ax.transAxes,
        )
        # col_ax = plt.gcf().add_axes(col_ax)
    else:
        col_ax = ax

    cbar = plt.colorbar(ref_plot, cax=col_ax, **kwargs)
    cbar.ax.set_title(title, fontsize=titlesize)
    cbar.set_ticks(ticks)

    if not tick_visible:
        cbar.ax.tick_params(size=0.0)
        cbar.outline.set_visible(False)
    if ticklabels is not None:
        cbar.set_ticklabels(ticklabels)

    if labelsize is not None:
        cbar.ax.tick_params(labelsize=labelsize)

    return cbar


def despine(ax, sides=("right", "top"), rmticks=True):
    if sides == "all":
        sides = ["right", "top", "left", "bottom"]
    if rmticks:
        if sides == "all":
            ax.set(xticks=[], yticks=[])
        if "left" in sides:
            ax.set(yticks=[])
        if "bottom" in sides:
            ax.set(xticks=[])
    [ax.axes.spines[s].set_visible(False) for s in sides]


def add_scalebar(
    ax=None,
    xlen=None,
    ylen=None,
    xpos=None,
    ypos=None,
    xunits=None,
    yunits=None,
    xlabel=None,
    ylabel=None,
    fontsize=8,
    line_params=None,
    text_params=None,
    disable_axis=True,
    line_spacing_coef=0.1,
    text_spacing_coef=0.06,
    lw=1,
    c=(0.2,) * 3,
):
    """Function to add a scale bar to an existing plot. Currently implemented only
    for both axes.

    Parameters
    ----------
    ax : plt.Axis obj
        The target axis for the scalebar. If none, get current (default=None).
    xlen : Int or Float
        Extension of the bar in x.
    ylen : int or float
        Extension of the bar in y.
    xpos : int or float
        Position of the bar in x.
    ypos : int or float
        Position of the bar in y.
    xunits : str
        Units of the x axis, added after number in label (default=None).
    yunits : str
        Units of the x axis, added after number in label (default=None).
    xlabel : str
        Label over the x axis. Overrides the standard '{number} {units}' (default=None).
    ylabel : str
        Label over the y axis. Overrides the standard '{number} {units}' (default=None).
    line_params : dict
        Dictionary of parameters for the plt.plot function for the line (default=None).
    text_params : dict
        Dictionary of parameters for the plt.txt adding the labels (default=None).
    disable_axis : bool
        Flag to hide the orgiginal axis after the colorbar is added (default=True).
    line_spacing_coef : float
        Spacing between minimum point on the plot and the bar, as a fraction of the
        data extension over that axis (default: 0.1).
    text_spacing_coef : float
        Spacing between the bar and the labels, as a fraction of the bar length
        (default: 0.06).


    """

    if ax is None:
        ax = plt.gca()

    line_params_def = dict(lw=lw, c=c)
    text_params_def = dict(fontsize=fontsize, c=c)

    for default_params, params_in in zip(
        [line_params_def, text_params_def], [line_params, text_params]
    ):
        if params_in is not None:
            default_params.update(params_in)

    if xlen is None:
        xlen = ax.xaxis.get_ticklocs()[1] - ax.xaxis.get_ticklocs()[0]
    if ylen is None:
        ylen = ax.yaxis.get_ticklocs()[1] - ax.yaxis.get_ticklocs()[0]

    plot_data_lims = (
        ax.dataLim.min - (ax.dataLim.max - ax.dataLim.min) * line_spacing_coef
    )
    if xpos is None:
        xpos = plot_data_lims[0]
    if ypos is None:
        ypos = plot_data_lims[1]

    if xlabel is None:
        xlabel = f"{xlen}" if xunits is None else f"{xlen} {xunits}"
    if ylabel is None:
        ylabel = f"{ylen}" if yunits is None else f"{ylen} {yunits}"

    ax.plot([xpos, xpos, xpos + xlen], [ypos + ylen, ypos, ypos], **line_params_def)
    ax.text(
        xpos - np.abs(xlen) * text_spacing_coef,
        ypos + ylen / 2,
        ylabel,
        ha="right",
        va="center",
        rotation="vertical",
        **text_params_def,
    )
    ax.text(
        xpos + xlen / 2,
        ypos - ylen * text_spacing_coef,
        xlabel,
        ha="center",
        va="top",
        **text_params_def,
    )

    if disable_axis:
        despine(ax, "all")
