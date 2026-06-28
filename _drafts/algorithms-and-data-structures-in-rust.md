---
layout: post
title: "Algorithms and data structures in rust"
date: 2020-07-24 16:40:00+00:00
tags: [rust, algorithms, data structures]
---

use rand::Rng;

  


fn main\(\) \{

    let mut array: \[u8; 10\] = \[0; 10\];

    //Fill the array with random values

    rand::thread\_rng\(\).fill\(&mut array\);

  


    println\!\("Bubble sort ->"\);

    println\!\("Unsorted array \{:?\}", array\);

    bubble\_sort\(&mut array\);

    println\!\("Sorted array \{:?\}  ", array\);

  


    rand::thread\_rng\(\).fill\(&mut array\);

    println\!\("Selection sort ->"\);

    println\!\("Unsorted array \{:?\}", array\);

    selection\_sort\(&mut array\);

    println\!\("Sorted array \{:?\}  ", array\);

  


    rand::thread\_rng\(\).fill\(&mut array\);

    println\!\("Insertion sort ->"\);

    println\!\("Unsorted array \{:?\}", array\);

    selection\_sort\(&mut array\);

    println\!\("Sorted array \{:?\}  ", array\);

\}

  


pub fn bubble\_sort\(array: &mut \[u8\]\) \{

    //Take each element of the array - the range below is not inclusive of

    //last index i.e length of the array

    for i in 0..array.len\(\) \{

        //Start at the begining of the array, compare it with the next element

        //Swap if the current is less than the next element bubbling the next max

        //element to the index one less than the previous max element's index

        let mut swapped = false;

        for j in 0..array.len\(\) - 1 - i \{

            if array\[j\] > array\[j + 1\] \{

                swap\(array, j, j + 1\);

                swapped = true;

                //Swapping has taken place - in this current iteration of the inner

                //loop

            \}

        \}

        if \!swapped \{

            //No sawpping has taken place - array is all sorted by now - no more

            //iteration of the outer loop is required - break out of outer loop to

            //avoid unnecessary iteration.

            break;

        \}

    \}

\}

  


/\*

Space complexity: log\(1\) - since the sorting happens in place without the use of any

extra space.

  


Time complexity: In the worst case when the input is completely reverse sorted, the

first element with be compared and swapped n-1 times, second element will be compared and

swapped n-2 times - till at the last step there would be one comparison and swap. For

example :

  


input - \[5,4,3,2,1\]

After first iteration - \[4,3,2,1,5\] - 4 comparisons and 4 swaps

After second  iteration - \[3,2,1,4,5\] - 3 comparisons and 3 swaps

After 3rd  iteration - \[2,1,3,4,5\] - 2 comparisons and 2 swaps

After 4th  iteration - \[1,2,3,4,5\] - 1 comparisons and 1 swaps

  


Hence in general, for input size n, there will be \(n-1\)+\(n-2\)+ ... 1. This would

lead to a runtime complexity of n\(n+1\)/2 - which is log\(n^2\).

  


\*/

  


pub fn selection\_sort\(array: &mut \[u8\]\) \{

    //Iterate through each element of the array till the last to last element

    for i in 0..array.len\(\) - 1 \{

        //Current element position would be the position for next minimum element

        let mut min\_index = i;

        for j in i + 1..array.len\(\) \{

            //Compare current minimum element with each next element till the last element of

            //the array - swap the index of next element with min\_index if following condition holds true

            if array\[j\] < array\[min\_index\] \{

                min\_index = j;

            \}

        \}

        //Swap ith element of the outer loop with element at min\_index - if required

        if min\_index == i \{

            continue;

        \} else \{

            swap\(array, i, min\_index\);

        \}

    \}

\}

  


/\*

Space complexity: o\(1\) - in place sorting - no extra space used.

Time complexity: Consider a fully reverse sorted descending array as input. For the first element n-1 comparsion, n-1 assignment and

of min\_index variable and 1 swap. For the second element these values are n-2, n-2 & 1. Henece worst case time complexity will

be \(n-1\) + \(n-2\)+ ...1 => n\(n+1\)/2 => log\(n^2\). n-1 max swap which less than bubble sort which takes n^2 swap at the worst

case scenario.

  


\*/

  


pub fn insertion\_sort\(array: &mut \[u8\]\) \{

    //Consider each element starting with second - first element is assumed to be sorted

    for i in 1..array.len\(\) \{

        //Take out the current element

        let current = array\[i\];

        let mut j = i - 1;

        //Compare the current with previous element - shifting them to right as long as current is less than previous

        //element

        while current > array\[j\] \{

            array\[j + 1\] = array\[j\];

            j -= 1;

        \}

        //Post the while condition j will be pointing at an element less than or equal current - hence we put the current

        //element at the index j+1

        array\[j + 1\] = current;

    \}

\}

  


/\*

Space complexity: O\(1\) - no extra space

Time complexity: Worst case is an input array sorted in descending order. We traverse each element starting with the second.

input\[5 4 3 2 1\]

  


After first iteration: 4 5 3 2 1 -> 1 comparison, 1 shift

After 2nd Iteration:  3 4 5 2 1 -> 2 comparisons, 2 shifts

After 3rd Iteration:   2 3 4 5 1 -> 3 comparisons, 3 shifts

After 4th Iteration:  1 2 3 4 5 -> 4 comparisons, 4 shifts

  


Hence comparisons and shifts: 1+ 2+ 3 + ...\(n-1\) => n\(n-1\)/2 => O\(n^2\)

  


\*/

  


fn swap\(array: &mut \[u8\], i: usize, j: usize\) \{

    let temp = array\[i\];

    array\[i\] = array\[j\];

    array\[j\] = temp;

\}
