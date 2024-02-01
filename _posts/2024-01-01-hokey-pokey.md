---
title: "oblivious hokey-pokey"
---

{% include math.html %}

While reading some recent work by Gilad Asharov, et al. (*Secure Statistical Analysis on Multiple Datasets: Join and Group-By*, [CCS 2023](https://dl.acm.org/doi/abs/10.1145/3576915.3623119)), I noticed that the paper's **Protocol 3.4**, used for computing oblivious inner joins, bore a striking resemblance to the Hokey-Pokey, with only slight modifications:

$$
\begin{align*}
&\ \ \mathbf{k}L && \text{You put your left foot in,}\\
&\ \ \mathbf{k}L || \mathbf{k}R && \text{You put your left foot out,}\\
\vec f=&\,\left[\mathbf{k}L || \mathbf{k}R  || \mathbf{k}L\right] && \text{You put your left foot in,}\\
\vec g=&\,\mathsf{Sort}(\{A, \mathbf{0}^n, -A\} \text{ on } \vec f) && \text{And you shake it all about.}\\
\vec h=&\,\mathsf{PrefixSum}(\vec g) && \text{You do the hokey pokey,}\\
\vec f'=&\,\mathsf{Invert}(\vec h) && \text{And you turn yourself around,}\\
&\,\mathsf{Output}\ \vec f' && \text{That's what it's all about!}
\end{align*}
$$

This works if we assume \\(\text{put left foot out} \approx \text{put right foot in}\\); that is, \\(\mathsf{put}(L)=-\mathsf{put}(R)=-\mathsf{put}(-L)\\) so the function \\(\mathsf{put}(\cdot)\\) is odd.