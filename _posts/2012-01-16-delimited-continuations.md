---
layout: post
title: "Delimited continuations"
date: 2012-01-16 08:24:00+00:00
tags: [delimited continuation, scala, continuation, CPS]
excerpt: "Understanding Scala's delimited continuations by building a framework to capture and remotely execute frozen computations."
---

There have been a lot of blog posts, questions & answers about scala's delimited continuation. I would not again try to confuse the reader with another lame-duck explaination. I would, instead, present it as I have come to understand it and then go on to develop a basic framework where we capture a part of a computation and send that frozen computation to a remote machine where it gets executed and result of that computation is sent back to the criginal machine.     
If we think of a scala program as the whole computation - then we can say the whole continuation is from the begining to the end. Let's say whole computation takes value of type A as input and produces a value of type C as output. Also, let's assume the program cosists of 2 functions F1 & F2 which are called in a sequence. So if F is the whole program, then we can write F as follows:   
  
F=F1;F2  
  
So, F1 receives the initial input of type A, computes an intermediate result of type B which is fed to F2 which computes the final result of type C. Now what if we could pause the computation halfway after F1 has calculated it's value and freeze rest of the computation? So the the program now translates into some other function from B => C. Let's call that some other function F~. Now couple of things we need to take notice of here.  
  
Though F~ is a function from B => C, its frozen now - we can pass any value of type B - but it has no effect. We feed some value of type B at the moment we freeze it \(via shift\). The frozen state extends from end of F1's computation till end F2 computation\(this boundary is specified by reset\). There might be additional computations after F2 but they are not part of the frozen state. Astute reader by now must have figured out where the delimited qualifier is coming from in scala's continuation. Also, the moment we capture\(i.e. freeze\) the rest of the computation - control returns to the caller of F but shifting/capturing/freezing must respect the contractual obligation that F returns a value of type C. So, at the point of shifting we must return some value of type C or call F~ with some arbitray value of type B.  
  
Now let's try out a few example before embarking on the business of tossing around delimited continuations. Launch REPL with the continuation pluging enabled as shown below:  
  
scala -P:continuations:enable  
  
scala> class A  
defined class A  
  
scala> class B  
defined class B  
  
scala> class C  
defined class C  
  
scala> import util.continuations.\_  
import util.continuations.\_  
  
var cont: \(B => C\) = null  
  
def fun1\(a: A\): C = \{  
  println\("I am not part of frozen state\!"\)  
    reset \{  
      println\("reset marks the boundary where shift/freeze/capture can be done"\)  
      shift \{ continuation: \(B => C\) =>  
        cont= continuation  
        println\("I was realized with: "+a.hashCode\)  
        println\("I am returning an arbitrary C"\)  
        new C  
      \}  
      println\("I am the part of the frozen computation"\)  
      new C  
  \}  
  println\("fun is supposed to return a C"\)  
  new C  
\}  
  
fun1: \(a: A\)C  
  
Now let's invoke fun and capture the continuation.  
  
scala> fun1\(new A\)  
I am not part of frozen state\!  
reset marks the boundary where shift/freeze/capture can be done  
I was realized with: 13264767  
I am returning an arbitrary C  
fun is supposed to return a C  
res1: C = C@50d7c5  
  
Now we call cont:  
  
scala> cont\(new B\)  
  
I am the part of the frozen computation  
res2: C = C@3f348a  
  
Let's look at another example:  
  
scala> var cont: \(Int => String\) = null  
cont: \(Int\) => String = null  
  
scala>  
  
scala> def fun2\(i: Int\): String = reset \{  
shift \{ continuation: \(Int => String\) =>  
cont=continuation  
"Ratul Buragohain" //since shift will return control to caller of fun - but fun is supposed to return a String  
\}  
\(i to 10\).toList.mkString //Changing i's value has no effect after capturing the rest of the computation  
\}  
  
fun2: \(i: Int\)String  
  
Call fun to capture the continuation.  
  
scala> fun2\(0\)  
  
res7: String = Ratul Buragohain  
  
Now call cont.  
  
scala> cont\(0\)  
res8: String = 012345678910  
  
scala> cont\(5\)  
res9: String = 012345678910  
  
scala> cont\(null.asInstanceOf\[Int\]\)  
res12: String = 012345678910  
  
scala> cont\(100000000\)  
res15: String = 012345678910  
  
That's the crux of scala's delimited continuation.  
  
In the next post I will show how we can toss around delimited continuation across machines.

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2012/01/delimited-continuations.html)*
