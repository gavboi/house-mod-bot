async def search_word(word):
    with open("words.txt") as f:
        w = word.lower()
        ans = []
        ans_s = ""
        l = "temp"
        while (len(l) != 0):
            w_list = list(w)
            l = f.readline().strip()
            l_list = list(l)
            try:
                while (len(l_list) > 0):
                    w_list.remove(l_list.pop())
                if (len(w_list) == 0 and l != w):
                    ans.append(l)
                    ans_s += "`" + l + "` "
            except:
                pass
    return ans, ans_splp

def placeholder():
	return "Whoopsies! This hasn't been added yet."