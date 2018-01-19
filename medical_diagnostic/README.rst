.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

===================
Medical Diagnostics
===================

This module introduces a number of entities related to medical diagnostics:

* ``Category`` - A general grouping used to organize diagnostics, such as
  radiology or microbiology.
* ``Criterion`` - A standard for evaluating a particular type of diagnostic
  result, such as a normal range for vitamin D in a blood test.
* ``Observation`` - A specific diagnostic result, such as the actual
  concentration of vitamin D in a blood test.
* ``Report`` - A grouping of diagnostic observations for a single patient,
  along with any possible pathologies indicated by the results.
* ``Request`` - A request for one or more diagnostic procedures to be performed
  on a specific patient.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/159/10.0

Bug Tracker
===========

Bugs are tracked on
`GitHub Issues <https://github.com/OCA/vertical-medical/issues>`_. In case of
trouble, please check there if your issue has already been reported. If you
spotted it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association:
  `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Oleg Bulkin <obulkin@laslabs.com>
* Dave Lasley <dave@laslabs.com>
* Nhomar Hernandéz <nhomar@vauxoo.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
