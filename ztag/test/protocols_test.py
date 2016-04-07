from zsearch_definitions.protocols import Protocol, Subprotocol
import zsearch_definitions.protocols
import zschema.keys

import unittest


class ProtocolNameTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_from_name(self):
        protocol_long = "PROTO_HTTPS"
        protocol_short = "https"
        from_long = Protocol.from_name(protocol_long)
        from_short = Protocol.from_pretty_name(protocol_short)
        self.assertEqual(from_long.value, from_short.value)
        self.assertEqual(from_long.value, zsearch_definitions.protocols.HTTPS.value)

    def test_subprotocols_with_bonus_underscores(self):
        modbus = Protocol.from_pretty_name("modbus")
        self.assertTrue(hasattr(modbus, "DEVICE_ID"))
        self.assertFalse(hasattr(modbus, "MEI"))
        self.assertFalse(hasattr(modbus, "DEVICE"))

    def test_generic_subprotocols_exposed_as_attributes(self):
        proto_http = Protocol.from_pretty_name("http")
        self.assertTrue(hasattr(proto_http, "GET"))

from ztag import schema


class SchemaMatchesNamesTestCase(unittest.TestCase):

    def test_schema(self):
        host = schema.host
        for key, obj in host.definition.iteritems():
            if not type(key) == zschema.keys.Port:
                continue
            for protocol_name, proto in obj.definition.iteritems():
                try:
                    p = Protocol.from_pretty_name(protocol_name)
                except KeyError:
                    self.fail(protocol_name)
                for subprotocol_name, data in proto.definition.iteritems():
                    try:
                        s = Subprotocol.from_pretty_name(subprotocol_name)
                    except KeyError:
                        self.fail(subprotocol_name)


if __name__ == '__main__':
    unittest.main()
