---
layout: post
title: "Scala lists"
date: 2010-02-04 13:06:00+00:00
tags: [scala]
---

Scala has wide variety of collections classes. List is one of them. Let's get familiar with List.  
  
scala> val xs=List\(1,2,3,4,5\)xs: List\[Int\] = List\(1, 2, 3, 4, 5\)  
  
Here we have created a List which contains integers. One thing to note here is that the type of a list which has elements of type T is written as List\[T\] and not as List<T>.  
  
scala> val fruit = List\("apples", "oranges", "pears"\)fruit: List\[java.lang.String\] = List\(apples, oranges, pears\)  
  
The scala compiler can infer type - which is why the obove snippet and below ones are equivalent.  
  
scala> val fruit:List\[String\] = List\("apples", "oranges", "pears"\)fruit: List\[String\] = List\(apples, oranges, pears\)  
A scala list is covariant - which means List\[String\] is subtype of List\[Object\] - this not the case in java\!  
  
Let's create an empty List. And see what the scala prompt prints.  
  
scala> val xs=List\(\)xs: List\[Nothing\] = List\(\)  
  
Here compiler has said that an empty list has it's element type as 'Nothing', which in scala, is the subtype of all the other types. So, it's should be possible to add element of any type to an empty scala List and it turns out that indeed we can do so. Before we do so, let's know a bit about scala List. Scala List is a linked list - now to add to a linked list we will have to start at beginning \(the head of the List\) and traverse through rest of the List\(the tail of List\), find the last element and then add the new element. But that's going to be hugely inefficient as the list grows in size\(performance will be log\(n\)\). Instead, what we do is, add the element to the front of List\(before the head of the List\) and that has log\(1\) performance. Now let's add to an empty List:  
  
scala> val emptyList = List\(\)emptyList: List\[Nothing\] = List\(\)  
scala> val newList = 1 :: emptyListnewList: List\[Int\] = List\(1\)  
  
Couple of points here. The emptyList had element type Nothing after adding 1 \(Type Int\), the resulting List became of type List\[Int\]. Secondly, '::' method call is on the emptyList not on 1\(in the Int value or instance - Remember in scala everything is an object, which means that 1+1 is actually 1.+1, invokation of '+' method on one\!\). Let's see some more examples:  
  
scala> val xs= List\(1,2,3,4,5\)xs: List\[Int\] = List\(1, 2, 3, 4, 5\)  
  
  
//Add 100 to the front of the List  
  
scala> val l = 100 :: xs  
l: List\[Int\] = List\(100, 1, 2, 3, 4, 5\)  
  
//The head of the new list is 100  
  
scala> l.head  
  
res0: Int = 100  
//The tail of the new List is the List without the head  
  
scala> l.tail  
res1: List\[Int\] = List\(1, 2, 3, 4, 5\)  
  
//Nil represents an empty List  
  
scala> val xs = Nil  
xs: scala.collection.immutable.Nil.type = List\(\)  
//Adding 1 to an empty List  
  
scala> 1::Nil  
res8: List\[Int\] = List\(1\)  
scala> 1::2::3::4::Nil  
res9: List\[Int\] = List\(1, 2, 3, 4\)  
  
The above associates as follows:  
  
1::\(2::\(3::\(4::Nil\)\)\)  
  
  
We know already the basic operations head and tail, which respectively take the first element of a list, and the rest of the list except the first element. They each have a dual operation. They are init and last : last gives you the last element of a List as opposed to head and init gives you all the elements of a List except the last element as opposed to tail. The following shows these two operations.  
  
scala> val xs = List\(1,2,3,4,5,6,7\)  
xs: List\[Int\] = List\(1, 2, 3, 4, 5, 6, 7\)  
scala> xs.last  
res13: Int = 7  
scala> xs.init  
res14: List\[Int\] = List\(1, 2, 3, 4, 5, 6\)  
  
How about concatenating two Lists? The following shows that.  
  
scala> List\(1,2,3\) ::: List\(4,5,6\)  
res19: List\[Int\] = List\(1, 2, 3, 4, 5, 6\)  
Pattern matching on List  
  
In previous post I touched upon [scala pattern matching](<http://rbsomeg.blogspot.com/2010/01/match-making-with-scala-pattern.html>). Lists and pattern matching plays together very well. Let's some examples.  
  
scala> val xs=List\(1,2,3,4\)  
xs: List\[Int\] = List\(1, 2, 3, 4\)scala> xs match \{| case Nil => println\("Empty List"\)| case \_ => println\("Non empty list"\)| \}  
Non empty list  
scala> val xs=List\(\)   
xs: List\[Nothing\] = List\(\)  
scala> xs match \{| case Nil => println\("Empty List"\)| case \_ => println\("Non empty list"\)| \}  
Empty List  
scala> val xs=List\(1,2,3,4\)   
xs: List\[Int\] = List\(1, 2, 3, 4\)  
scala> xs match \{| case Nil => println\("Empty List"\)| case head :: tail =>  
println\("Head is : "+ head +" and tail is : "+ tail\)| \}  
Head is : 1 and tail is : List\(2, 3, 4\)  
Now let's write a function to reverse a given Int List\(List has it's own in-built reverse method\).  
  
scala> def reverse\(xs: List\[Int\]\): List\[Int\]  
= xs match \{| case Nil => Nil| case head :: tail =>  
reverse\(tail\) ::: List\(head\)| \}  
reverse: \(xs: List\[Int\]\)List\[Int\]  
scala> reverse\(List\(1,2,3,4,5,6,7\)\)  
res23: List\[Int\] = List\(7, 6, 5, 4, 3, 2, 1\)  
We can generalise the reverse function above for any type and not just for Int type. Following is how we can do that.  
  
//We are passing the type parameter A  
  
scala> def reverse\[A\]\(xs: List\[A\]\): List\[A\]  
= xs match \{ | case Nil => Nil| case head :: tail =>  
reverse\(tail\) ::: List\(head\)| \}  
reverse: \[A\]\(xs: List\[A\]\)List\[A\]  
scala> reverse\(List\("apple", "banana","orange"\)\)  
res24: List\[java.lang.String\] = List\(orange, banana, apple\)  
How about finding out the length of List? Again we can use pattern matching.  
  
  
scala> def length\[A\]\(xs: List\[A\]\): Int  
= xs match \{| case Nil => 0| case \_ :: tail => 1+ length\(tail\)| \}  
length: \[A\]\(xs: List\[A\]\)Int  
scala> length\(List\(\)\)  
res0: Int = 0  
scala> length\(List\(1\)\)  
res1: Int = 1  
scala> length\(List\(1,2,3,4\)\)  
res2: Int = 4  
  
In these above examples we have used recursion along with pattern matching. This might lead to StackOverflowException if the list is very big. With tail call elimination we can get around this problem but that I am going cover in another post. Let's get functional first.  
  
Fun with functions  
  
As we have said before scala is a hybrid language which merges features of object oriented programming and functional programming. In scala functions are like any other val or var which means they can be tossed around as val or vars. We can pass on functions as method parameters or return functions as return value from functions. We can define functions within functions. Functions accepting functions as input or functions outputting functions as return value are called [higher order function](<http://en.wikipedia.org/wiki/Higher-order_function>). Scala List has a host of higher order functions. One of them is 'map'. To 'map' we can pass in a function, to which all the elements of the List will be fed one by one, upon which the function will act on those elements, one by one and we can, in the process, transform whole List to another List, if needed.  
  
scala> List\(1,2,3,4,5,6\).map\(x=> x+1\)  
res3: List\[Int\] = List\(2, 3, 4, 5, 6, 7\)  
  
Here x=> x+1 is the function we have passed on to map. 'x' stands for each element of the List in turn. Since the scala compiler applies lot of syntatic sugar, the following is equaivalent to the above example.  
  
scala> List\(1,2,3,4,5,6\).map\( \_ +1\)  
res4: List\[Int\] = List\(2, 3, 4, 5, 6, 7\)  
  
Where '\_' , as we already know the scala wildcard and in this context, it's the placeholder for 'x'. Also, it need not be the case that application of map will have to result in a List of similar element type. Let's look another example.  
  
scala> List\(1,2,3,4,5,6\).map\(\_.toString\)  
res5: List\[java.lang.String\] = List\(1, 2, 3, 4, 5, 6\)  
  
The above example show that the element type of resulting List is whatever the result type of the function we pass in to 'map'\(In this case we are passing in 'toString'\).  
  
Let's look at some more example to have a hang of 'map'.  
  
scala> val words = List\("apples", "banana","orange"\)  
words: List\[java.lang.String\] = List\(apples, banana, orange\)  
  
  
scala> words.map\(\_ length\)  
res6: List\[Int\] = List\(6, 6, 6\)  
  
  
scala> List\("A", "VERY", "BIG", "CAT."\) map \(\_ toLowerCase\)  
res10: List\[java.lang.String\] = List\(a, very, big, cat.\)  
  
We have just scratched the the functional nature of scala. In next post, we will get more functional with List.
