.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

==============================
Medical Prescription Sale Auto
==============================

This module matches prescription order lines with sale order lines
when a prescription order is verified and confirms lines that match.
If a prescription order line does not match any sale order lines,
a new sale lead is generated.

Usage
=====

To use this module, you need to:

#. Create a prescription line and a sale order line that have the same product, quantity,
and patient/partner.
#. Move the prescription to "Verified."
#. Notice that the matching sale order line is moved to "Confirmed."
#. If the prescription line and sale order line differ in product, quantity, or patient/partner,
the sale order line will be moved to "Exception."
#. If an exception is on the same sale order as a confirmed order line, it will split off and turn
into its own sale order after a number of hours. This number can be configured on the order line
itself under the "Other Information" tab as "Hours until Split."
#. If the prescription line does not match any sale order lines, a sale lead will be created.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/159/10.0

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/LasLabs/vertical-medical/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

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
