// Code generated by protoc-gen-go. DO NOT EDIT.
// source: message.proto

package pb

import (
	fmt "fmt"
	proto "github.com/golang/protobuf/proto"
	math "math"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion3 // please upgrade the proto package

type Object_Kinect struct {
	Id                   uint32   `protobuf:"varint,1,opt,name=id,proto3" json:"id,omitempty"`
	X                    uint32   `protobuf:"varint,2,opt,name=x,proto3" json:"x,omitempty"`
	Y                    uint32   `protobuf:"varint,3,opt,name=y,proto3" json:"y,omitempty"`
	Dist                 uint32   `protobuf:"varint,4,opt,name=dist,proto3" json:"dist,omitempty"`
	Conf                 uint32   `protobuf:"varint,5,opt,name=conf,proto3" json:"conf,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Object_Kinect) Reset()         { *m = Object_Kinect{} }
func (m *Object_Kinect) String() string { return proto.CompactTextString(m) }
func (*Object_Kinect) ProtoMessage()    {}
func (*Object_Kinect) Descriptor() ([]byte, []int) {
	return fileDescriptor_33c57e4bae7b9afd, []int{0}
}

func (m *Object_Kinect) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Object_Kinect.Unmarshal(m, b)
}
func (m *Object_Kinect) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Object_Kinect.Marshal(b, m, deterministic)
}
func (m *Object_Kinect) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Object_Kinect.Merge(m, src)
}
func (m *Object_Kinect) XXX_Size() int {
	return xxx_messageInfo_Object_Kinect.Size(m)
}
func (m *Object_Kinect) XXX_DiscardUnknown() {
	xxx_messageInfo_Object_Kinect.DiscardUnknown(m)
}

var xxx_messageInfo_Object_Kinect proto.InternalMessageInfo

func (m *Object_Kinect) GetId() uint32 {
	if m != nil {
		return m.Id
	}
	return 0
}

func (m *Object_Kinect) GetX() uint32 {
	if m != nil {
		return m.X
	}
	return 0
}

func (m *Object_Kinect) GetY() uint32 {
	if m != nil {
		return m.Y
	}
	return 0
}

func (m *Object_Kinect) GetDist() uint32 {
	if m != nil {
		return m.Dist
	}
	return 0
}

func (m *Object_Kinect) GetConf() uint32 {
	if m != nil {
		return m.Conf
	}
	return 0
}

type Object_Omni struct {
	Id                   uint32   `protobuf:"varint,1,opt,name=id,proto3" json:"id,omitempty"`
	X                    uint32   `protobuf:"varint,2,opt,name=x,proto3" json:"x,omitempty"`
	Y                    uint32   `protobuf:"varint,3,opt,name=y,proto3" json:"y,omitempty"`
	Dist                 uint32   `protobuf:"varint,4,opt,name=dist,proto3" json:"dist,omitempty"`
	Conf                 uint32   `protobuf:"varint,6,opt,name=conf,proto3" json:"conf,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Object_Omni) Reset()         { *m = Object_Omni{} }
func (m *Object_Omni) String() string { return proto.CompactTextString(m) }
func (*Object_Omni) ProtoMessage()    {}
func (*Object_Omni) Descriptor() ([]byte, []int) {
	return fileDescriptor_33c57e4bae7b9afd, []int{1}
}

func (m *Object_Omni) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Object_Omni.Unmarshal(m, b)
}
func (m *Object_Omni) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Object_Omni.Marshal(b, m, deterministic)
}
func (m *Object_Omni) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Object_Omni.Merge(m, src)
}
func (m *Object_Omni) XXX_Size() int {
	return xxx_messageInfo_Object_Omni.Size(m)
}
func (m *Object_Omni) XXX_DiscardUnknown() {
	xxx_messageInfo_Object_Omni.DiscardUnknown(m)
}

var xxx_messageInfo_Object_Omni proto.InternalMessageInfo

func (m *Object_Omni) GetId() uint32 {
	if m != nil {
		return m.Id
	}
	return 0
}

func (m *Object_Omni) GetX() uint32 {
	if m != nil {
		return m.X
	}
	return 0
}

func (m *Object_Omni) GetY() uint32 {
	if m != nil {
		return m.Y
	}
	return 0
}

func (m *Object_Omni) GetDist() uint32 {
	if m != nil {
		return m.Dist
	}
	return 0
}

func (m *Object_Omni) GetConf() uint32 {
	if m != nil {
		return m.Conf
	}
	return 0
}

type Request_Omni_Calib struct {
	Check                bool     `protobuf:"varint,1,opt,name=check,proto3" json:"check,omitempty"`
	Image                []byte   `protobuf:"bytes,2,opt,name=image,proto3" json:"image,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Request_Omni_Calib) Reset()         { *m = Request_Omni_Calib{} }
func (m *Request_Omni_Calib) String() string { return proto.CompactTextString(m) }
func (*Request_Omni_Calib) ProtoMessage()    {}
func (*Request_Omni_Calib) Descriptor() ([]byte, []int) {
	return fileDescriptor_33c57e4bae7b9afd, []int{2}
}

func (m *Request_Omni_Calib) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Request_Omni_Calib.Unmarshal(m, b)
}
func (m *Request_Omni_Calib) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Request_Omni_Calib.Marshal(b, m, deterministic)
}
func (m *Request_Omni_Calib) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Request_Omni_Calib.Merge(m, src)
}
func (m *Request_Omni_Calib) XXX_Size() int {
	return xxx_messageInfo_Request_Omni_Calib.Size(m)
}
func (m *Request_Omni_Calib) XXX_DiscardUnknown() {
	xxx_messageInfo_Request_Omni_Calib.DiscardUnknown(m)
}

var xxx_messageInfo_Request_Omni_Calib proto.InternalMessageInfo

func (m *Request_Omni_Calib) GetCheck() bool {
	if m != nil {
		return m.Check
	}
	return false
}

func (m *Request_Omni_Calib) GetImage() []byte {
	if m != nil {
		return m.Image
	}
	return nil
}

type Request struct {
	Check                bool     `protobuf:"varint,1,opt,name=check,proto3" json:"check,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Request) Reset()         { *m = Request{} }
func (m *Request) String() string { return proto.CompactTextString(m) }
func (*Request) ProtoMessage()    {}
func (*Request) Descriptor() ([]byte, []int) {
	return fileDescriptor_33c57e4bae7b9afd, []int{3}
}

func (m *Request) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Request.Unmarshal(m, b)
}
func (m *Request) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Request.Marshal(b, m, deterministic)
}
func (m *Request) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Request.Merge(m, src)
}
func (m *Request) XXX_Size() int {
	return xxx_messageInfo_Request.Size(m)
}
func (m *Request) XXX_DiscardUnknown() {
	xxx_messageInfo_Request.DiscardUnknown(m)
}

var xxx_messageInfo_Request proto.InternalMessageInfo

func (m *Request) GetCheck() bool {
	if m != nil {
		return m.Check
	}
	return false
}

type Request_BS struct {
	Check                uint32   `protobuf:"varint,1,opt,name=check,proto3" json:"check,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Request_BS) Reset()         { *m = Request_BS{} }
func (m *Request_BS) String() string { return proto.CompactTextString(m) }
func (*Request_BS) ProtoMessage()    {}
func (*Request_BS) Descriptor() ([]byte, []int) {
	return fileDescriptor_33c57e4bae7b9afd, []int{4}
}

func (m *Request_BS) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Request_BS.Unmarshal(m, b)
}
func (m *Request_BS) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Request_BS.Marshal(b, m, deterministic)
}
func (m *Request_BS) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Request_BS.Merge(m, src)
}
func (m *Request_BS) XXX_Size() int {
	return xxx_messageInfo_Request_BS.Size(m)
}
func (m *Request_BS) XXX_DiscardUnknown() {
	xxx_messageInfo_Request_BS.DiscardUnknown(m)
}

var xxx_messageInfo_Request_BS proto.InternalMessageInfo

func (m *Request_BS) GetCheck() uint32 {
	if m != nil {
		return m.Check
	}
	return 0
}

type Response_Omni struct {
	Omni                 []byte         `protobuf:"bytes,1,opt,name=omni,proto3" json:"omni,omitempty"`
	ImgToSend            uint32         `protobuf:"varint,2,opt,name=img_to_send,json=imgToSend,proto3" json:"img_to_send,omitempty"`
	Objects              []*Object_Omni `protobuf:"bytes,3,rep,name=objects,proto3" json:"objects,omitempty"`
	XXX_NoUnkeyedLiteral struct{}       `json:"-"`
	XXX_unrecognized     []byte         `json:"-"`
	XXX_sizecache        int32          `json:"-"`
}

func (m *Response_Omni) Reset()         { *m = Response_Omni{} }
func (m *Response_Omni) String() string { return proto.CompactTextString(m) }
func (*Response_Omni) ProtoMessage()    {}
func (*Response_Omni) Descriptor() ([]byte, []int) {
	return fileDescriptor_33c57e4bae7b9afd, []int{5}
}

func (m *Response_Omni) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Response_Omni.Unmarshal(m, b)
}
func (m *Response_Omni) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Response_Omni.Marshal(b, m, deterministic)
}
func (m *Response_Omni) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Response_Omni.Merge(m, src)
}
func (m *Response_Omni) XXX_Size() int {
	return xxx_messageInfo_Response_Omni.Size(m)
}
func (m *Response_Omni) XXX_DiscardUnknown() {
	xxx_messageInfo_Response_Omni.DiscardUnknown(m)
}

var xxx_messageInfo_Response_Omni proto.InternalMessageInfo

func (m *Response_Omni) GetOmni() []byte {
	if m != nil {
		return m.Omni
	}
	return nil
}

func (m *Response_Omni) GetImgToSend() uint32 {
	if m != nil {
		return m.ImgToSend
	}
	return 0
}

func (m *Response_Omni) GetObjects() []*Object_Omni {
	if m != nil {
		return m.Objects
	}
	return nil
}

type Response_Kinect struct {
	Kinect               []byte           `protobuf:"bytes,1,opt,name=kinect,proto3" json:"kinect,omitempty"`
	KinectDepth          []byte           `protobuf:"bytes,2,opt,name=kinect_depth,json=kinectDepth,proto3" json:"kinect_depth,omitempty"`
	Objects              []*Object_Kinect `protobuf:"bytes,3,rep,name=objects,proto3" json:"objects,omitempty"`
	XXX_NoUnkeyedLiteral struct{}         `json:"-"`
	XXX_unrecognized     []byte           `json:"-"`
	XXX_sizecache        int32            `json:"-"`
}

func (m *Response_Kinect) Reset()         { *m = Response_Kinect{} }
func (m *Response_Kinect) String() string { return proto.CompactTextString(m) }
func (*Response_Kinect) ProtoMessage()    {}
func (*Response_Kinect) Descriptor() ([]byte, []int) {
	return fileDescriptor_33c57e4bae7b9afd, []int{6}
}

func (m *Response_Kinect) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Response_Kinect.Unmarshal(m, b)
}
func (m *Response_Kinect) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Response_Kinect.Marshal(b, m, deterministic)
}
func (m *Response_Kinect) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Response_Kinect.Merge(m, src)
}
func (m *Response_Kinect) XXX_Size() int {
	return xxx_messageInfo_Response_Kinect.Size(m)
}
func (m *Response_Kinect) XXX_DiscardUnknown() {
	xxx_messageInfo_Response_Kinect.DiscardUnknown(m)
}

var xxx_messageInfo_Response_Kinect proto.InternalMessageInfo

func (m *Response_Kinect) GetKinect() []byte {
	if m != nil {
		return m.Kinect
	}
	return nil
}

func (m *Response_Kinect) GetKinectDepth() []byte {
	if m != nil {
		return m.KinectDepth
	}
	return nil
}

func (m *Response_Kinect) GetObjects() []*Object_Kinect {
	if m != nil {
		return m.Objects
	}
	return nil
}

type ResponseTo_BS struct {
	Image                []byte   `protobuf:"bytes,1,opt,name=image,proto3" json:"image,omitempty"`
	Count                uint32   `protobuf:"varint,2,opt,name=count,proto3" json:"count,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *ResponseTo_BS) Reset()         { *m = ResponseTo_BS{} }
func (m *ResponseTo_BS) String() string { return proto.CompactTextString(m) }
func (*ResponseTo_BS) ProtoMessage()    {}
func (*ResponseTo_BS) Descriptor() ([]byte, []int) {
	return fileDescriptor_33c57e4bae7b9afd, []int{7}
}

func (m *ResponseTo_BS) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_ResponseTo_BS.Unmarshal(m, b)
}
func (m *ResponseTo_BS) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_ResponseTo_BS.Marshal(b, m, deterministic)
}
func (m *ResponseTo_BS) XXX_Merge(src proto.Message) {
	xxx_messageInfo_ResponseTo_BS.Merge(m, src)
}
func (m *ResponseTo_BS) XXX_Size() int {
	return xxx_messageInfo_ResponseTo_BS.Size(m)
}
func (m *ResponseTo_BS) XXX_DiscardUnknown() {
	xxx_messageInfo_ResponseTo_BS.DiscardUnknown(m)
}

var xxx_messageInfo_ResponseTo_BS proto.InternalMessageInfo

func (m *ResponseTo_BS) GetImage() []byte {
	if m != nil {
		return m.Image
	}
	return nil
}

func (m *ResponseTo_BS) GetCount() uint32 {
	if m != nil {
		return m.Count
	}
	return 0
}

func init() {
	proto.RegisterType((*Object_Kinect)(nil), "pb.Object_Kinect")
	proto.RegisterType((*Object_Omni)(nil), "pb.Object_Omni")
	proto.RegisterType((*Request_Omni_Calib)(nil), "pb.Request_Omni_Calib")
	proto.RegisterType((*Request)(nil), "pb.Request")
	proto.RegisterType((*Request_BS)(nil), "pb.Request_BS")
	proto.RegisterType((*Response_Omni)(nil), "pb.Response_Omni")
	proto.RegisterType((*Response_Kinect)(nil), "pb.Response_Kinect")
	proto.RegisterType((*ResponseTo_BS)(nil), "pb.Response_to_BS")
}

func init() {
	proto.RegisterFile("message.proto", fileDescriptor_33c57e4bae7b9afd)
}

var fileDescriptor_33c57e4bae7b9afd = []byte{
	// 455 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0xac, 0x93, 0xc1, 0x6f, 0xd3, 0x30,
	0x14, 0xc6, 0x9b, 0xb6, 0xeb, 0xe8, 0x4b, 0xd3, 0x69, 0x06, 0x4d, 0x51, 0x0f, 0x30, 0x7c, 0x40,
	0x45, 0x88, 0x56, 0x84, 0x0b, 0x07, 0x0e, 0x53, 0x07, 0x27, 0x0e, 0x93, 0x52, 0x2e, 0x70, 0x89,
	0x9c, 0xc4, 0xa4, 0x66, 0x8d, 0x6d, 0x6a, 0x57, 0x5a, 0xfe, 0x7b, 0x14, 0x3f, 0xb7, 0xa4, 0xc0,
	0x71, 0xb7, 0xf7, 0xbd, 0xbe, 0x7c, 0xbf, 0x7e, 0x5f, 0x14, 0x88, 0x6a, 0x6e, 0x0c, 0xab, 0xf8,
	0x42, 0xef, 0x94, 0x55, 0xa4, 0xaf, 0x73, 0x5a, 0x40, 0x74, 0x97, 0xff, 0xe4, 0x85, 0xcd, 0xbe,
	0x08, 0xc9, 0x0b, 0x4b, 0xa6, 0xd0, 0x17, 0x65, 0x1c, 0x5c, 0x07, 0xf3, 0x28, 0xed, 0x8b, 0x92,
	0x4c, 0x20, 0x78, 0x88, 0xfb, 0x4e, 0x06, 0x0f, 0xad, 0x6a, 0xe2, 0x01, 0xaa, 0x86, 0x10, 0x18,
	0x96, 0xc2, 0xd8, 0x78, 0xe8, 0x16, 0x6e, 0x6e, 0x77, 0x85, 0x92, 0x3f, 0xe2, 0x33, 0xdc, 0xb5,
	0x33, 0x65, 0x10, 0x7a, 0xc8, 0x5d, 0x2d, 0xc5, 0xa3, 0x21, 0x46, 0x1d, 0xc4, 0x0d, 0x90, 0x94,
	0xff, 0xda, 0x73, 0x83, 0x8c, 0xec, 0x96, 0x6d, 0x45, 0x4e, 0x9e, 0xc1, 0x59, 0xb1, 0xe1, 0xc5,
	0xbd, 0x83, 0x3d, 0x49, 0x51, 0xb4, 0x5b, 0x51, 0xb3, 0x8a, 0x3b, 0xe6, 0x24, 0x45, 0x41, 0x5f,
	0xc0, 0xb9, 0x77, 0xf8, 0xff, 0x63, 0x94, 0x02, 0x1c, 0x10, 0xab, 0xf5, 0xe9, 0x4d, 0x74, 0xb8,
	0x91, 0x10, 0xa5, 0xdc, 0x68, 0x25, 0x0d, 0xc7, 0xac, 0x04, 0x86, 0xaa, 0x96, 0xc2, 0x5d, 0x4d,
	0x52, 0x37, 0x93, 0xe7, 0x10, 0x8a, 0xba, 0xca, 0xac, 0xca, 0x0c, 0x97, 0xa5, 0x4f, 0x3e, 0x16,
	0x75, 0xf5, 0x55, 0xad, 0xb9, 0x2c, 0xc9, 0x6b, 0x38, 0x57, 0xae, 0x2e, 0x13, 0x0f, 0xae, 0x07,
	0xf3, 0x30, 0xb9, 0x58, 0xe8, 0x7c, 0xd1, 0x69, 0x30, 0x3d, 0xfc, 0x4e, 0x1b, 0xb8, 0x38, 0xf2,
	0xfc, 0x0b, 0xbc, 0x82, 0xd1, 0xbd, 0x9b, 0x3c, 0xd3, 0x2b, 0xf2, 0x12, 0x26, 0x38, 0x65, 0x25,
	0xd7, 0x76, 0xe3, 0xc3, 0x87, 0xb8, 0xfb, 0xd4, 0xae, 0xc8, 0x9b, 0xbf, 0xc1, 0x97, 0x1d, 0x30,
	0xda, 0xff, 0x41, 0x7f, 0x84, 0xe9, 0x11, 0x6d, 0x95, 0xaf, 0x04, 0x7b, 0x0d, 0x3a, 0xbd, 0xba,
	0xa2, 0xd4, 0x5e, 0x5a, 0x9f, 0x13, 0x45, 0xf2, 0x19, 0xc6, 0xdf, 0xd4, 0x56, 0x61, 0x49, 0x1f,
	0x60, 0xdc, 0x06, 0x47, 0x71, 0xd5, 0x32, 0xff, 0x7d, 0x97, 0xb3, 0x4b, 0xdc, 0x77, 0xca, 0xa5,
	0xbd, 0xe4, 0x06, 0x42, 0x67, 0xe3, 0xb3, 0xbf, 0x83, 0xd0, 0x19, 0x79, 0x19, 0x76, 0xac, 0x66,
	0x4f, 0x4f, 0x9e, 0xc7, 0x0b, 0xda, 0x4b, 0x6e, 0x21, 0x5a, 0x31, 0xc3, 0xb3, 0x35, 0xb3, 0xcc,
	0x0a, 0x25, 0x49, 0x02, 0xe0, 0x3c, 0x30, 0xd3, 0xb4, 0xfb, 0x6f, 0x56, 0xeb, 0x19, 0x39, 0x71,
	0x71, 0x37, 0xb4, 0xb7, 0x9a, 0x7f, 0x7f, 0x55, 0x09, 0xbb, 0xd9, 0xe7, 0x8b, 0x42, 0xd5, 0x4b,
	0xb6, 0x2b, 0x99, 0xdc, 0xb2, 0xdc, 0x2c, 0x75, 0x63, 0x37, 0x4a, 0xbe, 0xad, 0xd4, 0xb2, 0xda,
	0xe9, 0x62, 0xa9, 0xf3, 0x7c, 0xe4, 0x3e, 0xbd, 0xf7, 0xbf, 0x03, 0x00, 0x00, 0xff, 0xff, 0x80,
	0x8b, 0xe6, 0x56, 0x8b, 0x03, 0x00, 0x00,
}
