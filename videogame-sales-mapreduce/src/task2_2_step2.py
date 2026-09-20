from mrjob.job import MRJob
from mrjob.step import MRStep

Top3_genres = []
with open("task2_2_step1_output.txt", "r", encoding="utf-16") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            genre = parts[0].strip().strip('"')
            Top3_genres.append(genre)

print("Top 3 Genres:", Top3_genres)

class GenreDecadeSales(MRJob):

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

        if genre not in Top3_genres:
            return

        try:
            global_sales = float(global_sales)
            year = int(year)
        except ValueError:
            return

        # Convert year to decade
        decade = (year // 10) * 10

        yield (genre, decade), global_sales

    def reducer_sum_decade_sales(self, genre_decade, sales):
        genre, decade = genre_decade
        yield genre, (decade, round(sum(sales), 2))

    # STEP 2
    def mapper_sort_by_decade(self, genre, decade_sales):
        decade, sales = decade_sales
        yield genre, (decade, sales)

    def reducer_output_sorted(self, genre, decade_sales_pairs):
        sorted_pairs = sorted(
            decade_sales_pairs,
            key=lambda x: x[0]
        )

        for decade, sales in sorted_pairs:
            yield genre, (decade, sales)

if __name__ == "__main__":
    GenreDecadeSales.run()