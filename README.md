Miner
=====

Command line tool for data mining.


Requirements
------------

* Python 2.7+
* Scikit-learn 

Structure
---------

* tools/*.py - command line tools for data mining
* data/*.csv - input data for tools

How to use
----------

Import whole package using

```python
import miner
```

or 

```python
from miner.tools import *
```

Import specific tools using

```python 
from miner.tools.table import outCsv 
from miner.tools.xy_dt import *
```

More information
----------------

Check https://github.com/nave91/miner/wiki
