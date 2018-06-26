# Copyright (c) 2017 Sony Corporation. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

_header = """// Copyright (c) 2017 Sony Corporation. All Rights Reserved.
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// *WARNING*
// THIS FILE IS AUTO-GENERATED BY CODE GENERATOR.
// PLEASE DO NOT EDIT THIS FILE BY HAND!
"""

csrc_parameters_defines = _header + """
#ifndef H_{name_upper}_PARAMETERS_H__
#define H_{name_upper}_PARAMETERS_H__

#ifdef __cplusplus
extern "C" {{
#endif /* __cplusplus */

{parameter_defines}

#ifdef __cplusplus
}}
#endif /* __cplusplus */

#endif //H_{name_upper}_PARAMETERS_H__
"""

csrc_parameters_implements = _header + """
#include "{name}_parameters.h"

{parameter_implements}
"""


csrc_defines = _header + """
#ifndef H_{name_upper}_INFERENCE_H__
#define H_{name_upper}_INFERENCE_H__

#ifdef __cplusplus
extern "C" {{
#endif /* __cplusplus */

// All information for inference stores into context buffer.
// Detailed structure of context is unvisible from user.

/// Allocate memories and initialize buffers.
void* {prefix}_allocate_context(void** params);

/// Free all memories in the context
int {prefix}_free_context(void* context);

/// Number of input buffers.
#define {prefix_upper}_NUM_OF_INPUT_BUFFERS ({num_of_input_buffers})
/// Input buffer sizes.
{input_buffer_size_defines}
/// Pointer of allocated buffer.
float* {prefix}_input_buffer(void* context, int index);

/// Number of output buffers.
#define {prefix_upper}_NUM_OF_OUTPUT_BUFFERS ({num_of_output_buffers})
/// Output buffer sizes.
{output_buffer_size_defines}
/// Pointer of allocated buffer.
float* {prefix}_output_buffer(void* context, int index);
{param_buffer}
/// Exec inference
int {prefix}_inference(void* context);

#ifdef __cplusplus
}}
#endif /* __cplusplus */

#endif //H_{name_upper}_INFERENCE_H__
"""


csrc_implements = _header + """
#include "{name}_inference.h"

#include <nnablart/functions.h>

{internal_defines}

void* {prefix}_allocate_context(void** params)
{{
    {prefix}_local_context_t* c = malloc(sizeof({prefix}_local_context_t));
{initialize_context}
    return (void*)c;
}}

int {prefix}_free_context(void* context)
{{
    {prefix}_local_context_t* c = ({prefix}_local_context_t*)context;
{free_context}  
    free(context);
    return NN_ERROR_CODE_NOERROR;
}}

float* {prefix}_input_buffer(void* context, int index)
{{
    {prefix}_local_context_t* c = ({prefix}_local_context_t*)context;
{input_buffer}
    return 0;
}}

float* {prefix}_output_buffer(void* context, int index)
{{
    {prefix}_local_context_t* c = ({prefix}_local_context_t*)context;
{output_buffer}
    return 0;
}}
{param_buffer}
int {prefix}_inference(void* context)
{{
    {prefix}_local_context_t* c = ({prefix}_local_context_t*)context;
{inference}
    return NN_ERROR_CODE_NOERROR;
}}
"""

csrc_example = _header + """
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

{includes}

int main(int argc, char* argv[])
{{
    if(argc != {prefix_upper}_NUM_OF_INPUT_BUFFERS + 2) {{
        printf("Please specify {num_of_input_buffers} input files and a output file prefix\\n");
        return -1;
    }}

    // Allocate and initialize context
    {allocate}

    // Input files.
{prepare_input_file}

    // Exec inference
    {prefix}_inference(context);
    
    // Output file.
{prepare_output_file}

    // free all context
    {prefix}_free_context(context);
    return 0;
}}
"""

csrc_gnumake = """# Copyright (c) 2017 Sony Corporation. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# *WARNING*
# THIS FILE IS AUTO-GENERATED BY CODE GENERATOR.
# PLEASE DO NOT EDIT THIS FILE BY HAND!

all: {name}_example

{name}_example: {name}_example.c {name}_inference.c{param}
	$(CC) -Wall -Werror $(CFLAGS) $^ -o $@ $(LDFLAGS) -lnnablart_functions -lm

"""
