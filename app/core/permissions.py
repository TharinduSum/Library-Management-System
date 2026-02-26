from __future__ import annotations

from enum import StrEnum, auto
from typing import Dict, Iterable, List, Set


class Permission(StrEnum):
    BOOK_READ = "book:read"
    BOOK_CREATE = "book:create"
    BOOK_UPDATE = "book:update"
    BOOK_DELETE = "book:delete"

    BORROW_CREATE = "borrow:create"
    BORROW_READ = "borrow:read"
    BORROW_RETURN = "borrow:return"

    MEMBER_READ = "member:read"
    MEMBER_CREATE = "member:create"
    MEMBER_UPDATE = "member:update"
    MEMBER_DELETE = "member:delete"

    ROLE_MANAGE = "role:manage"


class RoleName(StrEnum):
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    MEMBER = "member"


def _all_permissions() -> Set[Permission]:
    return {p for p in Permission}


ROLE_PERMISSIONS: Dict[RoleName, List[Permission]] = {
    RoleName.ADMIN: sorted(_all_permissions(), key=lambda p: p.value),
    RoleName.LIBRARIAN: [
        Permission.BOOK_READ,
        Permission.BOOK_CREATE,
        Permission.BOOK_UPDATE,
        Permission.BOOK_DELETE,
        Permission.BORROW_CREATE,
        Permission.BORROW_READ,
        Permission.BORROW_RETURN,
        Permission.MEMBER_READ,
        Permission.MEMBER_CREATE,
        Permission.MEMBER_UPDATE,
    ],
    RoleName.MEMBER: [
        Permission.BOOK_READ,
        Permission.BORROW_CREATE,
        Permission.BORROW_READ,
        Permission.BORROW_RETURN,
    ],
}


def permissions_to_strings(perms: Iterable[Permission]) -> List[str]:
    return [p.value for p in perms]

