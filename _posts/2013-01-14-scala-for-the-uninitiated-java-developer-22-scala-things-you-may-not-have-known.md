---
layout: post
title: "Scala for the uninitiated java developer: 22 scala things you may not have known"
date: 2013-01-14 14:25:00.002+00:00
tags: []
---

Scala's popularity is rising among developers. Yet, many java developers have hardly paid any attention to it - thinking it is some sort of esoteric programming langauge isolated from the java main land. They are the target audience of this post. This post is not a tutorial - it presents the scala features with minimum technical detail and tries to show how java and scala reside under the same roof\(JVM\). 

  


First up - scala is a statically typed language that runs on the jvm and fully compatible with java. That means scala can use java classes and vice versa. It combines object oriented programming with functional programming - which means functions are treated on par with things like strings, objects, Integers etc. You can toss them around like you toss around an int as method parameter or a return value from a method. Scala is the brain child of Prof. Martin Odersky - the same guy who was hired by Sun to write the java compiler in those back old days. Big players like amazon, twitter, linkedin, NASA etc have already adopted scala. Martin Odersky taught a 7 week long online\(cousera.org\) scala course which ended in Nov 2012 - the course was attended by some 50,000 students\! That goes on to show the rising popularity of scala. With that background, let's see what are the featues that scala has to offfer.   

  
  
**1\) Seamless integration with Java**  
  


Scala has been designed for seamless interoperabilty with java. Scala codes get compiled to JVM byte codes. Scala can make use of existing java libraries. Scala code can call java methods, access java fields, extends java classes and implement java interfaces without any wrapper classes or glue code. Scala not only re-uses java's types -it also dresses them up. Following is perfectly vaild scala code.

  


import java.util.ArrayList

  


val users = new ArrayList\[String\]

users.add\("me"\)

users.add\("you"\)

val size = users.size

size: Int = 2

  


val res = 100 > 90 // Dressed up java int with \`>\` method  


res: Boolean = true

  
  
**2\) Scala is concise**  
  


In general scala programs are half the size of typical java programs. Fewer lines of code not only means less typing but also less bugs, less effort to develop and understand. Scala becomes less noisy and less boiler-platey by avoiding unnecessary keywords\(like classes are public by default - hence no need for \`public\` keyword\), making the body of the class definition the primary constructor, making semi colons optional and in most of the cases - by inferencing types, by allowing call to parameterless methods without parenthesis. Shown below are two classes with same functionality:

  
// this is Java  


public class MyClass \{

  private int index;

  private String name;

  


  public MyClass\(int index, String name\) \{

    this.index = index;

    this.name = name;

    System.out.println\("Constructor initialized"\)

  \}

\}

  
//This is scala  


class MyClass\(index: Int, name: String\) \{

  println\("Constructor initialized"\)

\}

  
// this is Java  


boolean nameHasUpperCase = false;

  for \(int i = 0; i < name.length\(\); ++i\) \{// name is String

   if \(Character.isUpperCase\(name.charAt\(i\)\)\) \{

     nameHasUpperCase = true;

     break;

   \}

\}

  
// this is scala  


val nameHasUpperCase = name.exists\(\_.isUpper\)

  
So much less noisy and less ceremony\!  
  
  
**3\) Traits - Eat your cake and have it too**  
  


We have been talking about component based, write once run anywhere software more than a decade now. But in reality, software is still a craft rather than a industry. We don't build software from reusable components. We keep re-implementing same interface again and again - violating the DRY principle. What if we could implement \`run\` method for running junit testcases once for all? Traits let's do that. Not only that, it also allows a scala class to inherit behaviour from multiple traits without leading to any diamond problem\! Is not that the best of the both worlds? You bet - In deed it is\!

  


class TestCase \{

  def setup = println\("setting up"\)

  def testMethod1 = println\("Test1"\)

  def testMethod2 = println\("Test2"\)

  def tearDown = println\("shutting down"\)

\}

  


trait TestRunner \{

 self: TestCase =>

 // Find the test methods via reflection and execute them 

 // Hard coded here\!

 def run = \{ 

   setup

   testMethod1

   testMethod2

   tearDown

 \}

\}

  


val tests = new TestCase with TestRunner

tests.run 

  


setting up

Test1

Test2

shutting down

  
In the following example we add \`product\` and \`add\` method to ArrayList.  
  


import java.util.ArrayList

  


trait Product \{

 self: ArrayList\[Int\] =>// I like to mingle with ArrayList

 def product = \{

  var p = 1

  for\(i <\- 0 until size\)

   p = p \* get\(i\)

  p

 \}

\}

  


trait Add \{

 self: ArrayList\[Int\] =>

 def add = \{

  var s = 0

  for\(i <\- 0 until size\)

   s = s + get\(i\)

  s

 \}

\}

  


val xs = new ArrayList\[Int\] with Product with Add

  


xs.add\(100\)

xs.add\(200\)

xs.add\(300\)

  
xs.add // 600  
xs.product // 6000000  
  
Needless to say, these are very simplified usage of traits but they show how code reuse can be achieved.  
  
  
**4\) Everything is objects**  
  


Scala is purely object oriented, in fact, more object oriented than java. Java distinguishes primitive types \(such as boolean and int\) from reference types - scala does not.So + is a method of the Int object and you can write 2.+\(3\) instead of 2+3. Methods are allowed to be operators, so that you can write 2+3 instead of 2.+\(3\). Scala functions are also objects which is why we can toss them around like any other value. 

  
  
**5\) Singleton objects**  
  


In the spirit of being purely object oriented, scala avoids arcane concepts like static classes and members because they are not so object oriented\! What scala has instead is singleton objects. They are automatically instantiated when accessed for the first time. They provide a nice way of modularising programs. Shown is an example of singleton object defintion.

  


object MySingleton \{

  println\("I am being materialized"\)

  def doIt = println\("Yes sirrrr\!"\)

\}

  


MySingleton.doIt

I am being instantiated

Yes sirrrr\!

  
  
**6\) Structural equality**  
  


Comparing to values for equality is every day business in programming. While java promotes referential equality, scala prefers structural equality with the commonly used \`==\` operator. We can check referential equality with the \`eq\` method though. Shown below is an example:

  


val list1 = new ArrayList\[String\]

list1.add\("apple"\)

list1.add\("banana"\)

list1.add\("orange"\)

  


val list2 = new ArrayList\[String\]

list2.add\("apple"\)

list2.add\("banana"\)

list2.add\("orange"\)

  
list1 == list2 //returns true  
  
list1 eq list2 //returns false  
  
  
**7\) Implicit conversion**  
  


This is a double-edged sword. While outrageously useful for extending and adapting existing and new types, care must to be taken since overuse might lead to ambiguity. They also support writing DSLs in scala. Shown below is an example where we add a new method to java String class without even touching it\!

  


class CamelCaser\(val str: String\) \{

  def toCamelCase =str.split\(" "\).map\(s=> s.head.toUpper + s.tail.toLowerCase\).mkString\(" "\)

\}

  


implicit def camelCase\(s: String\) = new CamelCaser\(s\)

  


"tHIS JAVA STRING iS being CONVERTED to camel case BY IMPLICT conversion".toCamelCase

  
Result: This Java String Is Being Converted To Camel Case By Implict Conversion  
  
**8\) Pattern matching**  
  


Scala has pattern matching, a functional programming technique that hasn't been seen before in mainstream languages.Pattern matching is switch statements on steroids. While java has recently added support for strings in switch statements - scala allows to pattern match on any sort of of data\! Is not that awesome? You can pattern match on even user defined types\! Just put the \`case\` keyword before your type definition and start match making as you like\! 

  
  


def whatIsIt\(thingy: Any \) = thingy match \{

 case \(x,y\) => println\(x + " and "+ y\)

 case \(x,y,z\) => println\(x + ", "+ y + " and " + z\)

 case s: String if s.length < 10 => println\("Its a short string : "+ s\)

 case s: String => println\("Long strings are sooo long: "+s\)

 case l:List\[String\] => println\("Got a list of String"\)

 case \_ => println\("I am not programmed to receive you\!"\)

\}

  


whatIsIt\(\(10,"big"\)\)//prints 10 and big  
whatIsIt\(new Object\)//I am not programmed to receive you\!  
  


case class Name\(first: String, last: String\)

  


case class Address\(name: Name,street: String, city: String, state: String, zip: Int\)

val name=Name\("Mr.","Cowboy"\)

  


val address = new Address\(name,"Luna road", "Dallas ","Texus", 75201\)

address match \{

 case Address\(Name\(first, last\), street, city, state, zip\) => println\(last + ", " + zip\)

 case \_ => println\("not an address"\) // the default case

\}

  
// prints Cowboy, 75201  
  
  
**9\) Option & Tuples **  
  


We need to check for Null references and guard against them all the time.It is such a nuisance. Programmers abhore them. That is where Option type comes handy. Option can be in two states - it has either something\(Some\(x\)\) or nothing\(None\). We can easily pattern match on option types.

  


val connection = Some\(getConnection\(url,user,password\)\)

  


connection match \{

  case Some\(con\) => println\("Connected"\)

  case None => println\("Opening connection"\)

\}

  


Another very useful type is the tuple type. Tuples can contain different types of elements - And this makes life whole lot more easier while writting code\! Bye bye value classes and pojos\! Life does not get better than this - atleast not for me\!

  


val item =\("Mango", "fruit", 2.5, 10\)

item: \(String, String, Double, Int\) = \(Mango,fruit,2.5,10\)

  


val quantity = item.\_4 //10  
  


val emp =\(101, "MARTIN", "SALESMAN", 7698, "28-11-81", 1400,30\)

emp: \(Int, String, String, Int, String, Int, Int\) = \(101,MARTIN,SALESMAN,7698,28-11-81,1400,30\)

  


emp.\_5 //returns 28-11-81  
  
  
  
**10\) Rich collection APIs**  
  


Scala has a common, uniform, and extremely useful collection framework. They are easy to use, concise, safe and performant.A small vocabulary of 20-50 methods is enough to solve most collection problems in a couple of operations.You can achieve with a single word what used to take one or several loops.

  
Example:  
  
Here's one line of code that demonstrates many of the advantages of Scala's collections.  
  


val \(minors, adults\) = people partition \(\_.age < 18\)

  
Concise and elegant\!  
  
  
**11\) For expression**  
  


In scala everything is an expression. Every expression eveluates to something. \`If\` is an expression and has to return something. The last expression of a method is the return value of the expression. If a method does not return anything, it still returns \`\(\)\` which is the instance value of \`Unit\`\(Unit is sort of java \`void\` type\). For expressions are not exception. They accept generators and optional guards and yield something.Also, any type that defines \`map\` can be used as a single genrator in a for expression. A type with map and \`flatMap\` allows for being used as multiple generators. Types with map, flatMap & \`withFilter\` can accept \`if\` conditions\(guards\) in for expression. And finally, types with \`foreach\` method can be used as for loop. Shown below is a usage of for expression used to count the occurrence of a particular word in the .txt files underneath the current directory.

  


import java.io.File

import io.Source

  


def wordCount\(word: String\) = \{

  def perLine\(line: String\) = line.split\(" "\).count\(w => w.equalsIgnoreCase\(word\)\)

 

  def lines\(f: File\) = Source.fromFile\(f\).getLines.toList

  


  val files = new File\("."\).listFiles

  val counts = for \{

    file <\- files //Generator  
    if file.isFile && file.getName.endsWith\(".txt"\)  //Guard  


    line <\- lines\(file\)

  \} yield perLine\(line\)

  counts.sum

\}

  
  
**12\) Asynch concurrency with futures**  
  


Like java scala has futures but unlike java they are much more pleasant to deal with. We can combine multiple futures together. You wrap your codes inside futures and let them loose out in the wild. Scala will turn back and do the rest. No submitting to thread pools and checking to see if they have completed what you told them to do. Really\!

  
  


val f = future \{ 

 println\("Going to do some time consuming stuff"\)

 Thread.sleep\(1000\)

 println\("Done the stuff and returning \`Some result\`"\)

 "Some result"

\}

  


f onComplete \{

 onDone

\} // Future returned : Some result  
      
  


def onDone\(r: Try\[String\]\): Unit = r match \{

 case Success\(v\) => println\("Future returned : " + v\)

 case Failure\(e\) => println\("Something gone wrong :"+e\)

\}

  
  
**13\) Scala is functional**  
  


This is where scala has raised the bar for future programming language development. Before scala, functional and object oriented programmers did not see eye to eye. Scala broke with tradition and unified functional and object oriented programming, after all, they both have their own sweet spots. 

  


Scala treats functions on par with other values like int, boolean objects. As a consequence, we can store a function in a variable, pass it as argument to some other function and return a function from a method call. This helps a lot in composing bigger things from smaller parts and vice versa. Functions accepting/returning functions are called higher order functions.

  
Let's define a function that adds the integers between a and b.  
  


def addInts\(a: Int, b: Int\): Int =

 if\(a > b\) 0 else a + addInts\(a+1, b\)

  


addInts\(10,20\) // 165

  
Now let's define another function that adds the squares of integers between a & b.  
  


def addSquares\(a: Int, b: Int\):Int = 

 if\(a > b\) 0 else a \* a + addSquares\(a+1, b\)

  


addSquares\(10,20\) //2585  
  
Now, we define two functions with following signatures.  
  


def id\(a: Int\) = a

def square\(a: Int\) = a \* a

  
Now, let's define a generic sum function which take a function as a parameter.  
  


def sum\(f: Int => Int, a: Int, b: Int\):Int =

 if\(a > b\) 0 else f\(a\) + sum\(f, a+1, b\)

  
We can now write:  
  


def addInts\(a: Int, b: Int\) = sum\(id,a,b\)

  


def addSquares\(a: Int, b: Int\) = sum\(square,a,b\)

  


We just touched upon the functional side of scala. We can nest functions\(refer to \`For expressions\`\), partially or incrementaly apply arguments to get back partially applied or curried functions. We can define partial functions that are not defined for some input values. We can also create closures and toss them around. We can even pattern match on functions.

  
What follows is an example of function composition:  
  


def str\(a: Int\) = String.valueOf\(a\)

def len\(s: String\) = s.length

def fun\(f: Int => String, g: String => Int\) = g compose f

val digits = fun\(toStr, strLen\)

val numOfDigits = digits\(10000\)

numOfDigits: Int = 5

  
  
**14\) By name parameter**  
  


In normal cases, arguments to functions are evaluated and then passed along. But in case of by name parameters, the arguments are evaluated late at the call site. They come very handy for logging frameworks etc where we don't want log messages to be evaluated in case logging is turned off.

  


var loggingOn = true

  


def log\(stmt: => Unit\) =

 if\(loggingOn\) stmt else \(\)

  


log \{ println\("A log message"\) \} // A log message   
  


loggingOn = false

  


log \{ println\("A log message"\) \} // Prints nothing  
  
In a by name parameter, the type of argument is preceded by \`=>\`.   
  
  
**15\) Structural types**  
  


Structural types are types having similar members. For example, we might want to be able to close a resource without caring whether it is a database connection or a file handle. So, given a resource we want do some operation on it and finally close the resource calling the \`close\` method on it. We also want to return the operation result. Let's call our method \`withResource\`. The type of the resource can be anything as long as it has a \`close\` method. Similarly, type of the operation result can be anything. Hence, \`withResource\` will have to have two type parameters. Shown below is the signature:

  
 def withResource\[T <: \{ def close\}, R\]\(resource: T\)  


   \(operation: T => R\) = \{

   val result = operation\(resource\)

   resource.close

   result

 \} 

  
  
**16\) Actor based concurrency**  
  


Actors are objects which encaptulate state and behaviours, and communicates exclusively via message passing. The messages are placed into the recipients' mail boxes. Messages are passed on to the \`receive\` method of an actor. Multiple actors piggy back on a single thread. Actors provide you following:

  


  * Simple and high-level abstractions for concurrency and parallelism.
  * Asynchronous, non-blocking and highly performant event-driven programming model.
  * Very lightweight event-driven processes \(Order of millions of actors per GB RAM\).

  
Shown below is a simple actor printing out the received message.  
  


import akka.actor.\_

val actorSystem = ActorSystem\("actorsystem"\)

  


class MyActor extends Actor \{

 def receive = \{

  case x => println\("Received : "+ x\)

 \}

\}

  


val myActor = actorSystem.actorOf\(Props\[MyActor\]\)

myActor \! "Hi" // Received : Hi   
  
**17\) Delimited continuations**  
  


Delimited continuations are wild beasts. Its one of those things that bends and hurts the mind. You might have to spend months in a state of stupor trying to grasp what the heck they are\!

  


It does help if I told you delimited continuations are segments of a program flow that has been reified into functions. The \`reset\` sets the limit for the continuation while the \`shift\` reifies the current continuation up to the innermost enclosing reset. 

  


var cont: Int => Int = \_

  


def f = \{

 reset \{

  shift \{ k: \(Int=>Int\) =>

    cont = k //Save it for calling later  
    k\(7\) //calling the continuation  
  \} + 1  
 \} //Continuation boundary ends  
 println\("Not part of reified continuation"\)  


\}

  


f // Not part of reified continuation  
cont\(100\) // 101  
  


As mentioned before, delimited continuations take some efforts to get used to. This post is not about teaching stuffs - its about showing features of scala with minimum technical details. 

  
**18\) Macro**  
  


Scala macros are functions that are called by the compiler during code compilations. Macros are written in scala and they work with expression trees rather than raw strings. They can generate and typecheck code and have access to compiler APIs.

  
  
**19\) Compiler plugin**  
  


Scala compiler has an architecture that allow for custom compiler plugins to be invoked during compilation. A plugin adds an extra phase in the compilation process - wherein it might do extra type checks, code generation etc. Delimited continuations are implemented via a compiler plugin in scala.

  
  
**20\) In-built xml support**  
  
Scala has inbuilt xml support. You can easily create, parse, and process XML documents in scala.   
  


val date = new java.util.Date

val xml = <today> \{date\} </today>

xml: scala.xml.Elem = <today> Mon Jan 14 15:54:44 IST 2013 </today>

  


xml \\\ "today"

scala.xml.NodeSeq = NodeSeq\(<today> Mon Jan 14 15:54:44 IST 2013 </today>\)

  
  
**21\) Combinator Parsing**  
  


This is one good thing parser and DSL writters would love. No need to roll out your own - which is difficult - if you are not an expert - or fall back on something like javacc or antlar etc. Scala combinator parsers greatly simplifies parsing your DSL or embedded language. 

  
  
**22\) GUI Programming**  
  


Scala provides a GUI library based on java swing classes but hides many of the complexities of swing APIs. The scala GUI APIs are much easier to deal with.

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2013/01/scala-for-the-uninitiated-java-developer-22-scala-things-you-may-not-have-known.html)*
