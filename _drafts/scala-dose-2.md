---
layout: post
title: "Scala dose #2"
date: 2010-01-15 10:30:00+00:00
tags: [scala]
---

In our Scala dose \#1, we said that in scala we can define something called 'object' which can have methods, vars and vals. So, let's now define an object called 'ScalaDose2'.  
scala> object ScalaDose2 \{// Not Object\!  
def sayHello\(name: String\): Unit = \{  
import java.util.\_  
val date =new Date\(\) // make use of any existing java class  
println\("Hello : "+ name + ". The current time is : "+ date\)  
\}  
\}  
scala> ScalaDose2.sayHello\("Mr. Beans"\)  
Hello : Mr. Beans. The current time is : Fri Jan 15 16:34:18 IST 2010  
  
So we defined the 'ScalaDose2' object which has method named 'sayHello' which takes a String type parameter. One thing you may have noticed is that there is a import statement right inside the method\( ' import java.util.\_'\). So in scala import statement can occur at any scope. Here the scope is the method body. This is not surprising considering the fact that scala treat methods/functions at par with classes/objects and vals/vars. Also, in scala the wild card is '-' not '\*'.  
  
  
So when we define an object and access it for the first time - the scala compiler takes care of instantiating the singleton object and giving it to us. You might wonder what is the value addition here over java singleton. Well first thing is - you get a singleton with just the 'object' keyword. Secondly, scala objects are java singletons and more. We will see that next.  
  
scala> class GlblContainer \{  
val v=ScalaDose2  
\}  
defined class GlblContainer  
  
scala> val gc1=new GlblContainer  
gc1: GlblContainer = GlblContainer@56d6cf  
  
scala> val gc2=new GlblContainer  
gc2: GlblContainer = GlblContainer@1adfbe3  
  
scala> gc1.v==gc2.v //Logical equality test  
res3: Boolean = true  
  
scala> gc1.v.eq\(gc2.v\) //Reference equality  
res4: Boolean = true  
  
  
scala> class Container \{  
object MyOwnObj  
\}  
defined class Container  
  
scala> val c1=new Container  
c1: Container = Container@145d7f2  
  
scala> val c2=new Container  
c2: Container = Container@688e91  
  
scala> c1.MyOwnObj == c2.MyOwnObj //this is logical equality test  
res5: Boolean = false  
  
scala> \(c1.MyOwnObj\).eq\(c2.MyOwnObj\) //reference equality.  
res6: Boolean = false  
So, you can use objects as java singleton or you can use them in a delimited scope - inside a class or a method as you like.
