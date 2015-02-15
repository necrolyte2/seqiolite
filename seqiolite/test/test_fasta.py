try:
    import unittest2 as unittest
except ImportError:
    import unittest

import mock

from .. import fasta

class TestFastaRecord(unittest.TestCase):
    def setUp(self):
        self.dna = 'ATGCN-atgcn'
        self.rna = 'UCAGN-atgcn'
        self.dna_fasta = '>dna description\n' + self.dna
        self.rna_fasta = '>rna description\n' + self.rna

    def test_sets_id_and_seq_dna(self):
        r = fasta.FastaRecord('foo', self.dna)
        self.assertEqual('foo', r.id)
        self.assertEqual('', r.description)
        self.assertEqual(self.dna, r.seq)
        
    def test_sets_id_and_seq_rna(self):
        r = fasta.FastaRecord('foo', self.rna)
        self.assertEqual('foo', r.id)
        self.assertEqual('', r.description)
        self.assertEqual(self.rna, r.seq)

    def test_raises_invalid_sequence_data(self):
        r = fasta.FastaRecord('foo', self.rna)
        self.assertRaises(
            fasta.InvalidFastaSequence,
            fasta.FastaRecord, 'foo', 'abcd'
        )

    def test_handles_sequence_multiple_lines(self):
        r = fasta.FastaRecord('foo', self.dna + '\n' + self.dna)
        self.assertEqual('foo', r.id)
        self.assertEqual('', r.description)
        self.assertEqual(self.dna * 2, r.seq)

    def test_parses_description(self):
        r = fasta.FastaRecord('foo\tbar\tbaz', self.dna)
        self.assertEqual(self.dna, r.seq)
        self.assertEqual('foo', r.id)
        self.assertEqual('bar\tbaz', r.description)
