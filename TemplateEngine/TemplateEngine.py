import re

def file_reader(file: str) -> list:
    """
    Takes the template html file and finds all of the variables and instructions for the template engine.
    It then outputs these as a list to be parsed by the evaluate function.
    :param file:
    :return:
    """
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


def evaluate_instructions(instructions: list) -> list:
    """
    Will take the list of instructions and determine what those instructions mean by passing them to the instruction function.
    :return:
    """
    for i in instructions:
        instruction(i)


def instruction(i: str) -> list:
    """
    Will take an instruction as input, work out what that instruction is, and output a list for the Execute Function to read.
    :param i:
    :return:
    """



    instruction_regex = [r'^FOR [(][a-zA-Z]+ in [a-zA-Z]+[)]:$', #For Statement
                         r'^RANGE [(][a-zA-Z0-9]+, [a-zA-Z0-9]+[)]$', #Range (int x, int y)
                         r'^WHILE [(][a-zA-z]+[)]:S', #While Statement (While condition is true do x)
                         r'^WHILE [(][a-zA-Z]+ ([=<>]|(>=)|(<=)|(!=)) [a-zA-Z]+[)]:$', #While statement (while var test var is true do x)
                         r'^[a-zA-Z]+ ([=<>]|(>=)|(<=)|(!=)) [a-zA-Z]+$', #Condtional statement
                         r'^[0-9]+$', #Matches any number
                         r'^[a-zA-Z_]+$', #Detects variable names
                         r'^ENDFOR$', #Detects the end of a for loop
                         r'^ENDWHILE$', #Detects end of while loop
                         r'^ENDIF', #Detects end of if statement
                         r'^ENDELIF$', #Detetcs end of elif statement
                         r'^ENDELSE$', #detects end of else statement
                         r'^[=<>]|(>=)|(<=)|(!=)$', #Detects conditional operator signs --Might not need
                         r'',
                         ]


    for x in range(instruction_regex.__len__()):
        r = instruction_regex[x]
        match = re.search(r, i)
        if match:
            print(match)
            break


def parse_html(template: str, variables: dict) -> str:
    """
    This function takes a template html file and returns a html file populated with variables and other information.
    :param html:
    :param variables:
    :return:
    """
    instructions = file_reader(template)
    print(instructions)


# parse_html("<h1>{{var1}}</h1><h1>{{var2}}</h1><h1>{{var3}}</h1>", {})
instruction("FOR (a in b):")