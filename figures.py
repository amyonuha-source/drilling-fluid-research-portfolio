"""Figures. Run from the repository root:  python -m src.figures"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from . import config as C
from .analyze import derived_properties
from .data import load_comparison

plt.rcParams.update({
    "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 11, "savefig.dpi": 200,
    "savefig.bbox": "tight", "axes.axisbelow": True,
})
FOOT = "Single batch of each mud, one test per property, no replicates. SIWES laboratory, FUTO Petroleum Engineering, September 2023."


def _save(fig, name):
    C.FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(C.FIG_DIR / name, facecolor="white")
    plt.close(fig)
    print("wrote", C.FIG_DIR / name)


def _grouped(ax, groups, series, ylabel, title, fmt="{:g}"):
    """groups: x-category labels; series: {label: (values, colour)}"""
    x = np.arange(len(groups))
    w = 0.8 / len(series)
    for i, (lab, (vals, col)) in enumerate(series.items()):
        pos = x + (i - (len(series) - 1) / 2) * w
        bars = ax.bar(pos, vals, w * 0.92, color=col, label=lab)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height(), fmt.format(v), ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(groups)
    ax.set_ylabel(ylabel); ax.set_title(title)
    ax.set_ylim(0, ax.get_ylim()[1] * 1.12)
    ax.grid(axis="y", color="#EEEEEE")


def fig_rheology():
    comp, d = load_comparison(), derived_properties()
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.8))
    ser = lambda getter: {C.LABELS[m]: (getter(m), C.COLOURS[m]) for m in C.MUDS}
    _grouped(axes[0], ["300 rpm", "600 rpm"],
             {C.LABELS[m]: ([comp.loc["dial_reading_300rpm", m], comp.loc["dial_reading_600rpm", m]], C.COLOURS[m]) for m in C.MUDS},
             "Viscometer dial reading", "A  Dial readings")
    _grouped(axes[1], ["Plastic viscosity (cP)", "Yield point (lb/100 ft$^2$)"],
             {C.LABELS[m]: ([d.loc["plastic_viscosity_cP", m], d.loc["yield_point_lb100ft2", m]], C.COLOURS[m]) for m in C.MUDS},
             "Calculated value", "B  PV and YP (PV = \u03b8600 \u2212 \u03b8300; YP = \u03b8300 \u2212 PV)")
    _grouped(axes[2], ["YP / PV", "Flow index n (two-point)"],
             {C.LABELS[m]: ([d.loc["yp_over_pv", m], d.loc["power_law_n_two_point", m]], C.COLOURS[m]) for m in C.MUDS},
             "Dimensionless", "C  Shape of the flow curve", fmt="{:.2f}")
    axes[0].legend(frameon=False, fontsize=9, loc="upper left")
    fig.suptitle("Rheology: the biodiesel mud is far more viscous (PV) but has a slightly lower yield point than the diesel mud",
                 fontsize=12, fontweight="bold")
    fig.text(0.5, -0.04, "A higher yield point relative to plastic viscosity (YP/PV) generally means better cuttings suspension at a given viscosity; n closer to 1 means flow closer to Newtonian.\n" + FOOT,
             ha="center", fontsize=8, color="#777")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    _save(fig, "fig1_rheology_profile.png")


def fig_gel_filtration():
    comp = load_comparison()
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.9), gridspec_kw={"width_ratios": [1.3, 1, 1]})

    # A: gels
    ax = axes[0]
    x = np.arange(2)
    for i, (lab, key, col) in enumerate((("10 s", "gel_strength_10sec", "#6A1B9A"), ("10 min", "gel_strength_10min", "#BA68C8"))):
        vals = [comp.loc[key, m] for m in C.MUDS]
        bars = ax.bar(x + (i - 0.5) * 0.38, vals, 0.35, color=col, label=f"{lab} gel")
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v, f"{v:g}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels([C.LABELS[m] for m in C.MUDS])
    ax.set_ylabel("Gel strength (lb/100 ft$^2$)")
    ax.set_title("A  Gel strength (recorded values)")
    ax.legend(frameon=False, fontsize=9, loc="center right")
    ax.set_ylim(0, 150)
    ax.text(0.5, 0.97, "\u26a0 10 s gel > 10 min gel in both muds,\nand gels exceed the 300 rpm dial: not a standard\n3 rpm gel measurement (see docs/data_quality_notes.md)",
            transform=ax.transAxes, ha="center", va="top", fontsize=8, color="#B71C1C",
            bbox=dict(boxstyle="round", facecolor="#FFEBEE", edgecolor="#E57373"))
    ax.grid(axis="y", color="#EEEEEE")

    # B, C: filtration
    for ax, key, ylabel, title, ymax in ((axes[1], "filtrate_volume", "Filtrate (mL)", "B  Filtrate volume", 14),
                                          (axes[2], "mud_cake_thickness", "Cake thickness (1/32 in)", "C  Filter-cake thickness", 10.5)):
        for i, m in enumerate(C.MUDS):
            v = comp.loc[key, m]
            if v > 0:
                ax.bar(i, v, 0.55, color=C.COLOURS[m])
                ax.text(i, v, f"{v:g}", ha="center", va="bottom", fontsize=9)
            else:
                ax.bar(i, ymax * 0.04, 0.55, color="none", edgecolor=C.COLOURS[m], hatch="///", linewidth=1.2)
                ax.text(i, ymax * 0.07, "none\nrecorded", ha="center", va="bottom", fontsize=9, color=C.COLOURS[m])
        ax.set_xticks([0, 1]); ax.set_xticklabels([C.LABELS[m] for m in C.MUDS])
        ax.set_ylabel(ylabel); ax.set_title(title); ax.set_ylim(0, ymax)
        ax.grid(axis="y", color="#EEEEEE")
    fig.suptitle("Gel strength and low-pressure filtration", fontsize=13, fontweight="bold")
    fig.text(0.5, -0.07, "Filtration test conditions (pressure, time, temperature) and the diesel mud recipe were not recorded. Oil-continuous muds normally give little or no filtrate at low pressure,\n"
             "so the diesel result mainly reflects fluid type. The informative result is the 10.8 mL from the biodiesel mud.  " + FOOT,
             ha="center", fontsize=8, color="#777")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    _save(fig, "fig2_gel_and_filtration.png")


def main():
    fig_rheology(); fig_gel_filtration()


if __name__ == "__main__":
    main()
