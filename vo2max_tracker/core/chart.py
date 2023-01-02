# Copyright (C) 2022-2023 Javier Albiero (jalbiero)
# Distributed under the MIT License (see the accompanying LICENSE file
# or go to http://opensource.org/licenses/MIT).

import logging
from datetime import date, datetime
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

import mplcursors
from matplotlib import pyplot as plt
from matplotlib import text
from matplotlib.dates import DateFormatter
from mplcursors import Cursor

from vo2max_tracker.config import Config
from vo2max_tracker.fit.decoder import FitData
from vo2max_tracker.fit.provider import fit_data_provider

_T = TypeVar("_T")
_FitDataList = List[FitData]
_PlotDataDict = Dict[str, _FitDataList]


def _get_plot_data(config: Config) -> _PlotDataDict:
    """
    Gets data classified by sport
    """

    plot_dict: _PlotDataDict = {}

    fit: FitData
    for fit in fit_data_provider(config):
        if fit.vo2max is not None and fit.vo2max > 0:
            sport: str = f"{fit.sport}-{fit.sub_sport}" if config.GROUP_BY_SUBSPORT else f"{fit.sport}"

            if sport not in plot_dict:
                plot_dict[sport] = [fit]
            else:
                plot_dict[sport].append(fit)

    # In order not to mess-up the conecting lines between dots,
    # data must be sorted by time
    if not config.SCATTER:
        for data in plot_dict.values():
            data.sort(key=lambda d: datetime(2000, 1, 1) if d.start_time is None else d.start_time)

    return plot_dict


def _na(value: Union[_T, None], fmt: Optional[str] = None) -> Union[_T, str]:
    """
    Returns the value (with its optional format) if value is not None, otherwise "N/A"
    """

    if value is None:
        return "N/A"

    return value if fmt is None else "{val:{fmt}}".format(val=value, fmt=fmt)


def _na_date(value: Union[date, None], fmt: str = "%c") -> str:
    if value is None:
        return _na(value)

    return _na(value.strftime(fmt))


def plot(config: Config) -> None:
    """
    Plots the activities found in config.ACTIVITY_DIR
    """

    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title('VO2Max Tracker')

    if config.DPI:
        fig.set_dpi(config.DPI)

    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    do_plot: Callable[..., Any] = ax.scatter if config.SCATTER else ax.plot

    # Plot the data
    artist_dict: Dict[Any, _FitDataList] = {}
    for sport, data in _get_plot_data(config).items():
        dates: List[Optional[date]] = [d.start_time for d in data]
        vo2maxs: List[Optional[float]] = [d.vo2max for d in data]

        artist: Any = do_plot(dates, vo2maxs, label=sport, marker="8")

        artist_key: Any = artist if config.SCATTER else artist[0]
        artist_dict[artist_key] = data

    # Prepare tooltip information
    cursor: Cursor = mplcursors.cursor(artist_dict.keys(), hover=config.TOOLTIP_ON_HOVER)

    @cursor.connect("add")
    def on_add(sel: mplcursors.Selection) -> None:
        if sel.artist in artist_dict:
            data_index: int = round(sel.index)
            data = artist_dict[sel.artist][data_index]

            ann: text.Text = sel.annotation
            ann.set_bbox(dict(alpha=0.9))
            ann.set_fontweight('bold')

            ann.set_text(
                f"[{_na(data.sport)}-{_na(data.sub_sport)}]\n"
                "\n"
                f"VO2Max = {_na(data.vo2max, '.4f')}\n"
                f"Date = {_na_date(data.start_time)}\n"
                "\n"
                f"Duration = {_na(data.duration)}\n"
                f"Distance = {_na(data.distance)}\n"
                f"Calories = {_na(data.calories)}\n"
                "\n"
                f"Avg.HR = {_na(data.avg_heart_rate)}\n"
                f"Max.HR = {_na(data.max_heart_rate)}\n"
                "\n"
                f"Avg.PWR = {_na(data.avg_power)}\n"
                f"Max.PWR = {_na(data.max_power)}\n"
                f"Nor.PWR = {_na(data.nor_power)}\n"
                "\n"
                f"Aerobic TE = {_na(data.aerobic_te)}\n"
                f"Anaerobic TE = {_na(data.anaerobic_te)}\n"
                "\n"
                f"Avg.Temp. = {_na(data.avg_temperature)}\n"
                f"Max.Temp. = {_na(data.max_temperature)}")

    # Final configuration before showing the chart
    plt.xlabel("Date (yyyy-mm-dd)")
    plt.ylabel('VO2Max (mL/(kg·min))')
    plt.legend()
    plt.grid()
    plt.show()
