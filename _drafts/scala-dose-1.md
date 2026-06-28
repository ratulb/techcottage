---
layout: post
title: "Scala dose #1"
date: 2010-01-14 09:07:00+00:00
tags: [scala]
---

The [scala](<http://www.scala-lang.org/>) language is getting lot of attention from software developer community. I am not going to describe it's features any more than saying that -  


  * It's hybrid language in the sense that it combines oop\(read side effects, java or imperative\) programming with FP\(read side effect free, haskell, pure\)
  * It is statically typed and compiles into Java byte code and runs on the JVM. It has feel of dynamically interpreted languages because the compiler infers type and reduces lot of boiler plate code.
  * It can transparently make use of any existing library in the Java ecosystem.
  * It does not have statics. It's replaced by singleton objects.
  * It replaces java interfaces by traits which can have concrete implementation.
  * Functions considered on par with other members which means they can be assigned to variables\(or vals which are akin to java final\), passed to other functions as parameters or defined inside other functions.
  * All these and many more

  
So let's get started. You can follow the instructions from the scala site and download and install scala. Once scala is in your path, you can type scala in the command prompt and this will bring up the scala interpreter where you can type in scala code snippets and execute them. There are eclipse/netbeans and intellij plugins are available for scala development. But we will take one step at a time. So you will be in the scala command prompt as shown below-  
Welcome to Scala version 2.8.0.r19367-b20091102023355 \(Java HotSpot\(TM\) Server VM, Java 1.6.0\_16\). Type in expressions to have them evaluated. Type :help for more information. scala>   
Now type in the following in the prompt:  
class ScalaDose1 \{  
def main\(args: Array\[String\]\): Unit = \{  
for\(arg <\- args\) println\(arg\) \} \} val sd = new ScalaDose1 sd.main\(Array\("This", "is", "just", "a", "test"\)\)  
  
This will print the following:  
This  
is   
just   
a   
test  
  
Now try to understand the program.  
class ScalaDose1 \{ // This line says that scala class declaration does not need a 'public' key word. Things are by default public.  
  
Scala infers the semi-colons. You can use them if you want.  
def main\(args: Array\[String\]\): Unit = // From this line we learn couple of things. Method definition start with the key word "def". Type is declared as 'identifier' : followed by type. The main method here takes an argument of type array of String and its return type is 'Unit'\( the ': Unit' part\) which analogous to java 'void' type.  
  
for\(arg <\- args\) // This is scala's basic for loop format. Contrast this with java's 'for\(arg : args\)'.  
  
val sd = new ScalaDose1 // Here we are defining an identifier 'sd' which is intialized to an instance of ScalaDose1. vals are similar to java final variables which when initialized can not be reassigned to. Also, this line says that we can omit parenthesis if we don't have to pass parameters\( think brevity\! But there is more to it\). So we have learnt quite a few new things so far.  
  
  
Now let's type in the following to the prompt.  
object ScalaDose1Obj \{  
def main\(args: Array\[String\]\)\{  
for\(arg <\- args\) println\(arg\) \} \} ScalaDose1Obj.main\(Array\("This", "is", "just", "a", "test"\)\)  
  
This will again print:  
This  
is  
just  
a  
test  
  
  
Now let's understand what we have done. All the other things remaining same, we just we replaced the 'class' keyword with the keyword 'object' and we are able to call the main method without instantiating any object with the 'new' keyword\! What it means is that we can define object directly and the scala compiler takes care of instantiating the object for us and we can use it directly\!
