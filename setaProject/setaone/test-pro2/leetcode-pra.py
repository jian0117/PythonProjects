import itertools

def generate_permutations(n):
    original_list = list(range(1, n+1))  # 生成[0, 1, 2, 3, ..., n]
    permutations = list(itertools.permutations(original_list))
    return permutations


def leet60(n, k):
    the_list = list(range(1, n+1))
    permutations = list(itertools.permutations(the_list))
    return ''.join(map(str, permutations[k-1]))

def leet01(nums:list[int], target:int):
    '''output = [(i, j) for i in range(len(nums)) for j in range(len(nums)) if nums[i] + nums[j] == target]
    return list(output[0])'''
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i


if __name__ == '__main__':
    a = {1:2 ,3:4}
    if 1 in a:
        print('true')