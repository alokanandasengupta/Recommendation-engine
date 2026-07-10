"""
Split a large .xlsx workbook into N smaller workbooks.

Every output file keeps all the original sheets (tabs) and all columns,
but only a slice of the rows -- so the data is partitioned by rows only.

Usage:
    python split_xlsx.py input.xlsx --parts 5 --output-dir split_output
"""

import argparse
import os

import pandas as pd


def _row_chunks(df, parts):
    """Split a DataFrame into `parts` roughly equal, contiguous row chunks."""
    n = len(df)
    base, extra = divmod(n, parts)
    chunks = []
    start = 0
    for i in range(parts):
        size = base + (1 if i < extra else 0)
        chunks.append(df.iloc[start:start + size])
        start += size
    return chunks


def split_workbook(input_path, parts=5, output_dir="split_output", output_prefix=None):
    if output_prefix is None:
        output_prefix = os.path.splitext(os.path.basename(input_path))[0]

    os.makedirs(output_dir, exist_ok=True)

    sheets = pd.read_excel(input_path, sheet_name=None)

    # Split every sheet's rows into `parts` roughly equal chunks.
    sheet_chunks = {
        name: _row_chunks(df, parts)
        for name, df in sheets.items()
    }

    output_paths = []
    for i in range(parts):
        out_path = os.path.join(output_dir, f"{output_prefix}_part{i + 1}.xlsx")
        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            for sheet_name, chunks in sheet_chunks.items():
                chunks[i].to_excel(writer, sheet_name=sheet_name, index=False)
        output_paths.append(out_path)

    return output_paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="Path to the source .xlsx file")
    parser.add_argument("--parts", type=int, default=5, help="Number of output files (default: 5)")
    parser.add_argument("--output-dir", default="split_output", help="Directory for the output files")
    parser.add_argument("--output-prefix", default=None, help="Filename prefix for output files")
    args = parser.parse_args()

    output_paths = split_workbook(
        args.input_file,
        parts=args.parts,
        output_dir=args.output_dir,
        output_prefix=args.output_prefix,
    )

    print(f"Created {len(output_paths)} files in '{args.output_dir}':")
    for path in output_paths:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
