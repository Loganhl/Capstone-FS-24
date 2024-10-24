

def check_anagram(string1, string2):
    string1 = string1.lower()
    string2 = string2.lower()
    
    if len(string1) != len(string2):
        return False
    
    s1_char_count = {}
    s2_char_count = {}

    for i in string1:
        s1_char_count[i] = s1_char_count.get(i, 0) + 1
    for i in string2:
        s2_char_count[i] = s2_char_count.get(i, 0) + 1

    return s1_char_count == s2_char_count


def check_palindrome(string1, string2):
    string1 = string1.lower()
    string2 = string2.lower()

    if len(string1) != len(string2):
        return False
    
    n = len(string1)
    for i in range(n):
        if string1[i] != string2[n - i - 1]:
            return False
        
    return True


print("Enter the first string: ")
string1 = input()
print("Enter the second string: ")
string2 = input()



anagram = check_anagram(string1, string2)
palindrome = check_palindrome(string1, string2)


if anagram and not palindrome : 
    print(f"'{string1}' and '{string2}' are anagrams but not palindromes.")
elif palindrome:
    print(f"'{string1}' and '{string2}' are palindromes and anagrams of eachother.")
else:
    print(f"'{string1}' and '{string2}' are are neither palindromes nor anagrams")




    





