.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

==============================
Medical Prescription Sale Auto
==============================

This module introduces automated prescription sale logic that is triggered when
a previously unverified prescription order line is first verified:

* If the prescription order line has sale order lines, those sale lines are
  confirmed or marked as exceptions based on alignment with the prescription
  line (i.e. same commercial partner, same product, and consistent quantity).
* If this process results in all of the lines on a sale order getting
  confirmed, the order itself is also confirmed.
* If the prescription order line does not have sale lines, then a new CRM
  opportunity is generated for that line or an appropriate existing CRM
  opportunity is updated to include the new line. This process groups
  prescription order lines based on commercial partner to reduce the number of
  resulting opportunities.

The module also introduces a recurring background process that periodically
checks for sale orders with confirmed and exception lines. If such orders are
found and determined to have been in this state for a configurable amount of
time, the exception lines are split off into their own sale order.

Usage
=====

The time cutoff for splitting sale orders can be configured by going to
``Sales`` >> ``Configuration`` >> ``Settings`` and changing the
``Hours Before Sale Order Split`` field under ``Medical``. Please note that
values below ``1`` will not actually result in the split happening instantly as
it is handled by a periodic background process.

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
* Kelly Lougheed <kelly@smdrugstore.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
