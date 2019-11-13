A = [0] * 4

def binary(n):
  if n < 1:
    print(A)
  else:
    A[n-1] = 0
    binary(n-1)
    A[n-1] = 1
    binary(n-1)


def ks(n, k):
  if n < 1:
    print(A)
  else:
    for j in range(k):
      A[n-1] = j
      ks(n-1, k)

# binary(4)
ks(4, 2)
