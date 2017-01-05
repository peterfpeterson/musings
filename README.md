# musings

Some of this is a
[webpage found here](https://peterfpeterson.github.io/musings/).

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

The webpages are being generated using [Jekyll](https://jekyllrb.com)
and
[gh-pages](https://help.github.com/articles/about-github-pages-and-jekyll/). To get things running from scratch:

1. install ruby and ruby developer packages (e.g. `dnf install ruby ruby-devel`)
2. `gem install bundle`
3. `cd docs`
4. `bundle update`
5. `bundle exec jekyll serve --watch --drafts`

Only the last step needs to be done if changes to the site are being
made.

Various bits of the design were borrowed from
[jekyll-bootstrap](https://github.com/plusjade/jekyll-bootstrap/).
