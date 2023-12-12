mylist = list(input("Enter list here: "))
print(f"rows: {len(mylist)}")
last_col = 0
same_cols = 1
for i, col in enumerate(mylist):
    curr_col = len(col)

    if curr_col != last_col:
        print(f"col at index {i}: {curr_col}")
    else:
        same_cols += 1

    last_col = curr_col

if same_cols == len(mylist):
    print("\nList is valid. All lengths are the same.")
