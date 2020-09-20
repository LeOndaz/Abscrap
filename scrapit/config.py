class ScrapersGlobalConfig:
    @classmethod
    def get_global_conf(cls):
        """
        This should return the global config json file as a dict.
        """
        return {
            "headers": {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
            },
            "timeout": 15
        }

    @classmethod
    def get_headers_config(cls):
        """
        Return headers config from scrapers_conf.json or None
        """
        return cls.get_global_conf().get('headers')

    @classmethod
    def get_timeout_config(cls):
        """"""
        return cls.get_global_conf().get('timeout')
