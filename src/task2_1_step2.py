from mrjob.job import MRJob
from mrjob.step import MRStep

Top3_Platforms = []
with open("task2_1_step1_output.txt", "r", encoding = "utf-16") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            platform = parts[0].strip().strip('"')
            Top3_Platforms.append(platform)

print("Top 3 Platforms:", Top3_Platforms)

class YearlySales(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_get_yearly_sales,
                reducer=self.reducer_sum_yearly_sales
            ),
            MRStep(
                mapper=self.mapper_sort_by_year,
                reducer=self.reducer_output_sorted
            )
        ]
    
    # Step 1
    def mapper_get_yearly_sales(self, _, line):
        fields = line.strip().split("\t")

        if len(fields) != 5:
            return

        genre, platform, publisher, global_sales, year = fields

        if platform not in Top3_Platforms:
            return
        try:
            global_sales = float(global_sales)
            year = int(year)
        except ValueError:
            return

        yield (platform, year), global_sales

    def reducer_sum_yearly_sales(self, platform_year, sales):
        # Sum sales for each platform-year combination
        platform, year = platform_year
        yield platform, (year, round(sum(sales), 2))

#Step 2
    def mapper_sort_by_year(self, platform, year_sales):
        year, sales = year_sales
        yield platform, (year, sales)

    def reducer_output_sorted(self, platform, year_sales_pairs):
        sorted_pairs = sorted(year_sales_pairs, key=lambda x: x[0])

        for year, sales in sorted_pairs:
            yield platform, (year, sales)

if __name__ == "__main__":
    YearlySales.run()