.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

==============================
Medical Physician - DEPRECATED
==============================

This module has been deprecated in favor of ``medical_practitioner`` and should
only be used to update a prior ``medical_physician`` install. To avoid issues,
please update as follows:

#. Trigger the update from the command line using the flag
   ``update=medical_physician,medical_physician_us,medical_pharmacy``. This
   makes it possible for all associated updates to happen in one pass and
   cannot be done through the UI.
#. After the update, remove the ``medical_appointment`` module if it is
   currently installed as it is no longer supported. Alternatives can be found
   in the ``medical_appointment`` README.

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

* Ken Mak <kmak@laslabs.com>
* Brett Wood <bwood@laslabs.com>
* Dave Lasley <dave@laslabs.com>
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
