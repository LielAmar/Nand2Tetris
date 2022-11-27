text = "if (x <0) {\n   \n// some comments\n" \
    + "let    state =   \"negative something\" ;   // yay, it works!\n" \
    + "if (\"hello\" == \"/*hello*/\") {}" \
    + "/* multi\nline\ncomment\n */\n}"

from JackTokenizer import JackTokenizer

if __name__ == "__main__":
    tokenizer = JackTokenizer(text)