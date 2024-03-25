import tkinter as tk
import math

class HoverButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        tk.Button.__init__(self, master=master, **kwargs)
        self.defaultBackground = "#00ccff"
        self["bg"] = self.defaultBackground
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(bg="#ff4500")  # Change background color on hover

    def on_leave(self, event):
        self.configure(bg=self.defaultBackground)  # Restore original background color

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("300x550")
        self.configure(bg="#6699FF")  # Set background color 
        self.create_widgets()

    def create_widgets(self):
        # Text widget to display input and output
        self.display = tk.Text(self, height=2, font=("Arial", 20), fg="#6699FF" ,bg="#000000", bd=2.5, relief=tk.SOLID) # set text colour and text background
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
            ('(', 6, 0), (')', 6, 1), ('^', 6, 2), ('π', 6, 3),
            ('bin', 7, 0), ('oct', 7, 1),('hex', 7, 2), ('dec', 7, 3), 
            ('C', 8, 0),('Del', 8, 1), ('%', 8, 2)
        ]

        # Create buttons
        for text, row, col in buttons:
            button = HoverButton(button_frame, text=text, font=("Arial", 15),
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")

            # Set button colors
            if text in ('=', 'C', 'Del', '%', 'bin', 'oct', 'hex', 'dec'):
                button.config(bg="#AA00AA", fg="black", bd=1.0, relief=tk.SOLID)  # Orchid purple background,white foreground,solid border
            elif text.isdigit() or text == '.':
                button.config(bg="#4169e1", fg="black", bd=1.0, relief=tk.SOLID)  # Blue background,white foreground,solid border
            else:
                button.config(bg="#99FFFF", fg="#000000", bd=1.0, relief=tk.SOLID)  # Teal background,white foreground,solid border

            # Store original colors
            button.bind("<Enter>", lambda event, b=button: self.on_hover_enter(b))
            button.bind("<Leave>", lambda event, b=button: self.on_hover_leave(b))

    def on_hover_enter(self, button):
        # Store original colors
        button.orig_bg = button.cget("bg")
        button.orig_fg = button.cget("fg")

        # Change colors on hover
        button.config(bg="white", fg="black")

    def on_hover_leave(self, button):
        # Restore original colors
        button.config(bg=button.orig_bg, fg=button.orig_fg)

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
        elif text == 'π':  # Handle π button
            self.display.insert(tk.END, math.pi)
        else:
            self.display.insert(tk.END, text)

    def evaluate_expression(self, expression):
        # Replace special functions with their math module counterparts
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('^', '**')
        expression = expression.replace('π', 'math.pi')

        # Evaluate the expression
        try:
            result = eval(expression)
            return result
        except Exception as e:
            return "Error: " + str(e)

    def convert_expression(self, expression, base):
        expression = expression.strip()
        if base == 'bin':
            try:
                return bin(int(expression))
            except ValueError as e:
                return "Error: " + str(e)
        elif base == 'oct':
            try:
                return oct(int(expression))
            except ValueError as e:
                return "Error: " + str(e)
        elif base == 'hex':
            try:
                return hex(int(expression))
            except ValueError as e:
                return "Error: " + str(e)
        elif base == 'dec':
            try:
                return int(expression, 16)
            except ValueError as e:
                return "Error: " + str(e)

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()


