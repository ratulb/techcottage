---
layout: post
title: "Scala constructor params"
date: 2010-01-28 15:11:00+00:00
tags: [scala]
---

scala> //'x' not prefixed with val or var and hence x can not be accessed outside.  
  
scala>   
  
scala> class ConsArgDemo\(x: String\) \{  
| def getX = x  
| \}  
defined class ConsArgDemo  
  
scala>   
  
scala> val v=new ConsArgDemo\("rbsomeg"\)  
v: ConsArgDemo = ConsArgDemo@12efcfe  
  
scala> v.x   
:7: error: value x is not a member of ConsArgDemo  
v.x   
^  
  
scala>   
  
scala> v.getX  
res1: String = rbsomeg  
  
scala>   
  
scala> //With val 'x' can be accessed but it can not be reassigned.  
  
scala>   
  
scala> class ConsArgDemo\(val x: String\) \{  
| def getX = x  
| \}  
defined class ConsArgDemo  
  
scala>   
  
scala> val v=new ConsArgDemo\("rbsomeg"\)  
v: ConsArgDemo = ConsArgDemo@1d6b049  
  
scala> v.x   
res2: String = rbsomeg  
  
scala>   
  
scala> v.getX  
res3: String = rbsomeg  
  
scala>   
  
scala> v.x="new value not allowed\!"  
:6: error: reassignment to val  
v.x="new value not allowed\!"  
^  
  
scala>   
  
scala> //var allows you reassignment  
  
scala>   
  
scala> class ConsArgDemo\(var x: String\) \{  
| def getX = x  
| \}  
defined class ConsArgDemo  
  
scala>   
  
scala> val v= new ConsArgDemo\("rbsomeg"\)  
v: ConsArgDemo = ConsArgDemo@10936a1  
  
scala>   
  
scala> v.x  
res4: String = rbsomeg  
  
scala>   
  
scala> v getX  
res5: String = rbsomeg  
  
scala>   
  
scala> v.x="New value can be assigned\!"  
  
scala>   
  
scala> v.x  
res6: String = New value can be assigned\!  
  
scala>   
  
scala> //Passing a function \(from String to Boolean\) as a constructor parameter and calling that as a part of constructor body.  
  
scala> class ConsArgDemo\(val f: String => Boolean, str: String\) \{ // Second one is a String parameter  
| println\(f\(str\)\)  
| \}  
defined class ConsArgDemo  
  
scala>   
  
scala> def func\(str: String\): Boolean = str.length > 5  
func: \(str: String\)Boolean  
  
scala>   
  
scala> val funcAsParam = func \_   
funcAsParam: \(String\) => Boolean =   
//Here we are not supplying the function parameter. We are saying that we will do so later. We are getting a partially applied function   
  
  
scala>   
  
scala> val v= new ConsArgDemo\(funcAsParam,"rbsomeg"\)  
true  
v: ConsArgDemo = ConsArgDemo@2a2ae9  
  
scala>   
  
scala> val v = new ConsArgDemo\(funcAsParam,"rbg"\)  
false  
v: ConsArgDemo = ConsArgDemo@11fdbef  
  
scala>
