text = "if (x <0) {\n   \n// some comments\nlet    state =   \"negative something\" ;   // yay, it works!\n/* multi\nline\ncomment\n */\n}"

from JackTokenizer import JackTokenizer

if __name__ == "__main__":
    tokenizer = JackTokenizer(text)