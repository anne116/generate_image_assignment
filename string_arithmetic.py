def arithmetic_calculation(expression: str):
    try:
        result = eval(expression, {"__builtins__": None} , {})
        return result
    except Exception as err:
        print(f"計算表達式遇到問題:{err}")

    
# example
a = "(2+3)*2"
print(arithmetic_calculation(a))

# test 2
b = "(12+345)/2"
print(arithmetic_calculation(b))

# test 3
c = "(a+b)/c"
result = arithmetic_calculation(c)
if result is not None:
    print(result)