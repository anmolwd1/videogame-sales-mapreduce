import matplotlib.pyplot as plt


data = {} 
with open("task2_2_step2_output.txt", "r", encoding="utf-16") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) != 2:
            continue

        genre = parts[0].strip().strip('"')
        value = parts[1].strip().strip("[]").split(", ")

        try:
            decade = int(value[0])
            sales = float(value[1])
        except ValueError:
            continue

        if genre not in data:
            data[genre] = {}
        data[genre][decade] = sales

with open("task2_2_output.txt", "w") as f:
    for genre in sorted(data.keys()):
        for decade in sorted(data[genre].keys()):
            sales = data[genre][decade]
            # Format decade as "1980s", "1990s" etc
            f.write(f"{genre}\t{decade}s\t{sales}\n")

print("Saved task2_2_output.txt")
plt.figure(figsize=(12, 6))

for genre in sorted(data.keys()):
    decades = sorted(data[genre].keys())
    sales = [data[genre][d] for d in decades]
    # Format decades as labels
    decade_labels = [f"{d}s" for d in decades]
    plt.plot(decade_labels, sales, marker="o", label=genre)

plt.title("Global Sales by Decade for Top 3 Genres")
plt.xlabel("Decade")
plt.ylabel("Global Sales (millions)")
plt.legend(title="Genre")
plt.grid(True)
plt.tight_layout()

plt.savefig("task2_2_output.pdf")
print("Saved task2_2_output.pdf")
plt.show()