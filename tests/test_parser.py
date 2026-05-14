from parser import parse_line


def test_colon_parsing():
    term, definition = parse_line(
        "Firewall: A security device"
    )

    assert term == "Firewall"
    assert definition == "A security device"


def test_is_parsing():
    term, definition = parse_line(
        "A subnet is a smaller division of a network"
    )

    assert term == "subnet"
    assert definition == "is a smaller division of a network"


def test_translates_parsing():
    term, definition = parse_line(
        "DNS translates domain names into IP addresses"
    )

    assert term == "DNS"
    assert definition == "translates domain names into IP addresses"


def test_forwards_parsing():
    term, definition = parse_line(
        "A router forwards packets between networks"
    )

    assert term == "router"
    assert definition == "forwards packets between networks"


def test_invalid_line_returns_none():
    term, definition = parse_line(
        "Professor said this will be on the exam"
    )

    assert term is None
    assert definition is None