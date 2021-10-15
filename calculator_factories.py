import tkinter as tk
from typing import List, Text


class Colors:
    bg_color = '#242424'
    btn_color = '#454545'
    light_text = '#ebebeb'
    highlight_color = '#383838'
    clear_btn_color = '#EA4335'
    equals_btn_color = '#4785F4'


def make_root() -> tk.Tk:
    root = tk.Tk()
    root.title('Calculator')
    root.iconbitmap('D:\py\calculadora\icon.ico')
    root.config(padx=10, pady=10, background=Colors.bg_color)
    root.resizable(False, False)
    return root


def make_label(root) -> tk.Label:
    label = tk.Label(
        root, text='No operations yet...',
        anchor='e', justify='right', background=Colors.bg_color, fg=Colors.light_text
    )

    label.grid(row=0, column=0, columnspan=5, sticky='news')
    return label


def make_display(root) -> tk.Entry:
    display = tk.Entry(root)
    display.grid(row=1, column=0, columnspan=5, sticky='news', pady=(0, 10))
    display.config(
        font=('Helvetica', 40, 'bold'),
        justify='right',
        bd=1,
        relief='flat',
        highlightthickness=1,
        highlightcolor=Colors.highlight_color
    )
    display.bind('<Control-a>', display_control_a)
    return display


def display_control_a(event):
    event.widget.select_range(0, 'end')
    event.widget.icursor('end')
    return 'break'


def make_buttons(root) -> List[List[tk.Button]]:
    button_texts: List[List[str]] = [
        ['7', '8', '9', '+', 'C'],
        ['4', '5', '6', '-', '/'],
        ['1', '2', '3', '*', '^'],
        ['0', '.', '(', ')', '='],
    ]

    buttons: List[List[tk.Button]] = []

    for row, row_value in enumerate(button_texts, start=2):
        button_row = []
        for col_index, col_value in enumerate(row_value):
            btn = tk.Button(root, text=col_value)
            btn.grid(row=row, column=col_index, sticky='news', padx=5, pady=5)
            btn.config(
                font=('Helvetica', 15, 'normal'),
                pady=10,
                width=1,
                background=Colors.btn_color,
                bd=0,
                cursor='hand2',
                highlightthickness=0,
                highlightcolor=Colors.highlight_color,
                highlightbackground=Colors.highlight_color,
                activebackground=Colors.highlight_color
            )
            button_row.append(btn)
        buttons.append(button_row)
    return buttons
