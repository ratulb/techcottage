---
layout: post
title: "Scala dose #3: Constructors"
date: 2010-01-18 12:23:00+00:00
tags: [scala]
---

We have not talked about constructors yet. It's time we do so now. Let's type in the following to the scala prompt:  
scala> class ScalaDose3 \{  
| println\("I am getting constructed"\)  
| \}  
defined class ScalaDose3  
  
scala> val v= new ScalaDose3  
I am getting constructed  
v: ScalaDose3 = ScalaDose3@1b951f2  
  
scala>   
  
  
So from this we see that the body of class itself is the scala class constructor. If that is so, how do we pass parameters to the constructor. Let's see below:  
  
scala> class ScalaDose3\(dose: String\) \{  
| println\("I am getting constructed "+ dose\)   
| def getDose\(\) = \{   
| dose   
| \}  
| \}  
defined class ScalaDose3  
  
scala> val v="This is dose no 3"  
v: java.lang.String = This is dose no 3  
  
scala> val sd = new ScalaDose3\(v\)  
I am getting constructed This is dose no 3  
sd: ScalaDose3 = ScalaDose3@1dba9f9  
  
scala> sd.getDose  
res0: String = This is dose no 3  
  
scala>  
  
  
So, we can pass parameters as part of class declaration itself as shown above \( class ScalaDose3\(dose: String\) \{ \) . One consequence of this is that this lead to concise code. Next time we will discuss auxillary constructors.
