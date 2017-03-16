import pandas as pd

def main(net, df=None):
  print('check if labels are unique')

  if df is None:
    df = net.export_df()

  print('check for unqiue row and col names, if not make unique')
  print(df.shape)

  # list row names
  rows = df.index.tolist()
  if type(rows[0]) is str:

    if len(rows) != len(list(set(rows))):
      print('found duplicate rows')
      new_rows = add_index_list(rows)
      print(new_rows)
      df.index = new_rows

  elif type(rows[0]) is tuple:
    print('TUPLE ROWS')

  cols = df.columns.tolist()
  print(cols[0])
  if type(cols[0]) is str:
    # list column names
    if len(cols) != len(list(set(cols))):
      print('found duplicate cols')
      new_cols = add_index_list(cols)
      df.columns = new_cols

  elif type(cols[0]) is tuple:
    print('TUPLE COLS')

  return df

def add_index_list(nodes):

  new_nodes = []
  for i in range(len(nodes)):
    index = i + 1
    inst_node = nodes[i]
    new_node = inst_node + '-' + str(index)
    new_nodes.append(new_node)

  return new_nodes
