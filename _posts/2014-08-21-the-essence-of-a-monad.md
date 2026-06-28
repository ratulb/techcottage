---
layout: post
title: "The essence of a monad"
date: 2014-08-21 13:07:00.006+00:00
tags: [scala, monad]
---

**Many people when they encounter the term 'monad' for the the first time, they decide to look it up, at least the curious bunch.** But when they do consult the blogs, articles, Wikipedia, haskell documentations- explaining the term monad - they **become deeply confused and angry at themselves for not being able to make any sense of it - at least people like me, whose brain is not bigger than the size of a peanut. They curse themselves and grok more blogs, articles, try to learn haskell in the hope that, may be this time they would be able to grasp it - but to no avail**. Their brain hurts and they become even more confused. As they keep persisting in their efforts -**they come across monads being described as elephants, space suits/burritos/fluffy clouds and what not**\! Some say - you need to know category theory to understand monad, some say no you do not - while people trying understand monad remain in a state of utter confusion for months or maybe years on end. This happened to me also - couple of years back\(As I said before my brain is not bigger than a peanut\!\).

  


People say, "when you finally figure out what a monad is - you write a blog about it - that is a tradition". Well, I had decided to break with that tradition and not to write about it then - when that enlightenment happened\! But I have now decided to go with tradition mainly because functional programming is being so ubiquitous and terms like monad/functors etc keep appearing all over the web and many people out their may be languishing to come to terms with monads. Hope this post would help them see what a monad is.

  


**Then, why is monad so difficult to understand? I suppose there are couple of reasons for this. First, expectation on part of the person trying to understand monad. He/she expects monad to be self describing one whole thing. Once you read couple of blogs and articles, you expect to get a self explanatory picture of a concrete thing. That is a wrong expectation on the part of the learner. Monad is an abstraction of a design concept and there are different concrete implementations of this concept specific to particular problems. We need to keep this in mind.**

  


Second, except for couple of blogs/presentations, people who try to explain monad to the uninitiated, are also, to some extent, to be blamed for the confusion they cause to the people trying learn monads. I just googled for "what is a monad" - opened three top links that came up.

  


This [one](<http://stackoverflow.com/questions/44965/what-is-a-monad>) straight away goes into examples like 'List comprehension', 'Input/Output', 'A parser' and ending with an example of 'Asynchronous programming'.The questioner was asking for a **brief, succinct, practical explanation** as to what a monad essentially is\! Straight away jumping to some arbitrary examples does not help. Not to speak of the haskell syntax that may be unfamiliar to the user. So the user trying to learn monad become bewildered, deeply confused and perplexed. Here questioner's mistake was that - he asked for a a **brief, succinct, practical** explanation. That is a wrong expectation.

  


Second one from [Wikipedia](<http://en.wikipedia.org/wiki/Monad_\(functional_programming\)>) says, "In functional programming, a monad is a structure that represents computations defined as sequences of steps. A type with a monad structure defines what it means to chain operations, or nest functions of that type together. This allows the programmer to build pipelines that process data in steps, in which each action is decorated with additional processing rules provided by the monad". This one does not help. It sounds too abstract.

  


Another post mentions- "[Douglas Crockford once said that monads are cursed – that once you understand monads for yourself you lose the ability to explain them to others](<https://www.youtube.com/watch?v=b0EF0VTs9Dc>)". Then goes on to talk about 'Maybe' & JQuery being monad. This does not help either - why should we be not able to explain what a monad is? 

  


All these and many more explanations have one thing in common. And that is that - they lack the motivation for monad and where it came from. That is where Brian Beckman: [Don't fear the Monads](<https://www.youtube.com/watch?v=ZhuHCtR3xq8>) and [sigfpe](<http://blog.sigfpe.com/2006/08/you-could-have-invented-monads-and.html>) shines. They talk about the motivation for monad.

  
**So what is a monad?**  
  


**In functional programming, functions are first class as is function composition**. We build small functions and compose them to build bigger functions.**So the way to tackle complexity is composition - it's of paramount importance. If functions do not compose, there arises an impedance mismatch.** **In pure functional languages like Haskell function are considered to be mathematical- no side effect, no logging,  ****no exceptions.** Same function called with same input should give the same output irrespective of who called it, when called it or however called it. Period. No deviation from this contract. **But real world is not like this - Exception occur, latency happens, we need to handle unexpected result. So how do we account for these deviations? Well, taking recourse to monads of course\!** Monad is the vehicle we hop on to stay in course in face of these unavoidable deviations. Let's see some examples:

  
**Example 1:**  
  
def getConnection\(c: Credentials\): Connection   
  


If we look at the signature of the method above carefully, we are lying about something\! We are hiding something. What if the network is down or the database is down? We might not get a connection at all. We are not being explicit about this aspect of getConnection method failing to give us connection. That is where motivation for using or designing Maybe/Option monad comes from.

  
So the correct signature should be:  
  
def getConnection\(c: Credentials\): Option\[Connection\]  
  
If indeed getConnection returns a connection, we return Some\(connection\) or None if it fails. That we say beforehand so that caller may take alternate processing pipe line in the event of failing to get a connection.  
  
While previous fails to compose, second composes and the signature speak out loudly what the contract is.  
  
**Example 2:**  
  
In scala, it is very idiomatic to do things like following:  
  
 \(1 to 10\).toList.filter\(\_ % 2 == 0\).flatMap\(x => \(0 to x\).toList  
  


Basically we like to keep piping or chaining output of one function call as the input to the other function till we compute our desired result\(Like after each semi-colon we keep executing statement afer statement in imperative programming\). But many very times output of one function call does not conform to the input of another function which is to say they do not compose. We need to coerce the output of a function to a format that can be fed as input to other function, we need to get rid of the impedance mismatch. That is the role flatMap/bind in monads. And each monad will have its own implementation of this method that is specific to the problem it is trying to solve. To drive home the point, we conjure up the following fictitious problem:

  
val urls = List\("facebook.com", "twitter.com"\)  
  
class Page  
  
def getPage\(url: String\): Page = new Page  
  
def outGoingLinks\(page: Page\): List\[String\] =List\("bbc.com", "cnn.com"\)  
  


What we want do to is this: we start with list of urls, crawl the pages corresponding to those urls & get the total count of outgoing urls for all those pages. To achieve this we have defined our functions above. So following is the call to get the job done:

  
 urls.map\(url => getPage\(url\)\).flatMap\(page => outGoingLinks\(page\)\).size  
  
res5: Int = 4  
  


And we are done. 'outGoingLinks' function takes a page and returns a List\[String\]. **This is the crucial point to understand**. So, when all the pages\(here two\) considered, the result would be List\(List\[String\], List\[String\]\). But this not what we want - we want List\[String\]. This where output is deviating. But 'flatMap' apart from calling the 'outGoingLinks' function for each page also does one more thing. It concatenates the List\[List\[String\], List\[String\]\) to one List\[String\]. 'flatMap' implementation in the case of List monad just happens to be that it takes a function \(something\) -> List\[something\] and concatenates the resulting lists into a single List\[something\] - so that we can stay the course. 'flatMap' guides you to the **happy path** as **Erik Meijer**\(of Rx/Link fame\) says while teaching '[Principles of Reactive Programming'](<https://www.coursera.org/instructor/headinthebox>) . It keeps you from falling off the cliff.

  


So, monad is an abstraction of a design concept in functional programming and the motivation comes from recognizing the fact that composition is important. There are various implementation of this concept like Try, Either, Future, Option etc.

  


Of course, there are **monadic laws that monad should hold. But they are not a prerequisite to an understanding of what the essence of monads is**. When monads hold all three monad laws, it is a guarantee that they will not misbehave. In fact, the Try monad above holds only two of the monad laws and but for all practical purposes, it behaves like a monad. 

  


As a last note, monads are not specific to functional programming alone. The .Net implementation [**Rx\(Reactive extention\)** has been ported to **java**](<https://github.com/ReactiveX/RxJava>) by Netflix and it is all monadic underneath. Its changing the the whole game of event/stream processing and how to write reactive applications that scales up to millions of user requests.

  
It has been a long post. But hope it helps people who are trying to get on with monad and removes some of the mists surrounding monads.

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2014/08/the-essence-of-a-monad.html)*
