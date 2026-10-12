
from src.members import Member, register_member, get_member, search_members, update_member
from src.members import activate_member, deactivate_member

def test_register_member():
    members = []

    result = register_member(
        members, 1, "John Smith", "john@example.com", "0412345678"
    )

    assert isinstance(result, Member)
    assert len(members) == 1
    assert result.name == "John Smith"


def test_duplicate_member_id():
    members = [Member(1, "John Smith", "john@example.com", "0412345678")]

    result = register_member(
        members, 1, "Jane Smith", "jane@example.com", "0498765432"
    )

    assert result == "Member ID already exists"


def test_invalid_email():
    members = []

    result = register_member(
        members, 2, "Jane Smith", "invalid-email", "0498765432"
    )

    assert result == "Valid email is required"


def test_get_member():
    members = [Member(1, "John Smith", "john@example.com", "0412345678")]

    result = get_member(members, 1)

    assert result.name == "John Smith"


def test_search_members():
    members = [
        Member(1, "John Smith", "john@example.com", "0412345678"),
        Member(2, "Jane Brown", "jane@example.com", "0498765432")
    ]

    results = search_members(members, "jane")

    assert len(results) == 1
    assert results[0].name == "Jane Brown"

def test_update_member():
    members = [
        Member(1, "John Smith", "john@example.com", "0412345678")
    ]

    result = update_member(
        members,
        1,
        "John Williams",
        "johnw@example.com",
        "0498765432"
    )

    assert result.name == "John Williams"
    assert result.email == "johnw@example.com"
    assert result.phone == "0498765432"

def test_deactivate_member():
    members = [
        Member(1, "John Smith", "john@example.com", "0412345678")
    ]

    result = deactivate_member(members, 1)

    assert result.status == "Inactive"


def test_activate_member():
    members = [
        Member(1, "John Smith", "john@example.com", "0412345678")
    ]

    deactivate_member(members, 1)
    result = activate_member(members, 1)

    assert result.status == "Active"
