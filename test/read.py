import sys
import os
import io
import time

stdin_raw = sys.stdin.buffer.raw
os.set_blocking(stdin_raw.fileno(), False)
stdin_buffer = io.BufferedReader(stdin_raw)
print(repr(stdin_buffer))
for _ in range(20):
    try:
        print(repr(stdin_buffer.read()))
    except Exception as exc:
        print(repr(exc))
    time.sleep(0.1)
