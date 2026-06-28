---
layout: post
title: "kubernetes on azure linux vm from scratch"
date: 2019-12-07 23:35:00.004+00:00
tags: []
---

Create VNet  
  


[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhArt0qtWB7mynICMgDJfIWXV2RsihU2A2KK7_Q3PKozE20vyT-W33_OodGD-yiK0y7mhTyT9WF040cB_8WBfZj03SFEaOE72ANsQ6ECC-f29fnKAgOLJuJnyc2X9aJv9x7iyKDQtcLidI/s640/create_vnet1.png)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhArt0qtWB7mynICMgDJfIWXV2RsihU2A2KK7_Q3PKozE20vyT-W33_OodGD-yiK0y7mhTyT9WF040cB_8WBfZj03SFEaOE72ANsQ6ECC-f29fnKAgOLJuJnyc2X9aJv9x7iyKDQtcLidI/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhArt0qtWB7mynICMgDJfIWXV2RsihU2A2KK7_Q3PKozE20vyT-W33_OodGD-yiK0y7mhTyT9WF040cB_8WBfZj03SFEaOE72ANsQ6ECC-f29fnKAgOLJuJnyc2X9aJv9x7iyKDQtcLidI/s1600/create_vnet1.png>)  
  
  
  
  
  
  
[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgM0XgncWg81EsfnzG6OqbE49FHjob9A3BnxwwLqUYXCYswHP0H6B7AqxCNdT6SLeAzzY6EsHFaWITNoD7g5iR235KRXWpN6W0p9dLioOJILj_C4k75TrlxZtwwX6KKjHdXDHxFMczNzkw/s640/create_vm_master.png)Create VMs in the VNet](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgM0XgncWg81EsfnzG6OqbE49FHjob9A3BnxwwLqUYXCYswHP0H6B7AqxCNdT6SLeAzzY6EsHFaWITNoD7g5iR235KRXWpN6W0p9dLioOJILj_C4k75TrlxZtwwX6KKjHdXDHxFMczNzkw/s1600/create_vm_master.png>)

  


[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)[  
](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhNhNe-MPThyphenhyphenamQYpq7F5AtHhFOncwJ5klUtcdfiSqQvJs9Wct2ikrRaioqSJdyoSjQupWnnGYEJuJBErCxHnA88IPVZQRsOAWnN1FWr1taprAWC9qF84b4AOxsp7xk4dDVwp-vszVTrkQ/s1600/create_vnet1.png>)
