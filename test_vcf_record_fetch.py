import gzip
import pytest


from pathlib import Path
from typing import Generator
from vcf import Reader


class TestVcfRecordFetch:
    """Test PyVCF class"""

    def test_retrieve_existing_markers(self, vcf_reader: Reader):
        """Test retrieving a location that exists in the VCF"""
        chrom = "Chr1"  # contig exists in the VCF
        end = 1277227  # this range also exists
        start = end - 1
        ref_exp = "A"
        alt_exp = ["C"]
        records = vcf_reader.fetch(chrom, start, end)
        records_list = list(records)
        assert len(records_list) == 1

        record = records_list[0]

        assert record.CHROM == chrom
        assert record.start == start
        assert record.end == end
        assert record.REF == ref_exp
        assert record.ALT == alt_exp

    def test_retrieve_complete_missing_pos(self, vcf_reader: Reader):
        """Test retrieving a non existant location for a contig that does exist in the VCF

        Should return an empty iterator (no records)
        """
        chrom = "Chr1"  # contig exists in the VCF
        end = 100000  # this range does not have any records
        start = end - 1
        records = vcf_reader.fetch(chrom, start, end)
        records_list = list(records)
        with pytest.raises(StopIteration):
            next(records)
        assert len(records_list) == 0

    def test_retrieve_complete_missing_chrom_and_pos(self, vcf_reader: Reader):
        """Test retrieving a non existant location for a contig that does not exist in the VCF

        Should return an empty iterator (no records)
        """
        chrom = "Chr10"  # contig does not exist in the VCF
        end = 100000  # this range does not have any records
        start = end - 1
        records = vcf_reader.fetch(chrom, start, end)
        records_list = list(records)
        with pytest.raises(StopIteration):
            next(records)
        assert len(records_list) == 0


@pytest.fixture
def vcf_reader() -> Generator[Reader, None, None]:
    """Get me a vcf with some records"""

    vcf_file = Path("data", "test_complete.vcf.gz")
    with gzip.open(vcf_file, "rt") as f_vcf:
        yield Reader(f_vcf, compressed=False)
