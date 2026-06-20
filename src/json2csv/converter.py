"""Módulo encargado de la conversión de formatos de archivo.

Cumple con las convenciones PEP257.
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List


def json_to_csv(json_path: Path, csv_path: Path) -> None:
    """Convierte un archivo JSON a formato CSV de manera segura.

    Args:
        json_path: Ruta del archivo JSON de origen.
        csv_path: Ruta del archivo CSV de destino.

    Raises:
        FileNotFoundError: Si el archivo de origen no existe.
        ValueError: Si el JSON está malformado o no es una lista válida.
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data: List[Dict[str, Any]] = json.load(f)

        if not isinstance(data, list):
            raise ValueError("El formato JSON raíz debe ser una lista de objetos.")

        if not data:
            raise ValueError("El archivo JSON está vacío.")

        # Obtener los encabezados a partir de las llaves del primer objeto
        headers = data[0].keys()

        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Archivo no encontrado: {json_path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido o malformado: {e.msg}") from e
