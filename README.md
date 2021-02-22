# BootstrapMeanComparator
A toy implementation of hypothesis testing (comparing means) using a bootstrap method.

### Dependencies
* This class depends on numpy as I only allow numpy arrays and use basic numpy functions (sum, concatenate, std)

### Features
* Supports two tailed, right tailed and left tailed hypothesis tests for mean comparison

### Quick Documentation
> Initialization

To create an instance of the bootstrapper, initialize it with:
```python
bsmc = BootstrapMeanComparator()
```

> Methods

Currently only one method for this class:
* **compareMeans(g1, g2)** : g1 and g2 are numpy arrays indicating the groups to test
  * **Returns**: A float indicating the P-Value for the hypothesis test

> Optional Parameters

There are two parameters that come with this class:
* **num_iter (default = 1000)** : number of iterations to resample and compute test statistic for generating null hypothesis distrubution
* **test_type (default = "both")** : type of test to perform; "both" for two tailed, "left" for left tailed and "right" for right tailed hypothesis test
  * NOTE: Ensure the order of your groups when calling compareMeans() aligns with your test_type, e.g make sure group_1 mean is greater than group_2 mean if performing a right tail test (and vice versa for left tailed). Order doesn't matter for a two-tailed test since it tests both ends.

### Examples
#### 1. Two Tailed test for equivalent groups
Let's use numpy's random normal generator for a sample size of 30 for two groups.
```python
group_1 = np.random.normal(loc = 2.2, scale = 0.3, size = 30)
group_2 = np.random.normal(loc = 2.2, scale = 0.3, size = 30)

bsmc = BootstrapMeanComparator()
print(bsmc.compareMeans(group_1, group_2) # prints 0.451 (may vary due to randomness, obviously)
```

#### 2. Two tailed test for "different" groups
I'm going to slightly modify group 2 to be a bit greater than group 1 so they can be "statistically different"
```python
group_1 = np.random.normal(loc = 2.2, scale = 0.3, size = 30)
group_2 = np.random.normal(loc = 2.5, scale = 0.3, size = 30)

bsmc = BootstrapMeanComparator()
print(bsmc.compareMeans(group_1, group_2) # prints 0.003 (may vary due to randomness, obviously)
```

#### 3. Right tailed test for equivalent groups
Let's take same groups from example one and perform a right-tailed test (we'd expect no significance since group 1 mean isn't greater than group 2)
```python
group_1 = np.random.normal(loc = 2.2, scale = 0.3, size = 30)
group_2 = np.random.normal(loc = 2.2, scale = 0.3, size = 30)

bsmc = BootstrapMeanComparator(test_type = "right")
print(bsmc.compareMeans(group_1, group_2) # prints 0.729 (may vary due to randomness, obviously)
```

#### 4. Right tailed test for group 1 > group 2
Let's make group 1 greater than group 2 to give us our expected "significant" result
```python
group_1 = np.random.normal(loc = 2.5, scale = 0.3, size = 30)
group_2 = np.random.normal(loc = 2.2, scale = 0.3, size = 30)

bsmc = BootstrapMeanComparator(test_type = "right")
print(bsmc.compareMeans(group_1, group_2) # prints 0.0 due to rounding (may vary due to randomness, obviously)
```

#### 5. Left tailed test for group 1 < group 2
Now let's make group 1 less than group 2 and perform a left tailed test
```python
group_1 = np.random.normal(loc = 2.2, scale = 0.3, size = 30)
group_2 = np.random.normal(loc = 2.5, scale = 0.3, size = 30)

bsmc = BootstrapMeanComparator(test_type = "left")
print(bsmc.compareMeans(group_1, group_2) # prints 0.01 (may vary due to randomness, obviously)
```
