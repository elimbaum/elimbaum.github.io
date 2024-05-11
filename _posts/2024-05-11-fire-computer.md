---
title: "fire computer"
---

Steve Mould put out [a video][1] a weeks back describing a neat effect: vaporized lighter fluid in a perfectly-sized channel allows a flame to travel down the channel, almost like an electrical pulse.

![still from steve's video](/assets/img/fire/steve.png){: width="50%"}

In the comments, Steve said he didn't think you could use this to build logic `gates, and therefore probably no fire computer. But I think we *can* build logic gates, and thus yes fire computer. Another commenter referenced the [Wireworld Computer][2], which, while having slightly different cellular-automata rules, served as good inspiration.

# the rules of fire

First, a slightly idealized mental model of the traveling flame.

1. A flame will travel along a channel at a fixed speed.
2. A flame approaching a branch will split and continue. For reliability, let's say we never have more than a four-way intersection.[^1]
3. A flame approaching a branch forming an acute angle (with respect to its own direction of travel) will continue straight and not return down the acute branch. (By property 2, a flame traveling in the opposite direction will split.)
4. Two flames traveling in opposite directions will cancel each other out when they meet.

To illustrate properties 2 and 3 a bit better:

![split and merge properties](/assets/img/fire/split.jpeg){: width="33%"}
_Pulse on the left does not travel backwards up the left branch. Pulse on the right splits in two._

[^1]: With too many branches, the intersection itself becomes quite large in area, and thus might not be able to hold enough vapor for the flame to persist.

I don't have easy access to a 3D printer, so I won't be able to confirm these are all correct. I would love to hear about any attempts to test out these theories.

Since a traveling flame cannot be statically persist, to have any notion of a signal, we need a clocked system. We'll assume some sort of "ready" channel (or you could think of it as "power"). Pulses in the clock channel will correspond to the existence of a signal, whereas pulses in other channels will represent data. I'll refer to signals as being "hot" (true, on fire) or "cold" (false, not on fire).

# building logic gates

## wire
The simplest gate is the identity. That's just two channels, one power and one data.

![wire](/assets/img/fire/wire.png){: width="33%"}

## not gate

To invert a signal, we apply the cancelling property: split the power signal, then route it such that it will cancel a data signal. If there *isn't* a data signal, however, the split clock signal continues on to the empty data line as a new signal.

An inverter might look something like this:

![not](/assets/img/fire/not.png){: width="33%"}

> `R` is the "ready" channel, and it signifies when a signal exists on the corresponding data line. In some of the diagrams below, I have dropped the `R` signal, but assume it always exists and is of the proper length to align with the data output.

An inverted signal will take a bit longer to reach the output than `R`. So, in reality, we need to stretch `R` by the appropriate amount:

![not with proper length](/assets/img/fire/not-squiggle.png){: width="33%"}

But I'll stylize this with a hash line, to signify that a wire should be stretched to the "proper" length.

## diode
Next, we'll need a diode, to prevent backpropagation of flames. Here's my idea:

![diode](/assets/img/fire/diode.png){: width="33%"}

Signals coming from the left (the forward direction) travel around the perimeter of the loop and exit. However, signals from the right split at the loop and cancel each other out at the bottom. Due to the angle of the inbound line, these signals will not propagate, by property 3.

Of course, this diode has a maximum switching speed: it can't handle signals coming from both directions particularly well. As we will see below, the other gates do *not* intrinsically prevent backpropagation, which could occur even in normal circumstances. So I think copious use of diodes will be required to have a somewhat reliable circuit.

## or gate
This is pretty simple: we just connect two wires in a T.

![or](/assets/img/fire/or.png){: width="33%"}

A signal coming from either `X` or `Y` will split at the shared node and produce an output. The case where both `X` and `Y` are hot is a bit more interesting: the flames will cancel at the shared node, but (I believe) will also allow an output flame.

We do need to be careful of backpropagation here. With a single hot input, that signal will split towards the output, but will _also continue back towards the other input_. So, to make a reliable OR gate, we need diodes:

![or with diodes](/assets/img/fire/or-diode.png){: width="33%"}

I'll simplify this using the standard circuit symbol for a diode.

![or with diode symbol](/assets/img/fire/or-diode2.png){: width="33%"}

## xor gate
This is similar to the OR gate; we just need to prevent the double-hot case from producing an output. To accomplish this, we move the output connection away from the center node. If `X ^ Y`, the signal travels around the extra loop and creates an output. But if both inputs are hot, they cancel in the middle, never reaching the output loop.

![xor](/assets/img/fire/xor.png){: width="33%"}

Of course, we should also have diodes here.

![xor](/assets/img/fire/xor-diode.png){: width="33%"}

## full basis
And that's it! We now have the tools to make a computer. We can implement an AND gate, for example, with three inverters and an OR gate:

![and](/assets/img/fire/and.png){: width="50%"}

The hashed wires in this gate should be resized so all signals arrive at the same time.

## the rest
We might also like a clock generator, which we see in Steve's video. Varying the diameter of a loop affects the frequency of the clock generator. Assume you light the circuit at the left-hand node (since, per the video, it's tricky to light a loop on its own).

![clock generator](/assets/img/fire/clock.png){: width="33%"}

Two clock generators give us a (pulsed) latch:

![latch](/assets/img/fire/latch.png){: width="33%"}

Though, again, we need diodes to prevent backpropagation.

![latch with diodes](/assets/img/fire/latch-diode.png){: width="40%"}

Unfortunately, there is a bit of a race condition here, since each clock will send pulses into the diode. The "reset" pulse will need to travel from the diode into the clock loop before any such clock pulse resets it on the diode branch. This can be mostly avoided if the clock frequency is low and the diode is very close to the loop. We may also be able to send a _series_ of pulses to ensure at least one pulse makes it through and disables the clock.

# prior work

The underlying phenomena here, as Steve mentions, is something known as "excitable media." It seems like building circuits in excitable media is actually a relatively well-studied phenomena, though mostly with respect to chemical reactions.

[Rössler 1974][3] appears to be one of the earliest works on this matter[^2]; [Tóth and Showalter 1995][4] considered the design of logic gates in a [specific chemical reaction][5]. [Motoike and Adamatzky][6] considered circuits built under a tri-state model (true, false, "nonsense"), which allows for more expressive designs in what is fundamentally an analog medium.

So it seems like - at least in principle - you could build a computer out of fire. Dealing with spurious ignition, timing issues, and lighter-fluid refills are left as exercise to the reader.

[^2]: Rössler [later protested the Large Hadron Collider][7] for fear of it creating miniature black holes.


[1]: https://www.youtube.com/watch?v=SqhXQUzVMlQ
[2]: https://www.quinapalus.com/wi-index.html
[3]: https://link.springer.com/chapter/10.1007/978-3-642-80885-2_23
[4]: https://doi.org/10.1063/1.469732
[5]: https://en.wikipedia.org/wiki/Belousov%E2%80%93Zhabotinsky_reaction
[6]: https://doi.org/10.1016/j.chaos.2004.07.021
[7]: https://en.wikipedia.org/wiki/Otto_R%C3%B6ssler