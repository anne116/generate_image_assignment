def arithmetic_calculation(expression: str):
    try:
        result = eval(expression, {"__builtins__": None} , {})
        return result
    except Exception as err:
        print(f"計算表達式遇到問題: {err}")
        return None
    
# example
a = "(2+3)*2"
print(arithmetic_calculation(a))

# test
b = "(12+345)/2"
print(arithmetic_calculation(b))

# test
c = "(a+b)/c"
print(arithmetic_calculation(c))