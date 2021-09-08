from .state import State


class ParseResultsState(State):
    """
    The state which is used to parse the results
    """

    def __init__(self, results):
        self.result = self.__parse(results)

    def __parse(self, results):
        if isinstance(results, bytes):
            results = results.decode("utf-8").strip()
        return results

    def on_event(self):
        return self.result
