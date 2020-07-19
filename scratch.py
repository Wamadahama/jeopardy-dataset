import multiprocessing


def f(x,y):
    print(x+y)
    return x + y

if __name__ == '__main__':
    pool = multiprocessing.Pool(4)
    pool.starmap(f, [(1,2), (2,3), (4,5)])
    pool.close()
