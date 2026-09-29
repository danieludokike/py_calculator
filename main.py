import tkinter as tk
import ast
import operator


# ============================================================
# COLORS
# ============================================================

BACKGROUND = "#171A2B"
DISPLAY_BACKGROUND = "#20243A"
BORDER = "#3A4157"

NUMBER_BG = "#303548"
NUMBER_FG = "#F4F7FF"
NUMBER_HOVER = "#3A4056"

OPERATOR_BG = "#2D4C78"
OPERATOR_FG = "#72D9FF"
OPERATOR_HOVER = "#365D91"

DANGER_BG = "#623646"
DANGER_FG = "#FF6576"
DANGER_HOVER = "#754052"

EQUAL_BG = "#1E6B59"
EQUAL_FG = "#25F0A7"
EQUAL_HOVER = "#27836D"

DISPLAY_FG = "#19F5A5"


# ============================================================
# CALCULATOR ENGINE
# ============================================================

class CalculatorEngine:
    """
    Safe calculator engine.

    We deliberately do NOT use eval().
    The expression is parsed with Python's AST module.
    """

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    UNARY_OPERATORS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    @classmethod
    def calculate(cls, expression):
        """
        Calculate an expression safely.
        """

        expression = expression.strip()

        if not expression:
            return 0

        # Convert calculator symbols into Python symbols.
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("−", "-")

        # Convert percentage expressions.
        expression = cls.convert_percentages(expression)

        try:
            tree = ast.parse(
                expression,
                mode="eval"
            )

            result = cls.evaluate_node(tree.body)

            return result

        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")

        except OverflowError:
            raise ValueError("Number too large")

        except (
            SyntaxError,
            ValueError,
            TypeError
        ):
            raise ValueError("Invalid expression")

    @classmethod
    def evaluate_node(cls, node):

        # ----------------------------------------------------
        # Numbers
        # ----------------------------------------------------

        if isinstance(node, ast.Constant):

            if isinstance(
                node.value,
                (int, float)
            ) and not isinstance(
                node.value,
                bool
            ):
                return node.value

            raise ValueError("Invalid number")

        # ----------------------------------------------------
        # Binary operators
        # ----------------------------------------------------

        if isinstance(node, ast.BinOp):

            operator_type = type(node.op)

            if operator_type not in cls.OPERATORS:
                raise ValueError("Operator not allowed")

            left = cls.evaluate_node(
                node.left
            )

            right = cls.evaluate_node(
                node.right
            )

            # Protect against absurdly large calculations.
            if abs(left) > 1e100:
                raise ValueError("Number too large")

            if abs(right) > 1e100:
                raise ValueError("Number too large")

            result = cls.OPERATORS[operator_type](
                left,
                right
            )

            if abs(result) > 1e100:
                raise ValueError("Number too large")

            return result

        # ----------------------------------------------------
        # Unary operators
        # ----------------------------------------------------

        if isinstance(node, ast.UnaryOp):

            operator_type = type(node.op)

            if operator_type not in cls.UNARY_OPERATORS:
                raise ValueError("Operator not allowed")

            value = cls.evaluate_node(
                node.operand
            )

            return cls.UNARY_OPERATORS[operator_type](
                value
            )

        # ----------------------------------------------------
        # Parentheses
        # ----------------------------------------------------

        if isinstance(node, ast.Expr):

            return cls.evaluate_node(
                node.value
            )

        raise ValueError("Invalid expression")

    @staticmethod
    def convert_percentages(expression):
        """
        Converts:

            50%

        into:

            (50/100)

        This allows expressions such as:

            200 + 10%

        to be interpreted as:

            200 + 0.10

        """

        import re

        # Replace a number followed by %.
        pattern = r"(\d+(?:\.\d+)?)%"

        expression = re.sub(
            pattern,
            r"(\1/100)",
            expression
        )

        return expression


# ============================================================
# MAIN APPLICATION
# ============================================================

class CalculatorApp:

    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # Application state
        # ----------------------------------------------------

        self.expression = ""

        self.last_result = None

        self.just_calculated = False

        self.last_expression = ""

        # ----------------------------------------------------
        # Window
        # ----------------------------------------------------

        self.root.title(
            "Modern Calculator"
        )

        self.root.geometry(
            "450x720"
        )

        self.root.minsize(
            400,
            650
        )

        self.root.configure(
            bg=BACKGROUND
        )

        # ----------------------------------------------------
        # Variables
        # ----------------------------------------------------

        self.display_var = tk.StringVar(
            value="0"
        )

        self.expression_var = tk.StringVar(
            value=""
        )

        # ----------------------------------------------------
        # Build application
        # ----------------------------------------------------

        self.create_main_container()

        self.create_display()

        self.create_buttons()

        self.bind_keyboard()

    # ========================================================
    # MAIN CONTAINER
    # ========================================================

    def create_main_container(self):

        self.main_frame = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=22
        )

    # ========================================================
    # DISPLAY
    # ========================================================

    def create_display(self):

        self.display_frame = tk.Frame(
            self.main_frame,
            bg=DISPLAY_BACKGROUND,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.display_frame.pack(
            fill="x",
            pady=(0, 18)
        )

        # ----------------------------------------------------
        # Small expression display
        # ----------------------------------------------------

        self.expression_label = tk.Label(
            self.display_frame,
            textvariable=self.expression_var,
            bg=DISPLAY_BACKGROUND,
            fg="#8991AA",
            font=(
                "Segoe UI",
                13
            ),
            anchor="e"
        )

        self.expression_label.pack(
            fill="x",
            padx=20,
            pady=(12, 0)
        )

        # ----------------------------------------------------
        # Main result display
        # ----------------------------------------------------

        self.display = tk.Label(
            self.display_frame,
            textvariable=self.display_var,
            bg=DISPLAY_BACKGROUND,
            fg=DISPLAY_FG,
            font=(
                "Segoe UI",
                34,
                "bold"
            ),
            anchor="e"
        )

        self.display.pack(
            fill="x",
            padx=20,
            pady=(2, 20)
        )

    # ========================================================
    # BUTTON FRAME
    # ========================================================

    def create_buttons(self):

        self.button_frame = tk.Frame(
            self.main_frame,
            bg=BACKGROUND
        )

        self.button_frame.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Five columns
        # ----------------------------------------------------

        for column in range(5):

            self.button_frame.columnconfigure(
                column,
                weight=1
            )

        # ----------------------------------------------------
        # Six rows
        # ----------------------------------------------------

        for row in range(6):

            self.button_frame.rowconfigure(
                row,
                weight=1
            )

        # ----------------------------------------------------
        # TOP ROW
        # ----------------------------------------------------

        self.create_button(
            "C",
            0,
            0,
            DANGER_BG,
            DANGER_FG,
            hover_bg=DANGER_HOVER
        )

        self.create_button(
            "DEL",
            0,
            1,
            DANGER_BG,
            DANGER_FG,
            hover_bg=DANGER_HOVER
        )

        self.create_button(
            "±",
            0,
            2,
            OPERATOR_BG,
            OPERATOR_FG,
            hover_bg=OPERATOR_HOVER
        )

        self.create_button(
            "(",
            0,
            3,
            OPERATOR_BG,
            OPERATOR_FG,
            hover_bg=OPERATOR_HOVER
        )

        self.create_button(
            ")",
            0,
            4,
            OPERATOR_BG,
            OPERATOR_FG,
            hover_bg=OPERATOR_HOVER
        )

        # ----------------------------------------------------
        # ROW 1
        # ----------------------------------------------------

        self.create_button(
            "÷",
            1,
            0,
            OPERATOR_BG,
            OPERATOR_FG,
            hover_bg=OPERATOR_HOVER
        )

        self.create_button(
            "×",
            1,
            1,
            OPERATOR_BG,
            OPERATOR_FG,
            hover_bg=OPERATOR_HOVER
        )

        self.create_button(
            "7",
            1,
            2,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        self.create_button(
            "8",
            1,
            3,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        self.create_button(
            "9",
            1,
            4,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        # ----------------------------------------------------
        # ROW 2
        # ----------------------------------------------------

        self.create_button(
            "−",
            2,
            0,
            OPERATOR_BG,
            OPERATOR_FG,
            hover_bg=OPERATOR_HOVER
        )

        self.create_button(
            "+",
            2,
            1,
            OPERATOR_BG,
            OPERATOR_FG,
            hover_bg=OPERATOR_HOVER
        )

        self.create_button(
            "4",
            2,
            2,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        self.create_button(
            "5",
            2,
            3,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        self.create_button(
            "6",
            2,
            4,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        # ----------------------------------------------------
        # ROW 3
        # ----------------------------------------------------

        self.create_button(
            "%",
            3,
            0,
            OPERATOR_BG,
            OPERATOR_FG,
            hover_bg=OPERATOR_HOVER
        )

        self.create_button(
            "00",
            3,
            1,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        self.create_button(
            "1",
            3,
            2,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        self.create_button(
            "2",
            3,
            3,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        self.create_button(
            "3",
            3,
            4,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        # ----------------------------------------------------
        # ROW 4
        # ----------------------------------------------------

        self.create_button(
            ".",
            4,
            0,
            OPERATOR_BG,
            OPERATOR_FG,
            hover_bg=OPERATOR_HOVER
        )

        self.create_button(
            "⌫",
            4,
            1,
            DANGER_BG,
            DANGER_FG,
            hover_bg=DANGER_HOVER
        )

        self.create_button(
            "0",
            4,
            2,
            NUMBER_BG,
            NUMBER_FG,
            hover_bg=NUMBER_HOVER
        )

        # ----------------------------------------------------
        # Equals spans the last two columns.
        # ----------------------------------------------------

        self.create_button(
            "=",
            4,
            3,
            EQUAL_BG,
            EQUAL_FG,
            columnspan=2,
            font_size=28,
            hover_bg=EQUAL_HOVER
        )

    # ========================================================
    # CREATE BUTTON
    # ========================================================

    def create_button(
        self,
        text,
        row,
        column,
        bg,
        fg,
        columnspan=1,
        font_size=23,
        hover_bg=None
    ):

        button = tk.Button(
            self.button_frame,
            text=text,
            bg=bg,
            fg=fg,
            activebackground=hover_bg or bg,
            activeforeground=fg,
            font=(
                "Segoe UI",
                font_size,
                "bold"
            ),
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            cursor="hand2",
            command=lambda value=text:
                self.handle_button(value)
        )

        button.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="nsew",
            padx=5,
            pady=5
        )

        # ----------------------------------------------------
        # Hover effect
        # ----------------------------------------------------

        if hover_bg:

            button.bind(
                "<Enter>",
                lambda event:
                button.configure(
                    bg=hover_bg
                )
            )

            button.bind(
                "<Leave>",
                lambda event:
                button.configure(
                    bg=bg
                )
            )

        return button

    # ========================================================
    # BUTTON HANDLER
    # ========================================================

    def handle_button(self, value):

        # ----------------------------------------------------
        # Numbers
        # ----------------------------------------------------

        if value.isdigit():

            self.input_number(
                value
            )

        # ----------------------------------------------------
        # Decimal
        # ----------------------------------------------------

        elif value == ".":

            self.input_decimal()

        # ----------------------------------------------------
        # Operators
        # ----------------------------------------------------

        elif value in {
            "+",
            "−",
            "×",
            "÷"
        }:

            self.input_operator(
                value
            )

        # ----------------------------------------------------
        # Percentage
        # ----------------------------------------------------

        elif value == "%":

            self.input_percentage()

        # ----------------------------------------------------
        # Parentheses
        # ----------------------------------------------------

        elif value == "(":

            self.input_open_parenthesis()

        elif value == ")":

            self.input_close_parenthesis()

        # ----------------------------------------------------
        # Sign
        # ----------------------------------------------------

        elif value == "±":

            self.toggle_sign()

        # ----------------------------------------------------
        # Clear
        # ----------------------------------------------------

        elif value == "C":

            self.clear()

        # ----------------------------------------------------
        # Delete
        # ----------------------------------------------------

        elif value in {
            "DEL",
            "⌫"
        }:

            self.delete()

        # ----------------------------------------------------
        # Equals
        # ----------------------------------------------------

        elif value == "=":

            self.calculate()

    # ========================================================
    # INPUT NUMBER
    # ========================================================

    def input_number(self, number):

        # After calculation, typing a number starts
        # a completely new calculation.

        if self.just_calculated:

            self.expression = ""

            self.expression_var.set("")

            self.just_calculated = False

        # ----------------------------------------------------
        # Prevent leading zeros such as 0007.
        # ----------------------------------------------------

        if self.expression == "0":

            self.expression = number

        elif self.expression == "-0":

            self.expression = "-" + number

        else:

            self.expression += number

        self.update_display()

    # ========================================================
    # DECIMAL
    # ========================================================

    def input_decimal(self):

        if self.just_calculated:

            self.expression = ""

            self.expression_var.set("")

            self.just_calculated = False

        # ----------------------------------------------------
        # Determine current number.
        # ----------------------------------------------------

        current_number = self.get_current_number()

        # Don't allow:
        #
        # 5.5.5
        #

        if "." in current_number:

            return

        # ----------------------------------------------------
        # If decimal starts a new number.
        # ----------------------------------------------------

        if (
            not self.expression
            or self.expression[-1] in "+−×÷("
        ):

            self.expression += "0."

        else:

            self.expression += "."

        self.update_display()

    # ========================================================
    # CURRENT NUMBER
    # ========================================================

    def get_current_number(self):

        current = self.expression

        positions = []

        for symbol in [
            "+",
            "−",
            "×",
            "÷",
            "(",
            ")"
        ]:

            position = current.rfind(
                symbol
            )

            if position != -1:

                positions.append(
                    position
                )

        if positions:

            last_position = max(
                positions
            )

            return current[
                last_position + 1:
            ]

        return current

    # ========================================================
    # OPERATOR
    # ========================================================

    def input_operator(self, operator_symbol):

        if not self.expression:

            # Allow a negative number.
            if operator_symbol == "−":

                self.expression = "−"

                self.update_display()

            return

        self.just_calculated = False

        # ----------------------------------------------------
        # Replace an existing operator.
        # ----------------------------------------------------

        if self.expression[-1] in {
            "+",
            "−",
            "×",
            "÷"
        }:

            self.expression = (
                self.expression[:-1]
                + operator_symbol
            )

        else:

            self.expression += operator_symbol

        self.update_display()

    # ========================================================
    # PERCENTAGE
    # ========================================================

    def input_percentage(self):

        if not self.expression:

            return

        if self.expression[-1] in {
            "+",
            "−",
            "×",
            "÷",
            "("
        }:

            return

        if self.expression.endswith("%"):

            return

        self.expression += "%"

        self.update_display()

    # ========================================================
    # OPEN PARENTHESIS
    # ========================================================

    def input_open_parenthesis(self):

        if self.just_calculated:

            self.expression = ""

            self.expression_var.set("")

            self.just_calculated = False

        # If the previous character is a number or ),
        # automatically multiply.
        if self.expression:

            if (
                self.expression[-1].isdigit()
                or self.expression[-1] == ")"
            ):

                self.expression += "×"

        self.expression += "("

        self.update_display()

    # ========================================================
    # CLOSE PARENTHESIS
    # ========================================================

    def input_close_parenthesis(self):

        if not self.expression:

            return

        # Count parentheses.
        opening = self.expression.count("(")
        closing = self.expression.count(")")

        if opening <= closing:

            return

        # Don't allow "(+" or "(×".
        if self.expression[-1] in {
            "+",
            "−",
            "×",
            "÷",
            "("
        }:

            return

        self.expression += ")"

        self.update_display()

    # ========================================================
    # TOGGLE SIGN
    # ========================================================

    def toggle_sign(self):

        if not self.expression:

            self.expression = "−"

            self.update_display()

            return

        # ----------------------------------------------------
        # If expression is a simple number.
        # ----------------------------------------------------

        if (
            self.expression.replace(
                ".",
                "",
                1
            ).isdigit()
        ):

            if self.expression.startswith("−"):

                self.expression = (
                    self.expression[1:]
                )

            else:

                self.expression = (
                    "−" + self.expression
                )

            self.update_display()

            return

        # ----------------------------------------------------
        # Find the last number.
        # ----------------------------------------------------

        operators = "+−×÷"

        end = len(
            self.expression
        )

        start = end

        while start > 0:

            if self.expression[
                start - 1
            ] in operators:

                break

            start -= 1

        number = self.expression[
            start:end
        ]

        if not number:

            return

        before = self.expression[:start]

        if before.endswith("−"):

            # Remove the unary minus.
            before = before[:-1]

        else:

            before += "−"

        self.expression = (
            before + number
        )

        self.update_display()

    # ========================================================
    # DELETE
    # ========================================================

    def delete(self):

        if self.just_calculated:

            self.expression = ""

            self.expression_var.set("")

            self.display_var.set("0")

            self.just_calculated = False

            return

        if self.expression:

            self.expression = (
                self.expression[:-1]
            )

        self.update_display()

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self):

        self.expression = ""

        self.last_result = None

        self.last_expression = ""

        self.just_calculated = False

        self.expression_var.set("")

        self.display_var.set("0")

    # ========================================================
    # CALCULATE
    # ========================================================

    def calculate(self):

        if not self.expression:

            return

        expression = self.expression

        # ----------------------------------------------------
        # Remove trailing operators.
        # ----------------------------------------------------

        while (
            expression
            and expression[-1] in {
                "+",
                "−",
                "×",
                "÷"
            }
        ):

            expression = expression[:-1]

        if not expression:

            return

        # ----------------------------------------------------
        # Close missing parentheses.
        # ----------------------------------------------------

        opening = expression.count("(")

        closing = expression.count(")")

        if opening > closing:

            expression += ")" * (
                opening - closing
            )

        try:

            result = CalculatorEngine.calculate(
                expression
            )

            formatted = self.format_number(
                result
            )

            # ------------------------------------------------
            # Save state.
            # ------------------------------------------------

            self.last_expression = expression

            self.last_result = result

            self.expression = formatted

            self.just_calculated = True

            # ------------------------------------------------
            # Update UI.
            # ------------------------------------------------

            self.expression_var.set(
                expression + " ="
            )

            self.display_var.set(
                formatted
            )

        except ValueError as error:

            self.expression_var.set(
                expression
            )

            self.display_var.set(
                str(error)
            )

            self.just_calculated = True

    # ========================================================
    # FORMAT NUMBER
    # ========================================================

    @staticmethod
    def format_number(number):

        if number == 0:

            return "0"

        # ----------------------------------------------------
        # Scientific notation for extremely large/small
        # numbers.
        # ----------------------------------------------------

        if (
            abs(number) >= 1e12
            or abs(number) < 1e-9
        ):

            return f"{number:.10g}"

        # ----------------------------------------------------
        # Integer
        # ----------------------------------------------------

        if float(number).is_integer():

            return f"{int(number):,}"

        # ----------------------------------------------------
        # Decimal
        # ----------------------------------------------------

        result = f"{number:,.10f}"

        result = result.rstrip("0")

        result = result.rstrip(".")

        return result

    # ========================================================
    # DISPLAY UPDATE
    # ========================================================

    def update_display(self):

        if self.expression:

            self.display_var.set(
                self.expression
            )

        else:

            self.display_var.set(
                "0"
            )

        # Remove old calculation information.
        if not self.just_calculated:

            self.expression_var.set(
                ""
            )

    # ========================================================
    # KEYBOARD SUPPORT
    # ========================================================

    def bind_keyboard(self):

        self.root.bind(
            "<Key>",
            self.keyboard_input
        )

    # ========================================================
    # KEYBOARD HANDLER
    # ========================================================

    def keyboard_input(self, event):

        key = event.keysym

        char = event.char

        # ----------------------------------------------------
        # Numbers
        # ----------------------------------------------------

        if char.isdigit():

            self.input_number(
                char
            )

            return

        # ----------------------------------------------------
        # Decimal
        # ----------------------------------------------------

        if char in {
            ".",
            ","
        }:

            self.input_decimal()

            return

        # ----------------------------------------------------
        # Operators
        # ----------------------------------------------------

        operator_map = {

            "+": "+",

            "-": "−",

            "*": "×",

            "/": "÷",

        }

        if char in operator_map:

            self.input_operator(
                operator_map[char]
            )

            return

        # ----------------------------------------------------
        # Percentage
        # ----------------------------------------------------

        if char == "%":

            self.input_percentage()

            return

        # ----------------------------------------------------
        # Parentheses
        # ----------------------------------------------------

        if char == "(":

            self.input_open_parenthesis()

            return

        if char == ")":

            self.input_close_parenthesis()

            return

        # ----------------------------------------------------
        # Enter / Return
        # ----------------------------------------------------

        if key in {
            "Return",
            "KP_Enter"
        }:

            self.calculate()

            return

        # ----------------------------------------------------
        # Backspace
        # ----------------------------------------------------

        if key == "BackSpace":

            self.delete()

            return

        # ----------------------------------------------------
        # Escape
        # ----------------------------------------------------

        if key == "Escape":

            self.clear()

            return

        # ----------------------------------------------------
        # Delete
        # ----------------------------------------------------

        if key == "Delete":

            self.clear()

            return


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CalculatorApp(
        root
    )

    root.mainloop()