import time


def gen():
    counter = 0
    while counter < 10:
    # while True:
        yield counter
        counter += 1


def main():
    print("Process started")
    g = gen()
    for i in range(10, 19):
        print(f"Step {i} returned {next(g)}")
        time.sleep(.05)
    print("Process complete")


if __name__ == "__main__":
    main()

