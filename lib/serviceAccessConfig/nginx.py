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

"""serviceAccessConfig plugin for nginx"""

import logging

from serviceAccessConfig.accessrulegenerator import ServiceAccessGenerator


class ServiceAccessGeneratorNginx(ServiceAccessGenerator):
    """Specific access rule generator for nginx"""

    # ======================================================================
    def __init__(self, ip_source_config_file_name):
        self.section_name = 'nginx'
        super(ServiceAccessGeneratorNginx, self).__init__(
            ip_source_config_file_name)

    # ======================================================================
    def _update_service_config(self, cidr_blocks):
        """Update the nginx configuragtion file"""

        cidr_blocks = cidr_blocks.split(',')

        header = '# ACL generated by serviceAccessConfig do not edit.\n'
        header += '# This file will be will be over written at the next \n'
        header += '# interval, see /etc/serviceaccess/srvAccess.cfg\n'

        deny_rule = 'deny all;\n'

        acl = map(lambda cidr: 'allow {};'.format(cidr), cidr_blocks)
        new_content = header + '\n'.join(acl) + '\n' + deny_rule

        for cfg in self.service_config.split(','):
            with open(cfg, 'w') as nginx_cfg:
                nginx_cfg.write(new_content)
            logging.info('Updated nginx config file %s' % cfg)
