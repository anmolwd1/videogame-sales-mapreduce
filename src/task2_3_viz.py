import matplotlib.pyplot as plt


data = {}

with open("task2_3_step3_output.txt", "r", encoding="utf-16") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) != 2:
            continue

        publisher = parts[0].strip().strip('"')

        # Parse [decade, sales] value
        value = parts[1].strip().strip("[]").split(", ")

        try:
            decade = int(value[0])
            sales = float(value[1])
        except ValueError:
            continue

        if publisher not in data:
            data[publisher] = {}
        data[publisher][decade] = sales

with open("task2_3_output.txt", "w") as f:
    for publisher in sorted(data.keys()):
        for decade in sorted(data[publisher].keys()):
            sales = data[publisher][decade]
            f.write(f"{publisher}\t{decade}s\t{sales}\n")

print("Saved task2_3_output.txt")


plt.figure(figsize=(12, 6))

for publisher in sorted(data.keys()):
    decades = sorted(data[publisher].keys())
    sales = [data[publisher][d] for d in decades]
    decade_labels = [f"{d}s" for d in decades]
    plt.plot(decade_labels, sales, marker="o", label=publisher)

plt.title("Global Sales by Decade for Top 3 Publishers\n(Within Top 3 Platforms)")
plt.xlabel("Decade")
plt.ylabel("Global Sales (millions)")
plt.legend(title="Publisher")
plt.grid(True)
plt.tight_layout()

plt.savefig("task2_3_output.pdf")
print("Saved task2_3_output.pdf")
plt.show()