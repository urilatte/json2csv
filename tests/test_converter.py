"""Pruebas unitarias para el conversor json2csv."""

import json
from pathlib import Path

import pytest

from json2csv.converter import json_to_csv


def test_conversion_exitosa(tmp_path: Path) -> None:
    """Prueba que un JSON válido se convierta correctamente a CSV."""
    json_file = tmp_path / "test.json"
    csv_file = tmp_path / "test.csv"

    datos = [{"nombre": "Juan", "edad": 30}, {"nombre": "Ana", "edad": 25}]
    json_file.write_text(json.dumps(datos), encoding="utf-8")

    json_to_csv(json_file, csv_file)

    assert csv_file.exists()
    lineas = csv_file.read_text(encoding="utf-8").splitlines()
    assert lineas[0] == "nombre,edad"
    assert lineas[1] == "Juan,30"


def test_archivo_no_encontrado() -> None:
    """Prueba el control de excepción ante un archivo inexistente."""
    with pytest.raises(FileNotFoundError):
        json_to_csv(Path("no_existe.json"), Path("salida.csv"))


def test_json_malformado(tmp_path: Path) -> None:
    """Prueba el control de excepción ante un JSON corrupto."""
    json_file = tmp_path / "corrupto.json"
    json_file.write_text("{malformado:", encoding="utf-8")

    with pytest.raises(ValueError, match="JSON inválido"):
        json_to_csv(json_file, tmp_path / "salida.csv")
