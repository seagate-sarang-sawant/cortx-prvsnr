#
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.
#

base:
  'G@roles:primary':
    - roles.primary
  '*':
    - ignore_missing: True
    - node_info.node_data
    - components.cluster                    # default all minions vars (here and below) TODO create task: move to groups.all.components...
    - components.commons
    - components.corosync-pacemaker
    - components.elasticsearch
    - components.motr
    - components.haproxy
    - components.openldap
    - components.release
    - components.s3clients
    - components.s3server
    - components.storage_enclosure
    - components.system
    - components.sspl
    - components.rabbitmq
    - components.rsyslog
    - components.uds
    - components.lustre
    - user.groups.all.*                     # user all minions vars (old style)
    - groups.all.*                     # all minions vars (new style)
  {{ grains.id }}:
    - ignore_missing: True
    - minions.{{ grains.id }}.*        # per-minion vars (new style)
    - user.minions.{{ grains.id }}.*   # user per-minion vars (old style)
