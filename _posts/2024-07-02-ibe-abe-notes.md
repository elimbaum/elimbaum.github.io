---
title: "some notes on identity- and attribute-based encryption"
---

{% include math.html %}

> These are my _very rough_ notes from a talk. There are probably a few mistakes. Use at your own risk! If (when) you find mistakes feel free to shoot me an email :)

1. TOC
{:toc}

Heavily drawn from:
- [Boneh-Shoup](https://toc.cryptobook.us/), chapter 15
- Bar-Ilan Winter School on Pairings [[full YouTube playlist](https://www.youtube.com/playlist?list=PLXF_IJaFk-9C4p3b2tK7H9a9axOm3EtjA)]
	- [Dan's slides](https://csrc.nist.gov/csrc/media/Presentations/2023/stppa5-ibe/images-media/20230209-stppa5-Dan-Boneh--IBE.pdf)

## Pairings
Pairings exist for certain elliptic curve groups. The actual operation is complicated and not worth going into; just understand the implications.

- \\(e:\mathbb G\times\mathbb G\rightarrow \mathbb G_T\\)
	- This is a _symmetric_ pairing; both input groups are the same. Can also have asymmetric.
	- \\(\mathbb G\\) is a subgroup of points on the elliptic curve.
	- \\(\mathbb G_T\\) is a group of integers. Watch out for different group operations!
- Basic rule: \\(e(u, ab)=e(u,a)e(u,b)\\)
	- also applies symmetrically on the left.
- Usual formulation: exponent rule. \\(e(g^a, g^b)=e(g,g)^{ab}\\)

Pairing solves DDH: given \\(g^a, g^b, g^c\\), check if \\(e(g^a, g^b)=e(g,g)^{ab}\overset ?=e(g,g^c) = e(g,g)^c\\). CDH is still hard. Dlog is equivalent in both groups, so must choose groups such that source and target both have hard dlog.

New hard problem: BDH: decision bilinear diffie hellman. given \\(g^\alpha,g^\beta,g^\gamma\\), \\(e(g,g)^{\alpha\beta\gamma}\\) indistinguishable from random

## IBE
**Identity-Based Encryption**. Introduced by Shamir 1984. Wasn't clear we could actually encrypt; only signatures.
- ElGamal doesn't work, because if you pick your public key \\(g^\alpha\\) to be a specific string, we can't extract secret key \\(\alpha\\) (dlog)

Under PK crypto: we need a PKI. You need to talk to the PKI for every new person you want to contact. (OK, on the internet, you don't have to talk to the CA for certs, but you need to check revocation lists. And you still need an extra round of communication to get a cert chain for the server.) Maybe better to flip this around and make *recipient* talk to PKI when they want to decrypt their messages.

What we have / what we want:
- PKC: I hold my SK, and post PK with trusted party / CA
- IBE: everyone knows my PK, and trusted party holds my SK, which I retrieve when it's time to decrypt

**Schematic**:
- public key is an arbitrary string, like my email. maybe add timestamp for freshness / easy revocation: `ID = "elibaum@bu.edu || 2 July 2024"`
- private key is held by a trusted party, with whom I somehow (???) authenticate
	- this authentication is hard, so maybe makes IBE best for organizations which can afford OOB auth
	- or, ZK?

Functionalities:
- **Setup:** \\((mpk,msk)\leftarrow S()\\)
- **KeyGen:** \\(sk_{id}\leftarrow G(msk,id)\\)
- **Encrypt:** \\(c\leftarrow E(mpk, id, m)\\)
- **Decrypt:** \\(m\leftarrow D(sk_{id},c)\\)

Blackbox separation from PK crypto, because we can think of IBE as compressing exponentially many public keys into the (small) public parameters.

...constructions from pairings (BF01, BB04); lattices (GPV08), quadratic residues. Seem to be nice parallels between these constructions.

**Trusted party** is an issue. (Again, works well for hierarchical orgs like large companies.) Alternative: distributed trusted party. Trusted _committee_ holds shares \\([s]_i\\) of secret key \\(s\\). See below.

Other things:
- Don't actually use _just_ your email, because key theft. Maybe your email + the date
	- If you do this, then revocation + future-encryption are easy
	- When you get fired, your company stops handing you new \\(sk\\)
	- Can also delegate keys for certain dates
- Trusted party here can decrypt *all* messages: not the case for a CA, which can only lie about your identity / cert (MitM)

### [[BF01]](https://eprint.iacr.org/2001/090)
Uses Weil Pairing. One of the early examples of using pairings "productively"; i.e., not as an attack against elliptic curves. Random Oracle.

Basic scheme, CPA-secure:

**Setup**:
- Pick random master key \\(s\in\mathbb Z\\) and generator \\(P\in\mathbb G\\).
- pick hash functions \\(H_1:\\{0,1\\}^\*\rightarrow\mathbb G\\) and \\(H_2:\mathbb G_T\rightarrow\\{0,1\\}^\*\\)
- public key is \\(P_{pub}=sP\\)
- _note_: secret key is a number. public key is a point on the curve.

**KeyGen**:
- Given an authenticated \\(\mathsf{ID}\\), compute private key \\(d_\mathsf{ID}=sH_1(\mathsf{ID})\\)

**Encrypt**:
- message \\(M\\). Choose random \\(r\in\mathbb Z\\)
- Compute \\(g_\mathsf{ID}=e(H_1(\mathsf{ID}), P_{pub})\\)
- \\(C=(rP, M\oplus H_2(g_\mathsf{ID}^r))\\)

**Decrypt**:
- Let \\(C=(U, V)\\).
- To decrypt with private key \\(d_\mathsf{ID}\\), compute: \\(M=V\oplus H_2(e(d_\mathsf{ID}, U))\\)

#### Correctness
$$
\begin{align*}
H_2(e(d_\mathsf{ID}, U))&=H_2(e(sH_1(\mathsf{ID}), rP))\\
&=H_2(e(H_1(\mathsf{ID}), P)^{rs})\\
&=H_2(e(H_1(\mathsf{ID}), sP)^r)\\
&=H_2(g_\mathsf{ID}^r)
\end{align*}
$$

To deal with some trust issues: split the secret key.
1. **Setup**: KeyGen committee each generate \\(s_i\\) and compute \\(s_iP\\). dlog is hard so can share this value publicly to compute \\(\sum_i s_i P=sP=P_{pub}\\).
2. **KeyGen**: compute shares of secret key, \\(d_\mathsf{ID}=\sum_i s_i H_1(\mathsf{ID})\\). Requestor reconstructs locally.
3. **Encrypt**: don't interact with committee.

*note:* not strictly a sum operation, but repeated group op. semantically close enough. This moves trust from a single party to a committee, of which you only need to trust one member. Additive scheme easiest to understand but using Shamir sharing instead gives you malicious security "for free" (can use pairing to check well-formed shares, malicious parties can't cheat bc DDH still hard in source group. See paper for details).
- You can use this as a basic voting system! (Where `you win election == you are given access to some secret key`)
- Committee consists of _everyone_. Only hand out your share of private key if you want to vote for a specific person / proposition.
	- how to make this partial threshold?

Generic transformation (Fujisaki-Okamoto) to get CCA: send some redundant info, basically make \\(r\\) dependent on other info including the message. Reject if inconsistent.

[[BB04]](https://eprint.iacr.org/2004/172), [[Waters05]](https://eprint.iacr.org/2004/180) remove RO but have very large public parameters (~ \\(\log\\) in the size of the ID), and loose reduction, so worse scaling with security parameter.

### [[Gentry06]](https://www.iacr.org/archive/eurocrypt2006/40040451/40040451.pdf)
Removes random oracle, and tiny public parameters, but crazy assumption. (\\(q\\)-ABDHE).
#### Decision problem
q-ABDHE. \\(q\\) here is the *number of ID queries* made my adversary: not great as a reduction even though it is tight.

> \\(q\\)-decision augmented bilinear diffie-hellman exponent

- **Input**: \\((g', g, g^\alpha, g^{\alpha^2},\dots,g^{\alpha^q}, g^{\alpha^{q+2}}, \dots, g^{\alpha^{2q}})\\). note missing \\(\alpha^{q+1}\\) term.
- (Try to) **Output**: \\(e(g, g')^{a^{q+1}}\\)

Even with weird assumption, _extremely_ conservative security bounds still give better security-parameter performance compared to earlier constructions.

#### CPA construction

**Setup**: Pick random generators \\(g,h\\) and secret key \\(\alpha\\). Output pp \\((g, g^\alpha, h)\\).

**KeyGen**: for each \\(\mathsf{ID}\\), choose a random \\(r_\mathsf{ID}\\) and output

$$
d_\mathsf{ID}=(r_\mathsf{ID}, h_\mathsf{ID});\qquad h_\mathsf{ID}=(hg^{-r_\mathsf{ID}})^{1/(\alpha-\mathsf{ID})}
$$

**Encrypt**: generate random \\(s\\) and output

$$
C=(g^{s(\alpha-\mathsf{ID})},\ e(g,g)^s,\ m\cdot e(g, h)^{-s})
$$

> Can precompute all pairings! Pairings are the slow part (~ cost 10x exponentiation), so precomputation helps a lot

**Decrypt**: Let ciphertext \\(C=(u, v, w)\\). Output:

$$
m=w\cdot e(u, h_\mathsf{ID})\cdot v^{r_\mathsf{ID}}
$$

#### Correctness
need to show masks are equivalent.

$$
\begin{align*}
e(u, h)v^r&=e\left(g^{s(\alpha-\mathsf{ID})}, (hg^{-r})^{1/(\alpha-\mathsf{ID})}\right)e(g,g)^{sr}\\
&=e\left(g^{s(\alpha-\mathsf{ID})},h^{1/(\alpha-\mathsf{ID})}\right)e\left(g^{s(\alpha-\mathsf{ID})},g^{-r/(\alpha-\mathsf{ID})}\right)e(g,g)^{sr}\\
&=e(g,h)^s e(g,g)^{-rs}e(g,g)^{sr}\\
&=e(g,h)^s
\end{align*}
$$

[[Waters09]](https://eprint.iacr.org/2009/385.pdf) did this under standard model (also HIBE), with no funny assumptions, but complex construction and novel proof technique. ("Dual System encryption")

### Other
**IBE implies simple signatures!** Use message as identity. Signature is the secret key!
- funny verification algorithm: encrypt random message \\(r\\) for ID. check that sig (_secret key_ for ID!) can decrypt correctly. This is a randomized verification algorithm!
- converse: many signature schemes also give IBE

**Anonymous IBE**: additional constraint: don't want ciphertext to reveal intended identity. This enables searching on encrypted data, as a nice side effect. BF already satisfies, bc RO. In std model, harder. Gentry works. BB is not anonymous.

**Hierarchical IBE:** break up the keys into multiple levels: you can decrypt if you have secret key for this node *or any of its parents*. Older constructions: ciphertext size grows linearly in tree depth, but more recently, independent of hierarchy depth (unbounded)
- Important functionality: *delegate* to your children
- Dual System encryption, [[Waters09]](https://eprint.iacr.org/2009/385.pdf)
- Unbounded depth, [[LW11]](https://eprint.iacr.org/2011/049.pdf)

**Searching on encrypted data**: (BS §15.6.4.3) search terms are identities. See if decryption works... maybe just encrypt `1` under each ID. Upon encryption, sender also includes `E(search-terms, 1)`. So can't have too many, maybe just searching the subject line? But then how to bind?

**Lattice constructions** like [[GPV08]](https://eprint.iacr.org/2007/432.pdf): dual of Regev public key. Effectively swap keygen and encrypt. Existing Regev construction allowed extracting secret key from (exp sparse) public keys using trapdoor, but here we need dense public keys, which the dual gives. structurally similar to QR constructions.

Other other things:
- wildcard IBE: encrypt to `*@cs.bu.edu` or `john@*.com`
- generalizations of searching (more than equality): inner product, vector, ranges, logical predicates... get into ABE
- [[DG17]](https://eprint.iacr.org/2017/543) bypasses prior impossibility results, builds IBE from CDH with no pairing. How? confusing construction; build "chameleon encryption" inside garbled circuits.
	- prohibitively expensive in practice; public params ~ length of \\(ID\\)
	- impossibility result was for blackbox constructions.
	- running encryption inside g.c. is extremely non-blackbox

## ABE
**Attribute-based Encryption**. ABE as IBE, for `id-equals` predicate. Private ABE: ciphertext does not reveal attribute; *"predicate encryption"*. However, below, considering public-policy case.

Policies must be monotonic, so no NOTs, by default, but you can hardcode `NOT-ATTR` as a positive attribute.

For collusion resistance, need to randomize keys, so that colluding users can't combine their keys. "Personalized randomness"

### Key Policy
- Generate a user key for a particular policy (formula)
- Encrypt a message with a number of attributes

> example: Eli can read a document if it follows policy `(TOPIC-CRYPTO and SECRET) or (TOPIC-CRYPTO and UNCLASSIFIED) or (TOPIC-SUBMARINE and UNCLASSIFIED) or TOPIC-ELEPHANTS`

Encrypt documents with attributes
- `TOPIC-SUBMARINE`, `SECRET` => can't decrypt
- `TOPIC-CRYPTO`, `SECRET` => can decrypt 
- `TOPIC-ELEPHANTS`, `TOP-SECRET` => can decrypt
- `TOPIC-CHOCOLATE` => can't decrypt

### Ciphertext Policy
- Generate a user key with a set of attributes
- Encrypt a message under a particular policy (formula over attributes)

> example: a certain document about hiring a new professor can be read by people who satisfy this policy:
```
DEPT-CHAIR
or
(HIRING-COMMITTEE and [
  (PROFESSOR and (TEACHES-CRYPTO or TEACHES-THEORY))
  or
  (STUDENT and TOOK-CRYPTO)
])
```

- Mayank: `HIRING-COMMITTEE`, `PROFESSOR`, `TEACHES-CRYPTO`. yes
- Leo: `PROFESSOR`, `TEACHES-CRYPTO`. no
- Matta: `DEPT-CHAIR`, `HIRING-COMMITTEE`. yes
- René: `HIRING-COMMITTEE`, `STUDENT`. no

To construct we can *basically* just flip everything around. Some small changes to randomize.

AND/OR: tree structure with cancellations. ORs for free. AND is a share split. attributes are leaves with values: *satisfying set of shares* should allow us to reconstruct \\(\alpha\\). (See Allison Bishop's ABE talk @ Bar-Ilan for a demo)

We don't (didn't?) know how to build general circuit ABE from pairings (limited to \\(\mathsf{NC}_1\\), log-depth circuits). Symmetric key CP-ABE, [[AY20]](https://eprint.iacr.org/2020/1432.pdf). 
- KP-ABE from LWE can support poly sized circuits

### Smaller-universe KP-ABE
Construction from [[GPSW06]](https://eprint.iacr.org/2006/309). Allison Bishop ABE talk @ 14m: simple view on the construction. abstract away the sharing scheme and reconstruction.

## etc

Predicate encryption, generally: you can decrypt with key \\(K_P\\) if \\(P(m)=1\\). Hide the policy; hand out keys based on what you want to key-holder to be able to decrypt.

Functional encryption: \\(sk_f\\) allows for evaluation of \\(f\\) over ciphertext, similar to homomorphic. Regular PK crypto is just functional with identity function. IBE has function that returns \\(m\\) if \\(id=id'\\) — equality over part of the ciphertext.

Other examples: output \\(s(m)\\), probability of message being spam. Or, fraud detection at gateway, only if certain thresholds are met.

This is different than FHE because we get a _plaintext_ output.

Constructions:
- low degree poly (\\(d=1,2\\)) from pairings... inner product 
- MPC client-server // GC
- [[AV19]](https://eprint.iacr.org/2019/314.pdf)