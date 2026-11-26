"""
compute.py - YOUR calculations. This is the file you edit for each project.

Run it through the VSCode build button (it runs before LaTeX), or by hand:
    .venv\\Scripts\\python.exe python\\compute.py   (from the project root)

Pattern:  1. INPUTS   2. CALCULATION   3. EXPORT to generated/ for LaTeX.
The example below is a toy model (damped acoustic oscillations); replace it
with your own physics, keeping the export calls.
"""
import numpy as np

from latexio import (fmt, new_figure, save_figure, set_plot_style,
                     write_macros, write_table)

# --------------------------------------------------------------------------
# 1. INPUTS - change these and rebuild: table, numbers and plot all follow.
# --------------------------------------------------------------------------
INPUTS = dict(
    amplitude=5.0e3,      # [muK^2]
    ell_acoustic=300.0,   # acoustic scale
    ell_damping=1200.0,   # damping scale
    ell_max=2000,
)

# --------------------------------------------------------------------------
# 2. CALCULATION (toy model)
# --------------------------------------------------------------------------
ell = np.arange(2, INPUTS["ell_max"] + 1)
spectrum = (INPUTS["amplitude"]
            * np.exp(-(ell / INPUTS["ell_damping"]) ** 2)
            * np.cos(np.pi * ell / INPUTS["ell_acoustic"]) ** 2)

# locate the peaks numerically: maximum inside a window around k * ell_acoustic
peaks = []
k = 1
while k * INPUTS["ell_acoustic"] <= INPUTS["ell_max"]:
    centre = k * INPUTS["ell_acoustic"]
    window = np.abs(ell - centre) <= INPUTS["ell_acoustic"] / 2
    i = np.argmax(np.where(window, spectrum, -np.inf))
    peaks.append((k, int(ell[i]), float(spectrum[i])))
    k += 1

# --------------------------------------------------------------------------
# 3. EXPORT TO LATEX
# --------------------------------------------------------------------------
# 3a. a table  ->  \input{latex/generated/table_peaks.tex}
write_table(
    "table_peaks.tex",
    header=["Peak", r"$\ell_{\rm peak}$", r"Height [$\mu$K$^2$]"],
    rows=[[kk, ll, hh] for kk, ll, hh in peaks[:4]],
)

# 3b. numbers for the running text  ->  \ellA, \ellD, \Npeaks, \Hone
#     (macro names: letters only!)
write_macros(dict(
    ellA=INPUTS["ell_acoustic"],
    ellD=INPUTS["ell_damping"],
    Npeaks=len(peaks),
    Hone=peaks[0][2],
))

# 3c. a plot  ->  \includegraphics{latex/generated/fig_spectrum.pdf}
font = set_plot_style()                      # "auto": follows main.tex
fig, ax = new_figure("column", aspect=0.72)  # exactly one column wide
ax.plot(ell, spectrum, color="C0")
ax.plot([p[1] for p in peaks], [p[2] for p in peaks], "o", ms=3, color="C3")
ax.set_xlabel(r"$\ell$")
ax.set_ylabel(r"$\ell(\ell+1)C_\ell/2\pi\ \ [\mu\mathrm{K}^2]$")
ax.set_xlim(0, INPUTS["ell_max"])
save_figure(fig, "fig_spectrum")

print(f"compute.py done: {len(peaks)} peaks, plot font = {font}")
