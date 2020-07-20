import sys
import os
import io
import time

# stdin_raw = sys.stdin.buffer.raw
# os.set_blocking(stdin_raw.fileno(), False)
stdin_buffer = sys.stdin.buffer
print(repr(stdin_buffer))
print(stdin_buffer.isatty())
for _ in range(20):
    try:
        print(repr(stdin_buffer.read(2)))
    except Exception as exc:
        print(repr(exc))
    time.sleep(0.1)
