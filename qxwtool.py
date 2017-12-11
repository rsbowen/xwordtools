# (Hacky) tools for reading the .qxw file.

# example line with the puzzle size
# GP 0 15 15 2 0 0

# example line with a letter square
# SQ 0 0 0 0 0 H

# example line with a black square
# SQ 3 0 0 0 1  


def ReadQXW(path):
  f = file(path)

  rows = 0;
  cols = 0;
  letters = []

  # no checks for well-formedness!
  for line in f.readlines():
    values = line.strip().split(" ")
    if values[0] == "GP":
      rows = int(values[2])
      cols = int(values[3])
      letters = ["" for i in range(rows*cols)]
      continue
    if values[0] == "SQ":
      row = int(values[2])
      col = int(values[1])
      if int(values[5]) ==  0:
        letters[row*cols + col] = values[6]
      else:
        letters[row*cols + col] = "."
  return (rows, cols, letters)
