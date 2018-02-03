from Parser import *


def parse_html(template: str, variables: dict) -> str:
    """
    This function takes a template html file and returns a html file populated with variables and other information.
    :param html:
    :param variables:
    :return:
    """
    instructions = file_reader(template)
    print(instructions)

parse_html("<h1>{{var1}}</h1><h1>{{var2}}</h1><h1>{{var3}}</h1>", {})
