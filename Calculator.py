import tkinter as tk
import math

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("400x600")
        self.configure(bg="#ffffff")  # Set background color
        self.create_widgets()

    def create_widgets(self):
        # Text widget to display input and output
        self.display = tk.Text(self, height=2, font=("Arial", 20), fg="#000000" ,bg="#ffffcc", bd=2.5, relief=tk.SOLID) # set text colour and text background
        self.display.pack(fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = tk.Frame(self, bg="#f0f0f0", bd=1, relief=tk.SOLID)  # Set background color
        button_frame.pack(fill=tk.BOTH, expand=True)

        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('sqrt', 5, 3),
            ('(', 6, 0), (')', 6, 1), ('^', 6, 2), ('C', 6, 3),
            ('Del', 6, 4), ('%', 6, 5), ('bin', 7, 0), ('oct', 7, 1),
            ('hex', 7, 2), ('dec', 7, 3)
        ]

        # Create buttons
        for text, row, col in buttons:
            button = tk.Button(button_frame, text=text, font=("Arial", 15),
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            # Set button colors
            if text in ('=', 'C', 'Del', '%', 'bin', 'oct', 'hex', 'dec'):
                button.config(bg="#ff6347", fg="white", bd=0.7, relief=tk.SOLID)  # Red background,white foreground,solid border
            elif text.isdigit() or text == '.':
                button.config(bg="#4169e1", fg="white", bd=0.7, relief=tk.SOLID)  # Blue background,white foreground,solid border
            else:
                button.config(bg="#20b2aa", fg="white", bd=0.7, relief=tk.SOLID)  # Green background,white foreground,solid border

    def on_button_click(self, text):
        if text == '=':
            try:
                expression = self.display.get("1.0", tk.END).strip()
                result = self.evaluate_expression(expression)
                self.display.delete("1.0", tk.END)
                self.display.insert(tk.END, result)
            except Exception as e:
                self.display.delete("1.0", tk.END)
                self.display.insert(tk.END, "Error")
        elif text == 'C':
            self.display.delete("1.0", tk.END)
        elif text == 'Del':  # Handle delete button
            current_text = self.display.get("1.0", tk.END)
            self.display.delete("1.0", tk.END)
            self.display.insert(tk.END, current_text[:-2])
        elif text == '%':
            try:
                expression = self.display.get("1.0", tk.END).strip()
                result = self.evaluate_expression(expression) / 100
                self.display.delete("1.0", tk.END)
                self.display.insert(tk.END, result)
            except Exception as e:
                self.display.delete("1.0", tk.END)
                self.display.insert(tk.END, "Error")
        elif text in ('bin', 'oct', 'hex', 'dec'):
            try:
                expression = self.display.get("1.0", tk.END).strip()
                result = self.convert_expression(expression, text)
                self.display.delete("1.0", tk.END)
                self.display.insert(tk.END, result)
            except Exception as e:
                self.display.delete("1.0", tk.END)
                self.display.insert(tk.END, "Error")
        else:
            self.display.insert(tk.END, text)

    def evaluate_expression(self, expression):
        # Replace special functions with their math module counterparts
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('^', '**')

        # Evaluate the expression
        result = eval(expression)
        return result

    def convert_expression(self, expression, base):
        expression = expression.strip()
        if base == 'bin':
            return bin(int(expression))
        elif base == 'oct':
            return oct(int(expression))
        elif base == 'hex':
            return hex(int(expression))
        elif base == 'dec':
            return int(expression, 16)

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()
