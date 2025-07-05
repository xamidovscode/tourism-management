class Solution:
    def add_arr(self, list1: list, list2: list):

        for i in list1:
            for j in list2:
                if j['id'] == i['id']:
                    j.update(i)
                    break
            else:
                list2.append(i)
        return list2


a = Solution()
list1 = [
    {
        "id": 1,
        "full_name": "Ali",
        "age":55
    },
    {
        "id": 3,
        "full_name": "Vali",
    },
]
list2 = [
    {
        "id": 1,
        "full_name": "Vali",
    },
    {
        "id": 2,
        "full_name": "Tom",
    },
]

print(a.add_arr(list1,list2))
