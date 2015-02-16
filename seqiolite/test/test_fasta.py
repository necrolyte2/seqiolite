try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

import mock

from .. import fasta

DNA = 'ATGCN-atgcn'
RNA = 'UCAGN-utgcn'
DNA_FASTA = '>dna description\n' + DNA
RNA_FASTA = '>rna description\n' + RNA

class TestFastaRecord(unittest.TestCase):
    def setUp(self):
        self.dna = DNA
        self.rna = RNA
        self.dna_fasta = DNA_FASTA
        self.rna_fasta = RNA_FASTA

    def test_sets_id_and_seq_dna(self):
        r = fasta.FastaRecord('>foo', self.dna)
        self.assertEqual('foo', r.id)
        self.assertEqual('', r.description)
        self.assertEqual(self.dna, r.seq)
        
    def test_sets_id_and_seq_rna(self):
        r = fasta.FastaRecord('>foo', self.rna)
        self.assertEqual('foo', r.id)
        self.assertEqual('', r.description)
        self.assertEqual(self.rna, r.seq)

    def test_raises_invalid_sequence_data(self):
        r = fasta.FastaRecord('>foo', self.rna)
        self.assertRaises(
            fasta.InvalidFastaSequence,
            fasta.FastaRecord, 'foo', 'abcd'
        )

    def test_handles_sequence_multiple_lines(self):
        r = fasta.FastaRecord('>foo', self.dna + '\n' + self.dna)
        self.assertEqual('foo', r.id)
        self.assertEqual('', r.description)
        self.assertEqual(self.dna * 2, r.seq)

    def test_parses_description(self):
        r = fasta.FastaRecord('>foo\tbar\tbaz', self.dna)
        self.assertEqual(self.dna, r.seq)
        self.assertEqual('foo', r.id)
        self.assertEqual('bar\tbaz', r.description)

class TestFastaIsFasta(unittest.TestCase):
    def setUp(self):
        self.dna = DNA
        self.rna = RNA
        self.dna_fasta = DNA_FASTA
        self.rna_fasta = RNA_FASTA

    def test_is_fasta_detects_fasta_from_path(self):
        with mock.patch.object(builtins, 'open') as mock_open:
            mock_open.return_value.readline.side_effect = \
                self.dna_fasta.splitlines()
            r = fasta.FastaFile.is_fasta('/path/to/foo.fasta')
            self.assertTrue(r, 'Did not detect fasta file')
            mock_open.assert_called_once_with('/path/to/foo.fasta')
            mock_open.return_value.close.assert_called_once_with()

    def test_is_fasta_detects_fasta_from_handle(self):
        handle = mock.MagicMock()
        handle.readline.side_effect = self.dna_fasta.splitlines()[0]
        handle.tell.return_value = 0
        r = fasta.FastaFile.is_fasta(handle)
        self.assertTrue(r, 'Did not detect fasta file')
        handle.seek.assert_called_once_with(0)

class TestFastaFileParse(unittest.TestCase):
    def setUp(self):
        self.dna = DNA
        self.rna = RNA
        self.dna_fasta = DNA_FASTA + '\n'
        self.rna_fasta = RNA_FASTA + '\n'

    def _check_fasta_records(self, records):
            count = 0
            recs = []
            for rec in records:
                recs.append(rec)
                count += 1
                self.assertEqual('dna', rec.id)
                self.assertEqual(self.dna, rec.seq)
            print(recs)
            self.assertEqual(2, count)

    def test_yields_fastarecord_objects_for_path(self):
        fastacontents = self.dna_fasta * 2
        with mock.patch.object(builtins, 'open') as mock_open:
            mock_open.return_value.readline.side_effect = fastacontents.splitlines()
            mock_open.return_value.__iter__.return_value = iter(fastacontents.splitlines())
            r = fasta.FastaFile('/path/to/foo.fasta')
            self._check_fasta_records(r)

    def test_yields_fastarecord_objects_for_handle(self):
        fastacontents = self.dna_fasta * 2
        handle = mock.MagicMock()
        handle.tell.return_value = 0
        handle.readline.side_effect = fastacontents.splitlines()
        handle.__iter__.return_value = iter(fastacontents.splitlines())
        r = fasta.FastaFile(handle)
        self._check_fasta_records(r)

    def test_raises_invalidfasta_exception(self):
        fastacontents = '@id\nATGC\n+\n!!!!'
        handle = mock.MagicMock()
        handle.return_value.readline.side_effect = fastacontents.splitlines()
        handle.__iter__.return_value = iter(fastacontents.splitlines())
        self.assertRaises(
            fasta.InvalidFastaFile,
            fasta.FastaFile, handle
        )
