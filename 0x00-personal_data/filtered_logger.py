#!/usr/bin/env python3
"""Module for handling personal data"""

import re
import logging
from typing import List
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in the log message.

    Args:
        fields: List of strings representing fields to obfuscate
        redaction: String to replace field values
        message: String representing the log line
        separator: String representing the character separating fields

    Returns:
        Obfuscated log message
    """
    for field in fields:
        pattern = f"({field}=)([^{separator}]*)"
        message = re.sub(pattern, f"\\1{redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as text.

        Args:
            record: A LogRecord instance representing the event being logged

        Returns:
            Formatted string with sensitive information redacted
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger named "user_data".

    Returns:
        logging.Logger: Configured logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    Connects to the MySQL database using environment variables.

    Returns:
        MySQLConnection: Database connection object
    """
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return connection


def main() -> None:
    """
    Main function to retrieve and display user data from the database.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()

    for row in cursor:
        message = "; ".join(f"{field}={value}" for field, value
                            in zip(cursor.column_names, row))
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
