import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans

def main(net, df=None, ds_type='kmeans', axis='row', num_samples=100):

  print('run downsampling\n')

  if df is None:
    df = net.export_df()

  # run downsampling
  random_state = 1000
  ds_df, cluster_labels = run_kmeans_mini_batch(df, num_samples, axis, random_state)

  print(ds_df.shape)

  net.load_df(ds_df)

def run_kmeans_mini_batch(df, num_samples=100, axis='row', random_state=1000):

  # string used to format titles
  super_string = ': '

  print('number of samples')
  print(num_samples)

  # downsample rows
  if axis == 'row':
    X = df
  else:
    X = df.transpose()

  # run until the number of returned clusters with data-points is equal to the
  # number of requested clusters
  num_returned_clusters = 0
  while num_samples != num_returned_clusters:

    clusters, num_returned_clusters, cluster_labels, cluster_pop = \
      calc_mbk_clusters(X, num_samples, random_state)

    random_state = random_state + random_state

  clust_numbers = range(num_returned_clusters)
  clust_labels = [ 'cluster-' + str(i) for i in clust_numbers]

  # Gather categories if necessary
  ########################################
  # if there are string categories, then keep track of how many of each category
  # are found in each of the downsampled clusters.
  cat_types = []
  col_info = df.columns.tolist()

  # this is the index where the categories can be found in the tuple, majority
  # cat will onle be calculated for the first category type at this time
  category_index = 1

  # check if there are categories
  if type(col_info[0]) is tuple:

    # gather possible categories
    for inst_col in col_info:

      inst_cat = inst_col[category_index]

      if super_string in inst_cat:
        inst_cat = inst_cat.split(super_string)[1]

      # get first category
      cat_types.append(inst_cat)

  else:
    # need to set something up if there are no categories
    pass

  cat_types = sorted(list(set(cat_types)))

  print(cat_types)

  num_cats = len(cat_types)

  # initialize count_cats dictionary
  count_cats = {}
  for inst_clust in range(num_samples):
    count_cats[inst_clust] = np.zeros([num_cats])

  # generate an array of orig_labels, using an array so that I can gather
  # label subsets using indices
  col_array = np.asarray(df.columns.tolist())

  # populate count_cats
  for inst_clust in range(num_samples):

    # get the indicies of all columns that fall in the cluster
    found = np.where(cluster_labels == inst_clust)
    found_indicies = found[0]

    clust_names = col_array[found_indicies]

    for inst_name in clust_names:

      # get first category name
      inst_name = inst_name[category_index]

      if super_string in inst_name:
        inst_name = inst_name.split(super_string)[1]

      tmp_index = cat_types.index(inst_name)

      count_cats[inst_clust][tmp_index] = count_cats[inst_clust][tmp_index] + 1

  # calculate fractions
  for inst_clust in range(num_samples):
    # get array
    counts = count_cats[inst_clust]
    inst_total = np.sum(counts)
    count_cats[inst_clust] = count_cats[inst_clust] / inst_total

  # add number of points in each cluster
  cluster_info = []
  for i in range(num_returned_clusters):

    inst_name = 'Cluster: ' + clust_labels[i]
    num_in_clust_string =  'number in clust: '+ str(cluster_pop[i])

    cat_values = count_cats[i]

    max_cat_fraction = cat_values.max()
    max_cat_index = np.where(cat_values == max_cat_fraction)[0][0]
    max_cat_name = cat_types[max_cat_index]

    # add category title if available
    cat_name_string = 'Majority Category: ' + max_cat_name

    inst_tuple = (inst_name, cat_name_string, num_in_clust_string)

    # # do not keep track of max fraction
    # fraction_string = 'Max Pct: ' + str(max_cat_fraction)
    # inst_tuple = inst_tuple + (fraction_string,)

    cluster_info.append(inst_tuple)

  if axis == 'row':
    cols = df.columns.tolist()
  else:
    cols = df.index.tolist()

  # ds_df is always downsampling the rows, if the user wants to downsample the
  # columns, the df will be switched back later
  ds_df = pd.DataFrame(data=clusters, index=cluster_info, columns=cols)

  # swap back for downsampled columns
  if axis == 'col':
    ds_df = ds_df.transpose()

  return ds_df, cluster_labels

def calc_mbk_clusters(X, n_clusters, random_state=1000):

  # kmeans is run with rows as data-points and columns as dimensions
  mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters,
                         max_no_improvement=100, verbose=0,
                         random_state=random_state)

  # need to loop through each label (each k-means cluster) and count how many
  # points were given this label. This will give the population size of each label
  mbk.fit(X)
  cluster_labels = mbk.labels_
  clusters = mbk.cluster_centers_

  mbk_cluster_names, cluster_pop = np.unique(cluster_labels, return_counts=True)

  num_returned_clusters = len(cluster_pop)

  return clusters, num_returned_clusters, cluster_labels, cluster_pop