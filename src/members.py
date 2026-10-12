
class Member:
    def __init__(self, member_id, name, email, phone):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.status = "Active"


def register_member(members, member_id, name, email, phone):
    name = name.strip() if name else ""
    email = email.strip() if email else ""
    phone = phone.strip() if phone else ""

    if not name:
        return "Member name is required"

    if not email or "@" not in email:
        return "Valid email is required"

    if any(member.member_id == member_id for member in members):
        return "Member ID already exists"

    if any(
        member.email.lower() == email.lower()
        for member in members
    ):
        return "Email already registered"

    member = Member(member_id, name, email, phone)
    members.append(member)

    return member


def get_member(members, member_id):
    for member in members:
        if member.member_id == member_id:
            return member

    return None


def search_members(members, keyword):
    keyword = keyword.strip().lower()

    return [
        member
        for member in members
        if keyword in member.name.lower()
        or keyword in member.email.lower()
    ]


def update_member(members, member_id, name, email, phone):
    member = get_member(members, member_id)

    if member is None:
        return "Member not found"

    name = name.strip() if name else ""
    email = email.strip() if email else ""
    phone = phone.strip() if phone else ""

    if not name:
        return "Member name is required"

    if not email or "@" not in email:
        return "Valid email is required"

    if any(
        existing.member_id != member_id
        and existing.email.lower() == email.lower()
        for existing in members
    ):
        return "Email already registered"

    member.name = name
    member.email = email
    member.phone = phone

    return member


def deactivate_member(members, member_id):
    member = get_member(members, member_id)

    if member is None:
        return "Member not found"

    member.status = "Inactive"

    return member


def activate_member(members, member_id):
    member = get_member(members, member_id)

    if member is None:
        return "Member not found"

    member.status = "Active"

    return member
