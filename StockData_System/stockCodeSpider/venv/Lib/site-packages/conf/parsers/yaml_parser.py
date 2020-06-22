try:
    import yaml
except ImportError:
    pass


def parse(file_stream):
    """
    Parse the given file stream of yaml format to a dict.
    """
    if hasattr(yaml, 'FullLoader'):
        # pyyaml >= 5.1
        loaded = yaml.load(file_stream, Loader=yaml.FullLoader)
    else:
        loaded = yaml.load(file_stream)

    if loaded:
        return dict(loaded.items())
    return {}
