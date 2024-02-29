from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object_Kinect(_message.Message):
    __slots__ = ["dist", "id", "x", "y"]
    DIST_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    dist: int
    id: int
    x: int
    y: int
    def __init__(self, id: _Optional[int] = ..., x: _Optional[int] = ..., y: _Optional[int] = ..., dist: _Optional[int] = ...) -> None: ...

class Object_Omni(_message.Message):
    __slots__ = ["dist", "id", "x", "y"]
    DIST_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    dist: int
    id: int
    x: int
    y: int
    def __init__(self, id: _Optional[int] = ..., x: _Optional[int] = ..., y: _Optional[int] = ..., dist: _Optional[int] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ["check"]
    CHECK_FIELD_NUMBER: _ClassVar[int]
    check: bool
    def __init__(self, check: bool = ...) -> None: ...

class Request_BS(_message.Message):
    __slots__ = ["check"]
    CHECK_FIELD_NUMBER: _ClassVar[int]
    check: int
    def __init__(self, check: _Optional[int] = ...) -> None: ...

class Request_Omni_Calib(_message.Message):
    __slots__ = ["image"]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: bytes
    def __init__(self, image: _Optional[bytes] = ...) -> None: ...

class Response_Kinect(_message.Message):
    __slots__ = ["kinect", "kinect_depth", "objects"]
    KINECT_DEPTH_FIELD_NUMBER: _ClassVar[int]
    KINECT_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    kinect: bytes
    kinect_depth: bytes
    objects: _containers.RepeatedCompositeFieldContainer[Object_Kinect]
    def __init__(self, kinect: _Optional[bytes] = ..., kinect_depth: _Optional[bytes] = ..., objects: _Optional[_Iterable[_Union[Object_Kinect, _Mapping]]] = ...) -> None: ...

class Response_Omni(_message.Message):
    __slots__ = ["img_to_send", "objects", "omni"]
    IMG_TO_SEND_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    OMNI_FIELD_NUMBER: _ClassVar[int]
    img_to_send: int
    objects: _containers.RepeatedCompositeFieldContainer[Object_Omni]
    omni: bytes
    def __init__(self, omni: _Optional[bytes] = ..., img_to_send: _Optional[int] = ..., objects: _Optional[_Iterable[_Union[Object_Omni, _Mapping]]] = ...) -> None: ...

class Response_to_BS(_message.Message):
    __slots__ = ["count", "image"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    count: int
    image: bytes
    def __init__(self, image: _Optional[bytes] = ..., count: _Optional[int] = ...) -> None: ...
