class InvalidFastaSequence(Exception):
    '''
    Raised for invalid dna or rna fasta sequences
    '''
    pass

class Fasta(object):
    @staticmethod
    def is_fasta(handleish):
        '''
        Return if file path or handle is fasta
        '''

    def parse(self, handleish):
        '''
        Parse a given filehandle or file path and generate FastaRecords
        '''

class FastaRecord(object):
    DNA = set('ATGCN-atgcn')
    RNA = set('UCAGN-ucagn')
    VALID_SEQ = DNA | RNA

    def __init__(self, identifierline, sequence):
        '''
        Fasta record object

        :param str identifierline: Line beginning with >
        :param str sequence: Line[s] after identifierline
        '''
        self._id, self._description = self._parse_identifier(identifierline)
        self.seq = sequence

    def _parse_identifier(self, identifier):
        '''
        Parse identifier line into id and description
        Return (id, description)
        '''
        s = identifier.split(None, 1)
        if len(s) == 1:
            return (s[0], '')
        else:
            return (s[0], s[1])

    @property
    def id(self):
        '''
        Everything between > and first space character
        or end of line
        '''
        return self._id

    @property
    def description(self):
        '''
        Everything after first space character
        on id line all the way to end of line(May be None)
        '''
        return self._description

    @property
    def seq(self):
        '''
        Sequence data
        '''
        return self._sequence

    def _is_valid_seq(self, seq):
        s = set(seq)
        return s.issubset(self.VALID_SEQ)

    @seq.setter
    def seq(self, value):
        value = value.replace('\n','')
        if not self._is_valid_seq(value):
            raise InvalidFastaSequence("Sequence provided is not valid fasta sequence")
        self._sequence = value
