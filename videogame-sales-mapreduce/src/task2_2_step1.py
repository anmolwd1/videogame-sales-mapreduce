from mrjob.job import MRJob
from mrjob.step import MRStep

class TopGenres(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper = self.mapper_get_genre_sales,
                reducer = self.reducer_sum_sales
            ),
            MRStep(
                mapper = self.mapper_sort_sales,
                reducer = self.reducer_get_top3
            )
        ]
# Step 1
    def mapper_get_genre_sales(self, _, line):
        fields = line.strip().split("\t")

        if len(fields) != 5:
            return 
        genre, platform, publisher, global_sales, year = fields

        try:
            global_sales = float(global_sales)
        except ValueError:
            return 
        yield genre, global_sales

    def reducer_sum_sales(self, genre, sales):
        yield genre, round(sum(sales), 2) 

# Step 2
    def mapper_sort_sales(self, genre, total_sales):
        yield None, (genre, total_sales)

    def reducer_get_top3(self, _, genre_sales_pairs):
        # Sort all genres by sales descending
        all_genres = sorted(
            genre_sales_pairs,
            key=lambda x: x[1],
            reverse=True
        )

        # Yield only top 3
        for genre, total_sales in all_genres[:3]:
            yield genre, total_sales

if __name__ == "__main__":
    TopGenres.run()

