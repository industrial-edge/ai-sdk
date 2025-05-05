<!--
SPDX-FileCopyrightText: Copyright (C) 2023 Siemens AG

SPDX-License-Identifier: MIT
-->

# Version History

AI Software Development Kit

Known issues:

-   Python 3.8.10 is the final regular bugfix release of Python 3.8 with binary installers. We recommend you to use the most recent bugfix release of Python 3.8 for productive use. For non-productive use, you can attempt using AI SDK with Python 3.8.10.
-   AI SDK has only been tested on 64-bit platforms. We do not recommend using AI SDK on 32-bit platforms.
-   The local pipeline runner might exceed the maximum path length allowed on Windows by default. To resolve this, please see the following article: https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry
-   As no TensorFlow Lite 2.7.0 installer was published for Windows systems, you cannot use the local pipeline runner on Windows to execute the TensorFlow Lite based pipeline packages, like the one provided in the Image Classification project template.
-   Markuppy is a new dependency in AI SDK 1.4.1 which is available as a source only wheel. As a consequence, you cannot simply include AI SDK 1.4.1 in a pipeline package, like you could in previous versions of AI SDK. As a workaround, you can include earlier version of AI SDK or include a manually created wheel of Markuppy along with AI SDK 1.4.1 in the pipeline package.
-   Python 3.7.x ≤ 3.11.2 - Remote Security Bypass Vulnerability - CVE-2023-24329 - AI SDK is not using blocklisting and hence is not affected

## 2.3.0

New features:

-   Optimizing dependency list to reduce package size
-   `Pipeline.export(...)` checks the size of the final generated zip package, throws error if it exceeds the limit of 2.2 GB
-   `PythonComponent` gives warning when TensorFlow dependency is detected
-   Warning about unused dependencies during LocalPipelineRunner execution
-   Incomplete input payload, output or metric does not throw AssertionError anymore; instead, a warning message will be issued about the missing variables

Deprecated features:

Fixed issues:
-   Python 3.10.x ≤ 3.10.14 - Multiple Vulnerabilities - 3.10.15
-   Python 3.11.x ≤ 3.11.9 - Multiple Vulnerabilities - 3.11.10


## 2.2.0

New features:

-   Adding new property of 'batch' to class 'Component'
-   LocalPipelineRunner can be used to run pipeline components with batch input or output
-   Enabled Python versions for using AI SDK is **'>=3.10.0'**. With Python 3.8, `simaticai >=2.2.0` cannot be installed.
-   Enabled Python versions for a `PythonComponent` is **3.10** and **3.11**.
-   Telemetry data is saved in the edge package

Deprecated features:

-   Python **3.8** is removed from supported Python versions.

Fixed issues:

-   Typo in `Boolean` type name

## 2.1.0

New Features:

-   `TensorRTOptimization` class is introduced
-   `ModelConfig` class is updated to include `TensorRTOptimization` instance as `optimization` and to add the config.pbtxt of `GPURuntimeComponent` pipeline step
-   LocalPipelineRunner is able to execute both pipeline configuration and edge packages
-   LocalPipelineRunner gives warnings about output variables so mismatching variable names can be detected
-   `Pipeline.export(...)` method, for directly generating an edge runtime package

Deprecated features:

-   `Pipeline.save(...)` and `deployment.convert_package(...)` should not be used separately, instead `Pipeline.export(...)` should be used.

Fixed issues:

-   Python 3.8.x ≤ 3.8.18 - Multiple Vulnerabilities - 3.8.19
-   Python 3.10.x ≤ 3.10.13 - Multiple Vulnerabilities - 3.10.14
-   Python Package: pip ≤ 23.2.1 - Local Security Bypass Vulnerability - 24.0
-   Python Package: idna < 3.7 - Local Denial of Service Vulnerability - GHSA-jjg7-2v4v-x38h
-   Python Package: onnx ≤ 1.15.0 - Remote Path Traversal Vulnerability - CVE-2024-27318
-   Input variable 'timestamp' is not allowed for Components (Pipeline Steps) as the AI Inference Server always put the message creation timestamp into the payload with the reserved name 'timestamp. Same AssertionError is raised when the user tries to add an input variable with this name.
-   GPURuntime.use_model(..) is able to handle onnx models with different name than 'model.onnx'. The model will be copied into the package with name 'model.onnx'.

## 2.0.0

New features:

-   New GPURuntimeComponent introduced for supporting ONNX models running on GPU enabled AI Inference Server
    -   GPURuntimeComponent can be created with name and version
    -   ONNX model can be added via GPURuntimeComponent.use_model(..)
    -   Default config.pbtxt is created
    -   Specific config.pbtxt can be added via GPURuntimeComponent.use_config(..)
    -   LocalPipelineRunner is able to execute GPURuntimeComponent with
        -   run_component(..), and
        -   run_pipeline(..)
-   The edge package's SHA256 hash is saved in a text file
-   Warning message in case pipeline components use different Python versions
-   Warning message in case no dependencies are added to the pipeline package

Updated features:

-   Component.add_metrics(..) is moved to PythonComponent.add_metrics(..), as GPURuntimeComponent is not able to produce a formatted output.
-   Supported AI Inference Server variable Types are extended with
    -   "UInt8Array", "UInt16Array", "UInt32Array", "UInt64Array",
    -   "Int8Array", "Int16Array", "Int32Array", "Int64Array",
    -   "Float16Array", "Float32Array", "Float64Array",
    -   "ImageSet"

Removed features:

-   Removed function: simaticai.deployment.from_saved_model().
-   Removed module: simaticai.pipeline
-   Removed module: progress.py

Fixed issues:

-   GPU runtime configuration option `max_batch_size` should behave the same for values 0 or 1.

## 1.6.0

New features:

-   Mathilda packages pipeline with image input and output
-   Support source only packages
-   Security fixes
-   Documentation Revamp

## 1.5.0

New features:

-   Version pipeline packages with UUID
-   Binary data type

## 1.4.1

New features:

-   Define custom metrics for a pipeline.
-   Enable adding a description for a pipeline and its elements.
-   Support for binary output from a pipeline or pipeline component.
-   Improved guideline for creating pipeline components.

Deprecated features:

-   Using function simaticai.deployment.from_saved_model() is deprecated. The file format is proprietary and will not be supported in future major versions of AI SDK. Please use explicit calls to add inputs, outputs and the model to the pipeline.

Fixed issues:

-   Unexpected scheme validation error during edge package creation
-   convert_package() includes wheel not supported on AI Inference Server
-   Python 3.8.x ≤ 3.8.15 - Remote Denial of Service Vulnerability - CVE-2022-45061
-   Python Package: certifi 2017.11.05 ≤ 2022.9.24 - Remote Improper Input Validation Vulnerability - GHSA-43fp-rhv2-5gv8

## 1.3.0

New features:

-   Full PEP 508 support in requirements.txt
-   Configure pipeline components to be executed in parallel in multiple instances.

Deprecated features:

-   Using module simaticai.pipeline is deprecated. Please use the source module pipeline provided as part of project template State Identifier.
-   Using AI Model Deployer to convert pipeline configuration packages to edge configuration packages is deprecated.

Fixed issues:

-   Python 3.8.x ≤ 3.8.13 - Open Redirect Vulnerability
-   Python 3.8.x ≤ 3.8.14 - Multiple Vulnerabilities
-   Python Package: joblib ≤ 1.1.0 - Remote Code Execution Vulnerability

## 1.2.0

New features:

-   Define and use pipeline parameters to adapt the behavior of a pipeline at runtime without redeployment.
-   Create Delta Configuration Packages to reduce the upload time for small changes in the Pipeline Package.
-   Streamline the entrypoint of the pipeline with the new entrypoint interface signature.
-   Use input type Object to receive Vision Connector payload via high-performance ZMQ connection.

Fixed issues:

-   `deployment.Component.add_dependencies()` does not duplicate packages in requirements.txt with different letter cases.
-   `deployment.convert_package()` method returns with `pathlib.Path` instead of string representation of the generated zip path.
-   `testing.pipeline_runner.LocalPipelineRunner` and `testing.pipeline_validator.validate_pipeline_dependencies()` can correctly handle components without requirements.txt.

## 1.1.0

New features:

-   Create Edge Configuration Package from a Pipeline Configuration Package.
-   Added generated reference manual.

Fixed issues:

-   Error stack trace is now complete under Windows when using LocalPipelineRunner.
-   deployment.find_dependencies() is not restricted anymore to versioning scheme X.Y.Z
-   LocalPipelineRunner updates pip to required version in the test venv

## 1.0.0

Initial released version.

Main features include:

-   Basic scikit-learn pipeline elements for building machine learning models that process time series of aligned signals.
-   Python API for packaging trained models into pipeline configuration packages to be executed on AI Inference Server.
    -   Supports pipeline configurations with multiple components running in isolated Python environments.
    -   Supports PEP 440 public version identifiers to specify required inference serving environment.
    -   Supports providing required Python packages as wheels.
-   Python API to check availability of required Python packages for AI Inference Server.
-   Python API to drive pipeline configuration packages with test data.
    -   Creates required inference serving environment automatically.
    -   Supports test driving the pipeline as a whole or component-by-component.
    -   Provides a local mock of the logging interface on AI Inference Server.
-   API reference manual.
-   Tested on Linux and Windows.
