class IncorrectParameters(Exception):
    '''Raised when the incorrect configuration of parameters is passed into a Class'''
    pass

class ParseResultsError(RuntimeWarning):
    '''Raised when innvocation returned an error from a remote machine/comamnd'''
    pass