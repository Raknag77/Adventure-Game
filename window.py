import tkinter as tk
from tkinter.font import Font
from typing import overload, Union, Protocol
from dataclasses import dataclass
from enum import Enum
import threading


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


class CustomConsole:
    def __init__(self, root_):
        self.root = root_
        self.root.title("Custom Console")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Animation speed (characters per second)
        self.animation_speed = 0.05
        self._target_time = 10.0  # Default target time (seconds) for a message to print
        self._is_printing_normal: bool = False
        self._is_printing_instruction: bool = False
        self._normal_queue: list[Message] = []
        self._instruction_queue: list[Message] = []
        self._skip_animation: bool = False  # Skip animation flag
        self._user_input = None  # Holds user input
        self._input_ready_var = tk.BooleanVar(value=False)  # Variable to signal that the input is ready

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

        # Wait for all animations to finish before activating the input box
        while self._is_printing_normal or self._is_printing_instruction:
            print("Waiting for animations to finish...")
            self.root.update_idletasks()  # Process pending tasks
            self.root.update()  # Keep the GUI responsive

        self.input_box.configure(state="normal")  # Enable the input box
        self.input_box.focus_set()  # Focus the input box

        # Block the loop until the input is provided
        self._input_ready_var.set(False)  # Reset the variable
        while not self._input_ready_var.get():
            self.root.update_idletasks()  # Process pending tasks
            self.root.update()  # Keep the GUI responsive

        # Return the user's input
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

    @property
    def target_time(self) -> float:
        return self._target_time

    @target_time.setter
    def target_time(self, new_time: float):
        if new_time <= 0:
            raise ValueError("Target time must be greater than 0.")
        self._target_time = new_time

    def _process_next_message(self, area: tk.Text, queue: list[Message], is_printing_flag: str):
        """Process the next message in the queue."""
        if queue:
            next_message = queue[0]
            self._write_to_area(area, next_message, is_printing_flag)

    def _write_to_area(self, area: tk.Text, message: Message, is_printing_flag: str):
        """Write a message to the selected area."""
        if message.animated:
            self._animate_message(area, message, is_printing_flag)
        else:
            area.configure(state="normal")
            area.insert("end", message.text + "\n")
            area.see("end")
            area.configure(state="disabled")
            setattr(self, is_printing_flag, False)
            self._remove_message_from_queue(message.type)

    def _animate_message(self, area: tk.Text, message: Message, is_printing_flag: str):
        """Animate the message in the selected area."""
        area.configure(state="normal")

        # Calculate delay per character to fit within the target time
        dynamic_speed = min(self._target_time / max(len(message.text), 1), self.animation_speed)

        animation_done = threading.Event()

        def print_next_char(remaining_text: Union[str, Stringable]):
            if not remaining_text:  # If the message is fully printed
                area.insert("end", "\n")
                area.configure(state="disabled")
                setattr(self, is_printing_flag, False)
                self._remove_message_from_queue(message.type)
                animation_done.set()  # Signal that the animation is done
                return

            if self._skip_animation:
                area.insert("end", remaining_text)
                area.see("end")
                area.configure(state="disabled")
                setattr(self, is_printing_flag, False)
                self._remove_message_from_queue(message.type)
                animation_done.set()  # Signal that the animation is done
                self._skip_animation = False
                return
            # Print the next character
            area.insert("end", remaining_text[0])
            area.see("end")
            # Schedule the next character to be printed
            self.root.after(int(dynamic_speed * 1000), lambda: print_next_char(remaining_text[1:]))

        print_next_char(message.text)
        animation_done.wait()  # Wait for the animation to finish

    def _remove_message_from_queue(self, message_type: AreaType):
        """Remove a processed message from the appropriate queue."""
        if message_type == AreaType.TEXT:
            self._normal_queue.pop(0)
            self._process_next_message(self.text_area, self._normal_queue, "_is_printing_normal")
        elif message_type == AreaType.INSTRUCTION:
            self._instruction_queue.pop(0)
            self._process_next_message(self.instruction_area, self._instruction_queue, "_is_printing_instruction")

    def print(self,
              message: Union[str, Stringable],
              animated: bool = True,
              speed: Union[float, None] = None
              ):
        """Print a message to the console, optionally animating it."""
        self._normal_queue.append(Message(text=message, animated=animated, speed=speed or self.animation_speed))
        if not self._is_printing_normal:
            self._is_printing_normal = True
            self._process_next_message(self.text_area, self._normal_queue, "_is_printing_normal")

    def print_instruction(self,
                          message: Union[str, Stringable],
                          animated: bool = False,
                          speed: Union[float, None] = None
                          ):
        """Print a message to the instruction area, optionally animating it."""
        self._instruction_queue.append(Message(message, animated, speed or self.animation_speed, AreaType.INSTRUCTION))
        if not self._is_printing_instruction:
            self._is_printing_instruction = True
            self._process_next_message(self.instruction_area, self._instruction_queue, "_is_printing_instruction")

    def wait_and_exit(self):
        """Wait for all messages to finish printing before exiting."""
        if self._is_printing_normal or self._is_printing_instruction:
            self.root.after(100, self.wait_and_exit)
        else:
            self.root.destroy()

    def clear(self, area: AreaType):
        """Clear the console."""
        area = getattr(self, f"{area.value}_area")

        area.configure(state="normal")
        area.delete("1.0", "end")
        area.configure(state="disabled")

    def key_listener(self, event: tk.Event):
        """Handle key press events."""
        if event.keysym == "space" and (self._is_printing_normal or self._is_printing_instruction):
            self._skip_animation = True
        if event.char == "q":  # Quit on 'q'
            self.print("Exiting... Goodbye!", animated=True)
            self.print_instruction("Closing...", animated=True)
            self.wait_and_exit()
        elif event.char == "c":  # Clear the console on 'c'
            self.clear(AreaType.TEXT)
            self.clear(AreaType.INSTRUCTION)



# Run the console
if __name__ == "__main__":
    root = tk.Tk()
    console = CustomConsole(root)
    console.print("Welcome to the custom console!", animated=True)
    console.print_instruction("Press 'q' to quit!", animated=True)
    root.mainloop()

