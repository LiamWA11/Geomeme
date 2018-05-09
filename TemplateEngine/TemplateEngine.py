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
                         r'^(\$\$)([a-zA-Z_]+)([.])([a-zA-Z_]+)$',  # Detect variable.variable - REPLACEMENT WORKING
                         r'^[0-9]+$',  # Matches any number
                         r'^(\$)([a-zA-Z_]+)$',  # Detects variable names - REPLACEMENT WORKING
                         ]

    for x in range(instruction_regex.__len__()):
        r = instruction_regex[x]
        match = re.search(r, i)
        if match:
            matched_instruction.append(match)
            matched_instruction.append(r)
            matched_instruction.append(x)
            matched_instruction.append(True)
            break

    return matched_instruction


def execute_instructions(html: str, instructions: list, matched_instructions: list, map: dict) -> str:
    formatted_html = html

    blocks = []  # [type, start match index, end match index]
    fcount = 0  # For loop counter - required for nested for loops

    b = []

    def exec_forloop(_m, _fh):
        print(_m.group(0))
        print(_m.group(1))
        print(_m.group(2))
        print(_m.group(3))

        try:
            _list = map[_m.group(3)]
            print(_list)
            for member in _list:
                print(member.NAME)
                _dum1 = _fh.find("{{"+_m.group(0)+"}}")
                _dum2 = _fh.find("{{ENDFOR}}") + 10
                _abc = _fh[_dum1+2+len(_m.group(0))+2:_dum2-10]
                _abd = _abc.replace(_m.group(1), member.__dict__[_m.group(2)])
                print(_abc)
                # return _fh.replace(_fh[_dum1:_dum2], (_abd*len(_list)))
                # print("aba")
        except KeyError:
            print("Key is not in given dictionary")
        return _fh

    # Variable replacement ($var)
    def exec_var(_m, _fh):
        print("\nVariable Detected")
        print(_m.group(2))
        try:
            print(map[_m.group(2)])
            return _fh.replace("{{$"+_m.group(2)+"}}", map[_m.group(2)])
        except KeyError:
            return _fh.replace("{{$"+_m.group(2)+"}}", '"' + "KeyError: UNKNOWN VARIABLE - " + _m.group(2) + '"')

    # Class Variable Replacement ($$var.var)
    def exec_classvar(_m, _fh):
        print("\nClass Variable Detected")
        print(_m.group(2)+"."+_m.group(4))
        try:
            print(map[_m.group(2)])
            __foo = map[_m.group(2)]
            try:
                print(__foo.__dict__[(_m.group(4))])
                return _fh.replace("{{$$"+_m.group(2)+"."+_m.group(4)+"}}", __foo.__dict__[(_m.group(4))])
            except KeyError:
                print("Not a member of class " + _m.group(2))
                return _fh.replace("{{$$" + _m.group(2) + "." + _m.group(4) + "}}", "NO VAR '"+_m.group(4)+"' for class/key '"+_m.group(2)+"'")
        except KeyError:
            print("Not a variable/No class defined")
            pass

        return _fh

    for bar in range(matched_instructions.__len__()):
        m = matched_instructions[bar][0]
        print("\n"+"Match: " + str(m))
        print("m(0): '" + str(m.group(0)) +"'")
        try:
            if m.group(1) == "FOR":
                if matched_instructions[bar][3]:
                    fcount += 1
                    print("For loop started")
                else:
                    print("Executing for loop: \n")
                    formatted_html = exec_forloop(m, formatted_html)
                    print("\nFor loop executed")
                    break
                # print(m.group(1))
                # print(m.group(2))
                # print(m.group(3))
            elif m.group(1) == "ENDFOR":
                fcount-=1
                print("For loop ended")
            if m.group(1) == "$":
                if fcount == 0:
                    formatted_html = exec_var(m, formatted_html)
            if m.group(1) == "$$":
                if fcount == 0:
                    formatted_html = exec_classvar(m, formatted_html)
            elif m.group(1) == "":
                pass

        except IndexError:
            print("Group not found")

        # For Loop Logic
        if fcount > 0:
            print("This object is part of for loop " + str(fcount))
            if b.__len__() < fcount:
                # print("b.len < fcount (b, b.len, fcount): " + str(b) + " " + str(b.__len__()) + " " + str(fcount))
                b.append([[m, "a", 1, False]])
                # print("b.len < fcount (b, b.len, fcount): " + str(b) + " " + str(b.__len__()) + " " + str(fcount))
            else:
                # print(str(b[fcount-1]))
                b[fcount-1].append([m, "a", 1, True])
                # print(str(b[fcount-1]))
            # print(b)

        if fcount == 0:
            blocks.append(b)

    try:
        formatted_html = execute_instructions(formatted_html, instructions, blocks[0][0], map)
    except IndexError:
        print("No for loops found")

    print("\n")
    # print(blocks)
    # print("\n\n\n")
    # print(blocks[0][0])
    # print("\n\n\n")
    # print(formatted_html)
    # print(blocks[1])

    return formatted_html


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
    print(execute_instructions(template, instructions, matched_instructions, variables))


html = """
<html>
    <h1>Users:</h1>
    Name: {{$abc}}
    {{FOR (USER in USERS):}}
        <h3>{{$$USER.NAME}}</h3>
        <h4>{{$$USER.DESCRIPTION}}</h4>
    {{ENDFOR}}
    {{FOR (USER in USERS):}}
        <h3>{{$$USER.NAME}}</h3>
        <h4>{{$$USER.DESCRIPTION}}</h4>
    {{ENDFOR}}
</html>
"""

# For nested for loop
# """{{FOR (PIC in PICTURES):}}
#             <img src="cool picture">
#             <h1>This is a cool picture made by {{$$USER.NAME}} at {{$TIMESTAMP}}</h1>
#             <h3>Location: {{$LOCATION}}</h3>
#         {{ENDFOR}}"""



class USER:
    def __init__(self):
        self.NAME = "Liam"
        self.USER = "joey"

x = USER()

user_list = [USER() for baz in range(10)]

dictionary = {"TIMESTAMP":"abc", "USER":x, "abc":"The Alphabet", "USERS":user_list}

parse_html(html, dictionary)
#instruction("FOR (a in b):")