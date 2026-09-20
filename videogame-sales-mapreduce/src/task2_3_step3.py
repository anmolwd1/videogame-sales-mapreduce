from mrjob.job import MRJob
from mrjob.step import MRStep


TOP3_PLATFORMS = []
with open("task2_3_step1_output.txt", "r", encoding="utf-16") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            platform = parts[0].strip().strip('"')
            TOP3_PLATFORMS.append(platform)

TOP3_PUBLISHERS = []
with open("task2_3_step2_output.txt", "r", encoding="utf-16") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            publisher = parts[0].strip().strip('"')
            TOP3_PUBLISHERS.append(publisher)

print("Top 3 Platforms:", TOP3_PLATFORMS)
print("Top 3 Publishers:", TOP3_PUBLISHERS)

class PublisherDecadeSales(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_get_decade_sales,
                reducer=self.reducer_sum_decade_sales
            ),
            MRStep(
                mapper=self.mapper_sort_by_decade,
                reducer=self.reducer_output_sorted
            )
        ]

    # STEP 1
    
    def mapper_get_decade_sales(self, _, line):
        fields = line.strip().split("\t")

        if len(fields) != 5:
            return

        genre, platform, publisher, global_sales, year = fields

        # Filter by top 3 platforms
        if platform not in TOP3_PLATFORMS:
            return

        # Filter by top 3 publishers
        if publisher not in TOP3_PUBLISHERS:
            return

        try:
            global_sales = float(global_sales)
            year = int(year)
        except ValueError:
            return

        decade = (year // 10) * 10

       
        yield (publisher, decade), global_sales

    def reducer_sum_decade_sales(self, publisher_decade, sales):
        publisher, decade = publisher_decade
        yield publisher, (decade, round(sum(sales), 2))

    # STEP 2 
    def mapper_sort_by_decade(self, publisher, decade_sales):
        decade, sales = decade_sales
        yield publisher, (decade, sales)

    def reducer_output_sorted(self, publisher, decade_sales_pairs):
        sorted_pairs = sorted(
            decade_sales_pairs,
            key=lambda x: x[0]
        )

        for decade, sales in sorted_pairs:
            yield publisher, (decade, sales)

if __name__ == "__main__":
    PublisherDecadeSales.run()