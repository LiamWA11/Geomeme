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
    boo = 0
    instructions = []

    for i in range(file.__len__()):
        if file[i] == "{" and file[i+1] == "{":
            # print("BINGO")
            foo = True
            baz = ""
            boo = i
        if file[i] == "}" and file[i+1] == "}":
            # print("BINGO OVER")
            foo = False
            baz = baz.replace("{{", "")
            instructions.append([baz, boo])

        if foo:
            baz += file[i]

    return instructions


def evaluate_instructions(instructions: list) -> list:
    """
    Will take the list of instructions and determine what those instructions mean by passing them to the instruction function.
    :return:
    """
    instructs = []
    for i in instructions:
        instructs.append(instruction(i[0]))

    return instructs


def instruction(i: str) -> list:
    """
    Will take an instruction as input, work out what that instruction is, and output a list for the Execute Function to read.
    :param i:
    :return:
    """

    matched_instruction = [] #Match object, regex string, regex string id

    instruction_regex = [r'^(FOR) [(]([a-zA-Z]+) in ([a-zA-Z]+)[)]:$',  #For Statement
                         r'^RANGE [(][a-zA-Z0-9]+, [a-zA-Z0-9]+[)]$',  #Range (int x, int y)
                         r'^WHILE [(][a-zA-z]+[)]:S',  #While Statement (While condition is true do x)
                         r'^WHILE [(][a-zA-Z]+ ([=<>]|(>=)|(<=)|(!=)) [a-zA-Z]+[)]:$',  #While statement (while var test var is true do x)
                         r'^[a-zA-Z]+ ([=<>]|(>=)|(<=)|(!=)) [a-zA-Z]+$',  #Condtional statement
                         r'^(ENDFOR)$',  #Detects the end of a for loop
                         r'^ENDWHILE$',  #Detects end of while loop
                         r'^ENDIF',  #Detects end of if statement
                         r'^ENDELIF$',  #Detetcs end of elif statement
                         r'^ENDELSE$',  #detects end of else statement
                         r'^[=<>]|(>=)|(<=)|(!=)$',  #Detects conditional operator signs --Might not need
                         r'^IF [(][a-zA-Z_]+ ([=<>]|(>=)|(<=)|(!=)) [a-zA-Z_]+[)]:$',  #Detects if statements
                         r'^ELSE IF [(][a-zA-Z_]+ ([=<>]|(>=)|(<=)|(!=)) [a-zA-Z_]+[)]:$',  #Detects else if statement
                         r'^ELSE:$',  #Detects else statement
                         r'^[a-zA-Z_]+[.][a-zA-Z_]+$', #Detect variable.variable
                         r'^[0-9]+$',  # Matches any number
                         r'^[a-zA-Z_]+$',  # Detects variable names
                         ]

    for x in range(instruction_regex.__len__()):
        r = instruction_regex[x]
        match = re.search(r, i)
        if match:
            matched_instruction.append(match)
            matched_instruction.append(r)
            matched_instruction.append(x)
            break

    return matched_instruction

def execute_instructions(html: str, instructions: list, matched_instructions: list, map: dict) -> str:
    formated_html = ""

    blocks = [] #[type, start match index, end match index]
    fcount = 0 #For loop counter - required for nested for loops

    b = []

    for x in range(matched_instructions.__len__()):
        m = matched_instructions[x][0]
        print("M" + str(m))
        print("m(0): " + str(m.group(0)))
        try:
            if m.group(1) == "FOR":
                fcount+=1
                print("For loop started")
                # print(m.group(1))
                # print(m.group(2))
                # print(m.group(3))
            elif m.group(1) == "ENDFOR":
                fcount-=1
                print("For loop ended")


        except IndexError:
            print("Group not found")

        if fcount > 0:
            print("This object is part of for loop " + str(fcount))
            if b.__len__() < fcount:
                print("b.len < fcount (b, b.len, fcount): " + str(b) + " " + str(b.__len__()) + " " + str(fcount))
                b.append([m])
                print("b.len < fcount (b, b.len, fcount): " + str(b) + " " + str(b.__len__()) + " " + str(fcount))
            else:
                print(str(b[fcount-1]))
                b[fcount-1].append(m)
            #print(b)

        if fcount == 0:
            blocks.append(b)

    print("\n\n\n")
    print(blocks)
    print("\n\n\n")
    print(blocks[0])
    print("\n\n\n")
    print(blocks[1])


def parse_html(template: str, variables: dict) -> str:
    """
    This function takes a template html file and returns a html file populated with variables and other information.
    :param template:
    :param variables:
    :return:
    """
    instructions = file_reader(template)
    matched_instructions = evaluate_instructions(instructions)
    print(instructions)
    print(matched_instructions)
    print("\n\n")
    execute_instructions("", instructions, matched_instructions, {})



parse_html("""<html>
    <h1>Users:</h1>
    {{FOR (USER in USERS):}}
    <h3>{{USER.NAME}}</h3>
    <h4>{{USER.DESCRIPTION}}</h4>
    {{FOR (PIC in PICTURES):}}
    <img src="cool picture">
    <h1>This is a cool picture made by {{USER.NAME}}</h1>
    {{ENDFOR}}
    {{ENDFOR}}
</html>""", {})
#instruction("FOR (a in b):")