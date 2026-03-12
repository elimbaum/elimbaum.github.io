---
title: perpetual cube calendar
---

{% include math.html %}

The doctor's office had a perpetual calendar [like this one](https://store.moma.org/products/perpetual-cubes-calendar-yellow-pink-blue) at the check-in desk.

![cube calendar](/assets/img/cube/calendar.png){: width="50%"}

I didn't think much of it until later: representing all 31 days of the month with only two cubes is nontrivial!

Each cube has six sides, so we should be able to represent 36 distinct values. Of course, the cubes need not be identical, and we can display them in either order (in some sense, we'll want to minimize redundancy between each cube).

- In order to represent `11` and `22`, both cubes must have those digits.

$$
\begin{array}{|c|c|c|c|c|c|}
\hline
1 & 2 &  &  &  &  \\ \hline
1 & 2 &  &  &  &  \\
\hline
\end{array}
$$

- We also need `10`, `20`, and `30`:

$$
\begin{array}{|c|c|c|c|c|c|}
\hline
1 & 2 & 3 &  &  &  \\ \hline
1 & 2 & 0 & &  &  \\
\hline
\end{array}
$$

- Filling out the remaining single-digit days leaves us into a pickle:

$$
\begin{array}{|c|c|c|c|c|c|}
\hline
1 & 2 & 3 & 4 & 5 & 6 \\ \hline
1 & 2 & 0 & 7 & 8 & 9 \\
\hline
\end{array}
$$

This works, as long as you're ok with single-digit dates standing alone (instead of with a leading zero). But we don't want to lose that extra cube...[^1]

[^1]: This would have been a whole lot more straightforward in base 6.

[John D. Cook](https://www.johndcook.com/blog/2020/11/29/cubic-calendars/) thought about this a few years ago, and noted that we can use `6` upside down as a `9`! (This is the only such inversion. `1`, `2`, `5`, and `8` are each their own inverse.) I'm assuming this is the trick most of the calendars on the market are using.

$$
\begin{array}{|c|c|c|c|c|c|}
\hline
1 & 2 & 3 & 4 & 5 & 0 \\ \hline
1 & 2 & 0 & 7 & 8 & 6/9 \\
\hline
\end{array}
$$

This is unsatisfying! We need $$\log_2 31 = 4.95$$ bits of information to represent a calendar day, but have more than 10 bits of entropy to work with (6 sides and 4 rotations for each cube, and two orderings). In fact, a single cube ($$6\times4=24$$) is nearly sufficient to represent every day in February.

If our cube holder had a cutout in the corner, we could show different digits with different rotations:

$$
\begin{array}{|cc|cc|cc|cc|cc|cc|cc|}
\hline
0 &   & 2 &   & 4 &   & 6 &   & 8 &   & \quad & \\
  & 1 &   & 3 &   & 5 &   & 7 &   & 9 \\
\hline
\end{array}
$$

*(Assume the lower numbers are flipped.)* Such a design allows displaying every two digit number (6.6 bits), and we even have an empty face on each cube! We're also not taking advantage of reordering. However, in the general case, we would want to support any multiple of 11, and thus each cube needs every digit (besides zero, I guess).

Using all four corners, we can represent 24 unique values per cube (say `0` through `23` in each corner); two unordered cubes gives 576 combinations. But considering ordering, we pass 1000, so -- information theoretically, at least -- we might be able to represent any three-digit number with two cubes.

![cube holder](/assets/img/cube/holder.png){: width="60%"}

The above idea gets stuck after 239 (`23 | 9`); no cube has `24` or `40`:

```
 0 | 1
 0 | 2
  ...
 0 | 9
 1 | 0
  ...
 9 | 9
10 | 0
10 | 1
  ...
10 | 9
11 | 0
  ...
23 | 8
23 | 9
```

However, observe that we are only using the right-hand cube for zero and single digit values. Thus fourteen of its slots are available: make these `24 - 37`. Then we can reach `37|9`.

Here's a quick python script to double check:

```python
# perpetual calendar
import itertools as it
import collections

cubes = [
    list(range(24)),
    list(range(10)) + list(range(24, 37 + 1))
]

assert(len(cubes[0]) == len(cubes[1]))

# cubes can be in either order
pr = it.chain(it.product(cubes[0], cubes[1]), it.product(cubes[1], cubes[0]))
count = collections.Counter()

for pair in pr:
    m = int(''.join(map(str, pair)))
    count[m] += 1

missing = set(range(1000)) - count.keys()

print("First missing:", min(missing))
print("# below 1000: ", len(list(filter(lambda x: x < 1000, count.keys()))))
```

```
First missing: 380
# below 1000:  548
```

At this point, we can represent every day of the year, so no need for additional month cube. This should give a significant reduction in raw material costs.