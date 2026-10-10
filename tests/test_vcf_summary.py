
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from vcf_summary import summarize_vcf


class TestVCFSummary(unittest.TestCase):

    def test_example_vcf(self):
        vcf_path = ROOT / "data" / "example.vcf"
        result = summarize_vcf(vcf_path)

        self.assertEqual(result["total"], 10)
        self.assertEqual(result["snps"], 5)
        self.assertEqual(result["indels"], 5)
        self.assertEqual(result["other"], 0)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            summarize_vcf(ROOT / "data" / "missing.vcf")


if __name__ == "__main__":
    unittest.main()
