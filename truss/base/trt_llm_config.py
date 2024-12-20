import json
import warnings
from enum import Enum
from typing import Optional

from huggingface_hub.errors import HFValidationError
from huggingface_hub.utils import validate_repo_id
from pydantic import BaseModel, PydanticDeprecatedSince20, validator

# Suppress Pydantic V1 warnings, because we have to use it for backwards compat.
warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)


class TrussTRTLLMModel(str, Enum):
    LLAMA = "llama"
    MISTRAL = "mistral"
    DEEPSEEK = "deepseek"
    WHISPER = "whisper"
    QWEN = "qwen"


class TrussTRTLLMQuantizationType(str, Enum):
    NO_QUANT = "no_quant"
    WEIGHTS_ONLY_INT8 = "weights_int8"
    WEIGHTS_KV_INT8 = "weights_kv_int8"
    WEIGHTS_ONLY_INT4 = "weights_int4"
    WEIGHTS_INT4_KV_INT8 = "weights_int4_kv_int8"
    SMOOTH_QUANT = "smooth_quant"
    FP8 = "fp8"
    FP8_KV = "fp8_kv"


class TrussTRTLLMPluginConfiguration(BaseModel):
    paged_kv_cache: bool = True
    gemm_plugin: str = "auto"
    use_paged_context_fmha: bool = False
    use_fp8_context_fmha: bool = False


class CheckpointSource(str, Enum):
    HF: str = "HF"
    GCS: str = "GCS"
    LOCAL: str = "LOCAL"
    # REMOTE_URL is useful when the checkpoint lives on remote storage accessible via HTTP (e.g a presigned URL)
    REMOTE_URL: str = "REMOTE_URL"


class CheckpointRepository(BaseModel):
    source: CheckpointSource
    repo: str


class TrussTRTLLMBatchSchedulerPolicy(str, Enum):
    MAX_UTILIZATION = "max_utilization"
    GUARANTEED_NO_EVICT = "guaranteed_no_evict"


class TrussSpecDecMode(str, Enum):
    DRAFT_EXTERNAL: str = "DRAFT_TOKENS_EXTERNAL"


class TrussTRTLLMBuildConfiguration(BaseModel):
    base_model: TrussTRTLLMModel
    max_seq_len: int
    max_batch_size: Optional[int] = 256
    max_num_tokens: Optional[int] = 8192
    max_beam_width: int = 1
    max_prompt_embedding_table_size: int = 0
    checkpoint_repository: CheckpointRepository
    gather_all_token_logits: bool = False
    strongly_typed: bool = False
    quantization_type: TrussTRTLLMQuantizationType = (
        TrussTRTLLMQuantizationType.NO_QUANT
    )
    tensor_parallel_count: int = 1
    pipeline_parallel_count: int = 1
    plugin_configuration: TrussTRTLLMPluginConfiguration = (
        TrussTRTLLMPluginConfiguration()
    )
    num_builder_gpus: Optional[int] = None
    speculative_decoding_mode: Optional[TrussSpecDecMode] = None
    max_draft_len: Optional[int] = None

    @validator("max_beam_width")
    def check_max_beam_width(cls, v: int):
        if isinstance(v, int):
            if v != 1:
                raise ValueError(
                    "max_beam_width greater than 1 is not currently supported"
                )
        return v


class TrussTRTLLMRuntimeConfiguration(BaseModel):
    kv_cache_free_gpu_mem_fraction: float = 0.9
    enable_chunked_context: bool = False
    batch_scheduler_policy: TrussTRTLLMBatchSchedulerPolicy = (
        TrussTRTLLMBatchSchedulerPolicy.GUARANTEED_NO_EVICT
    )
    request_default_max_tokens: Optional[int] = None
    # Speculative Decoding runtime configuration, ignored for non spec dec configurations
    num_draft_tokens: Optional[int] = (
        None  # number of draft tokens to be sampled from draft model in speculative decoding scheme
    )


class TRTLLMConfiguration(BaseModel):
    runtime: TrussTRTLLMRuntimeConfiguration = TrussTRTLLMRuntimeConfiguration()
    build: TrussTRTLLMBuildConfiguration

    def __init__(self, **data):
        super().__init__(**data)
        self._validate_kv_cache_flags()
        if self.build.checkpoint_repository.source == CheckpointSource.HF:
            self._validate_hf_repo_id()

    def _validate_kv_cache_flags(self):
        if self.build is None:
            return self
        if not self.build.plugin_configuration.paged_kv_cache and (
            self.build.plugin_configuration.use_paged_context_fmha
            or self.build.plugin_configuration.use_fp8_context_fmha
        ):
            raise ValueError(
                "Using paged context fmha or fp8 context fmha requires requires paged kv cache"
            )
        if (
            self.build.plugin_configuration.use_fp8_context_fmha
            and not self.build.plugin_configuration.use_paged_context_fmha
        ):
            raise ValueError("Using fp8 context fmha requires paged context fmha")
        return self

    def _validate_hf_repo_id(self):
        try:
            validate_repo_id(self.build.checkpoint_repository.repo)
        except HFValidationError as e:
            raise ValueError(
                f"HuggingFace repository validation failed: {str(e)}"
            ) from e

    @property
    def requires_build(self):
        if self.build is not None:
            return True
        return False

    # TODO(Abu): Replace this with model_dump(json=True)
    # when pydantic v2 is used here
    def to_json_dict(self, verbose=True):
        return json.loads(self.json(exclude_unset=not verbose))


class TRTLLMSpeculativeDecodingConfiguration(BaseModel):
    target: TRTLLMConfiguration
    draft: TRTLLMConfiguration
    total_token_limit: int = 500000

    def __init__(self, **data):
        super().__init__(**data)
        self._spec_dec_configs = [
            self.target.build.speculative_decoding_mode,
            self.target.build.max_draft_len,
        ] + (
            [self.draft.runtime.num_draft_tokens]
            if self.draft.runtime and self.draft.runtime.num_draft_tokens
            else [False]
        )
        self._validate_spec_dec()

    def _validate_spec_dec(self):
        if any(self._spec_dec_configs):
            if not all(self._spec_dec_configs):
                raise ValueError(
                    "Speculative decoding requires all of `target.build.speculative_decoding_mode`, `target.build.max_draft_len`, and `draft.runtime.num_draft_tokens` to be configured."
                )
        for trt_llm_config in [self.target, self.draft]:
            if trt_llm_config.build.base_model is TrussTRTLLMModel.WHISPER:
                raise ValueError("Speculative decoding for Whisper is not supported.")
        if (
            self.target.build.tensor_parallel_count
            != self.draft.build.tensor_parallel_count
        ):
            raise ValueError(
                "Speculative decoding requires the same tensor parallelism for target and draft models."
            )

    def to_json_dict(self, verbose=True):
        return json.loads(self.json(exclude_unset=not verbose))
