---
layout: post
title: "Scala auxillary constructors"
date: 2010-01-28 08:19:00+00:00
tags: [scala]
---

As we have said before - the body of the class defintion is constructor code for a scala class. So,in the following class:  
  
scala> class Person\(name: String\) \{  
| println\("This will be printed when the this class is instantiated : "+ name\);  
| \}  
defined class Person  
  
scala> val p=new Person\("rbsomeg"\)  
This will be printed when the this class is instantiated : rbsomeg  
p: Person = Person@a47cc3  
  
scala> class Person\(name: String\) \{  
| def this\(name: String, age: Int\) = \{  
| this\(name\)  
| println\("This is an auxillary constructor : "+ age\)  
| \}  
| \}  
defined class Person  
  
scala> val p=new Person\("rbsomeg",24\)  
This is an auxillary constructor : 24  
p: Person = Person@153e0c0  
  
scala> class Person\(name: String\) \{| println\("""An auxillary constructor should first call the base constructor  
| directly or thru some other auxillary constructor which calls the base constructor first"""\)  
|  
| def this\(\)= \{  
| this\("nobody"\)  
| println\("This an example of auxillary constructor"\)  
| \}  
| def this\(age: Int\) = \{  
| this\(\)  
| println\("""This auxillary constructor called the previous auxillary constructor  
| which in turn called the base constructor"""\)  
| \}  
| \}  
defined class Person  
  
scala> val p=new Person\(24\)  
An auxillary constructor should first call the base constructor  
directly or thru some other auxillary constructor which calls the base constructor first  
This an example of auxillary constructor  
This auxillary constructor called the previous auxillary constructor  
which in turn called the base constructor  
p: Person = Person@17d8769  
  
  
In next post I will talk about the constructor parameters.
