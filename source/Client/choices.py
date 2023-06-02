from agent import Agent, AgentFunction
from utils import Address


# Set Agent
def get_address():
    print("##############################")
    ip = input("INTRODUZCA DIRECCION IP: ")
    port = input("INTRODUZCA EL PUERTO")
    print("##############################")

    address = Address(ip, port)

    return address


def get_function_params():
    print()

    params = []

    print("########################################################")
    while True:
        choice = input("INTRODUZCA 1 PARA AÑADIR PARAMETROS, 2 PARA TERMINAR")

        if choice == "1":
            name = input()
            params.append(name)
        elif choice == "2":
            break
        else:
            print("E")
    print("########################################################")

    return params


def get_agent_functions():
    print()

    functions = []

    print("########################################################")
    while True:
        choice = input("SI DESEA AÑADIR UNA FUCNION ESCRIBA 1, 2 PARA TERMINAR.")

        if choice == "1":
            name = input("INTRODUZCA EL NOMBRE DE LA FUNCION")
            address = get_address()
            params = get_function_params()
            description = input()
            function = AgentFunction(name, address, params, description)
            functions.append(function)
        elif choice == "2":
            break
        else:
            print("E")

    print("########################################################")
    return functions


def agent_ctor():
    print("###################################")
    name = input("ENTER THE NAME OF THE AGENT: ")
    functions = get_agent_functions()

    new_agent = Agent(name, functions)

    print("###################################")
    return new_agent


def set_agent():
    new_agent = agent_ctor()

    # call backend


# Get Agent by Func


def get_agent_by_functionality():
    description = input("INTRODUZCA UNA FUNCIONALIDAD PARA BUSCAR EN LA PLATAFORMA.")

    # call backend
