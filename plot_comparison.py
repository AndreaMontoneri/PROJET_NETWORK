import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D

# ── INDICES DES LIENS ENTRANTS PAR PORTE ───────────────────────────────────────
# On extrait les indices (position dans df_link) des liens dont end_node == porte
idx_doors = [74, 429, 445]
door_names = ["Porte 1 (74)", "Porte 2 (429)", "Porte 3 (445)"]

DOOR_LINKS = {
    name: df_link.index[df_link["end_node"] == door_id].tolist()
    for name, door_id in zip(door_names, idx_doors)
}

# ── DONNÉES PAR DISTRIBUTION ───────────────────────────────────────────────────
scenarios = {
    "Even": {
        "ue": {"x_star": x_star_ue,      "gap": gap_ue,      "obj": obj_ue},
        "so": {"x_star": x_star_so,      "gap": gap_so,      "obj": obj_so},
    },
    "Random": {
        "ue": {"x_star": x_star_ue_rand, "gap": gap_ue_rand, "obj": obj_ue_rand},
        "so": {"x_star": x_star_so_rand, "gap": gap_so_rand, "obj": obj_so_rand},
    },
    "Closest": {
        "ue": {"x_star": x_star_ue_clos, "gap": gap_ue_clos, "obj": obj_ue_clos},
        "so": {"x_star": x_star_so_clos, "gap": gap_so_clos, "obj": obj_so_clos},
    },
}

# ── PALETTE ────────────────────────────────────────────────────────────────────
COLORS = {
    "Even":    {"ue": "#2196F3", "so": "#0D47A1"},
    "Random":  {"ue": "#FF7043", "so": "#BF360C"},
    "Closest": {"ue": "#43A047", "so": "#1B5E20"},
}
LINE_STYLE = {"ue": "-",  "so": "--"}
MARKERS    = {"ue": "o",  "so": "s"}

# ── HELPER : flux total par porte ──────────────────────────────────────────────
def flux_par_porte(x_star):
    return [np.sum(x_star[idx]) for idx in DOOR_LINKS.values()]

# ── FIGURE ─────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 13))
fig.suptitle("Comparaison UE vs SO — Even / Random / Closest",
             fontsize=15, fontweight="bold", y=0.98)

gs      = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.32)
ax_gap  = fig.add_subplot(gs[0, 0])
ax_obj  = fig.add_subplot(gs[0, 1])
ax_flux = fig.add_subplot(gs[1, :])

# ── 1. CONVERGENCE ─────────────────────────────────────────────────────────────
for dist, data in scenarios.items():
    for method in ("ue", "so"):
        gap   = data[method]["gap"]
        iters = np.arange(1, len(gap) + 1)
        ax_gap.plot(
            iters, gap,
            color=COLORS[dist][method],
            linestyle=LINE_STYLE[method],
            marker=MARKERS[method], markersize=3,
            markevery=max(1, len(gap) // 10),
            label=f"{dist} – {'UE' if method == 'ue' else 'SO'}",
        )

ax_gap.set_title("Convergence (gap relatif)", fontweight="bold")
ax_gap.set_xlabel("Itération")
ax_gap.set_ylabel("Gap relatif")
ax_gap.set_yscale("log")
ax_gap.legend(fontsize=7, ncol=2, loc="upper right")
ax_gap.grid(True, which="both", linestyle=":", alpha=0.5)

# ── 2. FONCTION OBJECTIF ───────────────────────────────────────────────────────
for dist, data in scenarios.items():
    for method in ("ue", "so"):
        obj   = data[method]["obj"]
        iters = np.arange(1, len(obj) + 1)
        ax_obj.plot(
            iters, obj,
            color=COLORS[dist][method],
            linestyle=LINE_STYLE[method],
            marker=MARKERS[method], markersize=3,
            markevery=max(1, len(obj) // 10),
            label=f"{dist} – {'UE' if method == 'ue' else 'SO'}",
        )

ax_obj.set_title("Fonction objectif", fontweight="bold")
ax_obj.set_xlabel("Itération")
ax_obj.set_ylabel("Valeur objectif")
ax_obj.legend(fontsize=7, ncol=2, loc="upper right")
ax_obj.grid(True, linestyle=":", alpha=0.5)

# ── 3. FLUX PAR SORTIE ─────────────────────────────────────────────────────────
door_labels = list(DOOR_LINKS.keys())
n_doors     = len(door_labels)
n_groups    = len(scenarios) * 2      # 3 distributions × 2 méthodes = 6 barres
bar_width   = 0.11
x_base      = np.arange(n_doors)

bar_idx = 0
for dist, data in scenarios.items():
    for method in ("ue", "so"):
        fluxes  = flux_par_porte(data[method]["x_star"])
        offsets = x_base + (bar_idx - n_groups / 2 + 0.5) * bar_width
        label   = f"{dist} – {'UE' if method == 'ue' else 'SO'}"

        bars = ax_flux.bar(
            offsets, fluxes,
            width=bar_width,
            color=COLORS[dist][method],
            label=label,
            edgecolor="white", linewidth=0.5,
            alpha=0.88,
        )
        for bar, val in zip(bars, fluxes):
            ax_flux.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{val:.1f}",
                ha="center", va="bottom", fontsize=6.5,
            )
        bar_idx += 1

ax_flux.set_title("Flux total par sortie", fontweight="bold")
ax_flux.set_xlabel("Sortie")
ax_flux.set_ylabel("Flux total (personnes)")
ax_flux.set_xticks(x_base)
ax_flux.set_xticklabels(door_labels)
ax_flux.legend(fontsize=8, ncol=3, loc="upper right")
ax_flux.grid(axis="y", linestyle=":", alpha=0.5)

# ── LÉGENDE COMMUNE (UE vs SO) ─────────────────────────────────────────────────
legend_style = [
    Line2D([0], [0], color="gray", linestyle="-",  marker="o", markersize=5, label="UE (trait plein / barre claire)"),
    Line2D([0], [0], color="gray", linestyle="--", marker="s", markersize=5, label="SO (trait pointillé / barre foncée)"),
]
fig.legend(handles=legend_style, loc="lower center", ncol=2, fontsize=9,
           bbox_to_anchor=(0.5, -0.01), frameon=True)

plt.savefig("comparison_ue_so.png", dpi=150, bbox_inches="tight")
plt.show()
print("Figure sauvegardée : comparison_ue_so.png")
