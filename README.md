# Algebra z Geometrią Analityczną

Materiały do algebry liniowej: notatki teoretyczne, zestawy zadań i przykłady
obliczeń.

## Zawartość

### Teoria

Pliki źródłowe LaTeX (`.tex`) i odpowiadające im dokumenty PDF znajdują się
w katalogu [`teoria/`](./teoria/):

- [Czym jest \(e^{i}\)](./teoria/czym_jest_e_do_i.pdf)
- [Grupy i ciała](./teoria/grupy_i_ciala.pdf)
- [Postać Jordana](./teoria/postac_jordana.pdf)
- [Przykład wyznaczania postaci Jordana](./teoria/postac_jordana_przyklad.pdf)
- [Postać kanoniczna formy kwadratowej](./teoria/postac_kanniczna_formy_kwadratowej.pdf)
- [Zmiana bazy](./teoria/zmiana_bazy.pdf)

### Zadania

Zestawy zadań są dostępne w katalogu [`zadania/`](./zadania/):

- [Dekompozycja macierzy](./zadania/dekompozycja_macierzy.pdf)
- [Formy kwadratowe](./zadania/formy_kwadratowe.pdf)
- [Geometria analityczna](./zadania/geometria_analityczna.pdf)
- [Grupy i ciała](./zadania/grupy_i_ciala.pdf)
- [Liczby zespolone II](./zadania/liczby_zespolone_2.pdf)
- [Macierze II](./zadania/macierze_2.pdf)
- [Optymalne rozwiązania przybliżone](./zadania/optymalne_rozwiazania_przyblizone.pdf)
- [Przestrzenie wektorowe I](./zadania/przestrzenie_wektorowe_1.pdf)
- [Przestrzenie wektorowe II](./zadania/przestrzenie_wektorowe_2.pdf)
- [Przestrzenie wektorowe III](./zadania/przestrzenie_wektorowe_3.pdf)
- [Układy równań](./zadania/uklady_rownan.pdf)

### Przykłady

Notatniki Jupyter z przykładami znajdują się w katalogu
[`przyklady/`](./przyklady/).

## Budowanie dokumentów PDF

Źródłem dokumentów są pliki `.tex` w katalogach `teoria/` i `zadania/`.
Aby zbudować odpowiadające im pliki PDF lokalnie, uruchom z katalogu głównego
repozytorium:

```sh
./scripts/build_pdfs.sh
```

Skrypt używa `latexmk`, jeśli jest dostępny, a w przeciwnym razie `pdflatex`.
Po wypchnięciu zmian na gałąź `main` GitHub Actions uruchamia ten skrypt
i zapisuje wygenerowane pliki PDF w repozytorium.
