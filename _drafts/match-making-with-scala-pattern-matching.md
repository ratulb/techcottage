---
layout: post
title: "Match making with scala pattern matching"
date: 2010-01-29 08:39:00+00:00
tags: [scala]
---

One very elegant feature of scala is - pattern matching. It's not to be confused with regular expressions\(scala has regular expressions too\). One way to look at scala pattern matching as java 'case' statement. But scala's pattern matching is much more powerfull and generalised. Let's look at the following code snippet to get a hang of it:

  
scala> "name" match \{  
  
case s: String => println\(s\)  
case \_ => println\("default all case match"\)  
  
\}  
name  
  
  


Couple of things first. 'match' is a keyword, scala wildcard is '\_' not '\*' and 'case' statement has the format 'case' followed by 'expression' followed by '=>'.  
  
Let's try to understand the above snippet now. Here we are trying to match "name" to the patterns \(s: String and \_ \(the wild card\)\). It matches the first pattern and binds the 's' variable with "name".

  
Let's look at another example:  
  
scala> val list=List\(1,2.0, "rbsomeg", new Object\)  
list: List\[Any\] = List\(1, 2.0, rbsomeg, java.lang.Object@b2fd30\)  
  
scala> var i=0;  
i: Int = 0  
  
scala> while\(i \!= list.size\) \{  
  
list\(i\) match \{  
  
  
case i: Int => println\("I got an int: "+ i\)  
  
case d: Double => println\("I got a double: "+d\)  
  
case s: String => println\("I got a String : "+ s\)  
  
case o: Object => println\("I got an object: "+ o\)  
  
case \_ => println\("I don't know what I got...."\)  
  
\}  
  
i+=1  
  
\}  
I got an int: 1  
I got a double: 2.0  
I got a String : rbsomeg  
I got an object: java.lang.Object@b2fd30  
  
Quite powerfull, is not it? Let's try another one.  
  
scala> val data = List\(List\(1,2\), \(100, "value"\), Map\(1->"One", 2->"two"\)\)  
  
data: List\[ScalaObject with Equals\] = List\(List\(1, 2\), \(100,value\), Map\(1 -> One, 2 -> two\)\)  
  
  
scala> var i=0  
  
i: Int = 0  
  
  
scala> while\(i \!= data.size\) \{  
  
data\(i\) match \{  
  
  
case l: List\[\_\] => println\("It's a list : "+ l\)  
  
  
case \(x,y\) => println\("It's tuple : "+ x + " " + y\)  
  
  
case m: Map\[\_,\_\] => println\("It's a map"\)  
  
  
case \_ => println\("It's a catch case..."\)  
  
  
\}  
  
  
i+=1  
  
  
\}  
It's a list with head : 1 and it's tail is : List\(2\)  
  
It's tuple : 100 value  
  
It's a map  
  
The above examples show the power of scala's pattern matching. But if want to write own classes and want to pattern match on constructor parameter's - how do we do that? It's turns out that that is what scala's 'case' classes are for. A case class has the keyword "case" prefixed to it's definition- that's all. Let's look at an example :  
  
  
scala> case class WildAnimal\(name: String, deadly: Boolean\)  
defined class WildAnimal  
  
  
scala> val animal1 = WildAnimal\("Lion",true\)  
  
animal1: WildAnimal = WildAnimal\(Lion,true\)  
  
  
  
scala> animal1 match \{  
  
case WildAnimal\(s,t\) => println\(Animal is : "+ s +" deadly? : "+ t\)  
  
\}  
  
This animal is : Lion and deadly? : true  
  
Couple of points to be noted here. We have not used "new" while instantiating WindAnimal - that's allowed for case classes - but you can use "new" if you want to. Also, the compiler automatically provide you with default implementation of "toString", "hashCode" and "equals" methods.  
  
Pattern matching works beautifully with scala Lists. But that I am going to discuss in another post. I want tell you about scala's pattern matching in exception handling. In try/catch/finally - scala is same as java in try and finally - it's little different in the catch clause. Let's see an example:  
  
scala> import java.io.\_  
import java.io.\_  
  
scala> def readFile\(fileName: String\): Unit = \{  
var br: BufferedReader = null  
var fr: FileReader = null  
try \{  
fr=new FileReader\(new File\(fileName\)\)  
br = new BufferedReader\(fr\)  
var line=""  
do \{  
line = br.readLine\(\)  
println\(line\)  
\} while\(line \!= null\)  
  
\}catch \{  
case fnfe: FileNotFoundException =>   
println\("File not found: "+ fileName\)  
case ex: Exception =>   
println\("Someother exception"\)  
\}finally \{  
if\(fr \!= null\) fr.close  
if\(br \!= null\) br.close  
\}  
\}  
  
readFile: \(fileName: String\)Unit  
  
The bold section above show how scala's pattern matching is used in exception handling.  
  
To conclude: Scala's pattern matching is extremely powerful. It's easy and once you get used to it comes very handy. In the web - I have seen people using pattern matching to replace the visitor design pattern. When you think about it you can achieve much more with pattern matching than the visitor design pattern and whole thing comes as a language feature\!
