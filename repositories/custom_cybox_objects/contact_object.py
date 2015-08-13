# coding=utf-8
from cybox.common.object_properties import CustomProperties, Property
from cybox.objects.custom_object import Custom


class Contact(Custom):
    def __init__(self):
        Custom.__init__(self)
        self.custom_name = 'Contact'
        self.custom_properties = CustomProperties()

    @property
    def display_name(self):
        return self.get_property('display_name')

    @display_name.setter
    def display_name(self, value):
        self.set_property('display_name', value)

    @property
    def first_name(self):
        return self.get_property('first_name')

    @first_name.setter
    def first_name(self, value):
        self.set_property('first_name', value)

    @property
    def last_name(self):
        return self.get_property('last_name')

    @last_name.setter
    def last_name(self, value):
        self.set_property('last_name', value)

    @property
    def phone_number(self):
        return self.get_property('phone_number')

    @phone_number.setter
    def phone_number(self, value):
        self.set_property('phone_number', value)

    @property
    def email(self):
        return self.get_property('email')

    @email.setter
    def email(self, value):
        self.set_property('email', value)

    @property
    def profile_picture(self):
        return self.get_property('profile_picture')

    @profile_picture.setter
    def profile_picture(self, value):
        self.set_property('profile_picture', value)

    @property
    def birthday(self):
        return self.get_property('birthday')

    @birthday.setter
    def birthday(self, value):
        self.set_property('birthday', value)

    def set_property(self, property_name, property_value):
        p = self.get_property(property_name)

        if p is None:
            p = Property()
            p.name = property_name
            self.custom_properties.append(p)

        p.value = property_value

    def get_property(self, prop_name):
        for p in self.custom_properties:
            if p.name == prop_name:
                return p
        return None
