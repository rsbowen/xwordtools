#Converts the output from QXW (https://www.quinapalus.com/qxw.html ) to a .puz file.
#To use, export two files from QXW:
#
# * The .qxw file
# * The .ans.txt file
#
# Then produce a file which are the clues you want, one clue per line, in the
# same order as the .ans.txt file. Probably you can do this by editing the
# .ans.txt file with your favorite text editor.

import argparse
import sys

sys.path.insert(0, './puzpy')
import puz

from qxwtool import ReadQXW

def OrderClues(clues, grid, rows, cols):
  across_clue_starts = [False] * rows*cols
  down_clue_starts = [False] * rows*cols
  num_across_clues = 0
  for row in xrange(rows):
    for col in xrange(cols):
      if grid[row*cols + col] == '.': continue
      if(row == 0 or grid[(row-1)*cols + col] == '.'):
        down_clue_starts[row*cols + col] = True
      if(col == 0 or grid[row*cols + (col-1)] == '.'):
        across_clue_starts[row*cols + col] = True
        num_across_clues += 1
  across_idx = 0 
  down_idx = num_across_clues

  clues_in_order = []
  for idx in range(rows*cols):
    if(across_clue_starts[idx]):
      clues_in_order.append(clues[across_idx])
      across_idx += 1
    if(down_clue_starts[idx]):
      clues_in_order.append(clues[down_idx])
      down_idx += 1
  return clues_in_order

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description = 'Convert a .qxw and .txt file to a .puz file')
  parser.add_argument('--qxwfile', metavar='q', type=str, help='Path to the .qxw file')
  parser.add_argument('--puzfile', metavar='p', type=str, help='Path to the output .puz file')
  parser.add_argument('--cluesfile', metavar='c', type=str, help="Path to the clues file")
  parser.add_argument('--author', metavar='a', type=str, help="Author")
  parser.add_argument('--title', metavar='t', type=str, help="Title")

  ns = parser.parse_args()

  (rows, cols, solution) = ReadQXW(ns.qxwfile)

  puzzle = puz.Puzzle()
  puzzle.solution = "".join(solution).upper()
  puzzle.height = rows
  puzzle.width = cols
  puzzle.fill = "".join([('.' if c=='.' else '-') for c in solution])
  clues = [s.strip() for s in file(ns.cluesfile).readlines()]
  puzzle.clues = OrderClues(clues, puzzle.fill, rows, cols)

  puzzle.author = ns.author
  puzzle.title = ns.title

  puzzle.save(ns.puzfile)
