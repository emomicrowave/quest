
Quest
=================================

Quick-start guide
-----------------

Add a task:

.. code-block:: bash

    $ quest new "travel to Lich's lair" --project lich --due tomorrow
    65f3 lich: travel to Lich's lair tomorrow

    $ quest new "defeat evil Lich" -p lich -d eow
    1fbb lich: defeat evil Lich in 2 days (Sun)

List all your tasks:

.. code-block::

    $ quest ls
    65f3 lich: travel to Lich's lair tomorrow
    1fbb lich: defeat evil Lich in 2 days (Sun)

Complete a task:

.. code-block::

    $ quest done 65f3
    65f3 lich: travel to Lich's lair tomorrow

    $ quest ls
    1fbb lich: defeat evil Lich in 2 days (Sun)

    $ quest ls --no-hide-done
    1fbb lich: defeat evil Lich in 2 days (Sun)
    65f3 lich: travel to Lich's lair today

.. toctree::
   :maxdepth: 2
   :caption: Contents:






Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
