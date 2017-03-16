import pandas as pd

def main(net, df=None):
  print('check if labels are unique')

  if df is None:
    df = net.export_df()

  print('check for unqiue row and col names, if not make unique')
  print(df.shape)

  # list row names
  rows = df.index.tolist()
  if len(rows) != len(list(set(rows))):
    print('found duplicate rows')
    new_rows = add_index_list(rows)
    print(new_rows)
    df.index = new_rows

  # list column names
  cols = df.columns.tolist()
  if len(cols) != len(list(set(cols))):
    print('found duplicate cols')
    new_cols = add_index_list(cols)
    df.columns = new_cols

  return df

def add_index_list(nodes):

  new_nodes = []
  for i in range(len(nodes)):
    index = i + 1
    inst_node = nodes[i]
    new_node = inst_node + '-' + str(index)
    new_nodes.append(new_node)

  return new_nodes
