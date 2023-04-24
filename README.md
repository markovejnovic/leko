# leko

Leko is a cell-based renderer that aims to replace `jupyter-notebook` for the
use-case I have. `jpnb` promotes bad practices and, in my opinion, is difficult
to work with.

### The Good

A couple things about `leko` and `nb` feature-parity (a check means
feature-paired):

- [x] Render nice output with data.
- [x] Run and render code output (text only).
- [ ] Jupyter can share data between cells.
- [ ] Render graphs, images and other `ipython` things.
- [ ] Conditionally render cells

### The bad

Some of the issues I have with it and would like to see resolved (a check means
implemented):

- [x] Run any programming language/script/whatever
- [x] Default separated scopes across cells
- [x] Text-based, human-readable format: **Work in any editor**
- [ ] Source cell content from other files.
