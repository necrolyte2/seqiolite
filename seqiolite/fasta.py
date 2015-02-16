class InvalidFastaSequence(Exception):
    '''
    Raised for invalid dna or rna fasta sequences
    '''
    pass

class InvalidFastaFile(Exception):
    '''
    Raised for files that are not fasta formatted
    '''
    pass

class FastaFile(object):
    def __init__(self, handleish):
        if not FastaFile.is_fasta(handleish):
            raise InvalidFastaFile('Not a fasta formatted file')
        if hasattr(handleish, 'tell'):
            self.handleish = handleish
            self.close = True
        else:
            self.handleish = open(handleish)
            self.close = True

    @staticmethod
    def is_fasta(handleish):
        '''
        Return if file path or handle is fasta
        '''
        if hasattr(handleish, 'tell'):
            # Get current file posision so we can reset later
            curpos = handleish.tell()
            handle = handleish
            close = False
        else:
            handle = open(handleish)
            curpos = 0
            close = True
        try:
            firstline = handle.readline()
            is_fasta = firstline.lstrip()[0] == '>'
            handle.seek(curpos)
            return is_fasta
        finally:
            if close:
                handle.close()

    def __iter__(self):
        idline = None
        seq = []
        for line in self.handleish:
            if line.startswith('>'):
                if idline:
                    # Found another idline so yield record
                    yield FastaRecord(idline, ''.join(seq))
                # Reset
                seq = []
                idline = line.strip()
            else:
                seq.append(line.strip())
        yield FastaRecord(idline, ''.join(seq))

class FastaRecord(object):
    '''
    FastaRecord contains data related to a fasta record
    '''
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
            _id = s[0][1:]
            _desc = ''
        else:
            _id = s[0][1:]
            _desc = s[1]
        return (_id, _desc)

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
