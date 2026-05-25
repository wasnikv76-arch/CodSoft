import re
import tkinter as tk   

#backend

def validate_expression(expr):

    exp = re.findall(r'\d+(?:\.\d+)?|[+\-*/()]', expr)

    if not expr.strip():     
       raise ValueError("Invalid Expression")
    
    if re.search(r'[^0-9+\-*/(). ]', expr):
       raise ValueError("Invalid Expression")

    joined = ''.join(exp)                 
    original = expr.replace(" ", "")      
   
    if joined != original:
        raise ValueError("Invalid Expression")

    def validate_braces(expr):
        depth = 0
        for ch in expr:
            if ch == '(':   depth += 1
            elif ch == ')':
                depth -= 1
                if depth < 0:
                    return False
        return depth == 0

    if not validate_braces(expr):
        raise ValueError("Invalid Expression")

def build_tokens(exp):
       tokens = []
       skip_until = -1

       for i in range(len(exp)):
           if i <= skip_until:
               continue
   
           if exp[i] in '+-' and (i == 0 or exp[i-1] in '+-*/('):
               if exp[i] == '+':
                   continue
               inner, j = consume_operand(exp, i + 1)
               tokens += ['(', '0', '-'] + inner + [')']
               skip_until = j
               continue
   
           if tokens:
               last = tokens[-1]
               curr = exp[i]
               if (last[-1].isdigit() or last == ')') and (curr[0].isdigit() or curr == '('):
                   tokens.append("*")

           tokens.append(exp[i])

       return tokens
    


def consume_operand(exp, j):
        toks = []
        while j < len(exp) and exp[j] in '+-':
           if exp[j] == '+':
                j += 1
           else:
                inner, j = consume_operand(exp, j + 1)
                toks += ['(', '0', '-'] + inner + [')']
                return toks, j

        if j >= len(exp):
            return toks, j

        if exp[j] == '(':
        # find matching closing paren
            depth = 0
            start = j
            while j < len(exp):
                if exp[j] == '(':   depth += 1
                elif exp[j] == ')':
                    depth -= 1
                    if depth == 0:  break
                j += 1
      
            inner_exp = exp[start+1 : j]        
            inner_tokens = build_tokens(inner_exp)
            toks += ['('] + inner_tokens + [')']
        else:
            toks.append(exp[j])

        return toks, j


def validate_tokens(tokens):
    for i in range(len(tokens) - 1):
        curr, nxt = tokens[i], tokens[i+1]
 
        if curr in '+-*/' and nxt in '*/':
            raise ValueError("Invalid Expression")
 
        if curr in '+-*/' and nxt == ')':
            raise ValueError("Invalid Expression")
 
        if curr == '(' and nxt in '*/':
            raise ValueError("Invalid Expression")
 
        if curr == '(' and nxt == ')':
           raise ValueError("Invalid Expression")
        
    if tokens and tokens[-1] in '+-*/':
           raise ValueError("Invalid Expression")
        
def priority(s):
    return {'+': 1, '-': 1, '*': 2, '/': 2}.get(s, -1)
 
operators = {"+", "-", "*", "/", "(", ")"}

def infix_to_postfix(tokens):
        st = []
        result = []
        for i in tokens:
            if i not in operators:
                result.append(i)
            elif i == "(":
                st.append(i)
            elif i == ")":
                while st and st[-1] != "(":
                    result.append(st.pop())
                st.pop()
            else:
                while st and priority(i) <= priority(st[-1]):
                    result.append(st.pop())
                st.append(i)
     
        while st:
          result.append(st.pop())
               
        return result

def postfix_calculation(result):
        st = []
        def calculate(a, b, op):
         match op:
            case "+": return a + b
            case "-": return a - b
            case "*": return a * b
            case "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                return a / b
            case _: raise ValueError(f"Invalid operator: {op}")
 
        def to_number(var):
          return float(var) if '.' in var else int(var)
 
        for i in result:
            if i not in operators:
                st.append(to_number(i))
            else:
                b = st.pop()
                a = st.pop()
                st.append(calculate(a, b, i))
 
        if len(st) != 1:
            raise ValueError("Invalid Expression")
        else:
            return st[0]
        


def calculate_expression(expr):
    
    validate_expression(expr)

    exp = re.findall(r'\d+(?:\.\d+)?|[+\-*/()]', expr)

    tokens = build_tokens(exp)

    validate_tokens(tokens)

    postfix = infix_to_postfix(tokens)

    return postfix_calculation(postfix)

#frontend

root = tk.Tk()

root.title("Expression Calculator")

top_frame = tk.Frame(root)
top_frame.pack()

bottom_frame = tk.Frame(root)
bottom_frame.pack()

root.geometry("420x600")
root.resizable(False, False)

root.configure(bg="#1E1E1E")
top_frame.configure(bg="#1E1E1E")
bottom_frame.configure(bg="#1E1E1E")


varString = tk.StringVar()
varString.set("")

label = tk.Label(top_frame, textvariable=varString, font=("Consolas",26,"bold"),
                 bg="#111111", fg="white", width=30, anchor="e", padx=10,pady=20)
label.pack()

def clicked(c):
    curr= varString.get()
    if c == "=":
       try:
        expr = curr.replace("×", "*").replace("÷", "/")

        answer = calculate_expression(expr)

        varString.set(answer)

       except Exception:
          varString.set("Error")
          expr = curr.replace("×", "*").replace("÷", "/")
          pass 
    elif c == "C":
        varString.set("")
    elif c == "←":
        varString.set(curr[:-1])
    else:
        varString.set(curr + c) 

b = ['7', '8', '9', '÷', '4', '5', '6', '×', '1', '2',
      '3', '-', '0', '.', '=', '+', '(', ')', 'C', '←']

for index,char in enumerate(b):
    row = index // 4
    col = index % 4
    if char in ['÷', '×', '-', '+']:
        color = "#FF9500"
        hover = "#FFB733"       
    elif char in ['C', '←']:
        color = "#505050"  
        hover = "#4A4A4A"    
    elif char == '=':
        color = "#4A90E2" 
        hover = "#54B8FA"      
    else:
        color = "#3A3A3A" 
        hover = "#4A4A4A"      
 
    btn = tk.Button(bottom_frame,text=char,font=("Consolas",34,"bold"),
                   width=3, height=1, padx=5, pady=5,
                   command=lambda c= char:clicked(c),
                   bg=color, fg="white",bd=0, relief="flat")
    btn.grid(row=row,column=col,padx=4,pady=4)
  

    btn.bind("<Enter>", lambda e, b=btn, h=hover: b.config(bg=h))
    btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
tk.mainloop()