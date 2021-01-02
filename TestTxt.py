
import dbm,pickle,os
class ParseTXT:
    """
    Attr:  self.letter_dict  type:{dict}
            Ex. {"d":["door","doorable",....,]}
    """
    def __init__(self,given_path=None):
        self.path = given_path
        if self.path != None:
            if "letter_databases.db.dat" not in os.listdir():
                self.startParse()
            else:
                self.letter_dict = self.downloadDatabase()
        else:
            # If none, it means that database allready created with names "letter_databases.db"
            self.letter_dict=self.downloadDatabase()
            print("Database Downloaded.")

    def startParse(self):
        self.letter_dict = {}
        with open(self.path,"r") as f:
            all_lines = f.readlines()
            for words in all_lines:
                first_letter = words[0]
                whole_word = words[:-1]
                if first_letter not in self.letter_dict:
                    self.letter_dict.setdefault(first_letter,[])
                self.letter_dict[first_letter].append(whole_word)
        self.savetoDatabse()

    def savetoDatabse(self):
        with dbm.open("letter_databases.db","c") as database:
                database["Letters"] = pickle.dumps(self.letter_dict)

    def downloadDatabase(self):
        with dbm.open("letter_databases.db","c") as database:
            return pickle.loads(database["Letters"])
    
    def findWord(self,given_word):
        first_letter = given_word[0]
        word_lists = self.letter_dict[first_letter]
        for words in range(len(word_lists)):
            if word_lists[words] == given_word:
                return True,words
        return False,-1
    
    def findSimilarWords(self,given_word):
        first_letter = given_word[0]
        words_lists = self.letter_dict[first_letter]
        similarity_lists = []
        for words in words_lists:
            try:
                if words[:len(given_word)] == given_word or words[len(given_word):] == given_word:
                    similarity_lists.append(words)
            except:
                continue
        return similarity_lists


ParseFile = ParseTXT("words.txt")
inside_check,idx=ParseFile.findWord("opera") 
print(f'Words is inside: {inside_check} and idx {idx}')
similarity_list = ParseFile.findSimilarWords("love")
print(similarity_list)
