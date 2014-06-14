from pymongo import MongoClient

class GalaxyMongo():
    def __init__(self):
        db = client.galaxy
        self.galaxy = db.galaxy

    def all_regions(self):
        regions = []
        distinct_regions = self.galaxy.distinct('region')
        for region in distinct_regions:
            regions.append(region)

        return regions

    def all_cells(self):
        cells = self.galaxy.find({'type': 'cell'})
        return cells

    def noncompute_vms(self, region):
        vms = self.galaxy.find({'region': region, 'type': 'vm', 'role': {'$ne': 'compute'}})
        return vms

    def cells_in_region(self, region):
        distinct_cells = self.galaxy.find({'region': region}).distinct('cell')
        return distinct_cells

    def hosts_in_cell(self, region, cell, count=False):
        if count:
            host_count = self.galaxy.find({'region': region, 'type': 'server', 'cell': cell}).count()
            return host_count
        else:
            hosts = self.galaxy.find({'region': region, 'type': 'server', 'cell': cell})
            return hosts

    def hosts_in_region(self, region, count=False):
        hosts = self.galaxy.find({'region': region, 'type': 'server'})
        return hosts

    def cabs_in_cell(self, region, cell, count=False):
        if count:
            distinct_cabs_count = self.galaxy.find({'region': region, 'cell': cell}).distinct('cab').count()
            return distinct_cabs_count
        else:
            distinct_cabs = self.galaxy.find({'region': region, 'cell': cell}).distinct('cab')
            return distinct_cabs

    def hosts_in_cab(self, region, cell, cab, count=False):
        if count:
            host_count = self.galaxy.find({'region': region, 'cell': cell, 'cab': cab}).count()
            return host_count
        else:
            hosts = self.galaxy.find({'region': region, 'cell': cell, 'cab': cab})
            return hosts

    def hosts_on_switch(self, region, cell, cab, switch, count=False):
        if count:
            host_count = self.galaxy.find({'region': region, 'cell': cell, 'cab': cab,
                                           'switch_symbol': switch, 'type': 'server'}).count()
            return host_count
        else:
            hosts = self.galaxy.find({'region': region, 'cell': cell, 'cab': cab,
                                      'switch_symbol': switch, 'type': 'server'})
            return hosts

    def switches_in_cab(self, region, cell, cab, count=False):
        if count:
            switch_count = self.galaxy.find({'region': region, 'type': 'server', 'cell': cell, 'cab': cab}).\
                distinct('switch_symbol').count()
            return switch_count
        else:
            switches = self.galaxy.find({'region': region, 'type': 'server', 'cell': cell, 'cab': cab}).\
                distinct('switch_symbol')
            return switches

    def cell_network_info(self, region, cell, net_type):
        net = self.galaxy.find_one({'region': region, 'cell': cell, net_type: {"$ne": 'None'}, 'type': 'server'})
        if net is not None:
            return net.get(net_type)
        else:
            return None

    def cell_snapshot(self, region, cell):
        cell_snapshot = self.galaxy.find_one({'region': region, 'cell': cell, 'type': 'cell'})
        return cell_snapshot

    def single_host(self, name):
        host = self.galaxy.find_one({'type': 'server', 'name': name})
        return host
