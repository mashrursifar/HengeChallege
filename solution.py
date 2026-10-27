import sys 

def solve(arr):

    val = arr[1:]
  
    
    if len(val) != int(arr[0]):
        print("xxxxxx")
        return -1

    num  = map(int, val)
    
    res = sum(map(lambda v:v**4, filter(lambda v:v <=0 , num)))

    return res
def rec(n,res):
    if n ==0:
        return res
    
    y = sys.stdin.readline().strip()
    y_n = sys.stdin.readline().strip()

    
    arr = [y]+y_n.split()
    res.append(solve(arr)) 
    
    return rec(n-1,res)
    
def main():
    n = int(sys.stdin.readline().strip())
    res = rec(n,[])
    print("\n".join(map(str, res)))


if __name__ == "__main__":
    main()