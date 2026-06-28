---
layout: post
title: "Iteratee fundamentals for the beginer"
date: 2012-12-28 12:13:00.001+00:00
tags: []
---

Iteratees are an alternative to commonly prevalent, imperative blocking IO. While reading from a stream, if is data is not available - the reading thread blocks - which is not desirable. The alernative would be to register a callback which gets invoked as data become available. Iteratees are callback handlers and much more. If you have heard about them but not sure what they are - then this post is for you.

  


Simply put, an iteratee is a consumer of data in chunks and it's counterpart, which is called \`Enumerator\`- is a producer of data. The imperative way of reading data conforms to pulling data out in chunks from the source. But in an iteratee based system, the producer pushes data into an iteratee in successive chunks, which finally computes a value. Iteratee's state changes as it receives chunks of data. Or to be more precise\(since state change is a side-effect and side-effects don't compose\) - when an iteratee receives a chunk of data - the iteratee is replicated with it's new state being computed from the old iteratee's state and chunk of input that it received. Also, with iteratees its a two way conversation between the producer and the consumer\(i.e. the iteratee\). The producer might hand out a chunk of data to the iteratee or it might say, I'm Empty now - but hang on - I will feed you as soon as I get a chunk in the near future or it might say - I have run out of data\(EOF\) - you make a call what to do next.

  


On the other hand, the iteratee might say - I am ready for next chunck\(Cont\), or I have had enough\(Done\) or it might throw up\(Error\) - because it is monday. I will not talk about Error anymore because ours' is an ideal world and it does not add any insight to the understanding of iteratees.

  


So, when an iteratee gets a chunk of input, it replicates itself transitioning from one state to other. It might transition to a \`Done\` state which would contain a computed value and possibly some unconsumed input. The iteratee might transition to a \`Cont\` state which would hold a function waiting to be invoked with next chunk of input once it arrives. Or the iteratee might enter into a Error state which might hold a error message and possibly the chunk of input that caused it to error out.

  
  


I have been talking about iteratees in the context of IO streams. For understanding's sake lets consider Lists as our source of data. So the examples I would develop would use Lists instead of streams. Once we get the idea of how iteratees behave - it should not be difficult to relate Lists to streams.

  


So, based on the ponderings so far, two types emerge. One is the input and another is the state of the iteratee. We parameterize on the element type of the input because each chunk of data could represent a byte, word, event or anything. So the types are:

  
scala> trait Input\[+E\]  
defined trait Input  
  
  
scala> object Empty extends Input\[Nothing\]  
defined module Empty  
  
scala> //Producer has finished producing  
  
scala> object EOF extends Input\[Nothing\]  
defined module EOF  
  
scala> //The producer has produced a chunk  
  
scala> case class Elem\[+E\]\(e: E\) extends Input\[E\]  
defined class Elem  
  


Next up, we define the iteratee itself anlong with the various states it can be in after it receives a chunk of input. We paramterize the iteratee with \`E\` and \`A\` where former and later being the type of input it consumes and value it computes respectively. We also add a run method to our iteratee to extract the computed value. If our iteratee is already in the Done state then - we return the value inside it. If on the other hand, the iteratee is still in the Cont state, we send a EOF signal to it to indicate that we are interested in the value it has computed thus far.

  
scala> :paste  
// Entering paste mode \(ctrl-D to finish\)  
  
trait Iteratee\[E,+A\] \{  
    def run: A = this match \{//run will get us the  result computed thus far - sending a EOF to itself if needed  
      case Done\(a, \_\) => a  
      case Cont\(k\) => k\(EOF\).run  
    \}  
\}  
  
//Done holds computed result of type A and input it may not have consumed  
  case class Done\[E,+A\]\(a: A, next: Input\[E\]\) extends Iteratee\[E,A\]  
  //Cont state holds a function, which given an input, would return a new iteratee instance\(Done or Cont\)   
  case class Cont\[E,+A\]\(k: Input\[E\] => Iteratee\[E,A\]\) extends Iteratee\[E,A\]  
  
  
// Exiting paste mode, now interpreting.  
  
defined trait Iteratee  
defined class Done  
defined class Cont  
  


We have said before that it is the job of the producer\(aka the enumerator\) to feed the iteratee its produce in chunks. To keep things simple lets write an enumerate function instead of a full-blown enumerator. In the enumerate function below, the produce is held in a List.

  
 scala> :paste  
// Entering paste mode \(ctrl-D to finish\)  
  
 def enumerate\[E,A\]\(produce: List\[E\], itr:Iteratee\[E,A\]\): Iteratee\[E,A\] = \{  
     produce match \{  
       //No produce - return the Iteratee as it is  
       case Nil => itr  
       case e :: elems => itr match \{//produced an elem/chunk  
         case i@Done\(\_,\_\) => i//if Done - return current Iteratee  
         case Cont\(k\) => enumerate\(elems, k\(Elem\(e\)\)\)//Not yet \`Done\` continue feeding chunks of produce  
       \}  
     \}  
  \}    
  
  
// Exiting paste mode, now interpreting.  
  
enumerate: \[E, A\]\(produce: List\[E\], itr: Iteratee\[E,A\]\)Iteratee\[E,A\]  
  
  


Iteratees can come in different categories - some would take finite chunks of input and then they would be in Done state. Iteratees that take the head of a List and returns it or drops few elements and then returns the rest of the List would fall in this category. On the other hand some would consume the entire List and then return a result - iteratees that sum up the List elements would fall in this category. Some other iteratees never enter the Done state even after receiving an \`EOF\` signal - these iteratees are termed as divergent iteratees. Below are shown few example iteratees.

  
  


An iteratee which returns the head from an enumerator's produce:

  
scala> :paste  
// Entering paste mode \(ctrl-D to finish\)  
  
def head\[E\]: Iteratee\[E, Option\[E\]\] = \{  
    def step\[E\]\(in: Input\[E\]\): Iteratee\[E, Option\[E\]\] = in match \{  
  //Got an elem - return a Done iteratee right away  
  case Elem\(e\) => Done\(Some\(e\),Empty\)  
  //Cont iteratee waiting for an input  
  case Empty => Cont\(step\)  
  case EOF => Done\(None, EOF\)   
\}  
  Cont\(step\)  
  \}  
  
// Exiting paste mode, now interpreting.  
  
head: \[E\]=> Iteratee\[E,Option\[E\]\]  
  
scala> val v =  enumerate\(List\(1,2,3\), head\[Int\]\)  
v: Iteratee\[Int,Option\[Int\]\] = Done\(Some\(1\),Empty$@ade4cd\)  
  
scala> val result = v.run  
result: Option\[Int\] = Some\(1\)  
  


Iteratee that computes the length of the produce of an enumerator:

  
scala> :paste  
// Entering paste mode \(ctrl-D to finish\)  
  
def length\[E\]: Iteratee\[E,Int\] = \{  
  def step\[E\]\(acc: Int\): Input\[E\] => Iteratee\[E,Int\] = \{  
    case Elem\(e\) => Cont\(step\(acc+1\)\)  
    case Empty => Cont\(step\(acc\)\)  
    case EOF => Done\(acc, EOF\)  
  \}  
  Cont\(step\(0\)\)  
\}   
  
// Exiting paste mode, now interpreting.  
  
length: \[E\]=> Iteratee\[E,Int\]  
  
scala> val lenItr = enumerate\(List\(1,2,3,4,5,6\), length\[Int\]\)  
lenItr: Iteratee\[Int,Int\] = Cont\(<function1>\)  
  
scala> val len = lenItr.run  
len: Int = 6  
  


Iteratee that will return a List containing every alternate element starting with the first:

  
scala> :paste  
// Entering paste mode \(ctrl-D to finish\)  
  
def alternate\[E\]: Iteratee\[E, List\[E\]\] = \{  
  def step\(flag: Boolean, xs: List\[E\]\): Input\[E\] => Iteratee\[E, List\[E\]\] = \{  
  case Elem\(e\) if\(flag\) => Cont\(step\(false,xs ::: List\(e\)\)\)  
  case Elem\(e\) if\(\!flag\) => Cont\(step\(true, xs\)\)  
  case Empty => Cont\(step\(flag,xs\)\)  
  case EOF => Done\(xs, EOF\)  
\}  
  Cont\(step\(true,Nil\)\)  
\}  
  
// Exiting paste mode, now interpreting.  
  
alternate: \[E\]=> Iteratee\[E,List\[E\]\]  
  
scala> val altItr = enumerate\(List\(1,2,3,4,5,6,7\), alternate\[Int\]\)  
altItr: Iteratee\[Int,List\[Int\]\] = Cont\(<function1>\)  
  
scala> val altList = altItr.run  
altList: List\[Int\] = List\(1, 3, 5, 7\)  
  
  


**Conclusion:** I have just shown the basics of iteratees. Frameworks like Play 2 - have taken the iteratees to a whole new level combining them with scala futures and executing them asynchronously. As web applications are becoming more and more real-time data centric, iteratees provide yet another tool in the arsenal of developer to scale up web application.

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2012/12/iteratee-fundamentals-for-the-beginer.html)*
