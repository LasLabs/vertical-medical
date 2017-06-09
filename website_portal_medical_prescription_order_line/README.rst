.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :alt: License: LGPL-3

==============================
Medical Portal - Prescriptions
==============================

This module adds prescription and prescription line info to the ``My Medical`` 
portal. Prescriptions can be filtered by patient and added to the cart 
directly from this page.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/159/10.0

Known Issues / Roadmap
======================

* Medicaments that are not in any pricelists cannot be added to the cart. Make 
  sure to at least select ``Specific prices per customer segment, currency, 
  etc.`` under ``Pricing`` in ``Sales > Settings``. Then add your medicament 
  to a pricelist so it can be added to the cart when the pricelist is active.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/vertical-medical/issues>`_. 
In case of trouble, please check there if your issue has already been 
reported. If you spotted it first, help us smash it by providing detailed and 
welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Dave Lasley <dave@laslabs.com>
* Brett Wood <bwood@laslabs.com>
* Oleg Bulkin <obulkin@laslabs.com>

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
