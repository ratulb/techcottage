---
layout: post
title: "scala xml wrapper utility"
date: 2012-10-22 13:51:00.002+00:00
tags: []
---

XDoc is a utility wrapper over scala.xml.Elem. It's simplifies xml processing. Following needs to be considered while using this utility:  
  
1\) It does not support namespaces. That can easily incorporated - But our use case did not have any namespaces.  
2\) It does not consider text within an element to be a child element of the container as opposed to normal convention - But text can set and retrieved from an element.  
  
  
Following REPL session shows how to use it.  
  
Shows how to create an instance XDoc:  
  
scala> var d = XDoc\("animals"\) addChild "tiger" addChild "lion" addAttr\("test", "attrValue"\)  
d: XDoc =   
<animals test="attrValue">  
  <tiger/>  
  <lion/>  
</animals>  
  
  
Querying child count:  
  
scala> d.childCount  
res13: Int = 2  
  
Setting text :  
  
scala> d = d.setText\("Sample text"\)  
d: XDoc = <animals test="attrValue">  
  Sample text  
  <tiger/>  
  <lion/>  
</animals>  
  
Shows that text is not considered as a child:  
  
scala> d.childCount  
res14: Int = 2  
  
scala> d = d addChild\(XDoc\("zebra"\).addAttr\("hasStripes", "true"\)\)  
d: XDoc = <animals test="attrValue">  
  Sample text  
  <tiger/>  
  <lion/>  
  <zebra hasStripes="true"/>  
</animals>  
  
scala> d.childCount  
res15: Int = 3  
  
scala> d = d.addAttr\("test2", "Value"\)  
d: XDoc = <animals test2="Value" test="attrValue">  
  Sample text  
  <tiger/>  
  <lion/>  
  <zebra hasStripes="true"/>  
</animals>  
  
Querying attributes. Attributes are an instance of the case class :  
  
**case class XAttr\(name: String, value: String\)**  
  
scala> val atrs = d.attrs  
atrs: List\[XAttr\] = List\(XAttr\(test,attrValue\), XAttr\(test2,Value\)\)  
  
scala> d.hasAttrs  
res16: Boolean = true  
  
scala> d.attr\("test2"\)  
res17: Option\[XAttr\] = Some\(XAttr\(test2,Value\)\)  
  
scala> d.attr\("testxx"\)  
res18: Option\[XAttr\] = None  
  
  
Querying childrens :  
  
scala> d.childrenByName\("tiger"\)  
res20: List\[XDoc\] = List\(<tiger/>\)  
  
scala> d = d addChild\(\(XDoc\("tiger"\).addAttr\("male", "true"\)\) addChild "females"\)  
d: XDoc = <animals test2="Value" test="attrValue">  
  Sample text  
  <tiger/>  
  <lion/>  
  <zebra hasStripes="true"/>  
  <tiger male="true">  
    <females/>  
  </tiger>  
</animals>  
  
scala> d.childrenByName\("tiger"\)  
res21: List\[XDoc\] =   
List\(<tiger/>, <tiger male="true">  
  <females/>  
</tiger>\)  
  
  
Filtering children based on a predicate:  
  
scala> d = d filter\(\_.name \!="zebra"\)  
d: XDoc = <animals test2="Value" test="attrValue">  
  <tiger/>  
  <lion/>  
  <tiger male="true">  
    <females/>  
  </tiger>  
</animals>  
  
  
Checking existence of children based on predicate:  
  
scala> d exists\(\_.isChildLess == false\)  
res22: Boolean = true  
  
scala> val tigerWithFemales = d filter \(\_.isChildLess == false\)  
tigerWithFemales: XDoc =   
<animals test2="Value" test="attrValue">  
  <tiger male="true">  
    <females/>  
  </tiger>  
</animals>  
  
Mapping over child elements and transforming them:  
  
scala> d = d map \(\_.addAttr\("wild","true"\)\)  
d: XDoc = <animals test2="Value" test="attrValue">  
  <tiger wild="true"/>  
  <lion wild="true"/>  
  <tiger wild="true" male="true">  
    <females/>  
  </tiger>  
</animals>  
  
  
Finding based on a predicate condition on children:  
  
scala> val withFemale = d find\(\_.isChildLess == false\)  
withFemale: Option\[XDoc\] =   
Some\(<tiger wild="true" male="true">  
  <females/>  
</tiger>\)  
  
Checking if some conditions holds for all children:  
  
scala> d forall\(\_.attr\("wild"\) match \{  
     |   case None => false  
     |   case Some\(x\) => true  
     |   \}\)  
res23: Boolean = true  
  
Finally, we can partition the elements based on some criteria.  
  
scala> val \(d1, d2\) = d partition \(\_.isChildLess\)  
d1: XDoc =   
<animals test2="Value" test="attrValue">  
  <tiger wild="true"/>  
  <lion wild="true"/>  
</animals>  
d2: XDoc =   
<animals test2="Value" test="attrValue">  
  <tiger wild="true" male="true">  
    <females/>  
  </tiger>  
</animals>  
  
  
As can be seen XDoc can be pretty handy for dealing with xmls without namespaces. It is an utility class of a bigger project - And can be improved upon. In the mean while the source can be found at:  
  
https://github.com/ratulb/scala-xml-wrapper

*Originally published on [https://rbsomeg.blogspot.com](https://rbsomeg.blogspot.com/2012/10/scala-xml-wrapper-utility.html)*
