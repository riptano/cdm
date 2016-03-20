Installer
=========

The installer is the primary class that dataset developers will be working with other than the :doc:`/context`.

Naming
------

The name of the installer file *must* be install.py found at the top level of the dataset project.  This file is created automatically when invoking :code:`cdm new` so this should not be a problem.

The installer class in the install.py may be any legal Python name.  It will be discovered automatically by the installer process.
