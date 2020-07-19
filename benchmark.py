import timeit

def main():
    N_times = 1
    print("=== No multi processing, no persistent connection ===")
    print(timeit.timeit("main_2()", setup="from generate_dataset import main_2", number= N_times))
          
    print("=== No multi processing, persistent connection ===")
    print(timeit.timeit("main_2()", setup="from generate_dataset_persistent_http import main_2", number= N_times))

main()
