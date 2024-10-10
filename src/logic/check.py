nums = [1, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

for i in nums:
    for j in nums:
        if i + j == 100:
            print(nums.index(i), nums.index(j))
