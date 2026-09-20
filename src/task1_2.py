from mrjob.job import MRJob

class GenreTotalSales(MRJob):
    def mapper(self, _, line):
        fields = line.strip().split("\t")

        if len(fields) != 5:
            return 
        
        genre, platform, publisher, global_sales, year = fields

        try:
            global_sales = float(global_sales)
        except ValueError:
            return 

        yield genre, global_sales  

    def reducer(self, genre, sales):
        yield genre, round(sum(sales), 2)

if __name__ == "__main__":
    GenreTotalSales.run()          