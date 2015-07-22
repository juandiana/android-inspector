# coding=utf-8
from cybox.common.object_properties import CustomProperties, Property
from cybox.objects.custom_object import Custom


class Contact(Custom):
    def __init__(self):
        super(Contact, self).__init__()
        self.custom_name = 'Contact'
        self.custom_properties = CustomProperties()

    @property
    def display_name(self):
        return get_property('display_name', self.custom_properties)

    @display_name.setter
    def display_name(self, value):
        set_property('display_name', value, self.custom_properties)

    @property
    def first_name(self):
        return get_property('first_name', self.custom_properties)

    @first_name.setter
    def first_name(self, value):
        set_property('first_name', value, self.custom_properties)

    @property
    def last_name(self):
        return get_property('last_name', self.custom_properties)

    @last_name.setter
    def last_name(self, value):
        set_property('last_name', value, self.custom_properties)

    @property
    def phone_number(self):
        return get_property('phone_number', self.custom_properties)

    @phone_number.setter
    def phone_number(self, value):
        set_property('phone_number', value, self.custom_properties)

    @property
    def email(self):
        return get_property('email', self.custom_properties)

    @email.setter
    def email(self, value):
        set_property('email', value, self.custom_properties)

    @property
    def profile_picture(self):
        return get_property('profile_picture', self.custom_properties)

    @profile_picture.setter
    def profile_picture(self, value):
        set_property('profile_picture', value, self.custom_properties)

    @property
    def birthday(self):
        return get_property('birthday', self.custom_properties)

    @birthday.setter
    def birthday(self, value):
        set_property('birthday', value, self.custom_properties)


def set_property(property_name, property_value, properties):
    p = get_property(property_name, properties)

    if p is None:
        p = Property()
        p.name = property_name
        properties.append(p)

    p.value = property_value


def get_property(prop_name, properties):
    for p in properties:
        if p.name == prop_name:
            return p
    return None
