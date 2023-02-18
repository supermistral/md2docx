import importlib
from typing import Any, Callable, Union

import config
from exceptions import MetadataValidationErrorItem, MetadataValidationErrorType


def concat_keys(key: str, child_key: str) -> str:
    """
    Creates keys path e.g. ``list.lvl.0.something``
    """
    return key + ('.' if key else '') + child_key


def _value_validator(
    key: str,
    current_key: str,
    value: Any,
    validators: dict[str, str] = config.ATTRIBUTES_VALIDATORS
) -> list[MetadataValidationErrorItem]:
    """
    Returns a list of errors received or generated as a result of calling the generator
    on the incoming validators map
    """
    full_key = concat_keys(key, current_key)
    validator_module = validators.get(current_key, None)

    if validator_module is None:
        return [(
            MetadataValidationErrorItem(
                key=full_key,
                err_type=MetadataValidationErrorType.UNKNOWN_KEY
            )
        )]

    validator = get_validator(validator_module)
    result = validator(key=full_key, value=value)

    # Create error instance if validator returns bool
    if isinstance(result, bool):
        if not result:
            return [(
                MetadataValidationErrorItem(
                    key=full_key,
                    err_type=MetadataValidationErrorType.WRONG_VALUE_TYPE
                )
            )]
        return []

    # It's list of error items
    return result


def float_validator(value: Any, **kwargs) -> bool:
    return isinstance(value, str) and value.isnumeric()


def integer_validator(value: Any, **kwargs) -> bool:
    return float_validator(value) and int(value) == float(value)


def existing_metadata_validator(metadata: dict[str, Any]) -> list[MetadataValidationErrorItem]:
    errors = []

    for key, value in metadata.items():
        errors += _value_validator(
            key='',
            current_key=key,
            value=value,
            validators=config.METADATA_VALIDATORS
        )

    return errors


def _is_dict_validator(key: str, value: Any, errors: list[MetadataValidationErrorItem]) -> bool:
    """
    Updates the list of errors if type of value is not dictionary
    """
    if not isinstance(value, dict):
        errors.append(
            MetadataValidationErrorItem(
                key=key,
                err_type=MetadataValidationErrorType.WRONG_VALUE_TYPE
            )
        )
        return False
    return True


def _existing_attributes_validator(
    key: str,
    value: Any,
    errors: list[MetadataValidationErrorItem],
) -> None:
    """
    Checks if a dictionary key exists in ``config.ATTRIBUTES_VALIDATORS``
    """
    if not _is_dict_validator(key, value, errors=errors):
        return

    for current_key, current_value in value.items():
        errors += _value_validator(key=key, current_key=current_key, value=current_value)


def _list_lvl_validator(key: str, value: Any, errors: list[MetadataValidationErrorItem]) -> None:
    """
    List's level validator. Level may contain integers indicating depth
    """
    if not _is_dict_validator(key, value, errors=errors):
        return

    for current_key, current_value in value.items():
        full_key = concat_keys(key, current_key)

        if not integer_validator(current_key) or int(current_key) not in range(0, 9):
            errors.append(
                MetadataValidationErrorItem(
                    key=full_key,
                    err_type=MetadataValidationErrorType.UNKNOWN_KEY
                )
            )
            continue

        # Depth section may have any of the available attributes
        _existing_attributes_validator(full_key, current_value, errors=errors)


def list_validator(key: str, value: Any) -> list[MetadataValidationErrorItem]:
    errors = []

    if not _is_dict_validator(key, value, errors=errors):
        return errors

    for current_key, current_value in value.items():
        # Validate lvl section
        if current_key == 'lvl':
            full_key = concat_keys(key, current_key)
            _list_lvl_validator(full_key, current_value, errors=errors)
            continue

        # it's possible to define any of the available attributes in list section
        errors += _value_validator(key=key, current_key=current_key, value=current_value)

    return errors


def get_validator(module: str) -> Callable[[Any], Union[bool, list[MetadataValidationErrorItem]]]:
    """
    Returns validator function at its string package location
    """
    package, method = module.rsplit('.', 1)
    module_object = importlib.import_module(package)
    return getattr(module_object, method)
