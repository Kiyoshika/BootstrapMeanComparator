class BootstrapMeanComparator():
    def __init__(self, num_iter = 1000, test_type = "both"):
        # total number of iterations to resample "master group" when generating null hypothesis distribution (default 1000)
        self.num_iter = num_iter
        # whether the hypothesis is testing for two tailed, right tailed or left tailed (default both)
        self.test_type = test_type

    """
    - @desc : method to compute the pooled variance for two groups
    - @param g1 : numpy array of group 1
    - @param g2 : numpy array of group 2
    - @returns : float of computed pool variance
    """
    def _computePooledVariance(self, g1: np.array, g2: np.array) -> float:
        numerator = (g1.shape[0] - 1)*np.std(g1) + (g2.shape[0] - 1)*np.std(g2)
        denominator = (g1.shape[0] - 1) + (g2.shape[0] - 1)
        return numerator / denominator

    """
    - @desc : A method to compute test statistic, in this case, for comparing means
    - @param g1 : numpy array of group 1
    - @param g2 : numpy array of group 2
    - @returns : float of computed test statistic
    """
    def _computeTestStatistic(self, g1: np.array, g2: np.array) -> float:
        return (np.mean(g1) - np.mean(g2)) / self._computePooledVariance(g1, g2)

    """
    - @desc : A method to statistically compare means of two groups (input as numpy arrays)
    - @param g1 : numpy array of group 1
    - @param g2 : numpy array of group 2
    - @returns : float of p-value
    """
    def compareMeans(self, g1: np.array, g2: np.array) -> float:
        # merge two groups into a "master" group and take the mean
        master_group = np.concatenate((g1, g2))
        
        # compute overall mean
        overall_mean = np.mean(master_group)
        # subtract overall mean to make null hypothesis true
        master_group = master_group - overall_mean

        # compute our "observed" test statistic
        # this is what's used to compute the p-value
        init_statistic = self._computeTestStatistic(g1, g2)

        # resample master group 10,000 times and compute test statistics
        statistic_values = []
        for i in range(self.num_iter):
            # note: sizes must be consistent with original sample size
            sample_1 = np.random.choice(master_group, replace = True, size = g1.shape[0])
            sample_2 = np.random.choice(master_group, replace = True, size = g2.shape[0])
            statistic_values.append(self._computeTestStatistic(sample_1, sample_2))
        statistic_values = np.array(statistic_values)

        # this is a two-tailed test, so check if our observed value is "extreme" on either end
        #return sum(abs(statistic_values) > abs(init_statistic)) / num_iter
        # right, left, both tail test
        if (self.test_type == "both"): # two tailed (null values either greater or less than observed statistic)
            return sum(abs(statistic_values) > abs(init_statistic)) / self.num_iter
        elif (self.test_type == "right"): # right tailed (null values >= observed statistic)
            return sum(statistic_values >= init_statistic) / self.num_iter
        else: # left tailed (null values <= observed statistic)
            return sum(statistic_values <= init_statistic) / self.num_iter
