class RunnerResults(dict):
    """ Wraps the results of parsed module_runner output. The result may
    be used just like it is in Ansible:

    result['contacted']['server']['rc']

    or it can alternatively be used thusly:

    result.rc('server')

    """
    def __init__(self, results):
        self.update(results)

    def __getattr__(self, item):
        return lambda server=None: self.acquire(server, item)

    def acquire(self, server, item):

        # if no server is given and exactly one contacted server exists
        # return the value of said server directly
        if server is None and len(self['contacted']) == 1:
            server = next((k for k in self['contacted'].keys()), None)

        if server not in self['contacted']:
            raise KeyError("{} could not be contacted".format(server))

        if item not in self['contacted'].get(server, {}):
            raise AttributeError

        return self['contacted'][server][item]
