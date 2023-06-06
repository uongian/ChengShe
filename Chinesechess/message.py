#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import json

class Message:
    MOVE = 'MOVE'
    QUIT = 'QUIT'

    def __init__(self, message_type, data=None):
        self.message_type = message_type
        self.data = data

    def to_dict(self):
        return {'type': self.message_type, 'data': self.data}

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d):
        return cls(d['type'], d['data'])

    @classmethod
    def from_json(cls, json_str):
        d = json.loads(json_str)
        return cls.from_dict(d)
class NameMessage(Message):
    SET_NAME = 'SET_NAME'

    def __init__(self, name):
        super().__init__(self.SET_NAME, name)

    def pack(self):
        name_bytes = self.data.encode('utf-8')
        name_length = len(name_bytes)
        packed_data = struct.pack(f'!I{name_length}s', name_length, name_bytes)
        return self.message_type.encode('utf-8') + packed_data