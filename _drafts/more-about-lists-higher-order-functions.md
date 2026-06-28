---
layout: post
title: "More about List's higher order functions"
date: 2010-02-06 07:32:00+00:00
tags: [scala, higher order function]
---

Scala List has a method called 'filter' which accepts a predicate. The predicate needs to return true or false. Let's use filter to get the list of odd integers between 1 to 20.  
  
scala> \(1 to 20\).toList.filter\(x=> x%2 == 1\)  
  
res3: List\[Int\] = List\(1, 3, 5, 7, 9, 11, 13, 15, 17, 19\)  
  
The same can done as shown below.  
  
scala> def isOdd\(x: Int\) = x % 2 == 1   
  
isOdd: \(x: Int\)Boolean  
  
scala> \(1 to 20\).filter\(isOdd\)  
  
res10: scala.collection.immutable.IndexedSeq\[Int\] = IndexedSeq\(1, 3, 5, 7, 9, 11, 13, 15, 17, 19\)  
We can do the same thing in java as follows:  
  
List list = ... ;  
List resultList = new ArrayList\(\);  
for\(int i : list\)\{  
if\(i% 2 ==1\) resultList.add\(i\)  
\}  
return resultList;  
  
scala> List\("Rbsomeg","robert", "Bruce", "Ricky", "tony"\).filter\(x=>  
Character.isUpperCase\(x.charAt\(0\)\)\)  
  
res9: List\[java.lang.String\] = List\(Rbsomeg, Bruce, Ricky\)  
  
Another useful method for picking up right element out of a List is 'takeWhile'. 'takeWhile' returns all elements until it finds an element, at which the function return false.  
  
scala> List\(2,4,6,8,10,11,12,13,14\).takeWhile\(x=> x % 2==0\)  
  
res13: List\[Int\] = List\(2, 4, 6, 8, 10\)  
  
Similarly, List has 'dropWhile' which filter out the elements until the passed in anonymous fuction return false and there after rest of the List is returned.  
  
scala> List\("123","4231","23","54","231","33","123"\).dropWhile\(x=> x.contains\("23"\)\)  
  
res1: List\[java.lang.String\] = List\(54, 231, 33, 123\)  
  
The flatMap is similar map but it takes a function returning a list of elements instead a function returning a single element.  
  
scala> List\(1\).flatMap\(x=> x to 5\)  
  
res7: List\[Int\] = List\(1, 2, 3, 4, 5\)  
  
scala> List\(2\).flatMap\(x=>x until 5\)  
  
res10: List\[Int\] = List\(2, 3, 4\)  
  
scala> List\(2\).flatMap\(x=> List\(x\)\)  
  
res11: List\[Int\] = List\(2\)  
  
Yet another map like operator is foreach. The function supplied to foreach is applied to each element of the list but that application does not return anything i.e. the return type is unit. Also, at the end no assembled list is returned.  
  
scala> var sum=0   
sum: Int = 0  
  
scala> List\(1,2,3,4,5,6\).foreach\(x=> sum=sum+x\)  
  
scala> println\(sum\)  
21  
  
  
reduceLeft and reduceRight  
  
reduceLeft and reduceRight operator works on the adjacent elements of a List. reduceLeft start with the first two elements of a List while reduceRight start with last two elements of a List. The function to reduceLeft is applied to the first two elements of the list, the result and the third element are then fed to the function and so on. Let's sum up the elements of a list.  
  
  
scala> List\(1,2,3,4,5,6,7\).reduceLeft\(\(x,y\)=>x+y\)   
res23: Int = 28  
  
In case of reduceRight the process starts from the end of the List.  
  
scala> List\(1,2,3,4,5,6,7\).reduceRight\(\(x,y\)=>x\*y\)  
res25: Int = 5040  
Let's use reduceLeft to find the max element of a List.  
  
scala> List\(4,5,1,8,23,7,0\).reduceLeft\(\(x,y\)=> if\(x > y\) x else y\)   
res27: Int = 23  
Or using scala's built-in max:  
  
scala> List\(8, 6, 22, 2\).reduceLeft\(\_ max \_\)  
res28: Int = 22Easy right? The same thing in java can be done the following way:  
  
List list = ...  
int max = Integer.MIN\_VALUE  
for\(int i : list\)\{  
if\(i> max\) max = i;  
\}  
foldLeft and foldRight are similar except that they also take an intial value also called the seed value. Also, the return type of the function and the return type of foldLeft/foldRight must match the type of the initial value passed in.  
  
scala> val sum=List\(1,2,3,4,5,6,7\).foldLeft\(0\)\(\(x,y\)=> x+y\)   
sum: Int = 28  
  
scala> val sum=List\(1,2,3,4,5,6,7\).foldLeft\(10\)\(\(x,y\)=> x+y\)  
sum: Int = 38  
  
scala> val sum=List\(1,2,3,4,5,6,7\).foldLeft\(100\)\( \_ + \_\)   
sum: Int = 128  
  
foldRight works similarly but starts from the back of the list.  
  
forall and exists  
  
forall takes a predicate and applies that predicate to the elements of the list and returns true if all the elements satisfy the predicate. Whereas, exists takes predicate and return true if one\(any one\) element of the list satisfy the predicate. Let's see some examples:  
  
scala> val v=List\("ubuntu","is","absolutely", "breezy\!"\)  
v: List\[java.lang.String\] = List\(ubuntu, is, absolutely, breezy\!\)  
  
scala> v.exists\(x=> x.length==10\)  
res29: Boolean = true  
  
scala> v.forall\(x=> x.length >= 2\)  
res30: Boolean = true  
  
scala> v.forall\(x=> x.length >= 3\)  
res31: Boolean = false  
  
Now let's imagine we want to visit a nearby school, visit some classes and find out if there is a class with all it's sections having strength 30. Following scala code mimics the situation.  
  
class Section\(val name: Char, val numOfStudents: Int\)  
class Clazz\(val name: String, val sections: List\[Section\]\)  
val section1=new Section\('A',30\)  
val section2=new Section\('B',35\)  
val class1=new Clazz\("One",List\(section1,section2\)\)  
val section3=new Section\('C',32\)   
val section4=new Section\('D',30\)   
val class2=new Clazz\("Two",List\(section3,section4\)\)  
val section5=new Section\('E',30\)   
val section6=new Section\('F',30\)  
val section7=new Section\('G',30\)  
val class3=new Clazz\("Three",List\(section5,section6,section7\)\)  
val clzs = List\(class1,class2,class3\)  
  
scala> clzs.exists\(clz => clz.sections.forall\(\_.numOfStudents == 30\)\)  
res38: Boolean = true  
  
Assuming Clazz and Section constructs are allready defined, we can achieve the same in java following way:  
  
List classes =... ;  
for\(Clazz clz : classes\)\{  
boolean all30 = true;  
for\(Section sec : clz\) \{  
all30 = all30 && sec.numOfStudents == 30  
\}  
if\(all30\) return true;  
\}  
  
  


So far, we have seen a few of the higher order functions of scala's List construct. There are many more. Higher order functions provide a good way to compose big pieces of computations from smaller pieces. We don't have to worry about looping, keep an eye on the variables and side effects etc. We tell the computer what to do and not how to do something. They provide a higher level of abstraction where it becomes easier for us to reason about programmes.
