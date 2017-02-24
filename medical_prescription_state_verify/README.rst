.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

============================================
Odoo Medical Prescription State Verification
============================================

Adds a concept of types to MedicalPrescriptionOrderState that may be validated
on. Defaults with a ``verified`` type that will not allow attribute updates, or
status changes to types other than ``exception`` and ``cancel``.


Usage
=====

#. Go to Medical -> Medicine -> Prescription Orders
#. If a prescription has been moved into Verified, it can only be moved to Exception or Cancelled
#. Go to Medical -> Medicine -> Prescription Lines
#. If the parent prescription has been verified, the prescription line cannot be modified

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/159/10.0

For further information, please visit:

* https://www.odoo.com/forum/help-1

Known issues / Roadmap
======================

* Improve and provide a full description for this module into the README.rst


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/vertical-medical/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/vertical-medical/issues/new?body=module:%20medical_prescription_state_verify%0Aversion:%2010.0.1.0.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Dave Lasley <dave@laslabs.com>
* Ken Mak <kmak@laslabs.com>

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
