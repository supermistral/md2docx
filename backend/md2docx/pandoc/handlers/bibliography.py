from typing import Any, Iterable, Optional
from string import Formatter

import config
from pandoc.handlers.base import BaseHandler


class BibliographyHandler(BaseHandler):
    """
    The handler contains the bibliography processing logic
    """

    __slots__ = ['metadata', 'bibliography_dict', 'bibliography_refs']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bibliography_dict = None

    def _get_valid_settings(self, keys: Iterable[str], value: dict[str, Any],
                            base: dict[str, Any] = config.BIBLIOGRAPGHY_SETTINGS) -> dict[str, Any]:
        settings = {}

        for key in keys:
            setting_key = key.split('.', maxsplit=1)
            cur_key = setting_key[0]

            if cur_key not in settings:
                settings[cur_key] = {}

            if len(setting_key) == 2:
                next_keys = setting_key[1]
                settings[cur_key] |= self._get_valid_settings((next_keys,), value[cur_key], base[cur_key])
            else:
                val = value.get(cur_key, None) or base[cur_key]
                settings[cur_key] = val

        return settings

    def _get_default_format_key(self) -> str:
        return config.BIBLIOGRAPGHY_SETTINGS['default']

    def _create_format_rules(self) -> dict[str, dict[str, str]]:
        """
        Creates dictionary with values:

            >>> {'base': <"string to format">,
                 'electronics': <"string to be format when url is used">}

        Each key is taken from all the keys defined in `['format']['keys']` section
        """
        default_key = self._get_default_format_key()

        valid_settings = self._get_valid_settings(
            ('settings.order', 'settings.format', f'settings.{default_key}'),
            self.metadata,
            {'settings': config.BIBLIOGRAPGHY_SETTINGS}
        )['settings']

        def fill_data(settings: list[dict[str, Any]], data: dict[str, dict[str, str]]) -> None:
            for format_item in settings:
                keys = format_item.pop('keys')

                for key in keys:
                    data[key] = format_item

        data = {}

        fill_data(config.BIBLIOGRAPGHY_SETTINGS['format'], data)
        fill_data(valid_settings['format'], data)

        data[default_key] = data[valid_settings[default_key]]
        return data

    def _format_bibliography_item(self, item: dict[str,  Any],
                                  format_rules: dict[str, dict[str, str]]) -> str:
        """
        Returns a formatted bibliography item according to `base` or
        `electronic` key depends on the use `url` in the book definition
        """
        default_key = self._get_default_format_key()
        format_rule = format_rules.get(item.get('type', None) or default_key)

        url = item.get('url', None)

        if url is not None:
            rule = format_rule.get('electronic', None) or format_rule['base']
        else:
            rule = format_rule['base']

        # TODO: probably make strict mode and throw exception when there are not
        # enough keys
        formatter = Formatter()

        keys = {x[1]: '' for x in formatter.parse(rule) if x[1]}
        keys |= item

        return rule.format(**keys)

    def _create_bibliography_dict(self, format_rules: dict[str, dict[str, str]]) -> list[str]:
        """
        Creates a bibliography dictionary. Each key is an `id` from the book definition,
        value is a formatted string
        """
        bibiography = {}

        for item in self.metadata.get('items', {}):
            id = item.pop('id')
            bibiography[id] = self._format_bibliography_item(item, format_rules)

        return bibiography

    def _format_bibliography_ref(self, id: str) -> str:
        return f'[{id}]'

    def _create_bibliography_refs(self, bibliography_dict: list[str]) -> dict[str, str]:
        """
        Creates references with structure `id: ref`. Ref is represents as it is given
        in `_format_bibliography_ref()`
        """
        refs = {}
        id = 1

        for key in bibliography_dict:
            refs[key] = self._format_bibliography_ref(id)
            id += 1

        return refs

    @property
    def metadata_field(self) -> Optional[str]:
        return 'bibliography'

    def run(self) -> list[str]:
        if self.bibliography_dict is None:
            format_rules = self._create_format_rules()
            self.bibliography_dict = self._create_bibliography_dict(format_rules)
            self.bibliography_refs = self._create_bibliography_refs(self.bibliography_dict)

        return list(self.bibliography_dict.values())

    def get_reference(self, id: str) -> str:
        return self.bibliography_refs.get(id, id)
