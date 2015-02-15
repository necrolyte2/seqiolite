class SeqRecord(object):
    def seq(self):
        '''
        Returns sequence as string of text
        '''
        raise NotImplemented('Needs to be implemented')

    def id(self):
        '''
        Returns sequence identifier
        '''
        raise NotImplemented('Needs to be implemented')

    def description(self):
        '''
        Returns record description
        '''
        raise NotImplemented('Needs to be implemented')
