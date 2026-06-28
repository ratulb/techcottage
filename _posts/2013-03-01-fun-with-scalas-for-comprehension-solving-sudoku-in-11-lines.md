---
layout: post
title: "Fun with scala's for comprehension: Solving sudoku in 11 lines!"
date: 2013-03-01 16:12:00.001+00:00
tags: []
---

Scala's for loop\(comprehension\) may look deceptively similar to java's for loop, but it is much more powerful than java's for loop. While java's for loop is just to repeat some computation for specified number of times, scala's for comprehension has a mathematical underpining to it. They are analogous to set comprehensions, which are normally used for building more specific sets out of general sets. Shown below is a basic set comprehension of 10 even natural numbers.

  
**  S = \{2\*x; x <\- N; x <= 10\}**  
  


The first part **2\*x** is called the output, **N** is the input set and **x <= 10** is the predicate filter. The same translated to for comprehension along with output is shown below:

  


scala> val s = for \{ 

     |  x <\- 1 to Integer.MAX\_VALUE

     |  if\(x <= 10\)

     | \} yield 2\*x

  


s: \(2, 4, 6, 8, 10, 12, 14, 16, 18, 20\)

  
**Problem: Given a positive integer n, find all the pairs of integers \(i,j\) such that 1 <= j < i < n, and i+j is a prime number.**  
  


Such combinatorial problems lend themselves to be solved beautifully with for comprehensions. Let's first define a function that tells us if a number is prime or not\!

  


We know a number is a prime if it's only divisors are 1 and the number itself. While in imperative style we would start out with how to do it, in functional style we state what the problem is\! So here goes our definition of isPrime.

  
scala> def isPrime\(n: Int\) = \(2 until n\).forall\(d => n % d \!= 0\)  
isPrime: \(n: Int\)Boolean  
  
  


Now, to find all the pairs of numbers such that each two elements of the pairs sum up to a prime number, we just make use of for comprehensions and the isPrime function defined above:

  


scala> def findPrimePairs\(n: Int\) = 

     |  for \{

     |   i <\- 1 until n

     |   j <\- 1 until i

     |   if isPrime\(i+j\)

     |  \} yield\(i,j\)

findPrimePairs: \(n: Int\) IndexedSeq\[\(Int, Int\)\]

  


scala> val primePairs = findPrimePairs\(10\)

primePairs: IndexedSeq\[\(Int, Int\)\] = Vector\(\(2,1\), \(3,2\), \(4,1\), \(4,3\), \(5,2\), \(6,1\), \(6,5\), \(7,4\), \(7,6\), \(8,3\), \(8,5\), \(9,2\), \(9,4\), \(9,8\)\)

  
Neat, elegant and concise.  
  
Let's try one more problem before we delve into solving sudoku in less than 11 line\!  
  
Let's try find the numbers **x,y,z** below **n** such that **x^2 + y^2 == z^2**. Let's call the function rightAngledNumbers\!  
  
scala> def rightAngledNumbers\(n: Int\) =   
     |  for \{  
     |   x <\- 1 until n  
     |   y <\- x+1 until n  
     |   z <\- y+1 until n  
     |   if\(x\*x + y\*y == z\*z\)  
     |  \} yield \(x,y,z\)  
  
rightAngledNumbers: \(n: Int\)IndexedSeq\[\(Int, Int, Int\)\]   
  
val result = rightAngledNumbers\(100\)  
  
result: = Vector\(\(3,4,5\), \(5,12,13\), \(6,8,10\), \(7,24,25\), \(8,15,17\), \(9,12,15\), \(9,40,41\), \(10,24,26\), \(11,60,61\), \(12,16,20\), \(12,35,37\), \(13,84,85\), \(14,48,50\), \(15,20,25\), \(15,36,39\), \(16,30,34\), \(16,63,65\), \(18,24,30\), \(18,80,82\), \(20,21,29\), \(20,48,52\), \(21,28,35\), \(21,72,75\), \(24,32,40\), \(24,45,51\), \(24,70,74\), \(25,60,65\), \(27,36,45\), \(28,45,53\), \(30,40,50\), \(30,72,78\), \(32,60,68\), \(33,44,55\), \(33,56,65\), \(35,84,91\), \(36,48,60\), \(36,77,85\), \(39,52,65\), \(39,80,89\), \(40,42,58\), \(40,75,85\), \(42,56,70\), \(45,60,75\), \(48,55,73\), \(48,64,80\), \(51,68,85\), \(54,72,90\), \(57,76,95\), \(60,63,87\), \(65,72,97\)\)  
  


I am not sure how many lines of code will be needed, if we try to do the same thing in an imperative way\!

  


Now, let's get back to solving sudoku in 11 lines. Let me clarify here - though our main logic of solving sudoku is confined to only 11 lines, yet the whole program is hardly but 11 lines. That is because, we have to do things like read the input from a file, index the cells with row, column and cell value etc. Also, we have to check on which box an empty cell falls along with a helper function to tell us if a particular value is allowed in an empty cell. Barring these, actual logic is, indeed confined to 11 lines. Let's first define few type aliases and show the function with 11 lines which solves the problem.

  
**type Cell = \(Int,Int,Int\)**  
  


Cell represents a sudoku cell with **.\_1** being the **value** ,**.\_2** being the **row** and **.\_3**

being **column** of the cell.

  
**type Solutions = List\[List\[Cell\]\]**  
  


We can have more than one possible solution to a sudoku problem depending on how many cells are already filled in. That is why our **Solutions** type alias is List of List of Cells. Shown below is the function that solves the sudoku.

  
def fillCells\(emptyCells: List\[Cell\]\): Solutions = \{  
   if\(emptyCells == Nil\) List\(List\(\)\)  
   else \{  
   for \{  
     filledCells <\- fillCells\(emptyCells.init\)  
     cellValue <\- 1 to 9  
     cell = \(cellValue,emptyCells.last.\_2, emptyCells.last.\_3\)  
     if\(isOk\(cell, filledCells ::: nonEmpties\)\)     
    \} yield cell :: filledCells   
   \}\}  
  
  


**Explanation:** We first take all the empty cells. Out of these empty cells, take all but last one and call fillCells recursively, which in turn repeats the process until we hit the base case when we call fillCells\(Nil\) - this returns an empty list of list. Now call stack unfolds inside out, calling fillCells with one empty cell and trying fill that with one of the possible values in the range from 1 to 9 and checking if that value is ok\(isOk\) for that cell. If so, that cell is concatenated to the base case, giving us one partial solution. And process continues till we fill all the empty cells.

  


Shown below is couple of inputs and along with their solutions. The whole Sudoku code is to be found at:

  
**https://github.com/ratulb/sudoku/**  
  
**Problem 1:**  
  
1 9 0 2 0 0 8 0 0  
4 0 7 0 9 0 0 0 0  
0 3 0 0 0 1 4 0 0  
0 0 3 0 0 0 0 0 2  
9 8 0 0 0 0 0 7 3  
2 0 0 0 0 0 6 0 0  
0 0 5 3 0 0 0 1 0  
0 0 0 0 4 0 9 0 6  
0 0 9 0 0 6 0 5 4    
  
  
scala> val sol1: Sudoku.Solution = List\(List\(\(3,8,6\), \(8,8,4\), \(1,8,3\), \(2,8,1\), \(7,8,0\), \(2,7,7\), \(7,7,5\), \(5,7,3\), \(8,7,2\), \(1,7,1\), \(3,7,0\), \(8,6,8\), \(7,6,6\), \(9,6,5\), \(2,6,4\), \(4,6,1\), \(6,6,0\), \(9,5,8\), \(8,5,7\), \(5,5,5\), \(3,5,4\), \(4,5,3\), \(1,5,2\), \(7,5,1\), \(5,4,6\), \(2,4,5\), \(1,4,4\), \(6,4,3\), \(4,4,2\), \(4,3,7\), \(1,3,6\), \(8,3,5\), \(7,3,4\), \(9,3,3\), \(6,3,1\), \(5,3,0\), \(5,2,8\), \(9,2,7\), \(6,2,4\), \(7,2,3\), \(2,2,2\), \(8,2,0\), \(1,1,8\), \(6,1,7\), \(2,1,6\), \(3,1,5\), \(8,1,3\), \(5,1,1\), \(7,0,8\), \(3,0,7\), \(4,0,5\), \(5,0,4\), \(6,0,2\)\)\)  
  
**Problem 2:**  
  
0 0 6 9 0 0 3 0 1  
0 0 4 0 3 1 0 0 7  
2 0 0 0 0 0 0 6 0  
1 0 0 0 0 0 0 0 0  
0 2 0 7 0 3 0 8 0  
0 0 0 0 0 0 0 0 3  
0 4 0 0 0 0 0 0 2  
3 0 0 1 7 0 9 0 0  
8 0 9 0 0 2 1 0 0  
  
scala> val sol2 = Sudoku.solution  
sol2: Sudoku.Solution = List\(List\(\(6,8,8\), \(3,8,7\), \(4,8,4\), \(5,8,3\), \(7,8,1\), \(8,7,8\), \(4,7,7\), \(6,7,5\), \(2,7,2\), \(5,7,1\), \(7,6,7\), \(5,6,6\), \(9,6,5\), \(8,6,4\), \(3,6,3\), \(1,6,2\), \(6,6,0\), \(1,5,7\), \(7,5,6\), \(5,5,5\), \(9,5,4\), \(2,5,3\), \(8,5,2\), \(6,5,1\), \(4,5,0\), \(4,4,8\), \(6,4,6\), \(1,4,4\), \(5,4,2\), \(9,4,0\), \(5,3,8\), \(9,3,7\), \(2,3,6\), \(8,3,5\), \(6,3,4\), \(4,3,3\), \(7,3,2\), \(3,3,1\), \(9,2,8\), \(4,2,6\), \(7,2,5\), \(5,2,4\), \(8,2,3\), \(3,2,2\), \(1,2,1\), \(2,1,7\), \(8,1,6\), \(6,1,3\), \(9,1,1\), \(5,1,0\), \(5,0,7\), \(4,0,5\), \(2,0,4\), \(8,0,1\), \(7,0,0\)\)\)  
  
Following listing shows the complete sudoku code.   
  

    
    
    import io.Source
    object Sudoku {
      type Input = List[List[Int]]
      type Cell = (Int,Int,Int)
      type Solutions = List[List[Cell]]
     def readFile = {
      val lines = io.Source.fromFile("sudoku1.txt").getLines.toList
      lines.map { line => line.split(" ").toList.map(e => e.toInt)
     }
    }
     def solution = {
      val in = readFile
      val cells = index(in)
      val empties = emptyCells(cells)
      val nonEmpties = nonEmptyCells(cells)
      solve(empties,nonEmpties)
     }
     def solve(empties: List[Cell], nonEmpties: List[Cell]): Solutions = {
      //Actual logic
      def fillCells(emptyCells: List[Cell]): Solutions = {
       if(emptyCells == Nil) List(List())
       else {
       for {
         filledCells <- fillCells(emptyCells.init)
         cellValue <- 1 to 9
         cell = (cellValue,emptyCells.last._2, emptyCells.last._3)
         if(isOk(cell, filledCells ::: nonEmpties))
        } yield cell :: filledCells
       }
      }
      fillCells(empties)
     }
     def isOk(c:Cell, cells: List[Cell]) = {
      (colCells(c,cells) ::: rowCells(c,cells) ::: boxCells(c,cells)).forall(e => e._1 != c._1)
     }
     def colCells(c: Cell, cells: List[Cell]) = cells.filter(e => e._3 == c._3)
     def rowCells(c: Cell, cells: List[Cell]) = cells.filter(e => e._2 == c._2)
     def emptyCells(cells: List[Cell]) = cells.filter(e => e._1 == 0) 
    
    
     def nonEmptyCells(cells: List[Cell]) = cells.filterNot(e => e._1 == 0) 
    
    
     def boxCells(c: Cell, cells: List[Cell]) = {
      val inBox = cellAt(c)
      val filtered = inBox match {
        case 1 => cells.filter{e =>(e._2 < 3 && e._3 < 3)}
        case 2 => cells.filter{e =>(e._2 < 3 && (e._3 > 2 && e._3 < 6))}
        case 3 => cells.filter{e => (e._2 < 3 && e._3 > 5)}
        case 4 => cells.filter{e => ((e._2 > 2 && e._2 < 6) && e._3 < 3)}
        case 5 => cells.filter{e => ((e._2 > 2 && e._2 < 6) && (e._3 > 2 && e._3 < 6))}
        case 6 => cells.filter{e => ((e._2 > 2 && e._2 < 6) && (e._3 > 5))}
        case 7 => cells.filter{e => (e._2 > 5 && e._3 < 3)}
        case 8 => cells.filter{e => (e._2 > 5 && (e._3 > 2 && e._3 < 6))}
        case 9 => cells.filter{e => (e._2 > 5 && e._3 > 5)}
      }
     filtered
     }
     def index(in: Input) = in.zipWithIndex.map{r => r._1.zipWithIndex.map { c => (c._1, r._2, c._2) }}.flatMap(l => l) 
    
    
     def cellAt(c: Cell) = c match {
       case (_,x,y) if(x < 3 && y < 3) => 1
       case (_,x,y) if (x < 3 && ( y > 2 && y < 6)) => 2
       case (_,x,y) if (x < 3 && (y > 5 && y < 9)) => 3
       case (_,x,y) if ((x > 2 && x < 6) && y < 3) => 4
       case (_,x,y) if ((x > 2 && x < 6) && (y > 2 && y < 6)) => 5
       case (_,x,y) if ((x > 2 && x < 6) && (y > 5 && y < 9)) => 6
       case (_,x,y) if (x > 5 && y < 3) => 7
       case (_,x,y) if (x > 5 && (y > 2 && y < 6)) => 8
       case _ => 9
     }
    }

  
  
  


**Conclusion:** Scala's for comprehensions might look very ordinary - but they are not. They turn out to be extremely handy while trying to solve combinatorial problems like the ones shown above. Like many other constructs of functional programming, for comprehensions allow programmers to tackle complicated problems from a higher level of abstraction.

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2013/03/fun-with-scalas-for-comprehension-solving-sudoku-in-11-lines.html)*
