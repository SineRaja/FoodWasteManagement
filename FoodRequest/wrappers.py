from Address.exportapi import create_address, validate_address, get_address_string_for_address_id, \
    get_address_details, update_address
from collections import defaultdict


def check_valid_address(address):
    return validate_address(address)


def post_create_address(address_data):
    return create_address(address_data)


def post_update_address(address_id, address_data):
    return update_address(address_id, address_data)


def get_address_id_wise_address_details(address_ids):
    address_details = get_address_details(address_ids)
    address_id_wise_address_details = defaultdict(dict)
    for address in address_details:
        address_id_wise_address_details[address["id"]] = address
    return address_id_wise_address_details


def get_address_string(address_id):
    return get_address_string_for_address_id(address_id)
