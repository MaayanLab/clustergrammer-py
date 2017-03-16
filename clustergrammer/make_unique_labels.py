import pandas as pd

def main(net, df=None):
  print('check if labels are unique')

  if df is None:
    df = net.export_df()

  print('check for unqiue row and col names, if not make unique')
  print(df.shape)

  return df