from flask import Flask, request

app = Flask(__name__)

valid_operators = ["+", "-", "*", "/"]

path = "http://localhost:5000/calculator?num1=2&num2=3&operator=%2B"

def solve(num1, num2, operator):
    """Returns the result of the operation between num1 and num2.
    If opertator is not in valid_operators, returns "Invalid operator".
    Valid operators are: "+", "-", "*", "/".

    Args:
        num1 (float): operand 1
        num2 (float): operand 2
        operator (string): operator with which to perform the operation

    Returns:
        _type_: _description_
    """
    if operator not in valid_operators:
        return f"Invalid operator {operator}"
    try:
        return eval(f"{num1} {operator} {num2}")
    except:
        return "ZeroDivisionError"    
    
@app.route('/calculator', methods=['GET'])
def calculator():
    num1 = request.args.get('num1')
    num2 = request.args.get('num2')
    operator = request.args.get('operator')
    result = solve(float(num1), float(num2), operator)
    return str(result)

if __name__ == '__main__':
    app.run(debug=True)
    