=====
Fasta
=====

Fasta sequence file reading


FastaFile
=========

Reads fasta formatted files and returns FastaRecords

.. code-block:: python

    >>> from seqiolite import fasta
    >>> records = fasta.FastaFile('/path/to/my.fasta')
    >>> for rec in records:
    ...   print rec.id
    ...   print rec.seq

FastaRecord
===========

A FastaRecord represents a single fasta record.

It contains the identifier, sequence and description if there was a description

Here you can see an example of how to create a fasta record

.. code-block:: python

    >>> from seqiolite import fasta
    >>> example = fasta.FastaRecord('>identifier description', 'ATGC')
    >>> print example.id
    identifier
    >>> print example.description
    description
    >>> print example.seq
    ATGC
