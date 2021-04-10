.. Think documentation master file, created by
   sphinx-quickstart on Thu Apr  8 15:23:44 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Think
=================================

Think is a Python-based library that allows users to build *cognitive models* using *cognitive code*. Cognitive modeling is a way of building intelligent agents that think and act as much like humans as possible. Typically, people write cognitive models to simulate human behavior in particular tasks and try to match a model's behavior with data from human experiments.

Cognitive code represents a new way of writing cognitive models. Whereas traditional cognitive models are written using their own specialized languages (e.g., ACT-R or Soar), cognitive code embeds cognitive-like processing within common general programming languages. For example, let's say that you want a realistic simulation of remembering a simple fact and then later recalling that fact. This code stores a simple fact that Jane's cat is named Whiskers, and then later, tries to recall this name::

    memory.store(isa='cat', owner='Jane', name='Whiskers')
    # ...
    fact = memory.recall(isa='cat', owner='Jane')

Each line of cognitive code in this example incurs some time cost that simulates the passage of time. The last line also incorporates some chance that the fact cannot be recalled (i.e., is forgotten) --- for example, if too much time passes between storing the fact and then trying to recall that fact.

The ideas behind Think have been implemented in several languages, but the current Think library is based solely on the `Python <http://www.python.org/>`_ programming language. ?? why

[see Salvucci2016_].

.. [Salvucci2016] Salvucci, D. D. (2016). `Cognitive code: An embedded approach to cognitive modeling <http://www.cs.drexel.edu/~salvucci/publications/Salvucci-ICCM16.pdf>`_. In *Proceedings of the 14th International Conference on Cognitive Modeling* (pp. 15-20). University Park, PA: The Pennsylvania State University.


.. toctree::
    :maxdepth: 4
    :caption: Contents:

    think
    examples

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
