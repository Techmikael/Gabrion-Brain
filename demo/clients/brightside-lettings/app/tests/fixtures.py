"""Synthetic test data only. Never put real tenant details in tests."""


def valid(**overrides):
    data = {
        "property_ref": "BL-TEST-001",
        "category": "plumbing",
        "description": "Kitchen tap drips constantly.",
        "tenant_name": "Test Tenant",
        "tenant_email": "tenant@example.test",
    }
    data.update(overrides)
    return data
