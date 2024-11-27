import tkinter as tk
from tkinter.font import Font
from typing import Union
from dataclasses import dataclass
from enum import Enum


class AreaType(Enum):
    TEXT = "text"
    INSTRUCTION = "instruction"


@dataclass
class Message:
    text: str
    animated: bool = False
    speed: Union[float] = None
    type: AreaType = AreaType.TEXT


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

        # Input handler
        self.root.bind("<KeyPress>", self.key_listener)

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

        def print_next_char(remaining_text: str):
            if not remaining_text:  # If the message is fully printed
                area.insert("end", "\n")
                area.configure(state="disabled")
                setattr(self, is_printing_flag, False)
                self._remove_message_from_queue(message.type)
                return

            # Print the next character
            area.insert("end", remaining_text[0])
            area.see("end")
            # Schedule the next character to be printed
            self.root.after(int(dynamic_speed * 1000), lambda: print_next_char(remaining_text[1:]))

        print_next_char(message.text)

    def _remove_message_from_queue(self, message_type: AreaType):
        """Remove a processed message from the appropriate queue."""
        if message_type == AreaType.TEXT:
            self._normal_queue.pop(0)
            self._process_next_message(self.text_area, self._normal_queue, "_is_printing_normal")
        elif message_type == AreaType.INSTRUCTION:
            self._instruction_queue.pop(0)
            self._process_next_message(self.instruction_area, self._instruction_queue, "_is_printing_instruction")

    def print(self, message: str, animated: bool = True, speed: Union[float, None] = None):
        """Print a message to the console, optionally animating it."""
        self._normal_queue.append(Message(text=message, animated=animated, speed=speed or self.animation_speed))
        if not self._is_printing_normal:
            self._is_printing_normal = True
            self._process_next_message(self.text_area, self._normal_queue, "_is_printing_normal")

    def print_instruction(self, message: str, animated: bool = False, speed: Union[float, None] = None):
        """Print a message to the instructions area, optionally animating it."""
        self._instruction_queue.append(Message(text=message, animated=animated, speed=speed or self.animation_speed, type=AreaType.INSTRUCTION))
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
        if event.char == "q":  # Quit on 'q'
            self.print("Exiting... Goodbye!", animated=True)
            self.print_instruction("Closing...", animated=True)
            self.wait_and_exit()
        elif event.char == "c":  # Clear the console on 'c'
            self.clear(AreaType.TEXT)
            self.clear(AreaType.INSTRUCTION)
        else:
            self.print(f"Key pressed: {event.char}", animated=True)



# Run the console
if __name__ == "__main__":
    root = tk.Tk()
    console = CustomConsole(root)
    console.print("Welcome to the custom console!", animated=True)
    console.print_instruction("Press 'q' to quit!", animated=True)
    root.mainloop()


# if __name__ == "__main__":
#     root = tkinter.Tk()
#     root.title("Adventure Game")
#     console = CustomConsole(root)
#     Thread(target=main, daemon=True).start()  # Start the Tkinter main event loop in a separate thread
#     root.mainloop()
