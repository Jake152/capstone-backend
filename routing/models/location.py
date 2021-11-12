from datetime import datetime

from neomodel import StructuredNode, StringProperty, IntegerProperty, BooleanProperty, FloatProperty, \
    DateTimeProperty, UniqueIdProperty, Relationship, StructuredRel, One

import routing


class Weight(StructuredRel):
    distance = FloatProperty(required=True)
    duration = FloatProperty(required=True)
    savings = FloatProperty()


class Address(StructuredNode):
    uid = UniqueIdProperty()
    address = StringProperty(index=True, required=True)
    city = StringProperty(index=True, required=True)
    state = StringProperty(index=True, required=True)
    zipcode = IntegerProperty(index=True, required=True)
    latitude = FloatProperty(index=True)
    longitude = FloatProperty(index=True)
    created_on = DateTimeProperty(index=True, default=datetime.now)
    modified_on = DateTimeProperty(index=True, default_now=True)

    neighbor = Relationship(cls_name='Address', rel_type='CONNECTED_TO', model=Weight)

    def __init__(self, *args, **kwargs):
        super(Address, self).__init__(*args, **kwargs)

    def __hash__(self):
        return hash((self.address, self.city, self.state, self.zipcode))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.address == other.address and self.city == other.city
                and self.state == other.state and self.zipcode == other.zipcode)

    def __str__(self):
        return '{address}, {city}, {state} {zipcode}'.format(address=self.address, city=self.city, state=self.state,
                                                             zipcode=self.zipcode)

    def distance(self, other):
        if isinstance(other, type(self)):
            return self.neighbor.relationship(other).distance if self.neighbor.relationship(other) else None
        raise ValueError(f'{type(other)} is not supported.')

    def duration(self, other):
        if isinstance(other, type(self)):
            return self.neighbor.relationship(other).duration if self.neighbor.relationship(other) else None
        raise ValueError(f'{type(other)} is not supported.')

    @classmethod
    def category(cls):
        pass


class Location(StructuredNode):
    __abstract_node__ = True
    is_center = BooleanProperty(index=True, default=False)
    uid = UniqueIdProperty()
    external_id = IntegerProperty(index=True, required=False)
    created_on = DateTimeProperty(index=True, default=datetime.now)
    modified_on = DateTimeProperty(index=True, default_now=True)
    geographic_location = Relationship(cls_name='Address', rel_type='LOCATED_AT', cardinality=One)

    def __init__(self, *args, **kwargs):
        super(Location, self).__init__(*args, **kwargs)
        self.is_assigned = False
        self.next = None
        self.previous = None

    @property
    def address(self) -> Address:
        try:
            return self.geographic_location.get()
        except routing.exceptions.AddressDoesNotExist:
            pass

    def reset(self):
        self.next = None
        self.previous = None

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.address == other.address
        raise ValueError(f'{type(other)} is not supported.')

    def duration(self, other):
        """Gets the duration (in minutes) between these two locations.

        This implementation guarantees that either location is in the graph database.
        """
        if isinstance(other, type(self)):
            self.__validate_edge_with(other)
            if self == other:
                return 0.0
            return self.address.duration(other.address)
        raise ValueError(f'{type(other)} is not supported.')

    def distance(self, other):
        """Gets the distance (in meters) between these two locations.

        This implementation guarantees that either location is in the graph database.
        """
        if isinstance(other, type(self)):
            self.__validate_edge_with(other)
            if self == other:
                return 0.0
            else:
                return self.address.distance(other.address)
        raise ValueError(f'{type(other)} is not supported.')

    def __validate_edge_with(self, other):
        if isinstance(other, type(Location)):
            if self == other:
                return True
            else:
                if self.address.neighbor.relationship(other.address):
                    return True
                else:
                    routing.services.BingMatrixService.build_matrices(start=self.address, end=[other.address])
                return True
        raise ValueError(f'{type(other)} is not supported.')

    @classmethod
    def category(cls):
        pass


class Customer(Location):
    demand = IntegerProperty(index=True)
    language = Relationship(cls_name='routing.models.language.Language', rel_type='SPEAKS')

    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)


class Depot(Location):
    is_center = BooleanProperty(index=True, default=True)

    def __init__(self, *args, **kwargs):
        super(Depot, self).__init__(*args, **kwargs)


class Pair:
    def __init__(self, location1: Location, location2: Location):
        self.location1 = location1
        self.location2 = location2

    def is_first(self, location: Location):
        return self.location1 == location

    def is_last(self, location: Location):
        return self.location2 == location

    @property
    def first(self):
        return self.location1

    @property
    def last(self):
        return self.location2

    def get_pair(self):
        return self.location1, self.location2

    def is_assignable(self):
        if self.location1 and self.location2:
            return not (self.location1.is_assigned or self.location2.is_assigned)
        elif (self.location1 is None and self.location2) or (self.location1 and self.location2 is None):
            return True

        return False

    def __str__(self):
        return '({}, {})'.format(self.location1, self.location2)
