import pandas as pd

class etl():

    def __init__(self):
        pass

    def rename_duplicate_columns(self):
        cols = pd.Series(self.df.columns)
        for dup in cols[cols.duplicated()].unique():
            count = 1
            for i in range(len(cols)):
                if cols[i] == dup:
                    if count > 1:
                        cols[i] = f"{dup}_{count}"
                    count += 1
        self.df.columns = cols
        return self.df
    


