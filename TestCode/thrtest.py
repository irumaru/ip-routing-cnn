from concurrent.futures import ProcessPoolExecutor

def t1():
  a = 0
  while(True):
    a += 1
    a -= 1

def Main():
  with ProcessPoolExecutor(max_workers=2) as executor:
    for i in range(8):
      executor.submit(t1)
  
if __name__ == "__main__":
  Main()
