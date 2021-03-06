#
# Copyright 2012-2014 John Whitlock
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Define Fare model for rows in fare_attributes.txt

Google documentation from
https://developers.google.com/transit/gtfs/reference

fare_attributes.txt is optional

- fare_id (required)
The fare_id field contains an ID that uniquely identifies a fare class. The
fare_id is dataset unique.

- price (required)
The price field contains the fare price, in the unit specified by
currency_type.

- currency_type (required)
The currency_type field defines the currency used to pay the fare. Please use
the ISO 4217 alphabetical currency codes which can be found at the following
URL:

  http://www.iso.org/iso/en/prods-services/popstds/currencycodeslist.html.

- payment_method (required)
The payment_method field indicates when the fare must be paid. Valid values for
this field are:

  * 0 - Fare is paid on board.
  * 1 - Fare must be paid before boarding.

- transfers (required)
The transfers field specifies the number of transfers permitted on this fare.
Valid values for this field are:

  * 0 - No transfers permitted on this fare.
  * 1 - Passenger may transfer once.
  * 2 - Passenger may transfer twice.
  * (empty) - If this field is empty, unlimited transfers are permitted.

- transfer_duration (optional)
The transfer_duration field specifies the length of time in seconds before a
transfer expires.

When used with a transfers value of 0, the transfer_duration field indicates
how long a ticket is valid for a fare where no transfers are allowed. Unless
you intend to use this field to indicate ticket validity, transfer_duration
should be omitted or empty when transfers is set to 0.
"""

from multigtfs.models.base import models, Base


class Fare(Base):
    """A fare class"""

    feed = models.ForeignKey('Feed')
    fare_id = models.CharField(
        max_length=255, db_index=True,
        help_text="Unique identifier for a fare class")
    price = models.DecimalField(
        max_digits=17, decimal_places=4,
        help_text="Fare price, in units specified by currency_type")
    currency_type = models.CharField(
        max_length=3,
        help_text="ISO 4217 alphabetical currency code")
    payment_method = models.IntegerField(
        default=1,
        choices=((0, 'Fare is paid on board.'),
                 (1, 'Fare must be paid before boarding.')),
        help_text="When is the fare paid?")
    transfers = models.IntegerField(
        default=None, null=True, blank=True,
        choices=((0, 'No transfers permitted on this fare.'),
                 (1, 'Passenger may transfer once.'),
                 (2, 'Passenger may transfer twice.'),
                 (None, 'Unlimited transfers are permitted.')),
        help_text="Are transfers permitted?")
    transfer_duration = models.IntegerField(
        null=True, blank=True,
        help_text="Time in seconds until a ticket or transfer expires")

    def __unicode__(self):
        return u"%d-%s(%s %s)" % (
            self.feed.id, self.fare_id, self.price, self.currency_type)

    class Meta:
        db_table = 'multigtfs_fare'
        app_label = 'multigtfs'

    # For Base import/export
    _column_map = (
        ('fare_id', 'fare_id'),
        ('price', 'price'),
        ('currency_type', 'currency_type'),
        ('payment_method', 'payment_method'),
        ('transfers', 'transfers'),
        ('transfer_duration', 'transfer_duration')
    )
