import matplotlib.pyplot as plt

data = {}

with open("task2_1_step2_output.txt", "r", encoding = "utf-16") as f:
    for line in f:
        parts= line.strip().split("\t")
        if len(parts) != 2:
            continue

        platform = parts[0].strip().strip('"')
        value = parts[1].strip().strip("[]").split(",")

        try:
            year = int(value[0])
            sales = float(value[1])
        except ValueError:
            continue

        if platform not in data:
            data[platform] = {}
        data[platform][year] = sales

with open("task2_1_output.txt", "w") as f:
    for platform in sorted(data.keys()):
        for year in sorted(data[platform].keys()):
            sales = data[platform][year]
            f.write(f"{platform}\t{year}\t{sales}\n")

print("Saved task2_1_output.txt")

plt.figure(figsize=(12, 6))

for platform in sorted(data.keys()):
    years = sorted(data[platform].keys())
    sales = [data[platform][y] for y in years]
    plt.plot(years, sales, marker="o", label=platform)

plt.title("Yearly Global Sales for Top 3 Platforms")
plt.xlabel("Year")
plt.ylabel("Global Sales (millions)")
plt.legend(title="Platform")
plt.grid(True)
plt.tight_layout()

plt.savefig("task2_1_output.pdf")
print("Saved task2_1_output.pdf")
plt.show()