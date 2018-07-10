from spider import price
import time


def main():
    start = time.time()
    price.run()
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()