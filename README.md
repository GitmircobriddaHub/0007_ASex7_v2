# Paper template (LaTeX + Python + C++ + Git)

## Folder map
    main.tex            the ONLY LaTeX file in the root: build this one
    README.md           this file
    requirements.in     Python packages you ask for (loose; edit this)
    requirements.txt    exact versions installed (generated; do not edit)
    .gitignore          what git must not save
    .vscode/            editor settings (the build recipe)
    .venv/              Python environment (created by you, not in git)
    build/              LaTeX output: PDF, aux, log ... (not in git)

    latex/              everything LaTeX except main.tex
      header.tex          packages and custom commands
      references.bib      bibliography
      chapters/           sections in their own files (.tex)
      figures/            figures you make by hand (.pdf, .png)
      generated/          WRITTEN BY PYTHON, read by LaTeX (committed to git)

    python/             .py files
      compute.py          your calculations (edit this)
      latexio.py          generic helpers (rarely edited)
      freeze_requirements.py  writes requirements.txt from the installed packages
    notebooks/          .ipynb files
    cpp/                C++ sources
    data/               input data
    ref/                reference papers (PDF) and notes

## Rule of thumb
* You write: `main.tex`, `latex/*`, `python/*`, `notebooks/*`, `cpp/*`.
* Programs write: `latex/generated/`, `build/`. Never edit those by hand.

## First-time setup (Windows, once per project/computer)
From the project root, in the VSCode terminal:

    py -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt

## Python packages and versions (two files on purpose)
* `requirements.in` = what you WANT: the direct dependencies, no version numbers.
* `requirements.txt` = what you HAVE: the exact version of every installed package.
  Setting up or rebuilding a project installs this file, so you always get the
  same versions: nothing changes behind your back.

To add a package:

    .venv\Scripts\python.exe -m pip install scipy
    (add the line  scipy  to requirements.in)
    .venv\Scripts\python.exe python\freeze_requirements.py

To update on purpose, run `rebuild_venvs.ps1 -Update` (it lives in the folder
above the projects); it upgrades the packages and rewrites requirements.txt.
`git diff requirements.txt` then shows exactly what changed, and `git checkout
requirements.txt` undoes it. For a submitted paper, never update: the pinned
requirements.txt is the record of what produced the results.
Note: the pins are for Windows + Python 3.14; on another system or Python
version some may not exist, so freeze again there.

## Everyday use
1. Edit `python/compute.py` and/or the `.tex` files.
2. Open the `main.tex` tab and build (Ctrl+Alt+B): runs `python/compute.py`,
   then latexmk (with biber). The PDF is `build/main.pdf`.
3. Snapshot and backup:

       git add .
       git commit -m "short note on what changed"
       git push

## Adding things
* **Number in the text**: `write_macros({"Hzero": 67.4})` in compute.py, then `$H_0=\Hzero$`.
* **Table**: `write_table("table_x.tex", header, rows)`, then
  `\input{latex/generated/table_x.tex}` inside a table float.
* **Plot**: `fig, ax = new_figure("column")` ... `save_figure(fig, "fig_x")`, then
  `\includegraphics[width=\columnwidth]{fig_x.pdf}` (\graphicspath finds it).
* **A new section file**: create `latex/chapters/name.tex`, put
  `% !TEX root = ../../main.tex` as its first line, and add
  `\input{latex/chapters/name}` in main.tex.
* **Another Python file**: put it in `python/`; `compute.py` can import it.
* **A notebook** in `notebooks/` that uses the helpers:

      import sys; sys.path.append("../python")
      from latexio import write_macros, write_table, new_figure, save_figure, set_plot_style

* **C++**: sources in `cpp/`; compile output (.exe, .o) is ignored by git.

## Switches at the top of main.tex
Layout (`\widetrue`/`\widefalse`) and fonts (`\timestrue`/`\timesfalse`) are
independent. `set_plot_style()` follows the font switch, so plots match the text.
If you change margins/column spacing in header.tex, update the two width
constants at the top of `python/latexio.py`.

## Starting a new paper from this template
On GitHub: Settings -> "Template repository". For each paper: **Use this template
-> Create a new repository** (private), clone it, create the `.venv`, edit, build.
