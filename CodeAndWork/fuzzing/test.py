import time
import signal
import subprocess



def test():
    x = 0
    while 1:
        print(x)
        x += 1

        time.sleep(5)

def clean(*args):
    print("bye bye")
    exit(1)


if __name__ == "__main__":

    signal.signal(signal.SIGTERM, clean)
    signal.signal(signal.SIGINT, clean)
    test()