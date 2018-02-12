def file_reader(file: str) -> list:
    '''
    Takes the template html file and finds all of the variables and instructions for the templating engine. It then outputs these
    :param file:
    :return:
    '''
    foo = False
    baz = ""
    instructions = []

    for i in range(file.__len__()):
        if file[i] == "{" and file[i+1] == "{":
            # print("BINGO")
            foo = True
            baz = ""
        if file[i] == "}" and file[i+1] == "}":
            # print("BINGO OVER")
            foo = False
            baz = baz.replace("{{", "")
            instructions.append(baz)

        if foo:
            baz += file[i]

    return instructions


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
