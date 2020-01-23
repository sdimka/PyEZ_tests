
"""
yml
"""
from jnpr.junos.factory import loadyaml

yml_file = "stp.yml"
globals().update(loadyaml(yml_file))

tbl = STPInterfaces(dev)
tbl.get()
for key in tbl:
    print(key.name, key.role, key.state)

#   pprint(dev.facts)

# tbl = STPI


from jnpr.junos.op.routes import RouteTable

routes = RouteTable(dev)

routes.get()
# pprint(routes.keys())

tbl = routes.get('192.168.0.0/24')

for key in tbl:
    for val in key.values():
        print(val.__class__)
    print(key.values())


# pprint(routes.keys())
RouteTable:
  rpc: get-route-information
  item: route-table/rt/rt-entry/nh
  key: rt-destination
  view: RouteTableView

RouteTableView:
  groups:
    entry: rt-entry
  fields_entry:
    nexthop: nh/to
    selected: nh/selected-next-hop