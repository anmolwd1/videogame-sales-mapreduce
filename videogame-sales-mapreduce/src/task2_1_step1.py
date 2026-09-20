from mrjob.job import MRJob
from mrjob.job import MRStep

class TopPlatforms(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_get_platform_sales,
                reducer=self.reducer_sum_sales
            ),
            MRStep(
                mapper=self.mapper_sort_sales,
                reducer=self.reducer_get_top3
            )
        ]
    
# Step 1
    def mapper_get_platform_sales(self, _ , line):
        fields = line.strip().split("\t")

        if len(fields) !=5:
            return
        
        genre, platform, publisher, global_sales, year = fields

        try:
            global_sales= float(global_sales)
        except ValueError:
            return
        yield platform, global_sales

    def reducer_sum_sales(self, platform, sales):
        yield platform, round(sum(sales), 2)

# Step 2 
    def mapper_sort_sales(self, platform, total_sales):
        yield None, (platform, total_sales)

    def reducer_get_top3(self, _, platform_sales_pairs):
        all_platforms = sorted(
            platform_sales_pairs,
            key=lambda x: x[1],
            reverse=True
        )

        # Yield only top 3
        for platform, total_sales in all_platforms[:3]:
            yield platform, total_sales

if __name__ == "__main__":
    TopPlatforms.run()