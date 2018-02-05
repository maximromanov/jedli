================
Technical manual
================

.. automodule:: jedli

Modules
=======


jedli_main
__________

This is the module that initiates the GUI (graphical user interface). In the executable version of the program, it is called jedli_main.exe

.. automodule:: jedli.jedli_main
   :members:

jedli_gui
_________

Contains the code for the main window of the Jedli GUI

.. automodule:: jedli.modules.jedli_gui
   :members:

jedli_logic
___________

Contains the code for the main Jedli search tools (Indexer, Highlighter, Context Search)

.. automodule:: jedli.modules.jedli_logic
   :members:

core_mining_functions
_____________________

Contains the functions that are used by all jedli tools

.. automodule:: jedli.modules.core_mining_functions
   :members:

jedli_global.py
_______________

Contains important global variables

.. automodule:: jedli.modules.jedli_global
   :members:

jedli_logger.py
_______________

Contains the code for the log screen that opens alongside the main Jedli window

.. automodule:: jedli.modules.jedli_logger
   :members:

jedli_EpubConverter
___________________

Contains an epub converter for Shamela texts

.. automodule:: jedli.modules.jedli_EpubConverter
   :members:

jedli_search_options
____________________

Contains the code for the search options window GUI

.. automodule:: jedli.modules.jedli_search_options
   :members:

source_selection
________________

Contains the code for the source selection window GUI

.. automodule:: jedli.modules.source_selection
   :members:

sourceUpdate
____________

Contains the code for the source update window GUI

.. automodule:: jedli.modules.sourceUpdata
   :members:

setDefaultValues
________________

Contains the code for the set default values window GUI

.. automodule:: jedli.modules.setDefaultValues
   :members:

date_plot
_________

Contains the code for the plotly graph that represents the spread of results over time

.. automodule:: jedli.modules.date_plot
   :members:

chronoplot
__________

Contains the code for the plotly scatter/line plot that represents the distribution of the sets of search words within the text

.. automodule:: jedli.modules.chronoplot
   :members:
