class Utils:

    @staticmethod
    def validate_positive_int(string: str) -> bool:
        try:
            return int(string) > 0
        except ValueError as e:
            return False

    @staticmethod
    def increase_value_with_key(dictionary: dict, key: object, value_to_add: int = 1) -> None:
        if key in dictionary.keys():
            dictionary[key] = dictionary[key] + value_to_add
        else:
            dictionary[key] = value_to_add
