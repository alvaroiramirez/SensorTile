"""

Some examples on how to read keyboard presses in asyncio and no extra dependencies.

Using a ThreadPoolExecutor from the (amazing) pre-asyncio concurrency builtin module ``concurrent.futures``,
one can create a separate thread to listen to keyboard input and not block the asyncio processing.

"""

import asyncio
import platform
from concurrent.futures import ThreadPoolExecutor
win_encoding = "mbcs"
XE0_OR_00 = "\x00\xe0"

if platform.system() == "Windows":
    import msvcrt
else:
    import tty
    import sys
    import termios

__all__ = ["async_input_requiring_enter", "async_input_without_enter_needed"]


async def async_input_requiring_enter(prompt: str = ""):
    """Gets input from stdin while allowing notifications. Echos to the screen.

    This will not stop e.g. Ctrl-C, but it will allow multiple characters to be read.

    Works in Windows, Linux and macOS.

    Returns:

        str: The string entered.

    """
    with ThreadPoolExecutor(1, "ainput") as executor:
        print("Waiting for input...")
        value = await asyncio.get_event_loop().run_in_executor(executor, input, prompt)
        value = value.rstrip()  # Remove trailing whitespace and newlines.
        print(f"Got {value}")
        return value


def _win_getch():
    """Get a single character on Windows.

    This method is appropriated from the readchar library (https://github.com/magmax/python-readchar).

    Returns:

        bytes: The key pressed as a binary string.

    """

    while msvcrt.kbhit():
        msvcrt.getch()
    ch = msvcrt.getch()
    while ch.decode(win_encoding) in XE0_OR_00:
        msvcrt.getch()
        ch = msvcrt.getch()
    return ch


def _unix_getch():
    """Turning stdin into a TeleTypewriter (ttl) and reading only one byte from it.

    This method is appropriated from the readchar library (https://github.com/magmax/python-readchar).

    Returns:

        bytes: The key pressed as a binary string.


    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        # The ttl return a string, but I encode it to binary to be identical to the Windows version.
        ch = sys.stdin.read(1).encode("ascii")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# Setting a "_getch" alias to the method appropriate to the current OS.
if platform.system() == "Windows":
    _getch = _win_getch
else:
    _getch = _unix_getch


async def async_input_without_enter_needed(message = None):
    """Gets a single character from standard input.  Does not echo to the screen.
    Using the Unix ``termios`` module.

    **Note that this will stop e.g. Ctrl-C as well!**

    Returns:

          bytes - The key pressed as a binary string.

    """
    with ThreadPoolExecutor(1, "ainput") as executor:
        if message != None:
            print(message)

        value = await asyncio.get_event_loop().run_in_executor(executor, _getch)  # This will use the aliased method.
        # print(f"Got {value}")
        return value.rstrip()
