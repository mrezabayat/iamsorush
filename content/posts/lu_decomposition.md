---
title: "Code LU decomposition step by step in object oriented way in C#"
date: 2020-06-28T22:06:30+01:00
draft: false
image: /images/matrix.webp
thumbnail: /images/matrix_tn.webp
jqmath: true
---
## Introduction

In this post I want to revisit PLU or LU decomposition or factorisation, which is used to find unknowns of a system of linear equations, for two reasons. Firstly to recode it in an object oriented way to use it in my C# projects and secondly to refresh myself on the topic. The library can be useful for you too as it is light and contains only LU decomposition not a whole math library of everything. I may only add a few solvers of linear system to it in future but nothing else.  

LU decomposition solves of a system of linear equations exactly (versus iteratively). It is similar to Gauss elimination technique with time complexity of O(N³). One advantage of LU decomposition over Gauss elimination is that decomposed matrices can be reused in cases that only matrix of constants changes.

If you search on the internet you will probably see many codes written in a procedural way. Unless you are very familiar with the topic, the codes needs a good amount of time to be understood. Here, I want to code PLU decomposition in an object oriented and clean way. I use some classes to encapsulate data, they can be extended, and an API will be exposed to user of the library. But for the sake of KISS principle, I won’t fit everything there. I try to have a clean code too, the functions will be short for readability and single responsibility.   Unfortunately, there is a trade-off between object oriented style and code speed which I talk about it in the summary section.

## Background  


Before going to coding, let’s refresh ourselves briefly on PLU decomposition.  A system of linear equations is defined as

$A X = B$             

where $A$ is the coefficient matrix, $X$ is the unknown matrix, and$B$is the constants matrix. This system can be solved using LU decomposition method. Matrix $A$ can be factorised as

$A = L U$         

where $L$ is lower matrix with all elements above diagonal zero and $U$ is upper matrix with all elements under diagonal zero. This way the system can be solved faster because we have

$L U X = B$                

we can first solve

$L Y = B$         

and then solve

$U X = Y$          

to find $X$. But what is $P$? In the first step of decomposition $A = LU$, most of the time we have to joggle lines to make sure diagonals are not zero. We record the final order of rows in $P$, permutation matrix. Then we can apply that to $B$ before solving $LY=B$. To make the code a little bit more memory efficient I will save both $L$ and $U$ matrices in $A$. I will explain it in detail in the example below.  

## Linear System Example

Here I solve an example step by step which help me to identify classes, functions and their relations.

$$[\table 4,4,5;3,2,2;1,3,1] [\table x_0;x_1;x_2] = [\table 27; 13;10]$$


### 1)	Only matrix $A$ is focused to be decomposed.

$$\table col0,col1,col2$$

$$A=[\table 4,4,5;3,2,2;1,3,1] \table row0;row1;row2 $$

* Make lower triangle zero to find $U$ matrix.  
* Inside the triangle, move column by column from left to right and from top to bottom.   
* First element, (row=1, col=0)=3, is focused.   
* Find diagonal element in the same column=>  Element(0,0)=4.   
* Find a multiplier that  
Focused element + multiplier × diagonal element = 0, so multiplier = - 3/4.   
* The multiplier is used to modify $A$ matrix as:   
Row of focused element = Row of focused element + multiplier × row of diagonal element,
therefore, $A$ is updated as row1 = row1 – 3/4 × row0


$$A=[\table 4,4,5;0 (3 /4),-1,-7 /4;1,3,1]$$


* Store the multiplier, as it is the element of lower matrix, $L$. It is shown in parenthesis in front of zero elements.
Do the same for the next element in the same column

$$A=[\table 4,4,5;0 (3 /4),-1,-7 /4;0 (1 /4),2,-1 /4]$$


I put emphasis again the numbers in parenthesis are negative of multipliers which are used to make those elements zero.

* When in this column, all lower elements are zero, go to next column, so column 1 is focused now.

* Before we continue, there is permutation step. The diagonal element, -1, is checked to make sure is the maximum absolute value compared to the rows below. If not, swap diagonal row with row of maximum of value. Here $|2|>|-1|$, so we swap row1 and row2

$$A=[\table 4,4,5;0 (1 /4),2,-1 /4;0 (3 /4),-1,-7 /4]$$


Record the change in a permutation matrix. For the sake of saving memory I record order of rows in a vector


$$P=[\table 0;2;1]$$


row0 didn’t change but row1 and row2 are swapped which are captured in $P$.

Now we can move on and make element(2,1) = -1 zero. With the same procedure explained above, row2 = row2 + 0.5 row1


$$A=[\table 4,4,5;0 (1 /4),2,-1 /4;0 (3 /4),0 (-1 /2),-15 /8]⇒ U$$


So now officially, $A$ is converted to $U$ matrix.

$$U=[\table 4,4,5;0,2,-1 /4;0,0,-15 /8]$$


And all the multipliers make $L$ matrix. Note $L$ matrix diagonals are one:

$$L=[\table 1,0,0;1 /4,1,0;3 /4,-1 /2,1]$$



### 2)	System is solved with forward and backward substitution.  

Apply row permutations, $P$, to $B$


$$B= [\table 27;10;13]$$  


Forward Substitution $LY=B$


$$L=[\table 1,0,0;1 /4,1,0;3 /4,-1 /2,1] [\table y_0;y_1;y2] = [\table 27;10;13]$$

$y_0 = 27$  

$ 1 /4 (27) + y_1 = 10  ⇒ y_1 = 3.25 $

$3 /4 (27) - 0.5 (3.25) + y_2 = 13    ⇒  y_2 = -5.625$

And a backward substitution $UX=Y$

$$[\table 4,4,5;0,2,-1 /4;0,0,-15 /8] [\table x_0;x_1;x_2]=[\table 27 ;3.25 ;-5.625]$$

$x_2 = -5.625 × (-8 /15) = 3$  
$2  x_1   –  1 /4 × 3 = 3.25    ⇒ x_1 = 2$   
$4 x₀ + 4×2 + 5 × 3 = 27   ⇒ x_0 = 1$   

## Code

Now we know the method, let’s write the code and start from bottom to top. From previous section, decomposition and substitution stages are two independent steps. So we can associate each with a class. The decomposition class is

``` c#
public class PluDecomposer
{
  private double[,] A;
  private int[] P;


  private SubMatrixBoundariess LowerTriangleBounds;
  private int numberOfColumns;
  private int numberOfRows;
…
}
```

`LowerTriangleBounds`, `numberOfColumns`, `numberOfRows` are variables to make the code readable so I don’t need to write comments about them.
The constructor is as below.

``` c#
public PluDecomposer(double[,] A)
{
  this.A = A;

  numberOfRows = A.GetLength(0);
  numberOfColumns = A.GetLength(1);

  InitializePWithRowNumbers();

  LowerTriangleBounds = new SubMatrixBoundariess()
  {
      StartColumn = 0,
      EndColumn = A.GetLength(1) - 1,
      StartRow = 1,
      EndRow = A.GetLength(0)

  };
}
```

$A$ is injected and all the related parameters are set. $P$ is initialized as no row is permuted.

``` c#
private void InitializePWithRowNumbers()
{
  P = new int[numberOfRows];
  for (int row = 0; row < numberOfRows; row++)
  {
    P[row] = row;
  }
}
```

Here, is the what want from this class: find $P$ and combined $LU$ matrix.

``` c#
public (int[], double[,]) FindPAndCombinedLU()
{
    ConvertAtoLU();
    return (P, A);
}
```

As you can see, I don’t need to put comment as everything is clear: first convert $A$ to $LU$ then return $P$ and $LU$ (formerly $A$).

How the conversion done? The lower triangle should become zero so we have $U$ matrix. And because we want to have a compact matrix, the zeros of $U$ filled with $L$.

``` c#
private void ConvertAtoLU()
{
  MakeLowerTriangleZeroAndFillWithL();
}
```

To do so, we iterate over columns of lower triangle. First we make sure, the diagonal element is the maximum in the focused column then make the column zero.

``` c#
private void MakeLowerTriangleZeroAndFillWithL()
{
  for (int column = LowerTriangleBounds.StartColumn; column < LowerTriangleBounds.EndColumn; column++)
  {
      MakeSureDiagonalElementIsMaximum (column);
      MakeColumnZero(column);
  }
}
```

In each column first, we swap the row of diagonal element with the row which has the maximum element.

``` c#
private void MakeSureDiagonalElementIsMaximum (int focusedColumn)
{

  var rowOfDiagonal = focusedColumn;
  var rowOfMaxElement = GetRowOfMaxElementUnderDiagonal(focusedColumn);

  if (rowOfMaxElement != rowOfDiagonal)
  {
      SwapRows(rowOfMaxElement, rowOfDiagonal);
  };

}
```

Details of how we find the row which has maximum element under diagonal element is shown below.

``` c#
private int GetRowOfMaxElementUnderDiagonal(int focusedColumn)
{
  var rowOfDiagonal = focusedColumn;
  var columnOfDiagonal = focusedColumn;
  var rowAfterDiagonal = rowOfDiagonal + 1;

  double maxElement = A[rowOfDiagonal, columnOfDiagonal];
  int rowOfMaxElement = rowOfDiagonal;

  for (int row = rowAfterDiagonal; row < numberOfRows; row++)
  {
    if (Math.Abs(A[row, focusedColumn]) > maxElement)
    {
        maxElement = Math.Abs(A[row, focusedColumn]);
        rowOfMaxElement = row;
    }
  }
  return rowOfMaxElement;
}
```

If we have to swap rows, we use below method, and record it in $P$.

``` c#
private void SwapRows(int row1, int row2)
{
  for (int column = 0; column < numberOfColumns; column++)
  {
    var tmp = A[row1, column];
    A[row1, column] = A[row2, column];
    A[row2, column] = tmp;
  }
  RecordSwap(row1, row2);
}
```
We record the swap in $P$.

``` c#
private void RecordSwap(int row1, int row2)
{
    var tmp = P[row1];
    P[row1] = P[row2];
    P[row2] = tmp;
}
```

Now how we can make the column zero. Remember, we make only lower triangle zero, so we focus on rows under diagonal element. All the rows are iterated and the corresponding element made zero and then replaced with $L$ matrix value.

``` c#
private void MakeColumnZero(int column)
{
  int rowUnderDiagonalElement = column + 1;
  for (int row = rowUnderDiagonalElement; row < LowerTriangleBounds.EndRow; row++)
  {
    MakeElementZeroAndFillWithLowerMatrixElement(row, column);
  }
}
```

So we broke the whole process into separate steps to reach a point we focus only on one element. The process is exactly the same as what I explained in the previous section.        

``` c#
private void MakeElementZeroAndFillWithLowerMatrixElement(int elementRow, int elementColumn)
{
  var element = A[elementRow, elementColumn];
  var sameColumnDiagonalElement = A[elementColumn, elementColumn];

  var rowMultiplier = -element / sameColumnDiagonalElement;

  for (int col = elementColumn; col < numberOfColumns; col++)
  {
    A[elementRow, col] += rowMultiplier * A[elementColumn, col];
  }

  var lowerMatrixElement = - rowMultiplier;
  A[elementRow, elementColumn] = lowerMatrixElement;
}
```

I used dummy variables like ` sameColumnDiagonalElement` and ` lowerMatrixElement` so the code be easily readable without comments. Since I don’t assume the reader of this code has knowledge of legacy codes, I do not implement i, j, or k variables as iterators but use meaningful words like row and column. The loop boundaries are set by variables which exactly explain what they are rather than being puzzles to be discovered.
Now, the class for finding $X$ is defined as below

``` c#
public class XFinder
{
  private double[,] lu;
  private double[] b;
  private double[] y;
  private double[] x;
  private readonly int[] p;

  private readonly int numberOfRows;
  private readonly int numberOfColumns;
…
}
```

The constructor accepts compact $LU$, $P$ and $B$. Their reference is stored in this class. `numberOfRows` and `numberOfColumns` are helper variables for readability. $X$ is the matrix of unknowns, $Y$ is the helper matrix defined in the previous section.

``` c#
public XFinder(double[,] lu, int[] p, double[] b)
{
  this.lu = lu;
  this.p = p;
  this.b = b;

  numberOfRows = lu.GetLength(0);
  numberOfColumns = lu.GetLength(1);

  y = new double[numberOfRows];
  x = new double[numberOfRows];
}
```

Users have access to `Solve` method which returns the solutions, $X$. I created functions in the order we need to solve the problem.$B$is reoredered, $Y$ is found from $LY=B$, $X$ is found from UX=Y, and finally $X$ is checked to see if it is valid. What I wrote is in this paragraph are exactly the name of methods. Because of that no comments added to the code.

``` c#
public double[] Solve()
{
  ReorderB();
  SolveYfromLYequalB();
  SolveXfromUXequalY();
  CheckXIsValid();
  return x;
}
```

$B$ is reordered according to $P$.

``` c#
private void ReorderB()
{
  double[] reorderedB = new double[b.Length];

  for (int row = 0; row < numberOfRows; row++)
  {
    reorderedB[row] = b[p[row]];
  }

  for (int row = 0; row < numberOfRows; row++)
  {
    b[row] = reorderedB[row];
  }
}
```

$Y$ is found using forward substitution mentioned in the previous section.

``` c#
void SolveYfromLYequalB()
{
  for (int row = 0; row < b.Length; row++)
  {
    double sum = 0;
    var columnOfDiagonal = row;
    for (int column = 0; column < columnOfDiagonal; column++)
    {
      sum += y[column] * lu[row, column];
    }
    y[row] = b[row] - sum;
  }
}
```

And a backward substitution to find $X$.


``` c#
void SolveXfromUXequalY()
{
  for (int row = y.Length - 1; row > -1; row--)
  {
    double sum = 0;
    var columnOfDiagonal = row;

    for (int column = columnOfDiagonal + 1; column < x.Length; column++)
    {
      sum += x[column] * lu[row, column];
    }
    x[row] = (y[row] - sum) / lu[row, row];
  }
}
```

Here I check if $X$ is a valid solution by checking there is not a `Nan` in it. You can add more conditions inside this function without effecting other part of the code.

``` c#
private void CheckXIsValid()
{
  for (int row = 0; row < x.Length; row++)
  {
    if (double.IsNaN(x[row]))
    {
      throw new Exception("Error: No solution for this, AX=B, system found.");
    }
  }
}
```


And lastly the API which is exposed to users of this library. It contains $A$, $B$, and the instances of decomposer and `XFinder`. Users only need to inject $A$ and $B$ in the constructor. The decomposer needs only $A$ to be initialized.  

``` c#
public class Solver
{
  private double[,] A;
  private double[] B;
  private PluDecomposer pluDecomposer;
  private XFinder xFinder;

  public Solver(double[,] A, double[] B)
  {
    this.A = A;
    this.B = B;

    pluDecomposer = new PluDecomposer(A);
  }
…}
```

The second method which users are interested is `SolveX` to get the solution. First we ask the decomposer to find $P$ and compact $LU$. Then they along $B$ are injected to `XFinder`. `XFinder` returns the solution.

``` c#
public double[] SolveX()
{
  (var p, var lu)=pluDecomposer.FindPAndCombinedLU();
  xFinder = new XFinder(lu, p, B);

  return xFinder.Solve();
}
```


## Summary

In this post, I coded LU decomposition in C# to have a stand-alone library. It is lightweight because it doesn’t include other non-related math stuff. You can implement it in lightweight projects like Blazor client side app.

I tried to make it more readable: small methods are created and their names explain what they do. Dummy variables are used to clear up ambiguous parts of the code.

The code has a simple API which accepts $A$ and $B$ matrices and returns the solution.

I should note breaking numerical stages into small functions usually decreases speed of the code. Because function calls carry computational overheads. Moreover, functions usually hide the details which can help compilers to optimise the executables. Of course, these points depend on the language and compilers.
