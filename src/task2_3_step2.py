from mrjob.job import MRJob
from mrjob.step import MRStep

TOP3_PLATFORMS = []
with open("task2_3_step1_output.txt", "r", encoding="utf-16") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            platform = parts[0].strip().strip('"')
            TOP3_PLATFORMS.append(platform)

print("Top 3 Platforms:", TOP3_PLATFORMS)

class TopPublishers(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_get_publisher_sales,
                reducer=self.reducer_sum_sales
            ),
            MRStep(
                mapper=self.mapper_sort_sales,
                reducer=self.reducer_get_top3
            )
        ]

    # STEP 1 
    def mapper_get_publisher_sales(self, _, line):
        fields = line.strip().split("\t")

        if len(fields) != 5:
            return

        genre, platform, publisher, global_sales, year = fields

        if platform not in TOP3_PLATFORMS:
            return

        try:
            global_sales = float(global_sales)
        except ValueError:
            return

        yield publisher, global_sales

    def reducer_sum_sales(self, publisher, sales):
        yield publisher, round(sum(sales), 2)

    # Step 2
    def mapper_sort_sales(self, publisher, total_sales):
        yield None, (publisher, total_sales)

    def reducer_get_top3(self, _, publisher_sales_pairs):
        all_publishers = sorted(
            publisher_sales_pairs,
            key=lambda x: x[1],
            reverse=True
        )

        for publisher, total_sales in all_publishers[:3]:
            yield publisher, total_sales

if __name__ == "__main__":
    TopPublishers.run()