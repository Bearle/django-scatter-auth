from fastecdsa import curve as ecdsa_curve
from fastecdsa import keys, ecdsa, point
import re
import base58
from hashlib import sha256
import hashlib
import math

from django import forms
from django.utils.translation import ugettext_lazy as _

class InvalidSignatureException(Exception):
    pass

def check_decode(key_string, key_type=None):
    # https://github.com/EOSIO/eosjs-ecc/blob/master/src/key_utils.js#L201
    buffer = bytearray(base58.b58decode(key_string))
    checksum = buffer[-4:]
    key = buffer[0:-4]
    if key_type == 'sha256x2':
        new_check = sha256(sha256(key))[0:4]
    else:
        h_ripe = hashlib.new('ripemd160')
        if key_type:
            temp_1 = bytearray(bytes(key_type, 'utf-8'))
            h_ripe.update(bytes(key + temp_1))
        else:
            h_ripe.update(bytes(key))
        hex_ripe_digest = h_ripe.hexdigest()
        new_check = bytearray.fromhex(hex_ripe_digest)[0:4]
    if not str(checksum) == str(new_check):
        raise InvalidSignatureException('Invalid hashsum')
    return key


def curve_point_from_x(curve, is_odd, x):
    # https://github.com/cryptocoinjs/ecurve/blob/master/lib/curve.js#L23
    alpha = (x ** 3 + curve.a * x + curve.b) % curve.p
    pOverFour = (curve.p + 1) >> 2
    beta = pow(alpha, pOverFour, curve.p)
    y = beta
    beta_is_even = beta % 2 == 0
    if beta_is_even ^ (not is_odd):
        y = curve.p - beta
    return y


def point_decode_from(curve, buffer):
    # https://github.com/cryptocoinjs/ecurve/blob/master/lib/point.js#L213
    typpe = int.from_bytes(bytes(buffer)[:1], byteorder='big', signed=False)
    compressed = typpe != 4
    byte_length = math.floor((curve.p.bit_length() + 7) / 8)
    x = buffer[1:1 + byte_length]
    int_x = int(x.hex(), 16)
    if compressed:
        if not len(buffer) == byte_length + 1:
            raise InvalidSignatureException('Invalid sequence length')
        if not (typpe == 0x02 or typpe == 0x03):
            raise InvalidSignatureException('Invalid sequence tag')
        is_odd = typpe == 0x03
        y = curve_point_from_x(curve, is_odd, int_x)
    else:
        if not len(buffer) == byte_length + byte_length + 1:
            raise InvalidSignatureException('Invalid sequence length')
        y = buffer[1 + byte_length:]
    return point.Point(int_x, y, curve)


def signature_from_string(signature):
    # https://github.com/EOSIO/eosjs-ecc/blob/master/src/signature.js#L259
    match = re.findall('^SIG_([A-Za-z0-9]+)_([A-Za-z0-9]+)$', signature)[0]
    if not len(match) == 2:
        raise InvalidSignatureException('Expecting signature like: SIG_K1_base58signature..')
    key_type, key_string = match[0], match[1]
    if not key_type == 'K1':
        raise InvalidSignatureException('Not K1 signature')
    return key_type, key_string


def signature_from_buffer(buf):
    # https://github.com/EOSIO/eosjs-ecc/blob/master/src/signature.js#L227
    if not len(buf) == 65:
        raise InvalidSignatureException('Invalid key length')
    i = int.from_bytes(bytes(buf)[:1], byteorder='big', signed=False)
    if not i - 27 == i - 27 & 7:
        raise InvalidSignatureException('Invalid signature parameter')
    r = int(buf[1:33].hex(), 16)
    s = int(buf[33:].hex(), 16)
    return r, s, i


def validate_signature(msg, sig, pubkey):
    key_type, key_string = signature_from_string(sig)
    key = check_decode(key_string, key_type)
    r,s,i = signature_from_buffer(key)
    pub_key_point = point_decode_from(ecdsa_curve.secp256k1, check_decode(pubkey[3:]))
    res = ecdsa.verify((r, s), msg, pub_key_point, ecdsa_curve.secp256k1)
    return res


