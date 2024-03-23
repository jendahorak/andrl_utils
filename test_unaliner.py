import unaliner
import pytest

def test_process_lines():
    lines = [">name1", "ATG", "CGT", ">name2", "GCT", "AGT"]
    expected = [">name1", "ATGCGT", ">name2", "GCTAGT"]
    result = unaliner.process_lines(lines)
    assert result == expected, f'Expected {expected}, but got {result}'