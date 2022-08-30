---
title: "Low-power backscatter communications"
---

![backscatter module with test truck](/assets/img/backscatter-truck.jpeg)

As part of MITRE's [National Security Accelerator Program][1], I had the opportunity to conduct independent research on a topic of my choosing.

After learning about [recent research that allowed for *gigabit* backscatter communications][2] (as opposed to the kilobit data rates that are common), I decided to try my hand at implementing a backscatter radio.

If you're not familiar with the technology, backscatter radios reflect incoming RF energy, rather than transmitting their own, as is the case for normal radio systems. Because of this change, backscatter systems are significantly less complex and use orders of magnitude less power. Some can even be [fully powered by harvesting the very RF energy they are reflecting][4].

Backscatter has traditionally been limited to near-field, low-data rate applications such as RFID and electronic toll collection. While the time and resource constraints of my research meant I was unable to demonstrate a long-range system, [some exciting work from 2017][3] demonstrated that backscatter coupled with clever modulation schemes could work over kilometers.

Unfortunately, the [radar range equation][5] means backscatter is not right for every scenario, as power scales inversely with the *fourth* power of distance, rather than the square. But while traditional radio systems continue to shrink, and wireless communications are pushed closer and closer to theoretical limits, we should not rule out the option of using backscatter.

- [Final research report][6]
- [Git repo][7]

*The lawyers would like you to know that this project has been*

> Approved for Public Release; Distribution Unlimited. Public Release Case Number 22-2392

[1]: https://careers.mitre.org/nsap
[2]: https://www.nature.com/articles/s41928-021-00588-8
[3]: https://doi.org/10.1145/3130970
[4]: https://batteryfreephone.cs.washington.edu/
[5]: https://en.wikipedia.org/wiki/Radar#Radar_range_equation
[6]: /assets/files/capstone.pdf
[7]: https://github.com/elimbaum/nsap-backscatter-capstone