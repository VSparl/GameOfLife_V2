def make_new(filename, height, length):
    with open(f"./boards/{filename}", "w", encoding="utf-8") as fp:
        for i in range(height):
            fp.write(" " * length + ("\n" if i < height - 1 else ""))

def append_to(filename, lines):
    with open(f"./boards/{filename}", "r+", encoding="utf-8") as fp:
        length = len(fp.readline()) - 1
        print(fp.tell())
        fp.seek(0, 2)
        print(fp.tell())
        fp.write("\n")
        for i in range(lines):
            fp.write(" " * length + ("\n" if i < lines - 1 else ""))

append_to("glider_gun.gol", 50)