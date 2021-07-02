# A Graph-Based Algorithm for the Automated Justification of Collective Decisions

The code is used in the experiments of the master thesis "A Graph-Based Algorithm for the Automated Justification of Collective Decisions".

## Usage

Alternatives are represented as integers and preference orders as strings of integers. For example, `012` means that 0 is preferred to 1, which is preferred to 2. The alternatives should always start from 0. A profile is represented as a comma-separated list of preference orders, either with or without counts. For example, `012,012,210` and `2:012,1:210` express the same profile. To justify a profile, run:

    python main.py --p <profile>

You can also specificy a certain outcome:

    python main.py --p <profile> --o <outcome>

Here, `<outcome>` is a set of alternatives, simply written as a string of alternatives. For example, `01` and `10` both mean {0, 1}. Moreover, to specify a corpus of axioms, add the `--corpus <file>` flag. `<file>` must be a text file (in the same folder as `main.py`) containing an endline-separated list of axiom names. Furthermore, add `--max_depth <d>` to place a restriction on the maximum depth (`<d>`). Default: no restriction. Lastly, specify `--limit <l>` to force the gMUS extractor to generate `<l>` gMUSes and pick the smallest one (in terms of number of instances). Default: `<l>=1`.

You can also generate a random profile, for testing purposes (you cannot specify an outcome in this mode). There are several options for this. 

    python main.py --random --n <N> --m <M> --alpha <alpha>

Generates a random profile with `<N>` voters and `<M>` alternatives. The `<alpha>` values is a positive `float` which controls the contagion rate of the random generation (see the Polya-Eggenberner Urn model). In particular, for `<alpha>=0` we get the impartial culture (uniform distribution), whereas for `<alpha>=<a very high number>` we get an unanimous profile. Furthermore, the following generate a single-peaked profile:

    python main.py --random --n <N> --m <M> --gen walsh
    python main.py --random --n <N> --m <M> --gen conitzer

Where `walsh` and `conitzer` are two different generation methods (by Toby Walsh and Vincent Conitzer, respectively). See https://arxiv.org/pdf/1503.02766.pdf and https://www.jair.org/index.php/jair/article/view/10607 for details.

Finally, one can generate data from preflib profiles (no outcome can be specified here, either):

    python main.py --random --n <N> --m <M> --preflib --file <filename>

Where `<filename>` must be the name of a file in the `Preflib/` folder. Do not add `.soc` add the end of file, please.

## Drawing

To ease the reading of the outputs, it is possible to specify the option `--draw` to visually represent the explanations. However, the code to do this (`drawGraph.py`) is not meant for distribution and update, is not properly documented, and might not support extensions. This requires the library `networkx`.

## Requirements

Written in `Python3`. Requires the libraries `pylgl` and `scipy`. The binaries of the gMUS extractor, MARCO, have been included, and that should work out of the box. For drawing, library `networkx` is necessary.

Alternatively, the required libraries (with the exact versions) are listed in the `requirements.txt` file. You can install the required libraries by running:

    pip install -r requirements.txt