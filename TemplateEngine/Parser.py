"""
This file takes the template html file and finds all of the variables and instructions for the templating engine. It then outputs these
"""
def file_reader(file: str) -> list:
    '''
    This is an inbuilt docstring!
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