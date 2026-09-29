import tkinter as tk

# ============================================================
# COLORS
# ============================================================

NUMBER_BG = "#303548"
NUMBER_FG = "#F4F7FF"

OPERATOR_BG = "#2D4C78"
OPERATOR_FG = "#72D9FF"

DANGER_BG = "#623646"
DANGER_FG = "#FF6576"

EQUAL_BG = "#1E6B59"
EQUAL_FG = "#25F0A7"

HOVER_NUMBER = "#3A4056"
HOVER_OPERATOR = "#365D91"
HOVER_DANGER = "#754052"
HOVER_EQUAL = "#27836D"



# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Modern Calculator")
root.geometry("430x700")
root.minsize(380, 600)
root.config(bg="#171A2B")


# ============================================================
# MAIN CONTAINER
# ============================================================
main_frame = tk.Frame(
    root,
    bg="#171A2B"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=25
)


# ============================================================
# DISPLAY FRAME
# ============================================================
display_frame = tk.Frame(
    main_frame,
    bg="#20243A",
    highlightbackground="#3A4157",
    highlightthickness=1
)

display_frame.pack(
    fill="x",
    pady=(0, 20)
)



# ============================================================
# DISPLAY
# ============================================================
display_var = tk.StringVar(value="0")

display = tk.Label(
    display_frame,
    textvariable=display_var,
    bg="#20243A",
    fg="#19F5A5",
    font=("Segoe UI", 30, "bold"),
    anchor="e",
    padx=20,
    pady=25
)

display.pack(
    fill="both"
)


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    main_frame,
    bg="#171A2B"
)

button_frame.pack(
    fill="both",
    expand=True
)


# ============================================================
# BUTTON FUNCTION
# ============================================================

def create_button(
    text,
    row,
    column,
    bg,
    fg,
    columnspan=1,
    font_size=24,
    hover_bg=None
):
    button = tk.Button(
        button_frame,
        text=text,
        bg=bg,
        fg=fg,
        activebackground=hover_bg or bg,
        activeforeground=fg,
        font=("Segoe UI", font_size, "bold"),
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground="#3A4157",
        cursor="hand2"
    )

    button.grid(
        row=row,
        column=column,
        columnspan=columnspan,
        sticky="nsew",
        padx=7,
        pady=7
    )

    if hover_bg:
        button.bind(
            "<Enter>",
            lambda event: button.configure(bg=hover_bg)
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(bg=bg)
        )

    return button


# ============================================================
# GRID CONFIGURATION
# ============================================================

for column in range(4):
    button_frame.columnconfigure(
        column,
        weight=1
    )

for row in range(6):
    button_frame.rowconfigure(
        row,
        weight=1
    )


# ============================================================
# BUTTONS
# ============================================================

# C
create_button(
    "C",
    0,
    0,
    DANGER_BG,
    DANGER_FG,
    columnspan=2,
    font_size=22,
    hover_bg=HOVER_DANGER
)

# DEL
create_button(
    "DEL",
    0,
    2,
    DANGER_BG,
    DANGER_FG,
    columnspan=2,
    font_size=22,
    hover_bg=HOVER_DANGER
)


# Row 1
create_button(
    "÷", 1, 0,
    OPERATOR_BG,
    OPERATOR_FG,
    hover_bg=HOVER_OPERATOR
)

create_button(
    "×", 1, 1,
    OPERATOR_BG,
    OPERATOR_FG,
    hover_bg=HOVER_OPERATOR
)

create_button(
    "7", 1, 2,
    NUMBER_BG,
    NUMBER_FG,
    hover_bg=HOVER_NUMBER
)

create_button(
    "8", 1, 3,
    NUMBER_BG,
    NUMBER_FG,
    hover_bg=HOVER_NUMBER
)


# Row 2
create_button(
    "9", 2, 0,
    NUMBER_BG,
    NUMBER_FG,
    hover_bg=HOVER_NUMBER
)

create_button(
    "−", 2, 1,
    OPERATOR_BG,
    OPERATOR_FG,
    hover_bg=HOVER_OPERATOR
)

create_button(
    "4", 2, 2,
    NUMBER_BG,
    NUMBER_FG,
    hover_bg=HOVER_NUMBER
)

create_button(
    "5", 2, 3,
    NUMBER_BG,
    NUMBER_FG,
    hover_bg=HOVER_NUMBER
)


# Row 3
create_button(
    "6", 3, 0,
    NUMBER_BG,
    NUMBER_FG,
    hover_bg=HOVER_NUMBER
)

create_button(
    "+", 3, 1,
    OPERATOR_BG,
    OPERATOR_FG,
    hover_bg=HOVER_OPERATOR
)

create_button(
    "1", 3, 2,
    NUMBER_BG,
    NUMBER_FG,
    hover_bg=HOVER_NUMBER
)

create_button(
    "2", 3, 3,
    NUMBER_BG,
    NUMBER_FG,
    hover_bg=HOVER_NUMBER
)


# Row 4
create_button(
    "3", 4, 0,
    NUMBER_BG,
    NUMBER_FG,
    hover_bg=HOVER_NUMBER
)

create_button(
    ".", 4, 1,
    OPERATOR_BG,
    OPERATOR_FG,
    hover_bg=HOVER_OPERATOR
)

create_button(
    "0", 4, 2,
    NUMBER_BG,
    NUMBER_FG,
    hover_bg=HOVER_NUMBER
)

create_button(
    "%", 4, 3,
    OPERATOR_BG,
    OPERATOR_FG,
    hover_bg=HOVER_OPERATOR
)


# Equals
create_button(
    "=",
    5,
    0,
    EQUAL_BG,
    EQUAL_FG,
    columnspan=2,
    font_size=28,
    hover_bg=HOVER_EQUAL
)


root.mainloop()