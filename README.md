# FhSparseGen – Fraunhofer Sparse Matrix Layout Generator for Compound Entries

The FhSparseGen – Fraunhofer Sparse Matrix Layout Generator for Compound Entries ("FhSparseGen") is used to generate sparse matrix layouts and associated algorithms for varying parallel execution schedules.

FhSparseGen was developed at Fraunhofer IGD to enable joint optimization of sparse matrix layouts and schedules for parallel execution of the sparse matrix vector product (SpMV), primarily on massively parallel graphics processing units (GPUs).

## Requirements

The FhSparseGen code generator requires [Python 3](https://www.python.org/) and [Jinja 2](https://jinja.palletsprojects.com/en/2.10.x/).
To compile the resulting code you will also need [a recent CUDA compiler and toolkit (9.2 or higher)](https://developer.nvidia.com/cuda-downloads) and a compatible C++11 compiler.

## Citation

### Journal Paper

Mueller-Roemer, J. S., A. Stork, and D. Fellner.
“Analysis of Schedule and Layout Tuning for Sparse Matrices With Compound Entries on GPUs.” 2020.
In: Computer Graphics Forum 39(6), pp. 133–143.
DOI: [10.1111/cgf.13957](https://doi.org/10.1111/cgf.13957).

```bibtex
@article{MUELLERROEMER2020,
  author = {{Mueller-Roemer}, Johannes Sebastian and Stork, André and Fellner, Dieter},
  title = {Analysis of Schedule and Layout Tuning for Sparse Matrices With Compound Entries on {GPUs}},
  year = {2020},
  journal = {Computer Graphics Forum},
  volume = {39},
  number = {6},
  pages = {133--143},
  doi = {10.1111/cgf.13957}
}
```

### Conference Paper

Mueller-Roemer, J. S., A. Stork, and D. W. Fellner.
“Joint Schedule and Layout Autotuning for Sparse Matrices with Compound Entries on GPUs.” 2019.
In: Vision, Modeling and Visualization. VMV ’19. 2019, pp. 109–116.
DOI: [10.2312/vmv.20191324](https://doi.org/10.2312/vmv.20191324).

```bibtex
@inproceedings{MUELLERROEMER2019,
  author = {{Mueller-Roemer}, Johannes Sebastian and Stork, André and Fellner, Dieter W.},
  title = {Joint Schedule and Layout Autotuning for Sparse Matrices with Compound Entries on {GPUs}},
  year = {2019},
  booktitle = {Vision, Modeling and Visualization},
  editor = {Schulz, Hans-Jörg and Teschner, Matthias and Wimmer, Michael},
  doi = {10.2312/vmv.20191324}
}
```

## License

FhSparseGen is licensed for non-commercial use under the terms found in `LICENSE.md`.
