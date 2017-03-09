

def main(net, df=None, ds_type='kmeans', axis='row'):

  print('run downsampling\n')

  if df is None:
    df = net.export_df()

  # run downsampling
  ds_df = df

  net.load_df(ds_df)
