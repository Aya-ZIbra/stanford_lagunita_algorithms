# The file jobs.txt describes a set of jobs with positive and integral weights
# and lengths. It has the format
#
# [number_of_jobs]
# [job_1_weight] [job_1_length]
# [job_2_weight] [job_2_length]
# ...
#
# For example, the third line of the file is "74 59", indicating that the
# second job has weight 74 and length 59.
#
# You should NOT assume that edge weights or lengths are distinct.
#
# Your task in this problem is to run the greedy algorithm that schedules jobs
# in decreasing order of the difference (weight - length).

# Recall from lecture that this algorithm is not always optimal.
# IMPORTANT: if two jobs have equal difference (weight - length), you should
# schedule the job with higher weight first. Beware: if you break ties in a
# different way, you are likely to get the wrong answer. You should report the
# sum of weighted completion times of the resulting schedule --- a positive
# integer --- in the box below.


class Job:

    def __init__(self, weight, length):
        self.weight = weight
        self.length = length
        self.diff = weight - length
        self.ratio = float(weight) / float(length)


def schedule(jobs):
    completion_time = 0
    weighted_sum = 0

    for job in jobs:
        completion_time += job.length
        weighted_sum += job.weight * completion_time

    return weighted_sum


def main():
    with open('jobs.txt', 'r') as f:
        # skip the first line that contains the number of jobs
        next(f)

        jobs = []
        for line in f:
            weight, length = line.split()
            jobs.append(Job(int(weight), int(length)))

    jobs_diff = sorted(jobs, key=lambda j: (j.diff, j.weight), reverse=True)
    jobs_ratio = sorted(jobs, key=lambda j: j.ratio, reverse=True)
    print([j.ratio for j in jobs_ratio[:5]])

    print('Weighted sum for 1st schedule: {}'.format(schedule(jobs_diff)))
    print('Weighted sum for 2nd schedule: {}'.format(schedule(jobs_ratio)))


if __name__ == '__main__':
    main()
