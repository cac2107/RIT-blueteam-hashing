import time
import hasher

def main():
    hasher.initialize()
    hasher.get_all_hashes()
    iterations = 0
    while True:
        time.sleep(120)
        hasher.compare_hashes("hashes.csv")
        iterations += 1
        print("Compared:", iterations)

main()
