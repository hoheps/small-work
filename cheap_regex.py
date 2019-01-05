def cheap_regex(pattern, string):
    i = 0
    max_i = len(string)
    q = 0
    for p, x in enumerate(pattern):
        if i > max_i:
            return False
        if q: #if the placeholder from * is here
            if x == '*':
                continue
            if x == '?':
                i += 1
                continue
            if x != string[i]:
                while i <= max_i:
                    i += 1
                    if x == string[i]:
                        continue
            q = False
        if x == '?': #just iterate through the next character, but advance the index of string by one
            i += 1
            continue
        if x == '*':
            if p == len(pattern)-1: #if this is the last
                return True
            else:
                q = True #otherwise, we put in a placeholer
        if x != string[i]: #if they dont match, it's false
            return False
        i += 1
    if i < max_i:
        return False
    return True #if the pattern is small


import re
def real_regex(pattern, string):
    regex_pattern = ""
    for x in pattern:
        if x == '?':
            regex_pattern += '.'
        elif x == '*':
            regex_pattern += '.*'
        else:
            regex_pattern += x
    print(regex_pattern)
    return (re.search(regex_pattern, string).group(0) == string)


if __name__ == '__main__':
    print(cheap_regex('g*?','gross')) #honestly i give up
    print(real_regex('g*???s','gross'))