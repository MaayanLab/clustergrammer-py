# Clustergrammer Python Module
The python module [clutergrammer.py](clustergrammer), takes a tab-separated matrix file as input (see format [here](#input-matrix-format)), calculates clustering, and generates the visualization json (see format [here](https://github.com/MaayanLab/clustergrammer-json)) for [clustergrammer.js](https://github.com/MaayanLab/clustergrammer). See an [example workflow](#example-workflow) below:


Pleae see Clustergramer-PY's [documentation](http://clustergrammer.readthedocs.io/clustergrammer_py.html) for more information.

## Installation
The module can be used by downloading the source code here or by installing with [pip](https://pypi.python.org/pypi?:action=display&name=clustergrammer):

```
# python 2
$ pip install clustergrammer

# python 3
$ pip3 install clustergrammer
```

## Example Workflow
```
from clustergrammer import Network
net = Network()

# load matrix file
net.load_file('txt/rc_two_cats.txt')

# calculate clustering
net.make_clust(dist_type='cos',views=['N_row_sum', 'N_row_var'])

# write visualization json to file
net.write_json_to_file('viz', 'json/mult_view.json')
```
The script [make_clustergrammer.py](make_clustergrammer.py) is used to generate the visualization jsons (see [json](https://github.com/MaayanLab/clustergrammer/tree/master/json) directory of the clustergrammer repo) for the examples pages on the [clustergrammer](https://github.com/MaayanLab/clustergrammer) repo. To visualize your own data modify the [make_clustergrammer.py](make_clustergrammer.py) script on the [clustergrammer](https://github.com/MaayanLab/clustergrammer) repo.

## Jupyter Notebook Examples

### Clustergrammer-Widget Example
Clustergrammer can be used as a notebook extension widget. To install the widget use

```
# python 2
$ pip install clustergrammer_widget

# python 3
$ pip3 install clustergrammer_widget
```

Within the Jupyter/IPython notebook the widget can be run using the following commands

```
# import the widget
from clustergrammer_widget import *
from copy import deepcopy

# load data into new network instance and cluster
net = deepcopy(Network())
net.load_file('rc_two_cats.txt')
net.make_clust()

# view the results as a widget
clustergrammer_notebook(network = net.export_net_json())
```

The [clustergrammer_widget](https://github.com/MaayanLab/clustergrammer-widget) repo contains the source code for the widget.

### IFrame Clustergrammer-web Results
The python module can make an IFramed visualization in Jupyter/Ipython Python notebooks. See [Jupyter_Notebook_Example.ipynb](Jupyter_Notebook_Example.ipynb) for and example notebook or the example workflow below:

```
# upload a file to the clustergrammer web app and visualize using an Iframe
from clustergrammer import Network
from copy import deepcopy
net = deepcopy(Network())
link = net.Iframe_web_app('txt/rc_two_cats.txt')
print(link)
```

## Clustergrammer Python Module API
The python module, [clustergrammer.py](clustergrammer), allows users to upload a matrix, normalize or filter data, and make a visualization json for clustergrammer.js.

The python module works in the following way. First, data is loaded into a data state (net.dat). Second, a clustered visualization json is calculated and saved in the viz state (net.viz). Third, the visualization object is exported as a json for clustergrammer.js. These three steps are shown in the [example workflow](#example-workflow) as: ```net.load_file```, ```net.make_clust```, and ```net.write_json_to_file```.

The data state is similar to a Pandas Data Frame. A matrix also can be loaded directly as a [Data Frame](#df_to_dat) or [exported](#dat_to_df).

Below are the available functions in the ```Network``` object:

##### ```load_file(filename)```
Load a tsv file, given by filename, into the ```Network``` object (stored as ```net.dat```).

##### ```load_tsv_to_net(file_buffer)```
Load a file buffer directly into the ```Network``` object.

##### ```df_to_dat()```
This function loads a Pandas Data Frame into the ```net.dat``` state. This allows a user to directly load a Data Frame rather than have to load from a file.

##### ```swap_nan_for_zero()```
Swap all NaNs in a matrix for zeros.

##### ```filter_sum(inst_rc, threshold, take_abs=True)```
This is a filtering function that can be run before ```make_clust``` that performs a permanent filtering on rows/columns based on their sum. For instance, to filter the matrix to only include rows with a sum above a threshold, 100, do the following: ```net.filter_sum('row', threshold=100)```. Additional, filtered views can also be added using the ```views``` argument in ```make_clust```.

##### ```filter_N_top(inst_rc, N_top, rank_type='sum')```
This is a filtering function that can be run before ```make_clust``` that performs a permanent filtering on rows/columns based on their sum/variance and return the top ```N``` rows/columns with the greatest (absolute value) sum or variance. For instance, to filter a matrix with >100 rows down to the top 100 rows based on their sum do the following: ```net.filter_N_top('row', N_top=100, rank_type='sum')```. This is useful for pre-filtering very large matrices to make them easier to visualize.

##### ```filter_threshold(inst_rc, threshold, num_occur)```
This is a filtering function that can be run before ```make_clust``` that performs a permanent filterin on rows/columns based on whether ```num_occur``` of their values have an absolute value greater than ```threshold```. For instance, to filter a matrix to only include rows that have at least 3 values with an absolute value above 10 do the following: ```net.filter_threshold('row', threshold=3, num_occur=10)```. This is useful for filtering rows/columns that have the same or simlar sums and variances.

##### ```make_clust()```
Calculate clustering and produce a visualization object (stored as ```net.viz```). The optional arguments are listed below:

- ```dist_type='cosine'``` The distance metric used to calculate the distance between all rows and columns (using Scipy). The defalt is cosine distance.

- ```run_clustering=True``` This determines whether clustering will be calculated. The default is set to ```True```. If ```False``` is given then a visualization of the matrix in its original ordering will be returned.

- ```dendro=True``` This determines whether a dendrogram will be included in the visualization. The default is True.

- ```linkage_type='average'``` This determines the linkage type used by Scipy to perform hierarchical clustering. For more options (e.g. 'single', 'complete') and information see [hierarchy.linkage documentation](http://docs.scipy.org/doc/scipy-0.17.0/reference/generated/scipy.cluster.hierarchy.linkage.html).

- ```views=['N_row_sum', 'N_row_var']``` This determines which row-filtered views will be calculated for the clustergram. Filters can be based on sum or variance and the cutoffs can be defined in absolute numbers (```N```) or as a percentage of the number of rows (```pct```). These views are available on the front-end visualization using the sliders. The defalt is ```['N_row_sum', 'N_row_var']```. The four options are:
  - ```N_row_sum``` This indicates that additional row-filtered views should be calculated based on the sum of the values in the rows with cutoffs defined by absolute number. For instance, additional views will be calculated showing the top 500, 250, 100, 50, 20, and 10 rows based on the absolute sum of their values.

  - ```pct_row_sum``` This indicates that additional row-filtered views should be calculated based on the sum of the values in the rows with cutoffs defined by the percentage of rows. For instance, additional views will be calculated showing the top 10%, 20%, 30%, ... rows based on the absolute sum of their values.

  - ```N_row_var``` This indicates that additional row-filtered views should be calculated based on the variance of the values in the rows with cutoffs defined by absolute number. For instance, additional views will be calculated showing the top 500, 250, 100, 50, 20, and 10 rows based on the variance of their values.

  - ```pct_row_sum``` This indicates that additional row-filtered views should be calculated based on the variance of the values in the rows with cutoffs defined by the percentage of rows. For instance, additional views will be calculated showing the top 10%, 20%, 30%, ... rows based on the variance of their values.

- ```sim_mat=False``` This determines whether row and column similarity matrix visualizations will be calculated from your input matrix. The default is ```False```. If it is set to ```True```, then the row and column distance matrices used to calculate hierarchical clustering will be convered to similarity matrices and clustered. These visualization jsons will be stored as ```net.sim['row']``` and ```net.sim['col']```. These can be exporeted for visualization using ```net.write_json_to_file('sim_row', 'sim_row.json')``` and an example of this can be seen in [make_clustergrammer.py](make_clustergrammer.py).

##### ```write_json_to_file(net_type, filename, indent='no-indent')```
This writes a json of the network object data, either ```net.viz``` or ```net.dat```, to a file. Choose ```'viz'``` in order to write a visualization json for clustergrammer.js, e.g. ```net.write_json_to_file('viz','clustergram.json')```

##### ```write_matrix_to_tsv(filename, df=None)```
This write the matrix, stored in the network object, to a tsv file. Optional row/column categories are saved as tuples. See [tuple_cats.txt](txt/tuple_cats.txt) or [export.txt](txt/export.txt) for examples of the exported matrix file format.

##### ```export_net_json(net_type, indent='no-indent')```
This exports a json string from either ```net.dat``` or ```net.viz```. This is useful if a user wants the json, but does not want to first write to file.

##### ```dat_to_df()```
Export a matrix that has been loaded into the ```Network``` object as a Pandas Data Frame.