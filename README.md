# musings

### Using conda for package management

```shell
conda env create
source activate musings
```

Read the [conda documenation](http://conda.pydata.org/docs/using/envs.html#use-environment-from-file) for full details.

### Jupyter notebooks

Once the dependencies are installed, just run

```shell
jupyter notebook
```
Alternatively, if your python is too old

```shell
ipython notebook
```

### Testing webpages

Create a link to host the page with the correct name then startup a
web server in python. From the root directory of the repository.
```
$ ln -s docs musings
$ python -m SimpleHTTPServer
```

This is so all of the pages are found.
