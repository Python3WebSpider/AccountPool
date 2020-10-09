class InitException(Exception):
    def __str__(self):
        """
        init error
        :return:
        """
        return repr('init failed')
