"""
Motor de firma XAdES-BES para el SRI de Ecuador.
Implementación definitiva de alta precisión criptográfica.
100% Python nativo usando cryptography (sin pyopenssl).
"""
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime
from cryptography.x509.extensions import KeyUsage
import re
import codecs
import base64
import hashlib
import xml.etree.ElementTree as ET
from lxml import etree

MAX_LINE_SIZE = 76
XML_NAMESPACES = 'xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:etsi="http://uri.etsi.org/01903/v1.3.2#"'


# ==================== UTILIDADES ====================

def encode_base64(data, encoding='UTF-8'):
    if isinstance(data, str):
        data = data.encode(encoding)
    return base64.b64encode(data).decode(encoding)


def sha1_base64(text):
    m = hashlib.sha1()
    if isinstance(text, str):
        text = text.encode('utf-8')
    m.update(text)
    sha1_digest = m.digest()
    return encode_base64(sha1_digest)


def split_string_every_n(cad, n):
    res = [cad[i:i + n] for i in range(0, len(cad), n)]
    return '\n'.join(res)


def random_integer():
    import random
    return random.randint(990, 999989)


def format_xml_string(xml_string):
    xml_string = xml_string.replace('\n', '')
    xml_string = re.sub(' +', ' ', xml_string).replace('> ', '>').replace(' <', '<')
    return xml_string


def canonicalize_lxml(xml_string):
    if isinstance(xml_string, str):
        xml_string = xml_string.encode('utf-8')
    root = etree.fromstring(xml_string)
    canonical_xml = etree.tostring(root, method="c14n", exclusive=False, with_comments=False)
    return canonical_xml.decode("utf-8")


def get_xml_end_node(xml_tree):
    return f"</{xml_tree.getroot().tag}>"


# ==================== CERTIFICADOS ====================

def get_certificados_validos(archivo, password):
    fecha_hora_actual = datetime.now()

    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(archivo, password)
    certificados_no_caducados = []
    certificados_validos = []

    if certificate:
        if certificate.not_valid_after > fecha_hora_actual:
            certificados_no_caducados.append(certificate)

    for cert in additional_certificates:
        if cert.not_valid_after > fecha_hora_actual:
            certificados_no_caducados.append(cert)

    for cert in certificados_no_caducados:
        for ext in cert.extensions:
            if type(ext.value) == KeyUsage:
                if ext.value.digital_signature == True:
                    certificados_validos.append(cert)

    if not certificados_validos and certificate:
        certificados_validos.append(certificate)

    return certificados_validos, private_key


def get_exponent(exp_int):
    # Obtener bytes del exponente de la clave pública
    num_bytes = (exp_int.bit_length() + 7) // 8
    exponent_bytes = exp_int.to_bytes(num_bytes, byteorder='big')
    return base64.b64encode(exponent_bytes).decode('utf-8').strip()


def get_modulus(modulus_int, max_line_size=MAX_LINE_SIZE):
    # Obtener bytes del módulo de la clave pública
    num_bytes = (modulus_int.bit_length() + 7) // 8
    modulus_bytes = modulus_int.to_bytes(num_bytes, byteorder='big')
    modulus_base64 = base64.b64encode(modulus_bytes).decode('utf-8')
    return split_string_every_n(modulus_base64, max_line_size)


# ==================== PLANTILLAS XML ====================

def get_signed_properties(signature_number, signed_properties_number, certificate_x509_der_hash, X509SerialNumber, reference_id_number, issuer_name):
    signing_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    signed_properties = f"""
    <etsi:SignedProperties Id="Signature{signature_number}-SignedProperties{signed_properties_number}">
        <etsi:SignedSignatureProperties>
            <etsi:SigningTime>
                {signing_time}
            </etsi:SigningTime>
            <etsi:SigningCertificate>
                <etsi:Cert>
                    <etsi:CertDigest>
                        <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
                        <ds:DigestValue>
                            {certificate_x509_der_hash}
                        </ds:DigestValue>
                    </etsi:CertDigest>
                    <etsi:IssuerSerial>
                        <ds:X509IssuerName>
                            {issuer_name}
                        </ds:X509IssuerName>
                        <ds:X509SerialNumber>
                            {X509SerialNumber}
                        </ds:X509SerialNumber>
                    </etsi:IssuerSerial>
                </etsi:Cert>
            </etsi:SigningCertificate>
        </etsi:SignedSignatureProperties>
        <etsi:SignedDataObjectProperties>
            <etsi:DataObjectFormat ObjectReference="#Reference-ID-{reference_id_number}">
                <etsi:Description>
                    contenido comprobante
                </etsi:Description>
                <etsi:MimeType>
                    text/xml
                </etsi:MimeType>
            </etsi:DataObjectFormat>
        </etsi:SignedDataObjectProperties>
    </etsi:SignedProperties>"""
    return format_xml_string(signed_properties)


def get_key_info(certificate_number, certificate_x509, modulus, exponent):
    key_info = f"""<ds:KeyInfo Id="Certificate{certificate_number}">
<ds:X509Data>
<ds:X509Certificate>
{certificate_x509}
</ds:X509Certificate>
</ds:X509Data>
<ds:KeyValue>
<ds:RSAKeyValue>
<ds:Modulus>
{modulus}
</ds:Modulus>
<ds:Exponent>{exponent}</ds:Exponent>
</ds:RSAKeyValue>
</ds:KeyValue>
</ds:KeyInfo>"""
    return key_info


def get_signed_info(signed_info_number, signed_properties_id_number, sha1_signed_properties, certificate_number, sha1_certificado, reference_id_number, sha1_comprobante, signature_number, signed_properties_number):
    signed_info = f"""<ds:SignedInfo Id="Signature-SignedInfo{signed_info_number}">
<ds:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
<ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
<ds:Reference Id="SignedPropertiesID{signed_properties_id_number}" Type="http://uri.etsi.org/01903#SignedProperties" URI="#Signature{signature_number}-SignedProperties{signed_properties_number}">
<ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
<ds:DigestValue>{sha1_signed_properties}</ds:DigestValue>
</ds:Reference>
<ds:Reference URI="#Certificate{certificate_number}">
<ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
<ds:DigestValue>{sha1_certificado}</ds:DigestValue>
</ds:Reference>
<ds:Reference Id="Reference-ID-{reference_id_number}" URI="#comprobante">
<ds:Transforms>
<ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
</ds:Transforms>
<ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
<ds:DigestValue>{sha1_comprobante}</ds:DigestValue>
</ds:Reference>
</ds:SignedInfo>"""
    return signed_info


def get_xades_bes(xmls, signature_number, object_number, signed_info, signature, key_info, signed_properties):
    xades_bes = f"""<ds:Signature {xmls} Id="Signature{signature_number}">
{signed_info}
<ds:SignatureValue Id="SignatureValue{signature_number}">
{signature}
</ds:SignatureValue>
{key_info}
<ds:Object Id="Signature{signature_number}-Object{object_number}">
<etsi:QualifyingProperties Target="#Signature{signature_number}">
{signed_properties}
</etsi:QualifyingProperties>
</ds:Object>
</ds:Signature>"""
    return xades_bes


# ==================== FIRMA PRINCIPAL ====================

def procesar_firmar_comprobante(archivo_p12, password, xml):
    certificados, private_key = get_certificados_validos(archivo_p12, password)

    if len(certificados) == 0:
        raise Exception("No se han encontrado certificados válidos en el archivo P12")

    cert = certificados[0]

    # 1. Obtener certificado DER y codificar en base64 de manera limpia y nativa (sin PEM parsing)
    cert_der = cert.public_bytes(serialization.Encoding.DER)
    certificate_x509_raw = base64.b64encode(cert_der).decode('utf-8')
    certificate_x509 = split_string_every_n(certificate_x509_raw, MAX_LINE_SIZE)

    # 2. Hash del certificado DER real (exigido por el estándar XAdES y el SRI)
    certificate_x509_der_hash = sha1_base64(cert_der)

    # 3. Clave pública modulo y exponente
    public_key_numbers = cert.public_key().public_numbers()
    modulus = get_modulus(public_key_numbers.n)
    exponent = get_exponent(public_key_numbers.e)

    serial_number = cert.serial_number

    # 4. Formatear el DN del emisor en formato LDAP estándar usando RFC 4514
    # rfc4514_string() devuelve CN=...,O=...,C=EC en el orden de LDAP oficial (exigido por el SRI)
    issuer_name = cert.issuer.rfc4514_string()

    # Parsear XML original
    xml_tree = ET.ElementTree(ET.fromstring(xml.encode('utf-8') if isinstance(xml, str) else xml))
    xml_no_header = canonicalize_lxml(xml)

    sha1_comprobante = sha1_base64(xml_no_header.encode('utf-8'))

    # Generar números aleatorios para los nodos
    certificate_number = random_integer()
    signature_number = random_integer()
    signed_properties_number = random_integer()
    signed_info_number = random_integer()
    signed_properties_id_number = random_integer()
    reference_id_number = random_integer()
    signature_value_number = random_integer()

    # --- Signed Properties ---
    signed_properties = get_signed_properties(
        signature_number, signed_properties_number, certificate_x509_der_hash,
        serial_number, reference_id_number, issuer_name
    )

    signed_properties_for_hash = signed_properties.replace('<etsi:SignedProperties', '<etsi:SignedProperties ' + XML_NAMESPACES)
    signed_properties_for_hash = canonicalize_lxml(signed_properties_for_hash)

    sha1_signed_properties = sha1_base64(signed_properties_for_hash.encode('utf-8'))

    # --- Key Info ---
    key_info = get_key_info(certificate_number, certificate_x509, modulus, exponent)

    # Workaround SRI: NO canonicalizar KeyInfo antes de hashearlo. 
    # El SRI aparentemente toma el string crudo o no le aplica C14N a este Reference.
    key_info_for_hash = key_info.replace('<ds:KeyInfo', '<ds:KeyInfo ' + XML_NAMESPACES)
    sha1_certificado = sha1_base64(key_info_for_hash.encode('utf-8'))

    # --- Signed Info ---
    signed_info = get_signed_info(
        signed_info_number, signed_properties_id_number, sha1_signed_properties,
        certificate_number, sha1_certificado, reference_id_number, sha1_comprobante,
        signature_number, signed_properties_number
    )

    # Canonicalizar SignedInfo para la firma criptográfica
    signed_info_for_signature = signed_info.replace('<ds:SignedInfo', '<ds:SignedInfo ' + XML_NAMESPACES)
    signed_info_for_signature = canonicalize_lxml(signed_info_for_signature)

    # Firmar usando cryptography nativa RSA PKCS#1 v1.5 con SHA-1
    sign = private_key.sign(
        signed_info_for_signature.encode("utf-8"),
        padding.PKCS1v15(),
        SHA1()
    )

    signature = encode_base64(sign)
    signature = split_string_every_n(signature, MAX_LINE_SIZE)

    # --- Ensamblar XAdES-BES ---
    xades_bes = get_xades_bes(
        xmls=XML_NAMESPACES,
        signature_number=signature_number,
        object_number=signature_value_number,
        signed_info=signed_info,
        signature=signature,
        key_info=key_info,
        signed_properties=signed_properties
    )

    # Insertar firma en el XML original (enveloped signature)
    tail_tag = get_xml_end_node(xml_tree)
    signed_xml = xml.replace(tail_tag, xades_bes + tail_tag)

    return signed_xml


def firmar_comprobante(ruta_p12_o_bytes, password, xml_cadena_o_bytes):
    if isinstance(ruta_p12_o_bytes, str):
        with open(ruta_p12_o_bytes, 'rb') as f:
            archivo_p12 = f.read()
    else:
        archivo_p12 = ruta_p12_o_bytes

    if isinstance(xml_cadena_o_bytes, bytes):
        xml = xml_cadena_o_bytes.decode('utf-8')
    else:
        xml = xml_cadena_o_bytes

    password = password.encode() if isinstance(password, str) else password

    return procesar_firmar_comprobante(archivo_p12, password, xml)
