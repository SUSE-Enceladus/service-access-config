#  Copyright (C) 2019 SUSE LLC
#  All rights reserved.
#
#  This file is part of serviceAccessConfig
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pytest
import sys

# Our test utilities
import unittest_utils as utils

sys.path.insert(0, utils.get_code_path())

from serviceAccessConfig.nginx import ServiceAccessGeneratorNginx
from serviceAccessConfig.generatorexceptions import \
    ServiceAccessGeneratorServiceRestartError


# ======================================================================
def test_update_config_no_file():
    """Test the generation if the ACL config file if the file does not exist"""

    utils.create_test_tmpdir()
    utils.copy_to_testdir('%s/nginx_setup.cfg' % utils.get_data_path())
    config = utils.get_config('%s/nginx_setup.cfg' % utils.get_data_path())
    gen = ServiceAccessGeneratorNginx(
        '%s/ip_data.cfg' % utils.get_data_path()
    )
    gen.set_config_values(config)
    with pytest.raises(ServiceAccessGeneratorServiceRestartError):
        gen.update_config()

    # Load the reference result data
    ref_result_file = (
        '%s/nginx-no-exist.cfg' % utils.get_reference_result_path()
    )
    ref_result = open(ref_result_file).read()

    # Load the generated result
    gen_result_file = (
        '%s/nginx-access.cfg' % utils.get_test_tmpdir()
    )
    gen_result = open(gen_result_file).read()

    if ref_result == gen_result:
        # success
        utils.remove_test_tmpdir()
    else:
        msg = 'Test failed, not removing test directory '
        msg += '"%s" to aid debugging ' % utils.get_test_tmpdir()
        assert False, msg


# ======================================================================
def test_update_config_with_data():
    """Test the generation if the ACL config file if a ACL config file exists
       and has unrelated data"""

    utils.create_test_tmpdir()
    utils.copy_to_testdir('%s/nginx_setup_w_data.cfg' % utils.get_data_path())
    config = utils.get_config(
        '%s/nginx_setup_w_data.cfg' % utils.get_data_path()
    )
    utils.copy_to_testdir(
        '%s/nginx-access-pre-data.cfg' % utils.get_data_path()
    )

    gen = ServiceAccessGeneratorNginx(
        '%s/ip_data.cfg' % utils.get_data_path()
    )
    gen.set_config_values(config)
    with pytest.raises(ServiceAccessGeneratorServiceRestartError):
        gen.update_config()

    # Load the reference result data
    ref_result_file = (
        '%s/nginx-pre-data.cfg' % utils.get_reference_result_path()
    )
    ref_result = open(ref_result_file).read()

    # Load the generated result
    gen_result_file = (
        '%s/nginx-access-pre-data.cfg' % utils.get_test_tmpdir()
    )
    gen_result = open(gen_result_file).read()

    if ref_result == gen_result:
        # success
        utils.remove_test_tmpdir()
    else:
        msg = 'Test failed, not removing test directory '
        msg += '"%s" to aid debugging ' % utils.get_test_tmpdir()
        assert False, msg


# ======================================================================
def test_update_config_with_data_and_acl():
    """Test the generation if the ACL config file if a ACL config file exists
       and has unrelated data"""

    utils.create_test_tmpdir()
    utils.copy_to_testdir(
        '%s/nginx_setup_w_data_acl.cfg' % utils.get_data_path()
    )
    config = utils.get_config(
        '%s/nginx_setup_w_data_acl.cfg' % utils.get_data_path()
    )
    utils.copy_to_testdir(
        '%s/nginx-access-pre-data-acl.cfg' % utils.get_data_path()
    )

    gen = ServiceAccessGeneratorNginx(
        '%s/ip_data.cfg' % utils.get_data_path()
    )
    gen.set_config_values(config)
    with pytest.raises(ServiceAccessGeneratorServiceRestartError):
        gen.update_config()

    # Load the reference result data
    ref_result_file = (
        '%s/nginx-pre-data.cfg' % utils.get_reference_result_path()
    )
    ref_result = open(ref_result_file).read()

    # Load the generated result
    gen_result_file = (
        '%s/nginx-access-pre-data-acl.cfg' % utils.get_test_tmpdir()
    )
    gen_result = open(gen_result_file).read()

    if ref_result == gen_result:
        # success
        utils.remove_test_tmpdir()
    else:
        msg = 'Test failed, not removing test directory '
        msg += '"%s" to aid debugging ' % utils.get_test_tmpdir()
        assert False, msg
