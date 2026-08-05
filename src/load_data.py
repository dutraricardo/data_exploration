"""Carrega a planilha DB_SIAPE_processado e gera um resumo descritivo."""

from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "DB_SIAPE_processado_20260729.xlsx"
REPORT_PATH = Path(__file__).resolve().parent.parent / "reports" / "summary.txt"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    return pd.read_excel(path)


def build_summary(df: pd.DataFrame) -> str:
    lines = []
    lines.append(f"Linhas: {df.shape[0]}")
    lines.append(f"Colunas: {df.shape[1]}")
    lines.append("")
    lines.append("Colunas disponiveis:")
    for col in df.columns:
        lines.append(f"  - {col} ({df[col].dtype})")
    lines.append("")

    numeric_df = df.select_dtypes(include="number")
    lines.append("Estatisticas descritivas (colunas numericas):")
    if numeric_df.empty:
        lines.append("  Nenhuma coluna numerica encontrada.")
    else:
        lines.append(numeric_df.describe().to_string())

    return "\n".join(lines)


def main() -> None:
    df = load_data()

    print("Colunas disponiveis:")
    for col in df.columns:
        print(f"  - {col} ({df[col].dtype})")

    summary = build_summary(df)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(summary, encoding="utf-8")
    print(f"\nResumo salvo em: {REPORT_PATH}")


if __name__ == "__main__":
    main()
