import logging
from datetime import datetime
from pprint import pformat

import me4storage.common.formatters as formatters
import me4storage.common.exceptions as exceptions

logger = logging.getLogger(__name__)

class Model:
    ''' Abstract Base Class for all models from the ME4 API

        Attributes:
            _attrs (dict): All attributes are documented in the '_attrs' dict
                These model the available attributes as documented in the ME4
                API docs.

                '_attrs' contains all attributes as keys, mapped to a string which
		represents the name of a type of formatter, defined
                in the base Model class' _formatters

            _formatters (dict): This represents a simple lookup table mapping
                the name of a formatter to a formatting function. The intention
                is to be used with the _attrs dict above, where _attrs
                will document which formatter is to be used with a certain
                field, and the _formatters dict is used to find the function
                for this.
    '''

    _attrs = {}

    _formatters = {
        'string': lambda x: x,
        'boolean': lambda x: 'yes' if x else 'no',
        'number': lambda x: str(x),
        'float': lambda x: str(x),
        'integer': lambda x: str(x),
        'percent': lambda x: f'{x:.2%}',
        'multiply': lambda x: f'{x:.2f}x',
        'array': lambda x: ','.join([str(i) for i in x]),
        'size': formatters.disk_size_formatter,
        'rate-bytes': formatters.bytes_rate_formatter,
        'date-time': formatters.date_time_formatter,
        'epoch': formatters.epoch_formatter,
        }

    def __init__(self, json_dict):
        """Initialize our basic object.

        All resources will pass in decoded JSON
        """

        logger.debug(f"Initialised: {type(self).__name__}")
        self.raw = json_dict.copy()

        try:
            self._update_attributes(json_dict)
        except Exception as err:
            raise exceptions.IncompleteResponseError(str(err))

    def _update_attributes(self, json_dict):
        """ Commmon function to extract all attributes from decoded JSON dict

        This function is common to all model classes and should be called
        at the end of each sub-class of Model's own _update_attributes
        method. The sub-class should focus on handling/extracting any special
        attributes, (eg: such as attributes that represent another model), and
        then call this base-class version of _update_attributes to extract
        all remaining attributes.

        We simply iterate over all keys in the Model's _attrs dictionary
        and lookup this key in json_dict to extract the value. Every key
        will be created as an attribute of this object, with the same name
        as the key.

        Args:
            json_dict (dict): the decoded JSON dictionary returned by the API
        """

        # All other attrs we gather from this model's _attrs definition
        for key, _ in self._attrs.items():
            # otherwise, do an explicit key lookup for all non-optional
            # keys - this will throw a KeyError exception if the key
            # is not present, which will indicate to us that the
            # the api response has changed, or we've made an error in
            # our model
            try:
                setattr(self, key.replace('-','_').lower(), json_dict[key])
            except KeyError as e:
                logger.debug(f"Failed to find key: {key} in dict:\n{pformat(json_dict)}")
                raise e

    def format_attribute(self, attr_name):
        """ For a given attribute, return a human-friendly representation

        This function looks up which formatter to use for the specifed
        attribute and returns the formatted version of this attribute's
        value.

        Args:
            attr_name (string): This must be the name of one of this
                object's attributes
        """
        # Get format for field from _attrs dict
        attr_format = self._attrs.get(attr_name, 'string')

        # Lookup format in _formatters dict to determine which function
        # to use to format the value
        formatter = self._formatters.get(attr_format, self._formatters['string'])

        return formatter(getattr(self, attr_name))

    def __repr__(self):
        output = []
        for attr in sorted(self.__dict__):
            value = self.format_attribute(attr)
            output.append(f"{attr}: {value}")
        return "\n".join(output)
