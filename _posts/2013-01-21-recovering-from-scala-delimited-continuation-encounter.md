---
layout: post
title: "Recovering from scala delimited continuation encounter"
date: 2013-01-21 15:40:00.001+00:00
tags: []
---

As I have said before, delimited continuations are wild beasts. Its one of those things that bends and hurts the mind. You might have to spend months in a state of delirium trying to figure them out\! In the scala-lang.org's delimited continuation page, one reader commented and I quote, **_"From my perspective, these are convoluted ways of adding numbers and I have no idea what is being gained or accomplished"_**. Reading his comment - I had laughed my heart out -really\! I could understand his frustration - even though my plight was only marginally better\! So, if this is the first time you are hearing about them - maybe you should do some googling for them before going through rest of the stuff in this post. Once you are sure that you are confused enough - you should take some rest and then start with this post. Hopefully, once you are through with this post - some of the mists would disappear and you will be better equipped to explore them further. So, without further ado, let's get to them.

  
**What is a continuation?**  
  


This is a rather simple idea. Its any computation that has a starting point, a body that the computation runs through and a exit point. It could be a servlet request-response cycle, where start point is when the request is received by the container, the whole rest of the compuation being the proccessing and rendering of the response by the container. Or in even more simplistic terms, it's just a method invocation. Starting with the call, till the method returns, is the full continuation. So you get the idea - it is nothing complicated - a routine idea. So, in the interest of keeping things simple, we would stick to this last defintion i.e. the method body is a continuation. 

  
**CPS:**  
  


Now, let's say our method takes a parameter of type \`A\` and produces a result of type \`C\`. Now, imagine, when the execution reaches some arbitray point \`P\`, we slice the method body into two halves with our mental scissor. Let us also presume that - at the moment we cut the method at point P, the first half was producing a value of type \`B\` and that value would have been passed on to the second half, as its input, had we not made the cut. If we think of our two halves as two methods, one taking an A and producing a B and another taking a B and producing a C and we combine them sequentially\(telling the first method to feed its output to the second\) - what we are effectively doing is - passing a continuation to the first method telling it not to return instead feed its produce to the supplied function. So, as it turns out, CPS\(continuation passing style\) is again a rather simple idea\!

  
**Delimited continuation:**  
  


In the above example, we passed a method to the first method which respresented the whole rest of the computation. Once the supplied continuation\(method representing the second half\) has run its run, we have a final result of type C. What if instead of passing the whole rest, we could pass a function\(or some snippet of code\) that would serve as partial rest? So, delimted or partial continuation denotes portion of the whole rest instead of the whole rest itself. This is important to remember. 

  
**Delimited continuation in scala:**  
  


**Deviation** :\[Delimited continuation in scala is achieved via code   transformation. This transormation is done by a compiler plugin\(enabled by passing \`-P:continuations:enable\` flag\). So, wherever the plugin sees reset/shift combinations, those code sections are CPS transformed.\] 

  
  


The extent to which, the continuation reaches is denoted by \`reset\`.\`shift\` can occur only within a reset. Using shift, we basically say, transform the code surrounded by the inner most reset into a function body. Input and output types of the transformed function, of course, should line up with those specified in the shift signature. The reified function we may call, call as many times as we like, store it somewhere and call later or throw it out of the window. Its all upto us. **This is all there is to in delimited continuation in scala**. Lets now look at some examples which would help straighten these ideas.

  
  


scala -P:continuations:enable

  


import util.continuations.\_

  


def fun = \{ println\("I am not part of reset. Hence not part of the reified function."\)

   reset \{

      shift \{k: \(Int => Int\) => //Reify reset body into Int => Int function

        println\("Calling the reified function with 2"\)

        k\(2\)

     \} \* 300 //reset body \_ \* 300 

  \} 

  


  println\("I am outside reset - hence not part of the delimited continuation"\)

  


 "Delimited continuations are hallucinating" // return value of fun

\}

  


fun: String

  


scala> val v = fun

I am not part of reset. Hence not part of the reified function.

Calling the reified function with 2

I am outside reset - hence not part of the delimited continuation

v: String = Delimited continuations are hallucinating

  


Shown below is the same function as above without comments and print statements. Also, we store the reified function in the cont variable. We are also not calling the continuation i.e. the reified function.

  
  


var cont: Int => Int = \_

  


def fun = \{ 

   reset \{

     shift \{k: \(Int => Int\) =>

      cont = k //Store it

     \} \* 300

  \} 

  


 "Delimited continuations are hallucinating" // return value of fun

\}

  


  


fun: String

  


scala> val v = fun

v: String = Delimited continuations are hallucinating

  


scala> val v = cont\(2\)

v: Int = 600

  
  
**Programming inside out:**  
  


Its illuminating to think about what would happen if we were to nest resets within shifts. Turns out that inner resets are evaluated before the outer ones\! Why would it behave like that? Well, as we now know, resets are reified into functions or closures. So when the outer reset is being reified, if there is any nested reset inside shift, that needs to be reified as well - and that has to happen before so that we are able to reify outer ones based on the inner ones. Some people call it programming inside out or inverted. Shown below is an example. 

  


def fun = \{

  reset \{

    shift \{ k1: \(Int => Int\) =>

     \{

      println\("A"\)

      reset \{

        shift \{ k2: \(Int => Int\) =>

         println\("C"\)

        \} \* 200

      \}

     \}

     println\("B"\)

    \} \* 300

  \}

\}

  


scala> fun

A

C

B

  
**Possible use cases for delimited continuation:**  
  


Though scala delimited continuations have been out there for quite some time now\(they came with scala 2.8\) - their adoption has not quite taken off. One reason being, at least, at first glance, they are quite hard to understand. But once, more more developers become more comfortable with them, their usage would definitely grow. The biggest apeal of delimited continuations' is that we can pause a running program and rerun it later. This  opens the door for event based programming and workflows. Since rest of the running program gets converted into a closure, we can transmit the closure accross the wire and rerun it at some other location. \`Swarm\` is an example of this. In the near future, we are definitely going to see some novel applications of delimited continuations.

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2013/01/recovering-from-scala-delimited-continuation-encounter.html)*
