// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             v3.12.4
// source: message.proto

package pb

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// Yolo_OmniClient is the client API for Yolo_Omni service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type Yolo_OmniClient interface {
	Send_Omni(ctx context.Context, in *Request_Omni_Calib, opts ...grpc.CallOption) (*Response_Omni, error)
}

type yolo_OmniClient struct {
	cc grpc.ClientConnInterface
}

func NewYolo_OmniClient(cc grpc.ClientConnInterface) Yolo_OmniClient {
	return &yolo_OmniClient{cc}
}

func (c *yolo_OmniClient) Send_Omni(ctx context.Context, in *Request_Omni_Calib, opts ...grpc.CallOption) (*Response_Omni, error) {
	out := new(Response_Omni)
	err := c.cc.Invoke(ctx, "/pb.Yolo_Omni/Send_Omni", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// Yolo_OmniServer is the server API for Yolo_Omni service.
// All implementations must embed UnimplementedYolo_OmniServer
// for forward compatibility
type Yolo_OmniServer interface {
	Send_Omni(context.Context, *Request_Omni_Calib) (*Response_Omni, error)
	mustEmbedUnimplementedYolo_OmniServer()
}

// UnimplementedYolo_OmniServer must be embedded to have forward compatible implementations.
type UnimplementedYolo_OmniServer struct {
}

func (UnimplementedYolo_OmniServer) Send_Omni(context.Context, *Request_Omni_Calib) (*Response_Omni, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Send_Omni not implemented")
}
func (UnimplementedYolo_OmniServer) mustEmbedUnimplementedYolo_OmniServer() {}

// UnsafeYolo_OmniServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to Yolo_OmniServer will
// result in compilation errors.
type UnsafeYolo_OmniServer interface {
	mustEmbedUnimplementedYolo_OmniServer()
}

func RegisterYolo_OmniServer(s grpc.ServiceRegistrar, srv Yolo_OmniServer) {
	s.RegisterService(&Yolo_Omni_ServiceDesc, srv)
}

func _Yolo_Omni_Send_Omni_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Request_Omni_Calib)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(Yolo_OmniServer).Send_Omni(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/pb.Yolo_Omni/Send_Omni",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(Yolo_OmniServer).Send_Omni(ctx, req.(*Request_Omni_Calib))
	}
	return interceptor(ctx, in, info, handler)
}

// Yolo_Omni_ServiceDesc is the grpc.ServiceDesc for Yolo_Omni service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Yolo_Omni_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "pb.Yolo_Omni",
	HandlerType: (*Yolo_OmniServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Send_Omni",
			Handler:    _Yolo_Omni_Send_Omni_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "message.proto",
}

// Yolo_KinectClient is the client API for Yolo_Kinect service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type Yolo_KinectClient interface {
	Send_Kinect(ctx context.Context, in *Request, opts ...grpc.CallOption) (*Response_Kinect, error)
}

type yolo_KinectClient struct {
	cc grpc.ClientConnInterface
}

func NewYolo_KinectClient(cc grpc.ClientConnInterface) Yolo_KinectClient {
	return &yolo_KinectClient{cc}
}

func (c *yolo_KinectClient) Send_Kinect(ctx context.Context, in *Request, opts ...grpc.CallOption) (*Response_Kinect, error) {
	out := new(Response_Kinect)
	err := c.cc.Invoke(ctx, "/pb.Yolo_Kinect/Send_Kinect", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// Yolo_KinectServer is the server API for Yolo_Kinect service.
// All implementations must embed UnimplementedYolo_KinectServer
// for forward compatibility
type Yolo_KinectServer interface {
	Send_Kinect(context.Context, *Request) (*Response_Kinect, error)
	mustEmbedUnimplementedYolo_KinectServer()
}

// UnimplementedYolo_KinectServer must be embedded to have forward compatible implementations.
type UnimplementedYolo_KinectServer struct {
}

func (UnimplementedYolo_KinectServer) Send_Kinect(context.Context, *Request) (*Response_Kinect, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Send_Kinect not implemented")
}
func (UnimplementedYolo_KinectServer) mustEmbedUnimplementedYolo_KinectServer() {}

// UnsafeYolo_KinectServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to Yolo_KinectServer will
// result in compilation errors.
type UnsafeYolo_KinectServer interface {
	mustEmbedUnimplementedYolo_KinectServer()
}

func RegisterYolo_KinectServer(s grpc.ServiceRegistrar, srv Yolo_KinectServer) {
	s.RegisterService(&Yolo_Kinect_ServiceDesc, srv)
}

func _Yolo_Kinect_Send_Kinect_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Request)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(Yolo_KinectServer).Send_Kinect(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/pb.Yolo_Kinect/Send_Kinect",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(Yolo_KinectServer).Send_Kinect(ctx, req.(*Request))
	}
	return interceptor(ctx, in, info, handler)
}

// Yolo_Kinect_ServiceDesc is the grpc.ServiceDesc for Yolo_Kinect service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Yolo_Kinect_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "pb.Yolo_Kinect",
	HandlerType: (*Yolo_KinectServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Send_Kinect",
			Handler:    _Yolo_Kinect_Send_Kinect_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "message.proto",
}

// Base_SatationClient is the client API for Base_Satation service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type Base_SatationClient interface {
	SendTo_BS(ctx context.Context, in *Request_BS, opts ...grpc.CallOption) (*ResponseTo_BS, error)
}

type base_SatationClient struct {
	cc grpc.ClientConnInterface
}

func NewBase_SatationClient(cc grpc.ClientConnInterface) Base_SatationClient {
	return &base_SatationClient{cc}
}

func (c *base_SatationClient) SendTo_BS(ctx context.Context, in *Request_BS, opts ...grpc.CallOption) (*ResponseTo_BS, error) {
	out := new(ResponseTo_BS)
	err := c.cc.Invoke(ctx, "/pb.Base_Satation/Send_to_BS", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// Base_SatationServer is the server API for Base_Satation service.
// All implementations must embed UnimplementedBase_SatationServer
// for forward compatibility
type Base_SatationServer interface {
	SendTo_BS(context.Context, *Request_BS) (*ResponseTo_BS, error)
	mustEmbedUnimplementedBase_SatationServer()
}

// UnimplementedBase_SatationServer must be embedded to have forward compatible implementations.
type UnimplementedBase_SatationServer struct {
}

func (UnimplementedBase_SatationServer) SendTo_BS(context.Context, *Request_BS) (*ResponseTo_BS, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SendTo_BS not implemented")
}
func (UnimplementedBase_SatationServer) mustEmbedUnimplementedBase_SatationServer() {}

// UnsafeBase_SatationServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to Base_SatationServer will
// result in compilation errors.
type UnsafeBase_SatationServer interface {
	mustEmbedUnimplementedBase_SatationServer()
}

func RegisterBase_SatationServer(s grpc.ServiceRegistrar, srv Base_SatationServer) {
	s.RegisterService(&Base_Satation_ServiceDesc, srv)
}

func _Base_Satation_SendTo_BS_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Request_BS)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(Base_SatationServer).SendTo_BS(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/pb.Base_Satation/Send_to_BS",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(Base_SatationServer).SendTo_BS(ctx, req.(*Request_BS))
	}
	return interceptor(ctx, in, info, handler)
}

// Base_Satation_ServiceDesc is the grpc.ServiceDesc for Base_Satation service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Base_Satation_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "pb.Base_Satation",
	HandlerType: (*Base_SatationServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Send_to_BS",
			Handler:    _Base_Satation_SendTo_BS_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "message.proto",
}