---
layout: post
title: "Asynch concurrency: In the promised land of scala futures"
date: 2012-12-05 08:25:00+00:00
tags: []
---

**_The basics:_**  
  


The concept of future is not new - java added them in 1.5 -scala actors had futures from the start, lift webframework had its own futures. As more and more libraries and toolkits sprang up based on the scala language - many had futures with more or less similar functionalities - akka, playframework, twitter's finagle etc had their respective implementations.

  


With SIP-14, the case was made that all these different implementations should be unified and made available as part of the scala core library. And the result is scala.concurrent package. This write-up looks at futures and promises API, how they take asynch concurrency to a whole new level and provide a higher level of abstraction.

  
Lets fire up the REPL and see futures in action:  
  
scala> import concurrent.future  
import concurrent.future  
  
scala> import concurrent.ExecutionContext.Implicits.global  
import concurrent.ExecutionContext.Implicits.global  
  
  


The first import is for the \`future\` method in the \`concurrent\` package object. The second import basically brings into scope the default execution context \(i.e. thread pool\) - which is used for computing chunks of code asynchronously. We can use our own custom execution context if one is available in the scope.

  


Computation of a future may yield a successful result or an exception and we can register callbacks to handle them appropriately.

  
scala> val f = future \{ 100 \}  
f: scala.concurrent.Future\[Int\] = scala.concurrent.impl.Promise...  
  
scala> f onComplete \{  
     |   case x => println\("Future has returned :"+ x\)  
     | \}  
Future has returned : 100  
  


We can attach multiple callbacks to a future, attach them even after the future has returned - all of them will be fired - the only caveat is that there is no guarantee in what order they will fire. Since - the future may or may not hold a value - we pattern match on instances of Either type - and as is the tradition - Left is used for signalling error condition.

  
scala> val f1 = future \{ 100 \}  
f1: scala.concurrent.Future\[Int\] = scala.concurrent.impl.Promise...  
  
scala> val f2 = future \{ throw new Exception\("Boom"\) \}  
f2: scala.concurrent.Future\[Nothing\] = scala.concurrent.impl.Promise...  
  
scala> f1 onComplete \{  
     |   case Success\(r\) => println\(r\)  
     |   case Failure\(e\) => println\(e\)  
     | \}  
100  
  
scala> f2 onComplete \{  
     |   case Success\(r\) => println\(r\)  
     |   case Failure\(e\) => println\(e\)  
     | \}  
java.lang.Exception: Boom  
  
  
\`onComplete\` is called called irrespective of success or failure. We could use \`onSuccess\` or \`onFailure\` - if we want.  
  
scala> f1 onSuccess \{  
     |   case r => println\(r\)  
     | \}  
100  
  
scala> f2 onFailure \{  
     |   case e => println\(e\)  
     | \}  
java.lang.Exception: Boom  
  
  


future has its counterpart called \`promise\`. future and promise are two sides of the same coin.futures are read-many \(times\) whereas promises are write-once. We can make a promise, fullfill that promise later - when we do so - the corresponding future get its value\(aka, returns\). Once a promise is made and fullfilled\(i.e. written to\) - we can not go back on it - it's illegal.

  
scala> import concurrent.promise  
import concurrent.promise  
  
scala> val p = promise\[Int\]  
p: scala.concurrent.Promise\[Int\] = scala.concurrent.impl.Promise...  
  
scala> val f = p.future  
f: scala.concurrent.Future\[Int\] = scala.concurrent.impl.Promise...  
  
scala> f onSuccess \{  
     |   case v => println\(v\)  
     | \}  
  
scala> p.success\(200\)  
200  
  
scala>  p.success\(500\)  
java.lang.IllegalStateException: Promise already completed.  
  
  
**_Higher order functions and future specific combinators:_**  
  
  


Apart from \`map\`, \`flatMap\` and \`filter\` - future has some other higher order functions making it possible to combine futures smart ways to achieve the task at hand.

  
scala> val f1 = future \{ 50 \}  
f1: scala.concurrent.Future\[Int\] = scala.concurrent.impl.Promise...  
  
scala> val f2 = future \{ 50 \}  
f2: scala.concurrent.Future\[Int\] = scala.concurrent.impl.Promise...  
  
scala> val result = for \{  
     |   x <\- f1  
     |   y <\- f2  
     | \} yield x \* y  
result: scala.concurrent.Future\[Int\] = scala.concurrent.impl.Promise...  
  
scala> result map\( \_ \* 2\) filter\(\_ > 4000\) onSuccess \{  
     |   case value => println\(value\)  
     | \}  
5000  
  
  
Fall back to that future in case of failure with \`fallbackTo\`  
  
  
scala> val blowUp = future \{ throw new Exception\("Crashed"\) \}  
blowUp: scala.concurrent.Future\[Nothing\] = scala.concurrent.impl.Promise...  
  
scala> val planB = future \{ "Recovered" \}  
planB: scala.concurrent.Future\[String\] = scala.concurrent.impl.Promise...  
  
scala> blowUp fallbackTo planB onComplete \{  
     |   case Failure\(e\) => println\(e\)  
     |   case Success\(r\) => println\(r\)  
     | \}  
Recovered  
  
  
Sequential execution with \`andThen\`  
  
scala> lazy val f = future \{ println\("First here"\) \}f: scala.concurrent.Future\[Unit\] = <lazy>  
  
scala> f andThen \{  
     |   case r => println\("Then here"\)  
     | \} andThen \{  
     |    case \_ => println\("At the end"\)  
     | \}  
  
First here  
Then here  
At the end  
  
  
Fold and reduce:  
  
  
scala> val f1 = future \{ 100 \}  
f1: scala.concurrent.Future\[Int\] = scala.concurrent.impl.Promise...  
  
scala> val f2 = future \{ 200 \}  
f2: scala.concurrent.Future\[Int\] = scala.concurrent.impl.Promise...  
  
scala> val f3 = future \{ 300 \}  
f3: scala.concurrent.Future\[Int\] = scala.concurrent.impl.Promise...  
  
scala> val futures = List\(f1,f2,f3\)  
futures: List\[scala.concurrent.Future\[Int\]\] = List...  
  
scala> import concurrent.Future  
import concurrent.Future  
  
scala> Future.fold\(futures\)\(0\)\(\_ + \_ \) onSuccess \{  
     |   case r => println\(r\)  
     | \}  
  
scala> 600  
  
  
scala> Future.reduce\(futures\)\(\_ \* \_ \) onSuccess \{  
     |   case r => println\(r\)  
     | \}  
  
scala> 6000000  
  
_**Conclusion:**_  
  


We have looked at just some of the APIs scala futures offer. And they by themselves are more than enough to solve many real world asynch concurrent problems. But there is more**** to them than what we have seen here. They will be an extremely useful tool in any developer's repertoire.

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2012/12/asynch-concurrency-in-the-promised-land-of-scala-futures.html)*
