from cleaner import clean_definition, clean_term, is_valid_card

def test_clean_definition_adds_period():
    assert clean_definition("a security device") == "A security device."


def test_clean_definition_capitalizes_first_letter():
    assert clean_definition("temporary memory used during active tasks") == "Temporary memory used during active tasks."


def test_clean_definition_removes_leading_is():
    assert clean_definition("is a smaller division of a larger network") == "A smaller division of a larger network."


def test_clean_definition_preserves_action_verbs():
    assert clean_definition("translates domain names into IP addresses") == "Translates domain names into IP addresses."


def test_clean_term_removes_leading_article():
    assert clean_term("A firewall") == "firewall"


def test_is_valid_card_rejects_empty_term():
    assert is_valid_card("", "A definition") is False


def test_is_valid_card_accepts_valid_card():
    assert is_valid_card("Firewall", "A security device") is True