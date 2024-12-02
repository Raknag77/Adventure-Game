import tkinter as tk
from threading import Thread
from tkinter.font import Font
from typing import Callable, Literal, overload, Union, Protocol
from dataclasses import dataclass, field
from enum import Enum



class AreaType(Enum):
    TEXT = "text"
    INSTRUCTION = "instruction"


class Stringable(Protocol):
    def __str__(self) -> str:
        """Return a string representation of the object."""
        ...

@dataclass
class Message:
    _text: str
    animated: bool = False
    speed: Union[float] = None
    type: AreaType = AreaType.TEXT

    @overload
    def __init__(self, text: str, animated: bool = False, speed: Union[float, None] = None, _type: AreaType = AreaType.TEXT):
        ...

    @overload
    def __init__(self, text: Stringable, animated: bool = False, speed: Union[float, None] = None, _type: AreaType = AreaType.TEXT):
        ...

    def __init__(self, text, animated=False, speed=None, _type=AreaType.TEXT):
        self._text = str(text)
        self.animated = animated
        self.speed = speed
        self.type = _type

    @property
    def text(self) -> str:
        return self._text

@dataclass
class _ConStatus:
    areaLiteral = Literal["text", "inst"]

    printing_text: bool = False
    printing_inst: bool = False

    # Use BooleanVars for synchronization
    text_done_var: tk.BooleanVar = field(init=False)
    inst_done_var: tk.BooleanVar = field(init=False)

    input_ready_var: tk.BooleanVar = field(init=False)

    skip_text_animation: bool = False
    skip_inst_animation: bool = False

    def __post_init__(self):
        self.text_done_var = tk.BooleanVar(value=True)  # Default to True (nothing printing)
        self.inst_done_var = tk.BooleanVar(value=True)
        self.input_ready_var = tk.BooleanVar(value=False)  # Initially, input is not ready

    def skip_animations(self):
        self.skip_text_animation = True
        self.skip_inst_animation = True

    @property
    def is_printing(self) -> bool:
        return self.printing_text or self.printing_inst


class CustomConsole:
    def __init__(self, root_: tk.Tk):
        self.root = root_
        self.root.title("Custom Console")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Animation speed (characters per second)
        self.animation_speed = 0.05
        self._target_time = 10.0  # Default target time (seconds) for a message to print
        self._normal_queue: list[Message] = []
        self._instruction_queue: list[Message] = []
        self._user_input = None  # Holds user input

        self._status = _ConStatus()
        # self._is_printing_normal: bool = False
        # self._is_printing_instruction: bool = False
        # self._skip_animation: bool = False  # Skip animation flag
        # self._input_ready_var = tk.BooleanVar(value=False)  # Variable to signal that the input is ready
        # self._instr_ready_var = tk.BooleanVar(value=False)  # Variable to signal that the instruction is ready
        # self._print_ready_var = tk.BooleanVar(value=False)  # Variable to signal that the print is ready

        # Custom font
        self.console_font = Font(family="Courier New", size=12)

        # Text display area
        self.text_area = tk.Text(
            self.root,
            bg="black",
            fg="white",
            font=self.console_font,
            wrap="word",
            state="disabled",
        )
        self.text_area.pack(fill="both", expand=True, padx=5, pady=(5, 40))

        # Input box
        self.input_box = tk.Entry(
            self.root,
            bg="black",  # Match the background color
            fg="white",  # Text color
            font=self.console_font,  # Match the font style
            insertbackground="black",  # Cursor color
            disabledbackground="black",  # Background colour when disabled
            state="disabled"  # Initially disabled
        )
        self.input_box.pack(fill="x", padx=5, pady=(5, 5), ipady=5)  # Fill horizontally and adjust height
        self.input_box.bind("<Return>", self._submit_input)

        # Instruction area
        self.instruction_area = tk.Text(
            self.root,
            bg="black",
            fg="yellow",
            font=self.console_font,
            wrap="word",
            state="disabled"
        )
        self.instruction_area.pack(fill="x", pady=5, expand=True)

        # Input tag styling for "You: your_input"
        self.text_area.tag_configure("user_input", foreground="green")

        # Input handler
        self.root.bind("<KeyPress>", self.key_listener)

        # Block keyboard and mouse input for text box and instructions box
        self.text_area.bind("<Key>", lambda e: "break")  # Block keyboard input
        self.text_area.bind("<Button-1>", lambda e: "break")  # Block mouse clicks

        # Block user input for the instruction area
        self.instruction_area.bind("<Key>", lambda e: "break")
        self.instruction_area.bind("<Button-1>", lambda e: "break")

    def input(self, prompt: str) -> str:
        """Block the input function until the user provides input."""
        # Print the prompt
        self.print("+GM: " + prompt)

        # Wait for all animations to finish
        if not self._status.text_done_var:
            print("Waiting for prompt to finish printing..." + str(self._status.text_done_var.get()))
            self.root.wait_variable(self._status.text_done_var)
        print("Prompt finished printing.")
        # Activate the input box
        self.input_box.configure(state="normal")  # Enable the input box
        self.input_box.focus_set()  # Focus the input box

        # Clear and wait for the input-ready variable
        self._status.input_ready_var.set(False)
        self.root.wait_variable(self._status.input_ready_var)

        return self._user_input

    def _submit_input(self, event: tk.Event):
        """Handle input submission."""
        user_input = self.input_box.get().strip()

        # Handle empty input with a default value
        if not user_input:
            user_input = ""

        # Insert the user's input into the text area
        self.text_area.configure(state="normal")
        self.text_area.insert("end", f"You: {user_input}\n", "user_input")
        self.text_area.see("end")
        self.text_area.configure(state="disabled")

        # Clear and disable the input box
        self.input_box.delete(0, "end")
        self.input_box.configure(state="disabled")

        # Notify that the input is ready
        self._user_input = user_input
        self._status.input_ready_var.set(True)

    @property
    def target_time(self) -> float:
        return self._target_time

    @target_time.setter
    def target_time(self, new_time: float):
        if new_time <= 0:
            raise ValueError("Target time must be greater than 0.")
        self._target_time = new_time

    def _process_next_message(self, area: tk.Text, queue: list[Message], area_flag: _ConStatus.areaLiteral):
        """Process the next message in the queue."""
        if queue:
            next_message = queue[0]
            self._write_to_area(area, next_message, area_flag)

    def _write_to_area(self, area: tk.Text, message: Message, area_flag: _ConStatus.areaLiteral):
        """Write a message to the selected area."""
        if message.animated:
            self._animate_message(area, message, area_flag)
        else:
            area.configure(state="normal")
            area.insert("end", message.text + "\n")
            area.see("end")
            area.configure(state="disabled")
            setattr(self._status, f"printing_{area_flag}", False)
            self._remove_message_from_queue(message.type)

    def _animate_message(self, area: tk.Text, message: Message, area_flag: _ConStatus.areaLiteral):
        """Animate the message in the selected area."""
        area.configure(state="normal")

        # Calculate delay per character to fit within the target time
        dynamic_speed = min(self._target_time / max(len(message.text), 1), self.animation_speed)

        def disable_area():
            area.see("end")
            area.configure(state="disabled")
            setattr(self._status, f"printing_{area_flag}", False)

            # Signal that the animation is complete
            if area_flag == "text":
                self._status.text_done_var.set(True)
            elif area_flag == "inst":
                self._status.inst_done_var.set(True)

            self._remove_message_from_queue(message.type)

        def print_next_char(remaining_text: Union[str, Stringable]):
            """Print the next character in the message."""
            if not remaining_text:  # If the message is fully printed
                area.insert("end", "\n")
                disable_area()
                return

            if getattr(self._status, f"skip_{area_flag}_animation"):
                area.insert("end", remaining_text)
                disable_area()
                setattr(self._status, f"skip_{area_flag}_animation", False)
                return

            # Print the next character
            area.insert("end", remaining_text[0])
            area.see("end")

            # Schedule the next character to be printed
            self.root.after(int(dynamic_speed * 1000), lambda: print_next_char(remaining_text[1:]))

        # Clear the variable and start the animation
        if area_flag == "text":
            self._status.text_done_var.set(False)
        elif area_flag == "inst":
            self._status.inst_done_var.set(False)

        print_next_char(message.text)

    def _remove_message_from_queue(self, message_type: AreaType):
        """Remove a processed message from the appropriate queue."""
        if message_type == AreaType.TEXT:
            self._normal_queue.pop(0)
            self._process_next_message(self.text_area, self._normal_queue, "text")
        elif message_type == AreaType.INSTRUCTION:
            self._instruction_queue.pop(0)
            self._process_next_message(self.instruction_area, self._instruction_queue, "inst")

    def print(self,
              *message: Union[str, Stringable],
              animated: bool = True,
              speed: Union[float, None] = None):
        """Print a message to the console, optionally animating it."""
        message = " ".join(map(str, message))
        self._normal_queue.append(Message(text=message, animated=animated, speed=speed or self.animation_speed))
        if not self._status.printing_text:
            self._status.printing_text = True
            self._process_next_message(self.text_area, self._normal_queue, "text")

        # Wait for the animation to finish
        self.root.wait_variable(self._status.text_done_var)

    def print_instruction(self,
                          *message: Union[str, Stringable],
                          animated: bool = False,
                          speed: Union[float, None] = None
                          ):
        """Print a message to the instruction area, optionally animating it."""
        message = " ".join(map(str, message))
        self._instruction_queue.append(Message(message, animated, speed or self.animation_speed, AreaType.INSTRUCTION))
        if not self._status.printing_inst:
            self._status.printing_inst = True
            self._process_next_message(self.instruction_area, self._instruction_queue, "inst")

        # Wait for the animation to finish
        self.root.wait_variable(self._status.inst_done_var)

    def wait_and_exit(self):
        """Wait for all messages to finish printing before exiting."""

        if self._status.is_printing:
            print(
                f"Waiting... Is printing normal: {self._status.printing_text}, "
                f"Is printing instruction: {self._status.printing_inst}")
            self.root.after(100, self.wait_and_exit)
        else:
            print("Exiting the program.")
            self.root.destroy()

    def clear(self, area: AreaType):
        """Clear the console."""
        area = getattr(self, f"{area.value}_area")

        area.configure(state="normal")
        area.delete("1.0", "end")
        area.configure(state="disabled")

    def key_listener(self, event: tk.Event):
        """Handle key press events."""

        if event.keysym == "space" and self._status.is_printing:
            self._status.skip_animations()
        if event.char == "q":  # Quit on 'q'
            self.print("Exiting... Goodbye!", animated=True)
            self.print_instruction("Closing...", animated=True)
            self.wait_and_exit()
        elif event.char == "c":  # Clear the console on 'c'
            self.clear(AreaType.TEXT)
            self.clear(AreaType.INSTRUCTION)

    @classmethod
    def run(cls, func: Callable[["CustomConsole"], None]) -> None:
        """
        Run the GUI console with the provided function.
        :param func: The main function from your script.
        Note that it must take a CustomConsole as the first parameter.
        E.g., def main (con: CustomConsole) -> None:
        :return: None
        """
        root = tk.Tk()
        _console = cls(root)
        Thread(target=func, args=[_console]).start()
        root.mainloop()

def main(con: CustomConsole) -> None:
    con.print("Welcome to the custom console!", animated=True)
    con.print_instruction("Press 'q' to quit!", animated=True)

# Run the console
if __name__ == "__main__":
    CustomConsole.run(main)
