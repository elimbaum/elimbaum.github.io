---
title: A cryptanalysis of Monk S4E8, "Mr. Monk and Little Monk"
---

{% include math.html %}

**Warning!** This posts contains spoilers for *Monk* S4E8. If you don't want an episode of a mid-2000s comedy/police procedural to be spoiled, don't read this!

---

![sketch](/assets/img/monk-crypt.png)
*A young Mr. Monk (left) and the bully Leo (right)*

I was recently watching an [episode of *Monk*][1] where we get some insight into Mr. Monk's childhood. In one middle-school flashback, Leo, the local bully, executes a pretty clever sleight of hand:

1. Leo helps Sherry, Monk's crush and locker neighbor, get some books out of her locker.

2. While closing the locker, Leo very quickly swaps his own padlock out for Sherry's, and locks it.[^1]

3. He returns later that night, unlocks his padlock, places some incriminating evidence in Sherry's locker, and replaces *her* padlock (still unlocked from earlier).

4. The next day, Sherry is framed for stealing the bake sale money!

[^1]: Going back through the episode, it doesn't *actually* look like Leo swapped the locks on set. Perhaps the mystery goes even deeper.

I had just read Matt Blaze's 2002 article "Cryptology and Physical Security: Rights Amplification in Master-Keyed Mechanical Locks" [[pdf]][2], which takes a cryptographer's magnifying glass to a physical security issue. So, I wondered, is there a cryptographic analog to the above scenario? This smells like some kind of integrity protection or non-repudiation, maybe... let's see.

## The Basics

The most natural comparison here is that the "locker" is protecting some secret message \\(M\\). Locking the locker is encryption; opening it is decryption. But this is clearly not symmetric encryption: *you don't need to know the combination to close an unlocked lock*.[^2]

[^2]: There's also some integrity protection at play: no one else can mess with the contents of your locker while it's locked. But I won't consider that here.

Call the combination \\(k_c\\) and the encrypted (locked) message \\(C\\). To open the lock, we decrypt:

$$
M = D(C, k_c)
$$

But to close the lock, we can't use \\(k_c\\), so there must be some *other* key:

$$
C = E(M, k_{?})
$$

Ok, well this is just a public key cryptosystem! And this is actually a great analog: anyone (who has your public key) can lock your locker, but only you can open your locker (with your combination → private key).

So we have our combination, \\(k_c\\), and some public "locking" key we'll call \\(k_p\\). What exactly did Leo do, then?

## Leo's Swap

In the episode, Leo swaps Sherry's lock with his own; that is, he encrypt's Sherry's locker with his *own* public key, \\(k_{p,L}\\):

$$
C' = E(M, k_{p,L})
$$

where \\(C'\\) is the maliciously encrypted locker. (Note that this implies that Leo *had read access to Sherry's message, but not write access*, which maybe breaks the analogy a little bit – but clarifies why he had to come back later to "write" the incriminating evidence. Perhaps, rather than imagining Leo performing the first swap, we imagine that Sherry locked her locker, but was tricked into using the wrong key.)

Leo comes back that night and performs the second swap, first using his own private key, then re-encrypting with Sherry's public key.

$$
M = D(C', k_{c,L})
$$

$$
C = E(M, k_{p}) 
$$

When Sherry returns the next morning, this looks no different than if she had locked the locker herself. Incidentally, this is a convenient analogy, as well: there's no way, in general, to tell which key was used to encrypt a given ciphertext, besides by attempting to decrypt it.[^3]

[^3]: But, then again, Monk solves the mystery by noticing that Sherry's lock was not reset to zero -- a habit of hers.

What's the lesson here? Don't let anyone touch your public key! If an attacker can trick you into encrypting a message with the wrong public key, they can pull a Leo and modify your data! This isn't necessarily an interesting conclusion but I'm glad we can draw connections between the physical and digital worlds.

## HMAC

Could integrity protection help? Originally, I thought not – but actually, I'd suggest this *is exactly what happened in the episode.*

In an authenticated encryption scheme, we encrypt our message with one key, and create a message authentication code with a second, appending it to our ciphertext.[^4] While this is actually meant to protect against active attackers (say, one who tries to manipulate our data while it is encrypted), it also provides us with confidence of authorship.

Granted, HMAC requires a pre-shared secret, which we're not assuming we have in this asymmetric case. In reality, if you were able to share a secret with somebody, you would just be using symmetric encryption - there would be no reason to use asymmetric encryption and allow other people to "lock" your locker.

In the episode, however, Sherry resetting her dial to zero is in some way akin to an authentication code -- *where the shared secret between her and Monk is the very fact that she is doing it*. This is more appropriately, I suppose, steganographic integrity protection...

Not a perfect analogy, but some fun parallels.

[^4]: IIRC you're not supposed to MAC-then-Encrypt; nice explanation from Moxie Marlinspike [here][3].

## Could this happen?

I'm trying to think if such a swap could even happen, and I don't think this is a super realistic concern outside of middle school. Basically, this is a question of PKI management, rather than cryptography. (In general, we can't stop social engineering with clever math!)

---

[1]: https://monk.fandom.com/wiki/Mr._Monk_and_Little_Monk
[2]: https://www.mattblaze.org/papers/mk.pdf
[3]: https://moxie.org/2011/12/13/the-cryptographic-doom-principle.html