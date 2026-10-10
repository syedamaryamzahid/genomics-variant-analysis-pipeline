
#!/usr/bin/env python3
"""Summarize SNPs and INDELs in a simple VCF file."""

import argparse
from pathlib import Path


def summarize_vcf(vcf_path):
    counts = {
        "total": 0,
        "snps": 0,
        "indels": 0,
        "other": 0,
    }

    with open(vcf_path, "r", encoding="utf-8") as vcf:
        for line in vcf:
            if line.startswith("#"):
                continue

            fields = line.rstrip("\n").split("\t")

            if len(fields) < 8:
                raise ValueError("Invalid VCF record: fewer than 8 columns")

            ref = fields[3]
            alts = fields[4].split(",")

            counts["total"] += 1

            if all(len(ref) == 1 and len(alt) == 1
                   and alt in "ACGT" and ref in "ACGT"
                   for alt in alts):
                counts["snps"] += 1

            elif any(len(ref) != len(alt)
                     and alt != "."
                     and not alt.startswith("<")
                     for alt in alts):
                counts["indels"] += 1

            else:
                counts["other"] += 1

    return counts


def main():
    parser = argparse.ArgumentParser(
        description="Summarize genomic variants in a VCF file."
    )
    parser.add_argument("vcf", type=Path, help="Input VCF file")
    args = parser.parse_args()

    counts = summarize_vcf(args.vcf)

    print(f"Total variant records: {counts['total']}")
    print(f"SNP records: {counts['snps']}")
    print(f"INDEL records: {counts['indels']}")
    print(f"Other records: {counts['other']}")


if __name__ == "__main__":
    main()
