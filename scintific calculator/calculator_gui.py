import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("400x600")
        
        # Result display
        self.display_var = tk.StringVar()
        self.display = tk.Entry(root, textvariable=self.display_var, font=('Arial', 24), 
                          bd=10, insertwidth=2, width=14, borderwidth=4, justify='right')
        self.display.grid(row=0, column=0, columnspan=5)
        
        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('C', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('(', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), (')', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('^', 4, 4),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('log', 5, 3), ('ln', 5, 4),
            ('sqrt', 6, 0), ('exp', 6, 1), ('pi', 6, 2), ('e', 6, 3), ('⌫', 6, 4)
        ]
        
        # Create buttons
        for (text, row, col) in buttons:
            if text in ['=', 'C', '⌫']:
                btn = tk.Button(root, text=text, padx=20, pady=20,
                              command=lambda t=text: self.special_button_click(t))
            else:
                btn = tk.Button(root, text=text, padx=20, pady=20,
                              command=lambda t=text: self.button_click(t))
            btn.grid(row=row, column=col, sticky="nsew")
        
        # Configure row/column weights
        for i in range(7):
            root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            root.grid_columnconfigure(i, weight=1)
    
    def button_click(self, char):
        current = self.display_var.get()
        if char in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'exp']:
            self.display_var.set(current + char + '(')  # Auto-add '(' for functions
        elif char in ['pi', 'e']:
            self.display_var.set(current + char)
        else:
            self.display_var.set(current + char)
    
    def special_button_click(self, char):
        if char == '=':
            self.calculate()
        elif char == 'C':
            self.display_var.set('')
        elif char == '⌫':
            current = self.display_var.get()
            self.display_var.set(current[:-1])
    
    def calculate(self):
        expression = self.display_var.get()
        if not expression:
            return
        
        try:
            # First try using the parser if available
            if os.path.exists('./parser'):
                process = subprocess.Popen(['./parser'], 
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         text=True)
                stdout, stderr = process.communicate(input=expression + '\n')
                
                if 'Result:' in stdout:
                    result = stdout.split('Result: ')[1].strip()
                    self.display_var.set(result)
                    return
            
            # Fallback to Python evaluation
            safe_dict = {'math': math}
            expr = expression.replace('^', '**')
            # Handle degree conversion for trig functions
            if any(f in expr for f in ['sin(', 'cos(', 'tan(']):
                expr = expr.replace('sin(', 'math.sin(math.radians(')
                expr = expr.replace('cos(', 'math.cos(math.radians(')
                expr = expr.replace('tan(', 'math.tan(math.radians(')
                expr += ')' * expr.count('math.radians(')  # Add closing parentheses
            result = eval(expr, {'__builtins__': None}, safe_dict)
            self.display_var.set(str(result))
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()