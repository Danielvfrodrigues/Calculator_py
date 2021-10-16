import re
import math
import tkinter as tk
from typing import List
from calculator_factories import Colors

"""Calculator Class"""


class Calculator:
    def __init__(
        self,
        root: tk.Tk,
        label: tk.Label,
        display: tk.Entry,
        buttons: List[List[tk.Button]]
    ):
        self.root = root
        self.label = label
        self.display = display
        self.buttons = buttons

    def start(self):
        global numLen
        self._config_buttons()
        self._config_display()
        self.initial_text()
        self.root.mainloop()

    def _config_buttons(self):
        global button_text
        buttons = self.buttons
        for row_values in buttons:
            for button in row_values:
                button_text = button['text']

                if button_text == 'AC':
                    button.bind('<Button-1>', (self.clear))
                    button.config(bg=Colors.clear_btn_color,
                                  fg=Colors.light_text)

                if button_text == 'C':
                    button.bind('<Button-1>', (self.cancel))
                    button.config(bg=Colors.clear_btn_color,
                                  fg=Colors.light_text)

                if button_text in '()':
                    button.bind('<Button-1>', (self.add_brackets_to_display))

                if button_text in '.+-/*':
                    button.bind('<Button-1>', (self.add_operators_to_display))

                if button_text in '0123456789':
                    button.bind('<Button-1>', (self.add_text_to_display))

                if button_text == '=':
                    button.bind('<Button-1>', (self.calculate))
                    button.config(bg=Colors.equals_btn_color,
                                  fg=Colors.light_text)

    def _config_display(self):
        self.display.bind('<Return>', self.calculate)
        self.display.bind('<KP_Enter>', self.calculate)

    def _fix_text(self, text):
        # Replace every character which is NOT in '0123456789.+-/*()^' to "nothing"
        text = re.sub(r'[^\d\.\/\*\-\+\(\)e]', r'', text, 0)
        # Replace every repeated math operators to only one
        text = re.sub(r'([\.\+\/\-\*])\1+', r'\1', text, 0)
        # Replace () or *() to "nothing"
        text = re.sub(r'\*?\(\)', '', text)

        return text

    def initial_text(self, event=None):
        self.display.insert(0, '0')

    def clear(self, event=None):
        self.display.delete(0, 'end')
        self.display.insert(0, '0')
        self.label.config(text='No operations yet...')

    def cancel(self, event=None):
        numLen = len(self.display.get())
        self.display.delete(numLen - 1, 'end')

    def add_brackets_to_display(self, event=None):
        current = self.display.get()
        numLen = len(self.display.get())

        if current == '0':
            self.display.delete(numLen - 1, 'end')
            self.display.insert('end', event.widget['text'])
        else:
            self.display.insert('end', event.widget['text'])

    def add_operators_to_display(self, event=None):
        self.display.insert('end', event.widget['text'])

    def add_text_to_display(self, event=None):
        current = self.display.get()
        numLen = len(self.display.get())

        if current == '0':
            self.display.delete(numLen - 1, 'end')

        if numLen == 8 or numLen == 17 or numLen >= 26:
            self.label.config(text='Max number length: 8')
        elif numLen == 9 or numLen == 18 or numLen == 27:
            self.display.insert('end', event.widget['text'])
            self.label.config(text='No operations yet...')
        else:
            self.display.insert('end', event.widget['text'])
        print(numLen)

    def calculate(self, event=None):
        fixed_text = self._fix_text(self.display.get())
        equations = self._get_equations(fixed_text)

        try:
            if len(equations) == 1:
                result = eval(self._fix_text(equations[0]))
            else:
                result = eval(self._fix_text(equations[0]))
                for equation in equations[1:]:
                    result = math.pow(result, eval(self._fix_text(equation)))

            self.display.delete(0, 'end')
            self.display.insert('end', result)
            self.label.config(text=f'{fixed_text} = {result}')

        except OverflowError:
            self.label.config(
                text='SORRY ABOUT THAT! I wasn´t able to solve the operation.')
        except Exception as e:
            print(e)
            self.label.config(
                text='SORRY ABOUT THAT! I wasn´t able to solve the operation.')

    def _get_equations(self, text):
        return re.split(r'\^', text, 0)
