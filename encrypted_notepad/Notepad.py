from tkinter import *
from customtkinter import *
from tkinter import filedialog
import random, math, json


class Cipher:
    def __init__(self):
        self.symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.ĄĆĘŁÓŻŹąćęłóżź"

    @staticmethod
    def findReverse(a, m):
        if math.gcd(a, m) != 1: return None
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m

    def fragmentsOfKeys(self, key):
        keyA = key // len(self.symbols)
        keyB = key % len(self.symbols)
        return keyA, keyB

    def code(self, key, message):
        keyA, keyB = self.fragmentsOfKeys(key)
        ciphertext = ""
        for symbol in message:
            if symbol in self.symbols:
                symbolIndex = self.symbols.find(symbol)
                ciphertext += self.symbols[(symbolIndex * keyA + keyB) % len(self.symbols)]
            else:
                ciphertext += symbol
        return ciphertext

    def decode(self, key, message):
        keyA, keyB = self.fragmentsOfKeys(key)
        tekst = ""
        reverseOfKeyA = self.findReverse(keyA, len(self.symbols))
        for symbol in message:
            if symbol in self.symbols:
                symbolIndex = self.symbols.find(symbol)
                tekst += self.symbols[(symbolIndex - keyB) * reverseOfKeyA % len(self.symbols)]
            else:
                tekst += symbol
        return tekst

    def randomKey(self):
        while True:
            keyA = random.randint(2, len(self.symbols))
            keyB = random.randint(2, len(self.symbols))
            if math.gcd(keyA, len(self.symbols)) == 1:
                return keyA * len(self.symbols) + keyB


class Notepad(Cipher):
    def __init__(self, key, entry):
        super().__init__()
        self.window = CTk()
        self.window.title("Notepad")
        self.window.geometry("600x600+100+100")
        self.window.iconbitmap("notepad.ico")
        self.window.resizable(False, False)

        self.entry1 = Text(self.window, width=75, height=35, wrap=WORD)
        self.entry1.place(x=0, y=25)

        self.filemenu = Menu(self.window)
        self.menu = Menu(self.filemenu)
        self.filemenu.add_cascade(label="Save file", command=self.save_file)
        self.filemenu.add_cascade(label="Open file", command=self.open_file)
        self.window.config(menu=self.filemenu)

        self.open_file, self.text1, self.text, self.file, self.content1, self.content = None, None, None, None, None, None
        self.entry = entry
        if key != 0:
            self.key = key
        else:
            self.key = self.randomKey()
        self.pause_var = StringVar()
        self.window.mainloop()

    def save_file(self):
        try:
            self.open_file = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
            if self.open_file is None:
                return
            self.text1 = str(self.entry1.get(1.0, END))
            self.text = self.code(self.key, self.text1)
            self.open_file.write(self.text)
            self.open_file.close()
            self.entry1.delete(1.0, END)
        except:
            pass

    def open_file(self):
        try:
            self.file = filedialog.askopenfile(mode="r", filetypes=[("text files", "*.txt")])
            if self.file is not None:
                self.content1 = self.file.read()
                self.entry1.delete(1.0, END)
            self.content = self.decode(self.key, self.content1)
            self.entry1.insert(INSERT, self.content)
        except:
            pass


def main():
    window = CTk()
    window.title("Log In / Sign In")
    window.geometry("300x120+200+200")
    window.iconbitmap("notepad.ico")
    window.resizable(False, False)
    CTkLabel(window, text="Enter your password / Create a password:", text_font=("Calibri", 12)).pack()
    password = CTkEntry(window, show="*")
    password.pack()

    def confirmPass():
        s = dict()
        c = Cipher()
        t = False
        e = str(password.get())
        window.destroy()
        with open("storage.txt", "r", encoding="utf8") as file:
            s1 = c.decode(950, file.read())
            if s1 != "":
                s = json.loads(s1)
                if e in s.keys():
                    key = s[e]
                    t = True
                file.close()
        if not t:
            with open("storage.txt", "w", encoding="utf8") as file:
                r = c.randomKey()
                s[e] = r
                s2 = c.code(950, str(s))
                s3 = ""
                for x in s2:
                    if x == "'":
                        s3 += '"'
                    else:
                        s3 += x
                file.write(s3)
                key = r
        d = Notepad(int(key), e)

    CTkButton(window, text="Confirm", pady=10, command=confirmPass).pack()
    window.mainloop()


if __name__ == "__main__":
    main()
