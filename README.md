# FhSparseGen – Fraunhofer Sparse Matrix Layout Generator for Compound Entries

The FhSparseGen – Fraunhofer Sparse Matrix Layout Generator for Compound Entries ("FhSparseGen") is used to generate sparse matrix layouts and associated algorithms for varying parallel execution schedules.

FhSparseGen was developed at Fraunhofer IGD to enable joint optimization of sparse matrix layouts and schedules for parallel execution of the sparse matrix vector product (SpMV), primarily on massively parallel graphics processing units (GPUs).

## Requirements

The FhSparseGen code generator requires [Python 3](https://www.python.org/) and [Jinja 2](https://jinja.palletsprojects.com/en/2.10.x/).
To compile the resulting code you will also need [a recent CUDA compiler and toolkit (9.2 or higher)](https://developer.nvidia.com/cuda-downloads) and a compatible C++11 compiler.

## Citation

Mueller-Roemer, J. S., A. Stork, and D. W. Fellner.
*Joint Schedule and Layout Autotuning for Sparse Matrices with Compound Entries on GPUs.* 2019.
Conditionally accepted for presentation at and publication in the proceedings of the 24th International Symposium on Vision, Modeling and Visualization.

```bibtex
@Misc{MUELLERROEMER2019,
  author   = {{Mueller-Roemer}, Johannes Sebastian and Stork, André and Fellner, Dieter W.},
  title    = {Joint Schedule and Layout Autotuning for Sparse Matrices with Compound Entries on {GPUs}},
  year     = {2019},
  pubstate = {Conditionally accepted for presentation at and publication in the proceedings of the 24th International Symposium on Vision, Modeling and Visualization},
}
```

## License

FhSparseGen is licensed for non-commercial use under the terms found in `LICENSE.md`.
