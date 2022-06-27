from doctest import testmod


def get_description(bmi_result: float) -> dict[str]:
    """Method that's return description of BMI result and color.

    :param bmi_result: `float` numer of calculated result.
    :return: `dict` description and color message

    >>> get_description(15.0)
    {'color': 'red', 'description': 'wygłodzenie'}
    >>> get_description(16.8)
    {'color': 'red', 'description': 'wychudzenie (spowodowane często przez ciężką chorobę)'}
    >>> get_description(17.9)
    {'color': 'orange', 'description': 'niedowaga'}
    >>> get_description(23)
    {'color': 'green', 'description': 'waga prawidłowa'}
    >>> get_description(25.0)
    {'color': 'orange', 'description': 'nadwaga'}
    >>> get_description(34.9)
    {'color': 'red', 'description': 'I stopień otyłości'}
    >>> get_description(37)
    {'color': 'red', 'description': 'II stopień otyłości'}
    >>> get_description(58.7)
    {'color': 'red', 'description': 'III stopień otyłości (otyłość skrajna)'}
    >>> get_description(-10)
    Traceback (most recent call last):
    ...
    ValueError: Podano nieprawidłową wagę lub wzrost
    >>> get_description(1000)
    Traceback (most recent call last):
    ...
    ValueError: Podano nieprawidłową wagę lub wzrost
    """

    result = {
        "color": None,
        "description": None,
    }
    if 3 <= bmi_result < 16.0:
        result["color"] = "red"
        result["description"] = "wygłodzenie"
    elif 16 <= bmi_result <= 17:
        result["color"] = "red"
        result["description"] = "wychudzenie (spowodowane często przez ciężką chorobę)"
    elif 17 <= bmi_result <= 18.5:
        result["color"] = "orange"
        result["description"] = "niedowaga"
    elif 18.5 <= bmi_result < 25:
        result["color"] = "green"
        result["description"] = "waga prawidłowa"
    elif 25 <= bmi_result < 30:
        result["color"] = "orange"
        result["description"] = "nadwaga"
    elif 30 <= bmi_result < 35:
        result["color"] = "red"
        result["description"] = "I stopień otyłości"
    elif 35 <= bmi_result < 40:
        result["color"] = "red"
        result["description"] = "II stopień otyłości"
    elif 40 <= bmi_result <= 720:
        result["color"] = "red"
        result["description"] = "III stopień otyłości (otyłość skrajna)"
    else:
        raise ValueError("Podano nieprawidłową wagę lub wzrost")
    return result


testmod()
