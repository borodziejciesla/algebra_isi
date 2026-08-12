#!/usr/bin/env bash
set -euo pipefail

# Skript buduje pliki PDF z plików .tex w katalogach "teoria" i "zadania"
# i czyści pliki tymczasowe. Najpierw używa latexmk, a jeśli go brak,
# używa pdflatex jako zapas.

dirs=("teoria" "zadania")
cleanup_ext=(aux bbl blg brf idx lof lot toc out synctex.gz log fdb_latexmk fls nav snm vrb aux)

function cleanup_files() {
  local texfile="$1"
  local base="${texfile%.*}"
  for ext in "${cleanup_ext[@]}"; do
    rm -f "${base}.${ext}"
  done
}

if command -v latexmk >/dev/null 2>&1; then
  for d in "${dirs[@]}"; do
    [ -d "$d" ] || continue
    while IFS= read -r -d '' tex; do
      dir="$(dirname "$tex")"
      file="$(basename "$tex")"
      echo "Building (latexmk): $tex"
      (cd "$dir" && latexmk -pdf -interaction=nonstopmode -file-line-error -halt-on-error "$file")
      (cd "$dir" && latexmk -c -quiet "$file") || true
      cleanup_files "$tex"
    done < <(find "$d" -maxdepth 1 -type f -name '*.tex' -print0)
  done
else
  echo "latexmk not found — fallback na pdflatex."
  for d in "${dirs[@]}"; do
    [ -d "$d" ] || continue
    while IFS= read -r -d '' tex; do
      dir="$(dirname "$tex")"
      file="$(basename "$tex")"
      [ -e "$tex" ] || continue
      echo "Building (pdflatex): $tex"
      (cd "$dir" && pdflatex -interaction=nonstopmode -halt-on-error "$file" >/dev/null)
      (cd "$dir" && pdflatex -interaction=nonstopmode -halt-on-error "$file" >/dev/null)
      cleanup_files "$tex"
    done < <(find "$d" -maxdepth 1 -type f -name '*.tex' -print0)
  done
fi

echo "Gotowe: PDF-y z katalogów 'teoria' i 'zadania' zbudowane, pliki tymczasowe usunięte."
