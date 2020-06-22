import configparser


def parse(file_stream):
    # Parse the given file stream of ini format to a dict.
    parser = configparser.ConfigParser()
    parser.read_file(file_stream)
    return {section: dict(parser[section].items())
            for section in parser.sections()}
