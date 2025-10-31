class CVEError(Exception):
    """
    General CVE Exception
    """
    pass


class CVEMalformedError(CVEError):
    """
    Exception for malformed input CVE data.
    """
    pass


class CVEMandatoryError(CVEError):
    """
    Exception for missing mandatory fields.
    """
    pass


class CVEMissingData(CVEMandatoryError):
    """
    Exception for missing requested fields.
    """
    pass
