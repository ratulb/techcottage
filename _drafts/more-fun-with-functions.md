---
layout: post
title: "More fun with functions"
date: 2021-01-22 11:48:00.002+00:00
tags: []
---

Scala functions are object instances and hence they can be tossed around like any object instances.

  


scala> val func: String=> Int = x => Integer.parseInt\(x\)   
func: \(String\) => Int  

  


For the beginner, the above snippet might seem quite hard to digest and he might decry - "Scala is hard and not for me". Same was the case when java came to the scene. People were familiar with c style of programming - not familiar with objects. Objects? What are they? Yet OOP is so ubiquitous now. A little persistence is all that is needed. Once you get a hang of it - it becomes a breeze. In fact, when I had started with scala, I had to stare hard to make sense of it. Well, enough of sidetrack. What we are doing above is - defining function 'from String to Int'\(String=> Int\) and assigning it to a val called 'func'. x\(it could be any other identifier\) represents the String input\(After all, the function is from String to int\) and => Integer.parseInt\(x\) represents the body of the function. Cool right? scala> func\("200"\)  
res1: Int = 200  
  
scala> func\(200\)  
:6: error: type mismatch;  
found : Int\(200\)  
required: String  
func\(200\)  
^  
Also, the scala compiler compiles the definition into a class and func is an instance of that class. scala> func.hashCode  
res3: Int = 20868995  
  
scala> func.toString  
res5: java.lang.String =   
  
scala> val funcRef = func  
funcRef: \(String\) => Int =   
  
scala> funcRef.hashCode  
res6: Int = 20868995  
  
So, scala functions are objects after all. Let's extend the above to take in two input parameters instead of one. scala> val func: \(String,String\) => Int = \(x,y\) => Integer.parseInt\(x\)\*Integer.parseInt\(y\)  
func: \(String, String\) => Int =   
  
scala> func\("10","10"\)  
res17: Int = 100  
  
scala> func.toString  
res18: java.lang.String =   
The above '<function2>' denotes that func expects two input parameters. What happens if we supply only one parameter? Let's see. scala> val x=func\("10",\_: String\)  
x: \(String\) => Int =   
  
scala> x\("10"\)  
res19: Int = 100 Here x is a function object which now expects only one parameter.
