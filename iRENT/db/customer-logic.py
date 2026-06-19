# UNIQUE constraint handling:
# - duplicate contact -> sqlite3.IntegrityError(code='duplicate_contact')
# - duplicate email   -> sqlite3.IntegrityError(code='duplicate_email')

# to store annotations as strings
from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Optional

# Reuse the shared schema + connection helper.
from sqlite_crudop import get_connection, make_database


def init_db() -> sqlite3.Connection:
    """Ensure tables exist and return a connection with foreign keys enabled."""
    make_database()
    return get_connection()


def _normalize_str(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _parse_integrity_error(exc: sqlite3.IntegrityError) -> str:
    """Map SQLite constraint failures to stable error codes."""
    msg = str(exc)
    if "Customer.ContactNumber" in msg:
        return "duplicate_contact"
    if "Customer.EmailAddress" in msg:
        return "duplicate_email"
    return "integrity_error"


def _row_to_customer_dict(row: sqlite3.Row | tuple) -> Dict[str, Any]:
    # Must match SELECT column order
    keys = [
        "CustomerID",
        "FirstName",
        "MiddleName",
        "LastName",
        "Suffix",
        "ContactNumber",
        "EmailAddress",
        "Street",
        "Barangay",
        "City",
        "Province",
        "ZIPCode",
        "BirthMonth",
        "BirthDay",
        "BirthYear",
    ]
    return dict(zip(keys, row))


# CREATE (Add customer)
def create_customer(
    conn: sqlite3.Connection,
    *,
    first_name: str,
    middle_name: str,
    last_name: str,
    suffix: str,
    contact_number: str,
    email_address: str,
    street: str,
    barangay: str,
    city: str,
    province: str,
    zipcode: str,
    birth_month: str,
    birth_day: str,
    birth_year: str,
) -> int:
    """Add a new customer and return the new CustomerID."""

    required = {
        "first_name": first_name,
        "last_name": last_name,
        "contact_number": contact_number,
        "email_address": email_address,
        "street": street,
        "barangay": barangay,
        "city": city,
        "province": province,
        "zipcode": zipcode,
        "birth_month": birth_month,
        "birth_day": birth_day,
        "birth_year": birth_year,
    }
    missing = [k for k, v in required.items() if _normalize_str(v) == ""]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Customer (
                FirstName, MiddleName, LastName, Suffix,
                ContactNumber, EmailAddress,
                Street, Barangay, City, Province, ZIPCode,
                BirthMonth, BirthDay, BirthYear
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _normalize_str(first_name),
                _normalize_str(middle_name),
                _normalize_str(last_name),
                _normalize_str(suffix),
                _normalize_str(contact_number),
                _normalize_str(email_address),
                _normalize_str(street),
                _normalize_str(barangay),
                _normalize_str(city),
                _normalize_str(province),
                _normalize_str(zipcode),
                _normalize_str(birth_month),
                _normalize_str(birth_day),
                _normalize_str(birth_year),
            ),
        )
        conn.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError as e:
        code = _parse_integrity_error(e)
        # Re-raise with stable error code.
        raise sqlite3.IntegrityError(code) from e


# READ
def get_customer_by_id(conn: sqlite3.Connection, customer_id: int) -> Optional[Dict[str, Any]]:
    """Fetch a customer record by primary key."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            CustomerID,
            FirstName, MiddleName, LastName, Suffix,
            ContactNumber, EmailAddress,
            Street, Barangay, City, Province, ZIPCode,
            BirthMonth, BirthDay, BirthYear
        FROM Customer
        WHERE CustomerID = ?
        """,
        (customer_id,),
    )
    row = cursor.fetchone()
    return None if not row else _row_to_customer_dict(row)


# UPDATE (Edit customer)
def update_customer(conn: sqlite3.Connection, customer_id: int, **fields: Any) -> bool:
    """Edit an existing customer.

    Example:
        update_customer(conn, 1, contact_number='...', email_address='...', city='...')

    Returns True if a row was updated; False if no valid fields were provided
    or the record was not found.
    """

    allowed = {
        "first_name": "FirstName",
        "middle_name": "MiddleName",
        "last_name": "LastName",
        "suffix": "Suffix",
        "contact_number": "ContactNumber",
        "email_address": "EmailAddress",
        "street": "Street",
        "barangay": "Barangay",
        "city": "City",
        "province": "Province",
        "zipcode": "ZIPCode",
        "birth_month": "BirthMonth",
        "birth_day": "BirthDay",
        "birth_year": "BirthYear",
    }

    updates: List[str] = []
    params: List[Any] = []

    for k, v in fields.items():
        if k not in allowed:
            continue
        col = allowed[k]
        updates.append(f"{col} = ?")
        params.append(_normalize_str(v))

    if not updates:
        return False

    params.append(customer_id)
    sql = f"UPDATE Customer SET {', '.join(updates)} WHERE CustomerID = ?"

    cursor = conn.cursor()
    try:
        cursor.execute(sql, tuple(params))
        conn.commit()
        return cursor.rowcount > 0

    except sqlite3.IntegrityError as e:
        code = _parse_integrity_error(e)
        raise sqlite3.IntegrityError(code) from e


# DELETE
def delete_customer(conn: sqlite3.Connection, customer_id: int) -> bool:
    """Delete customer profile.

    Note: Rental(CustomerID) is ON DELETE CASCADE, so rentals are removed too.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Customer WHERE CustomerID = ?", (customer_id,))
    conn.commit()
    return cursor.rowcount > 0


# SEARCH (to be wired into GUI later on)
def search_customers(conn: sqlite3.Connection, term: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Search customers using LIKE across name/contact/email/address."""
    term = _normalize_str(term)
    if term == "":
        return []

    like = f"%{term}%"

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            CustomerID,
            FirstName, MiddleName, LastName, Suffix,
            ContactNumber, EmailAddress,
            Street, Barangay, City, Province, ZIPCode,
            BirthMonth, BirthDay, BirthYear
        FROM Customer
        WHERE
            FirstName LIKE ? OR
            LastName LIKE ? OR
            (FirstName || ' ' || LastName) LIKE ? OR
            ContactNumber LIKE ? OR
            EmailAddress LIKE ? OR
            Street LIKE ? OR
            Barangay LIKE ? OR
            City LIKE ? OR
            Province LIKE ?
        ORDER BY CustomerID DESC
        LIMIT ?
        """,
        (
            like,
            like,
            like,
            like,
            like,
            like,
            like,
            like,
            like,
            int(limit),
        ),
    )

    rows = cursor.fetchall()
    return [_row_to_customer_dict(r) for r in rows]


# CUSTOMER RENTAL HISTORY
def get_customer_rental_history(conn: sqlite3.Connection, customer_id: int) -> List[Dict[str, Any]]:
    """Return rental history rows for a customer."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            r.RentalID,
            r.RentalStatus,
            r.TotalRentalFee,
            r.SRentalMonth,
            r.SRentalDay,
            r.SRentalYear
        FROM Rental r
        WHERE r.CustomerID = ?
        ORDER BY r.RentalID DESC
        """,
        (customer_id,),
    )

    results: List[Dict[str, Any]] = []
    for rental_id, status, total_fee, sm, sd, sy in cursor.fetchall():
        results.append(
            {
                "RentalID": rental_id,
                "RentalStatus": status,
                "TotalRentalFee": total_fee,
                "StartMonth": sm,
                "StartDay": sd,
                "StartYear": sy,
            }
        )
    return results