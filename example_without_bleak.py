"""

Simple keyboard reading example without Bleak

"""

import asyncio
import signal

from aiokeyboard import async_input_requiring_enter, async_input_without_enter_needed


async def main():
    print("Running example needing a Enter to confirm key/string")
    while True:
        key = await async_input_requiring_enter()
        if key == 'q':
            break


async def main2():
    print("Running example which reacts to key presses.")
    print("*** Note that this will prevent usage of Ctrl-C! ***")

    # --- This part does not do anything while listening to keyboard.
    keyboard_interrupt_event = asyncio.Event()
    signal.signal(
        signal.SIGINT,
        lambda *args: keyboard_interrupt_event.set()
    )
    # ---------------------------------------------------------------
    while True:
        if keyboard_interrupt_event.is_set():
            break
        key = await async_input_without_enter_needed()
        if key == b'q':
            break
        # This corresponds to the Ctrl-C combination, if one wants to still use it to quit.
        # if key == b'\x03':
        #     keyboard_interrupt_event.set()
        #     # Or just break


asyncio.run(main())
asyncio.run(main2())

