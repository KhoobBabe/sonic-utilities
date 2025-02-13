import json
import jsonpatch
import os
import traceback
from unittest import mock

from click.testing import CliRunner

import config.main as config
import show.main as show
from utilities_common.db import Db

test_path = os.path.dirname(os.path.abspath(__file__))
ip_config_input_path = os.path.join(test_path, "ip_config_input")

ERROR_MSG = "Error: IP address is not valid"

class TestConfigIP(object):
    @classmethod
    def setup_class(cls):
        os.environ['UTILITIES_UNIT_TESTING'] = "1"
        print("SETUP")

    ''' Tests for IPv4  '''

    def test_add_del_interface_valid_ipv4(self):
        db = Db()
        runner = CliRunner()
        obj = {'config_db':db.cfgdb}

        # config int ip add Ethernet64 10.10.10.1/24
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["add"], ["Ethernet64", "10.10.10.1/24"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert ('Ethernet64', '10.10.10.1/24') in db.cfgdb.get_table('INTERFACE')

        # config int ip remove Ethernet64 10.10.10.1/24
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["remove"], ["Ethernet64", "10.10.10.1/24"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code != 0
        assert ('Ethernet64', '10.10.10.1/24') not in db.cfgdb.get_table('INTERFACE')

    def test_add_interface_invalid_ipv4(self):
        db = Db()
        runner = CliRunner()
        obj = {'config_db':db.cfgdb}

        # config int ip add Ethernet64 10000.10.10.1/24
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["add"], ["Ethernet64", "10000.10.10.1/24"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code != 0
        assert ERROR_MSG in result.output

    def test_add_interface_ipv4_invalid_mask(self):
        db = Db()
        runner = CliRunner()
        obj = {'config_db':db.cfgdb}

        # config int ip add Ethernet64 10.10.10.1/37
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["add"], ["Ethernet64", "10.10.10.1/37"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code != 0
        assert ERROR_MSG in result.output

    def test_add_interface_ipv4_with_leading_zeros(self):
        db = Db()
        runner = CliRunner()
        obj = {'config_db':db.cfgdb}

        # config int ip add Ethernet68 10.10.10.002/24
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["add"], ["Ethernet68", "10.10.10.0002/24"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code != 0
        assert ERROR_MSG in result.output

    '''  Tests for IPv6 '''

    def test_add_del_interface_valid_ipv6(self):
        db = Db()
        runner = CliRunner()
        obj = {'config_db':db.cfgdb}

        # config int ip add Ethernet72 2001:1db8:11a3:19d7:1f34:8a2e:17a0:765d/34
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["add"], ["Ethernet72", "2001:1db8:11a3:19d7:1f34:8a2e:17a0:765d/34"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert ('Ethernet72', '2001:1db8:11a3:19d7:1f34:8a2e:17a0:765d/34') in db.cfgdb.get_table('INTERFACE')

        # config int ip remove Ethernet72 2001:1db8:11a3:19d7:1f34:8a2e:17a0:765d/34
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["remove"], ["Ethernet72", "2001:1db8:11a3:19d7:1f34:8a2e:17a0:765d/34"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code != 0
        assert ('Ethernet72', '2001:1db8:11a3:19d7:1f34:8a2e:17a0:765d/34') not in db.cfgdb.get_table('INTERFACE')

    def test_del_interface_case_sensitive_ipv6(self):
        db = Db()
        runner = CliRunner()
        obj = {'config_db':db.cfgdb}

        obj['config_db'].set_entry('INTERFACE', ('Ethernet72', 'FC00::1/126'), {})
        assert ('Ethernet72', 'FC00::1/126') in db.cfgdb.get_table('INTERFACE')

        # config int ip remove Ethernet72 FC00::1/126
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["remove"], ["Ethernet72", "FC00::1/126"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code != 0
        assert ('Ethernet72', 'FC00::1/126') not in db.cfgdb.get_table('INTERFACE')

    def test_add_interface_invalid_ipv6(self):
        db = Db()
        runner = CliRunner()
        obj = {'config_db':db.cfgdb}

        # config int ip add Ethernet72 20001:0db8:11a3:09d7:1f34:8a2e:07a0:765d/34
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["add"], ["Ethernet72", "20001:0db8:11a3:19d7:1f34:8a2e:17a0:765d/34"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code != 0
        assert ERROR_MSG in result.output

    def test_add_interface_ipv6_invalid_mask(self):
        db = Db()
        runner = CliRunner()
        obj = {'config_db':db.cfgdb}

        # config int ip add Ethernet72 2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d/200
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["add"], ["Ethernet72", "2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d/200"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code != 0
        assert ERROR_MSG in result.output

    def test_add_del_interface_ipv6_with_leading_zeros(self):
        db = Db()
        runner = CliRunner()
        obj = {'config_db':db.cfgdb}

        # config int ip add Ethernet68 2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d/34
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["add"], ["Ethernet68", "2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d/34"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert ('Ethernet68', '2001:db8:11a3:9d7:1f34:8a2e:7a0:765d/34') in db.cfgdb.get_table('INTERFACE')

        # config int ip remove Ethernet68 2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d/34
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["remove"], ["Ethernet68", "2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d/34"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code != 0
        assert ('Ethernet68', '2001:db8:11a3:9d7:1f34:8a2e:7a0:765d/34') not in db.cfgdb.get_table('INTERFACE')

    def test_add_del_interface_shortened_ipv6_with_leading_zeros(self):
        db = Db()
        runner = CliRunner()
        obj = {'config_db':db.cfgdb}

        # config int ip add Ethernet68 3000::001/64
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["add"], ["Ethernet68", "3000::001/64"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert ('Ethernet68', '3000::1/64') in db.cfgdb.get_table('INTERFACE')

        # config int ip remove Ethernet68 3000::001/64
        result = runner.invoke(config.config.commands["interface"].commands["ip"].commands["remove"], ["Ethernet68", "3000::001/64"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code != 0
        assert ('Ethernet68', '3000::1/64') not in db.cfgdb.get_table('INTERFACE')

    def test_remove_interface_case_sensitive_mock_ipv6_w_apply_patch(self):
        runner = CliRunner()
        any_patch_as_json = [{"op": "remove", "path": "/INTERFACE/Ethernet12|FC00::1~1126"}]
        any_patch = jsonpatch.JsonPatch(any_patch_as_json)
        any_patch_as_text = json.dumps(any_patch_as_json)
        ipv6_patch_file = os.path.join(ip_config_input_path, 'patch_ipv6.test')

        # config apply-patch patch
        mock_generic_updater = mock.Mock()
        with mock.patch('config.main.GenericUpdater', return_value=mock_generic_updater):
            with mock.patch('builtins.open', mock.mock_open(read_data=any_patch_as_text)):
                result = runner.invoke(config.config.commands["apply-patch"], [ipv6_patch_file], catch_exceptions=False)
        print(result.exit_code, result.output)
        assert "converted ipv6 address to lowercase fc00::1~1126 with prefix /INTERFACE/Ethernet12| in value: /INTERFACE/Ethernet12|FC00::1~1126" in result.output

    def test_intf_vrf_bind_unbind(self):
        runner = CliRunner()
        db = Db()
        obj = {'config_db':db.cfgdb, 'namespace':db.db.namespace}

        result = runner.invoke(config.config.commands["interface"].commands["vrf"].commands["bind"], ["Ethernet64", "Vrf1"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0

        result = runner.invoke(config.config.commands["interface"].commands["vrf"].commands["unbind"], ["Ethernet64"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0

    @classmethod
    def teardown_class(cls):
        os.environ['UTILITIES_UNIT_TESTING'] = "0"
        print("TEARDOWN")
