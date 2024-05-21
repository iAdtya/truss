# flake8: noqa
# type: ignore

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: briton.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0c\x62riton.proto\x12\x06\x62riton"\xb0\x04\n\x10InferenceRequest\x12\x12\n\nrequest_id\x18\x01 \x01(\x03\x12\x12\n\ninput_text\x18\x02 \x01(\t\x12\x11\n\tinput_ids\x18\x03 \x03(\x05\x12\x1f\n\x12request_output_len\x18\x05 \x01(\rH\x00\x88\x01\x01\x12\x13\n\x06\x65nd_id\x18\x06 \x01(\rH\x01\x88\x01\x01\x12\x13\n\x06pad_id\x18\x07 \x01(\rH\x02\x88\x01\x01\x12\x17\n\nbeam_width\x18\n \x01(\rH\x03\x88\x01\x01\x12\x18\n\x0btemperature\x18\x0b \x01(\x02H\x04\x88\x01\x01\x12\x1a\n\rruntime_top_k\x18\x0c \x01(\rH\x05\x88\x01\x01\x12\x1a\n\rruntime_top_p\x18\r \x01(\x02H\x06\x88\x01\x01\x12\x18\n\x0blen_penalty\x18\x0e \x01(\x02H\x07\x88\x01\x01\x12\x1f\n\x12repetition_penalty\x18\x0f \x01(\x02H\x08\x88\x01\x01\x12\x1d\n\x10presence_penalty\x18\x10 \x01(\x02H\t\x88\x01\x01\x12\x11\n\tbad_words\x18\x11 \x03(\t\x12\x12\n\nstop_words\x18\x12 \x03(\tB\x15\n\x13_request_output_lenB\t\n\x07_end_idB\t\n\x07_pad_idB\r\n\x0b_beam_widthB\x0e\n\x0c_temperatureB\x10\n\x0e_runtime_top_kB\x10\n\x0e_runtime_top_pB\x0e\n\x0c_len_penaltyB\x15\n\x13_repetition_penaltyB\x13\n\x11_presence_penalty"R\n\x13InferenceAnswerPart\x12\x12\n\nrequest_id\x18\x01 \x01(\x03\x12\x13\n\x0boutput_text\x18\x02 \x01(\t\x12\x12\n\noutput_ids\x18\x03 \x03(\x05"\xfa\x03\n\x0c\x42ritonConfig\x12\x13\n\x0b\x65ngine_path\x18\x01 \x01(\t\x12\x14\n\x0chf_tokenizer\x18\x02 \x01(\t\x12N\n\x16\x62\x61tch_scheduler_policy\x18\x05 \x01(\x0e\x32).briton.BritonConfig.BatchSchedulerPolicyH\x00\x88\x01\x01\x12\x1f\n\x12\x65nable_trt_overlap\x18\x06 \x01(\x08H\x01\x88\x01\x01\x12)\n\x1cmax_tokens_in_paged_kv_cache\x18\n \x01(\x04H\x02\x88\x01\x01\x12+\n\x1ekv_cache_free_gpu_mem_fraction\x18\x0b \x01(\x02H\x03\x88\x01\x01\x12!\n\x14medusa_decoding_mode\x18\x0c \x01(\x08H\x04\x88\x01\x01"D\n\x14\x42\x61tchSchedulerPolicy\x12\x13\n\x0fMAX_UTILIZATION\x10\x00\x12\x17\n\x13GUARANTEED_NO_EVICT\x10\x01\x42\x19\n\x17_batch_scheduler_policyB\x15\n\x13_enable_trt_overlapB\x1f\n\x1d_max_tokens_in_paged_kv_cacheB!\n\x1f_kv_cache_free_gpu_mem_fractionB\x17\n\x15_medusa_decoding_mode2L\n\x06\x42riton\x12\x42\n\x05Infer\x12\x18.briton.InferenceRequest\x1a\x1b.briton.InferenceAnswerPart"\x00\x30\x01\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "briton_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_INFERENCEREQUEST"]._serialized_start = 25
    _globals["_INFERENCEREQUEST"]._serialized_end = 585
    _globals["_INFERENCEANSWERPART"]._serialized_start = 587
    _globals["_INFERENCEANSWERPART"]._serialized_end = 669
    _globals["_BRITONCONFIG"]._serialized_start = 672
    _globals["_BRITONCONFIG"]._serialized_end = 1178
    _globals["_BRITONCONFIG_BATCHSCHEDULERPOLICY"]._serialized_start = 967
    _globals["_BRITONCONFIG_BATCHSCHEDULERPOLICY"]._serialized_end = 1035
    _globals["_BRITON"]._serialized_start = 1180
    _globals["_BRITON"]._serialized_end = 1256
# @@protoc_insertion_point(module_scope)
