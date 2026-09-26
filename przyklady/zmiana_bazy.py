"""Demonstrate a change of coordinates between two bases of R^2.

Run with ``python3 przyklady/zmiana_bazy.py``. The script prints the
coordinate calculations and writes an SVG illustration to the current
directory (or to the path supplied with ``--output``).
"""

import argparse
from fractions import Fraction
from pathlib import Path
from typing import TypeAlias


Vector2: TypeAlias = tuple[Fraction, Fraction]
Matrix2: TypeAlias = tuple[Vector2, Vector2]

BASIS_CHANGE: Matrix2 = (
    (Fraction(2), Fraction(1)),
    (Fraction(1), Fraction(2)),
)
NEW_COORDINATES: Vector2 = (Fraction(2), Fraction(1))


def matrix_vector_product(matrix: Matrix2, vector: Vector2) -> Vector2:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def inverse_2x2(matrix: Matrix2) -> Matrix2:
    a, b = matrix[0]
    c, d = matrix[1]
    determinant = a * d - b * c
    if determinant == 0:
        raise ValueError("Wektory nowej bazy muszą być liniowo niezależne.")
    return (
        (d / determinant, -b / determinant),
        (-c / determinant, a / determinant),
    )


def format_number(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def format_vector(vector: Vector2) -> str:
    return f"({format_number(vector[0])}, {format_number(vector[1])})"


def format_matrix(matrix: Matrix2) -> str:
    return "\n".join(
        f"    [{format_number(row[0]):>3}, {format_number(row[1]):>3}]"
        for row in matrix
    )


def make_svg(old_coordinates: Vector2, new_coordinates: Vector2) -> str:
    width, height = 900, 640
    origin_x, origin_y, scale = 100, 520, 55

    def point(x: Fraction | int, y: Fraction | int) -> tuple[float, float]:
        return origin_x + float(x) * scale, origin_y - float(y) * scale

    def line(
        start: tuple[Fraction | int, Fraction | int],
        end: tuple[Fraction | int, Fraction | int],
        color: str,
        stroke_width: int = 2,
        dash: str = "",
        arrow: bool = False,
        opacity: float = 1,
    ) -> str:
        x1, y1 = point(*start)
        x2, y2 = point(*end)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        marker_attr = ' marker-end="url(#arrow)"' if arrow else ""
        return (
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
            f'y2="{y2:.1f}" stroke="{color}" stroke-width="{stroke_width}"'
            f' opacity="{opacity}"{dash_attr}{marker_attr}/>'
        )

    def label(
        x: Fraction | int,
        y: Fraction | int,
        text: str,
        color: str,
        dx: int = 9,
        dy: int = -10,
    ) -> str:
        px, py = point(x, y)
        return (
            f'<text x="{px + dx:.1f}" y="{py + dy:.1f}" fill="{color}" '
            f'font-family="sans-serif" font-size="15" font-weight="600">'
            f'{text}</text>'
        )

    old_e1 = (Fraction(1), Fraction(0))
    old_e2 = (Fraction(0), Fraction(1))
    new_e1 = (BASIS_CHANGE[0][0], BASIS_CHANGE[1][0])
    new_e2 = (BASIS_CHANGE[0][1], BASIS_CHANGE[1][1])
    vector = (
        old_coordinates[0],
        old_coordinates[1],
    )
    twice_new_e1 = (
        NEW_COORDINATES[0] * new_e1[0],
        NEW_COORDINATES[0] * new_e1[1],
    )
    old_color = "#1769aa"
    new_e1_color = "#8e44ad"
    new_e2_color = "#d97706"
    vector_color = "#202124"

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        "<defs><marker id=\"arrow\" markerWidth=\"10\" markerHeight=\"10\" "
        "refX=\"8\" refY=\"5\" orient=\"auto\" markerUnits=\"strokeWidth\">"
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/>'
        "</marker></defs>",
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="24" y="34" font-family="sans-serif" font-size="21" '
        'font-weight="600">'
        "Ten sam wektor w dwóch bazach</text>",
        '<text x="24" y="61" font-family="sans-serif" font-size="15" '
        'fill="#555">'
        "Wszystkie strzałki są narysowane w tej samej płaszczyźnie."
        "</text>",
    ]

    for x in range(-1, 8):
        elements.append(line((x, -1), (x, 7), "#e7e7e7", 1))
    for y in range(-1, 8):
        elements.append(line((-1, y), (7, y), "#e7e7e7", 1))

    elements.extend(
        [
            line((-1, 0), (7, 0), "#555555", 2, arrow=True),
            line((0, -1), (0, 7), "#555555", 2, arrow=True),
            line((0, 0), old_e1, old_color, 4, arrow=True),
            line((0, 0), old_e2, old_color, 4, arrow=True),
            line((0, 0), new_e1, new_e1_color, 4, arrow=True),
            line((0, 0), new_e2, new_e2_color, 4, arrow=True),
            line((0, 0), twice_new_e1, new_e1_color, 2, "6 5", opacity=0.6),
            line(
                twice_new_e1,
                vector,
                new_e2_color,
                2,
                "6 5",
                opacity=0.6,
            ),
            line((0, 0), vector, vector_color, 5, arrow=True),
            label(*old_e1, "e1", old_color, dx=7, dy=21),
            label(*old_e2, "e2", old_color, dx=-24, dy=-9),
            label(*new_e1, "e1' = (2, 1)", new_e1_color, dx=10, dy=18),
            label(*new_e2, "e2' = (1, 2)", new_e2_color, dx=10, dy=-12),
            label(*vector, "v = (5, 4)", vector_color, dx=10, dy=-10),
            '<text x="540" y="125" font-family="sans-serif" font-size="17" '
            'font-weight="600">Baza stara B1</text>',
            f'<line x1="540" y1="151" x2="574" y2="151" '
            f'stroke="{old_color}" stroke-width="4" marker-end="url(#arrow)"/>',
            f'<text x="586" y="156" font-family="sans-serif" font-size="15" '
            f'fill="{old_color}">e1 = (1, 0)</text>',
            f'<line x1="540" y1="181" x2="574" y2="181" '
            f'stroke="{old_color}" stroke-width="4" marker-end="url(#arrow)"/>',
            f'<text x="586" y="186" font-family="sans-serif" font-size="15" '
            f'fill="{old_color}">e2 = (0, 1)</text>',
            '<text x="540" y="232" font-family="sans-serif" font-size="17" '
            'font-weight="600">Baza nowa B2</text>',
            f'<line x1="540" y1="258" x2="574" y2="258" '
            f'stroke="{new_e1_color}" stroke-width="4" marker-end="url(#arrow)"/>',
            f'<text x="586" y="263" font-family="sans-serif" font-size="15" '
            f'fill="{new_e1_color}">e1\' = (2, 1)</text>',
            f'<line x1="540" y1="288" x2="574" y2="288" '
            f'stroke="{new_e2_color}" stroke-width="4" marker-end="url(#arrow)"/>',
            f'<text x="586" y="293" font-family="sans-serif" font-size="15" '
            f'fill="{new_e2_color}">e2\' = (1, 2)</text>',
            '<text x="540" y="339" font-family="sans-serif" font-size="17" '
            'font-weight="600">Ten sam wektor</text>',
            f'<line x1="540" y1="365" x2="574" y2="365" '
            f'stroke="{vector_color}" stroke-width="5" marker-end="url(#arrow)"/>',
            f'<text x="586" y="370" font-family="sans-serif" font-size="15" '
            f'fill="{vector_color}">v = (5, 4)</text>',
            '<line x1="540" y1="402" x2="574" y2="402" '
            'stroke="#777" stroke-width="2" stroke-dasharray="6 5"/>',
            '<text x="586" y="407" font-family="sans-serif" font-size="14" '
            'fill="#555">składniki 2e1\' + e2\'</text>',
            '<text x="24" y="590" font-family="sans-serif" font-size="16">'
            f'[v]_B1 = {format_vector(old_coordinates)}'
            f'     [v]_B2 = {format_vector(new_coordinates)}'
            "     (v = 2e1' + e2')"
            "</text>",
            "</svg>",
        ]
    )
    return "\n".join(elements)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pokazuje współrzędne tego samego wektora w dwóch bazach R^2."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("zmiana_bazy.svg"),
        help="plik SVG z rysunkiem (domyślnie: zmiana_bazy.svg)",
    )
    args = parser.parse_args()

    old_coordinates = matrix_vector_product(BASIS_CHANGE, NEW_COORDINATES)
    inverse = inverse_2x2(BASIS_CHANGE)
    recovered_new_coordinates = matrix_vector_product(inverse, old_coordinates)
    determinant = (
        BASIS_CHANGE[0][0] * BASIS_CHANGE[1][1]
        - BASIS_CHANGE[0][1] * BASIS_CHANGE[1][0]
    )

    print("Stara baza B1: e1 = (1, 0), e2 = (0, 1)")
    print("Nowa baza B2: e1' = (2, 1), e2' = (1, 2)")
    print("\nMacierz przejścia P (kolumny to wektory nowej bazy w B1):")
    print(format_matrix(BASIS_CHANGE))
    print(f"Wyznacznik P: {format_number(determinant)}")
    print(f"\nWspółrzędne wektora w nowej bazie: {format_vector(NEW_COORDINATES)}")
    print(
        "Współrzędne w starej bazie: "
        f"P [v]_B2 = {format_vector(old_coordinates)}"
    )
    print(
        "Sprawdzenie przez macierz odwrotną: "
        f"P^(-1) [v]_B1 = {format_vector(recovered_new_coordinates)}"
    )
    print(
        f"\nRysunek zapisany w pliku: {args.output.resolve()}"
    )

    args.output.write_text(
        make_svg(old_coordinates, recovered_new_coordinates),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
