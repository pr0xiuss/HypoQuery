> **Note:** This document describes the architecture and implementation decisions for Phase 2 of HypoQuery. It focuses on the generic execution platform that powers every workflow within the system. The execution engine is intentionally independent of SQL optimization, allowing future capabilities such as production workload ingestion, observability, validation, Retrieval-Augmented Generation (RAG), and AI-assisted optimization to reuse the same execution infrastructure.


# Phase 2 – Generic Execution Platform

## Objective

The objective of Phase 2 is to transform HypoQuery from a deterministic SQL optimization engine into a reusable execution platform capable of orchestrating complex workflows through a generic pipeline architecture.

While Phase 1 established the deterministic optimization engine responsible for collecting PostgreSQL execution plans, parsing execution trees, analyzing optimization opportunities, and generating structured findings, its execution flow remained tightly coupled to benchmark orchestration.

Phase 2 introduces a clear separation between **how work is executed** and **what work is being performed**.

Rather than embedding optimization logic directly into service orchestration, every workflow is modeled as a pipeline composed of independent execution nodes connected through a generic execution engine. Each node performs a single responsibility while the execution framework coordinates scheduling, state propagation, lifecycle management, error handling, and result generation.

This architectural separation enables multiple workflows to coexist on the same execution platform. SQL optimization becomes the first pipeline implemented on top of the engine, while future capabilities—including production workload ingestion, PostgreSQL telemetry collection, recommendation validation, Retrieval-Augmented Generation (RAG), and AI-assisted optimization—can be introduced as additional pipelines without requiring changes to the execution framework itself.

By abstracting execution into reusable contracts, pipelines, queues, workers, and dispatchers, Phase 2 establishes the infrastructure required for scalable, observable, and extensible workflow orchestration throughout the remainder of the project.

The execution platform developed during this phase serves as the architectural foundation upon which every subsequent phase of HypoQuery is built.

## Goals

The primary goal of Phase 2 is to establish a generic execution platform capable of orchestrating complex workflows independently of their underlying business logic. Instead of implementing workflow-specific execution mechanisms, the platform introduces reusable execution primitives that allow multiple pipelines to share the same runtime infrastructure.

The objectives achieved during this phase include:

* Designing immutable and mutable execution contracts to clearly separate execution metadata from runtime state.
* Developing a generic pipeline engine capable of executing directed workflows through reusable pipeline nodes.
* Implementing a configurable pipeline builder responsible for constructing validated pipeline instances.
* Creating a node registry to support dynamic registration and resolution of execution nodes.
* Introducing a reusable queue abstraction to decouple workload ingestion from execution.
* Building a worker framework responsible for processing queued pipeline executions.
* Implementing a dispatcher that assigns queued workloads to available workers using a scheduling strategy.
* Integrating the deterministic SQL optimization workflow into the generic execution framework by representing each optimization stage as an independent pipeline node.
* Developing a benchmark ingestion framework capable of transforming SQL benchmark queries into executable pipeline jobs.
* Establishing a standardized execution lifecycle consisting of workload collection, queueing, dispatching, execution, and result generation.
* Providing runtime execution metrics and structured execution results for every pipeline execution.
* Validating the execution platform through comprehensive unit tests, integration tests, and successful end-to-end execution of the complete benchmark workload.

At the conclusion of Phase 2, HypoQuery evolves from a standalone SQL optimization engine into a reusable execution platform capable of supporting multiple independent workflows while maintaining low coupling, extensibility, and clear architectural separation between execution infrastructure and business logic.

## Scope

Phase 2 focuses exclusively on the development of a generic execution platform that serves as the foundation for all future workflows within HypoQuery. The scope of this phase is intentionally limited to execution infrastructure and workflow orchestration, without introducing production database telemetry, recommendation validation, or AI-assisted optimization.

The implementation includes a reusable execution framework composed of execution contracts, pipeline definitions, pipeline builders, node registries, queue abstractions, worker management, dispatching strategies, and a generic pipeline executor. These components collectively provide a standardized mechanism for executing any workflow represented as a sequence of independent pipeline nodes.

To validate the execution platform, the deterministic SQL optimization workflow developed during Phase 1 is migrated into the new architecture. Each optimization stage—including SQL normalization, query fingerprint generation, execution plan collection, execution plan parsing, optimization analysis, and result persistence—is implemented as an independent pipeline node executing under the control of the generic execution engine.

A benchmark ingestion framework is also introduced to transform benchmark SQL queries into executable pipeline jobs. These jobs are collected, queued, dispatched to workers, executed through the optimization pipeline, and returned as standardized pipeline results. This demonstrates that the execution framework is capable of orchestrating complete end-to-end workflows without embedding workflow-specific logic within the execution infrastructure.

Comprehensive unit tests and integration tests are included within the scope of this phase to verify the correctness of the execution engine, queue system, worker framework, optimization pipeline, and benchmark execution workflow.

The following capabilities are intentionally excluded from Phase 2 and deferred to subsequent phases:

* Production observability, including structured logging, metrics aggregation, distributed tracing, execution timelines, and failure analytics.
* Live PostgreSQL workload ingestion using `pg_stat_statements`.
* Automatic execution plan collection using `auto_explain`.
* HypoPG-based validation and recommendation scoring.
* Knowledge graph construction, Retrieval-Augmented Generation (RAG), and AI-assisted recommendation generation.
* Distributed execution using Redis-backed queues and multiple worker processes.
* API endpoints, authentication, dashboards, WebSocket communication, and other application-layer components.

By explicitly limiting the scope to execution infrastructure, Phase 2 establishes a stable and reusable architectural foundation upon which all remaining phases of HypoQuery are built.


# Architecture Overview

Phase 2 introduces a layered execution architecture that separates workflow orchestration from business logic. Rather than embedding execution responsibilities within individual optimization services, every workflow is executed through a generic pipeline engine composed of reusable infrastructure components.

The execution process begins with workload ingestion. A collector is responsible for discovering executable workloads and converting them into standardized `PipelineExecution` objects containing the immutable execution context, mutable execution state, and job metadata required by the execution engine. These executions are then placed into a queue, allowing workload generation and execution to remain completely decoupled.

Workers continuously retrieve queued executions through the dispatcher, which determines the next available worker according to the configured scheduling strategy. Each worker delegates execution to the generic `PipelineExecutor`, ensuring that workers remain responsible only for processing jobs rather than implementing workflow-specific logic.

The `PipelineExecutor` serves as the central orchestration component of the execution platform. It manages the complete execution lifecycle, including pipeline initialization, node execution, lifecycle hooks, state propagation, error handling, execution metrics, and result generation. The executor is completely unaware of the underlying workflow and interacts only with generic execution contracts and registered pipeline nodes.

Business logic is implemented entirely within independent pipeline nodes. Each node performs a single responsibility and progressively enriches the mutable pipeline state before passing execution to the next node. Since nodes remain isolated from one another, individual execution stages can be added, removed, reordered, or replaced without modifying the execution engine itself.

The first workflow implemented using this architecture is the SQL optimization pipeline. Benchmark queries are transformed into pipeline executions, processed through the execution engine, and passed sequentially through normalization, fingerprint generation, execution plan collection, execution plan parsing, optimization analysis, and result persistence before producing a standardized `PipelineResult`.

The resulting architecture establishes a clear separation between infrastructure and domain logic. Execution infrastructure—including pipelines, queues, workers, dispatchers, and execution contracts—forms a reusable platform capable of supporting multiple independent workflows, while optimization logic becomes a single implementation built upon that platform.

The high-level execution flow is illustrated below:

```text
                        Benchmark Queries
                               │
                               ▼
                     Benchmark Collector
                               │
                               ▼
                     PipelineExecution
                               │
                               ▼
                        In-Memory Queue
                               │
                               ▼
                          Dispatcher
                               │
                               ▼
                            Worker
                               │
                               ▼
                      PipelineExecutor
                               │
                               ▼
                    Optimization Pipeline
                               │
     ┌──────────────┬──────────────┬
     ▼              ▼              ▼
 Normalize → Fingerprint → Explain Collect
                              │
                              ▼
                       Explain Parse
                              │
                              ▼
                       Plan Analyze
                              │
                              ▼
                       Persist Result
                              │
                              ▼
                       PipelineResult
```

This layered architecture serves as the execution backbone of HypoQuery and provides the reusable infrastructure upon which future capabilities—including production observability, live PostgreSQL workload ingestion, recommendation validation, and Retrieval-Augmented Generation (RAG)—will be implemented.


# Execution Contracts

The execution platform is built upon a collection of reusable contracts that establish a standardized interface between every component participating in pipeline execution. These contracts define the information exchanged throughout the execution lifecycle while ensuring that execution infrastructure remains independent of workflow-specific business logic.

A fundamental architectural decision introduced in Phase 2 is the separation of execution data into **immutable execution context** and **mutable execution state**.

The immutable execution context describes **what** is being processed. It contains metadata that uniquely identifies an execution and remains constant throughout the lifetime of the pipeline. Examples include the query fingerprint, target database, schema information, execution metadata, and other contextual information required by downstream nodes. Since this information never changes during execution, it can be safely shared across every stage of the pipeline without introducing synchronization concerns or accidental modification.

In contrast, the mutable execution state represents **what has been produced** during pipeline execution. Rather than creating new objects after every processing stage, each pipeline node progressively enriches a shared execution state with additional information generated during execution. As the pipeline advances, new artifacts, execution plans, optimization findings, metrics, and errors are accumulated within the state object until the workflow completes.

To encapsulate an entire execution, the platform introduces the `PipelineExecution` contract. This object combines the immutable execution context, mutable execution state, and pipeline job metadata into a single unit of work that flows through the execution engine. Every component—including queues, workers, dispatchers, pipeline executors, and pipeline nodes—operates exclusively on this standardized execution object.

Upon completion of a workflow, the execution engine produces a `PipelineResult`, providing a consistent representation of the overall execution outcome. The result includes pipeline status, execution timing, summary information, and a reference to the completed execution state, allowing downstream consumers to inspect the artifacts and metrics produced during processing.

Individual pipeline nodes communicate their local execution outcome through the `NodeResult` contract. Rather than exposing implementation-specific behavior, each node reports standardized execution statuses such as successful completion, failure, or skipped execution. This consistent contract enables the execution engine to manage node lifecycles without requiring knowledge of the underlying business logic.

Collectively, these execution contracts establish a clear boundary between execution infrastructure and domain-specific processing. Pipelines remain capable of executing arbitrary workflows while every infrastructure component communicates through a common, strongly defined contract, significantly improving extensibility, maintainability, and long-term scalability of the execution platform.


# Pipeline Engine

The Pipeline Engine is the core orchestration layer of the execution platform. It is responsible for transforming a collection of independent processing nodes into a validated executable workflow while remaining completely agnostic to the business logic implemented by those nodes.

Rather than hardcoding execution logic for a specific workflow, the engine models every workflow as a directed sequence of reusable pipeline nodes connected through an immutable pipeline definition. Each node performs a single responsibility and communicates exclusively through the shared `PipelineExecution` object, allowing complex workflows to be assembled without introducing dependencies between individual processing stages.

Pipeline construction begins with the `PipelineDefinition`, which provides a declarative description of the workflow. The definition specifies the pipeline identifier, version, participating nodes, execution graph, and entry point. By separating pipeline definition from execution, workflows become immutable specifications that can be validated before execution begins.

The `PipelineBuilder` is responsible for transforming a pipeline definition into an executable pipeline instance. During construction, the builder validates the pipeline graph, verifies that all referenced nodes have been registered, confirms the existence of the entry node, and ensures that all graph edges reference valid destinations. This validation phase prevents invalid workflows from reaching runtime and shifts structural errors to pipeline construction rather than execution.

Pipeline nodes are managed through the `NodeRegistry`, which acts as a centralized registry for all available node implementations. Instead of creating node instances directly within the execution engine, the builder resolves registered nodes through the registry, promoting loose coupling and allowing multiple pipelines to reuse the same node implementations.

Once constructed, the `Pipeline` represents the runtime view of a validated workflow. It provides access to registered nodes, maintains the execution graph, and determines the next node to execute based on the pipeline definition. The pipeline itself contains no business logic; its responsibility is limited to representing workflow structure and execution order.

Execution is coordinated by the `PipelineExecutor`, which serves as the central orchestration component of the platform. For each `PipelineExecution`, the executor initializes execution metrics, traverses the pipeline beginning at the configured entry node, invokes node lifecycle hooks, executes each pipeline node, propagates execution state, records execution metrics, handles runtime failures, and ultimately produces a standardized `PipelineResult`.

Throughout execution, the executor remains completely independent of workflow-specific processing. It does not understand SQL optimization, PostgreSQL execution plans, or optimization findings. Its sole responsibility is coordinating execution according to the pipeline definition while ensuring consistent lifecycle management, state propagation, error handling, and result generation for every workflow executed on the platform.

This separation between pipeline definition, pipeline construction, runtime orchestration, and business logic establishes a highly extensible execution model. New workflows can be introduced simply by registering additional pipeline nodes and defining new pipeline graphs, without requiring any modification to the execution engine itself. Consequently, the optimization pipeline implemented in Phase 2 becomes the first consumer of a generic execution framework capable of supporting future workflows such as observability, PostgreSQL telemetry collection, recommendation validation, and Retrieval-Augmented Generation (RAG).


# Queue and Worker Framework

The execution platform decouples workload generation from workload execution through a generic queue and worker framework. Rather than executing pipeline jobs immediately after they are created, workloads are first transformed into standardized execution objects and placed into a queue, allowing collection, scheduling, and execution to operate as independent responsibilities.

At the core of this layer is the `BaseQueue` abstraction, which defines a common contract for queue implementations regardless of their underlying storage mechanism. The execution engine interacts only with this abstraction, enabling future queue implementations to be introduced without modifying workers or pipeline execution logic. During Phase 2, an in-memory FIFO queue is implemented to support benchmark execution and simplify local development while establishing the interface for future distributed queue backends.

Each queued item is represented by a `QueueEntry`, which encapsulates a single `PipelineExecution`. This design ensures that the queue remains completely unaware of workflow-specific details and is responsible only for storing and delivering executable work units.

Execution of queued workloads is performed by the worker framework. A `Worker` retrieves the next available execution from the queue and delegates processing to the generic `PipelineExecutor`. Workers intentionally contain no business logic and perform no optimization-specific processing. Their sole responsibility is coordinating the movement of work between the queue and the execution engine.

To support scalable execution, workers are managed through a `WorkerPool`, which maintains the collection of available workers within the system. Rather than coupling workload assignment to individual workers, scheduling decisions are delegated to the `Dispatcher`. During Phase 2, the dispatcher implements a simple Round Robin scheduling strategy, distributing pipeline executions evenly across the available workers. This scheduling policy is intentionally isolated within the dispatcher, allowing future load-balancing strategies—such as least-loaded scheduling, weighted dispatching, or priority-based execution—to be introduced without affecting workers or the execution engine.

This separation of concerns results in a layered execution model in which collectors generate work, queues store work, dispatchers assign work, workers process work, and the pipeline executor performs orchestration. Each component has a clearly defined responsibility and communicates exclusively through standardized execution contracts.

By introducing the queue and worker framework as reusable infrastructure rather than optimization-specific services, Phase 2 establishes the foundation for future distributed execution. Subsequent phases will replace the in-memory queue with a Redis-backed implementation and extend the worker framework to support multiple concurrent worker processes while preserving the same execution contracts and orchestration logic.


# Optimization Pipeline Integration

To validate the generic execution platform developed during Phase 2, the deterministic SQL optimization engine implemented in Phase 1 was refactored into an executable pipeline composed of independent processing nodes. Rather than embedding optimization logic directly within orchestration services, each stage of the optimization workflow was transformed into an isolated pipeline node responsible for performing a single well-defined task.

The optimization pipeline serves as the first production workflow executed by the generic execution engine. It demonstrates that complex domain-specific logic can be decomposed into reusable execution stages while remaining completely independent of the underlying execution infrastructure.

Execution begins with the **Normalize Node**, which standardizes the input SQL query to eliminate formatting inconsistencies and produce a canonical representation suitable for downstream processing. The normalized query is stored within the execution state and becomes the basis for subsequent analysis.

The **Fingerprint Node** generates a deterministic fingerprint for the normalized query. This fingerprint uniquely identifies the logical structure of the SQL statement and enables future capabilities such as workload aggregation, historical analysis, duplicate detection, and execution tracking.

Once the query has been normalized and identified, the **Explain Collect Node** interacts with PostgreSQL to execute an `EXPLAIN ANALYZE` statement with detailed execution statistics. The resulting execution plan is collected in JSON format and attached to the pipeline state for further processing.

The raw execution plan is then transformed by the **Explain Parse Node**, which converts PostgreSQL's hierarchical JSON output into a strongly typed execution plan model. This abstraction provides a consistent representation of execution plans, allowing subsequent analysis stages to remain independent of PostgreSQL's native output format.

The parsed execution plan is analyzed by the **Plan Analyze Node**, which applies the deterministic optimization rules developed during Phase 1. The analyzer traverses the execution tree, evaluates each node against the registered optimization rules, aggregates detected issues, and produces a collection of optimization findings representing potential performance improvements.

Finally, the **Persist Result Node** prepares the execution results for persistence by consolidating the execution plan, optimization findings, execution metadata, and pipeline metrics into standardized result models. Although persistence remains intentionally lightweight during Phase 2, the node establishes a dedicated extension point for future storage, reporting, and observability capabilities.

The complete optimization workflow executed during Phase 2 is illustrated below:

```text
                    SQL Query
                        │
                        ▼
                Normalize Node
                        │
                        ▼
              Fingerprint Node
                        │
                        ▼
            Explain Collect Node
                        │
                        ▼
             Explain Parse Node
                        │
                        ▼
              Plan Analyze Node
                        │
                        ▼
             Persist Result Node
                        │
                        ▼
                 Pipeline Result
```

By expressing the SQL optimization workflow as a pipeline, Phase 2 successfully separates execution infrastructure from optimization logic. The execution engine remains entirely unaware of PostgreSQL, SQL queries, execution plans, or optimization rules, while the optimization pipeline becomes a reusable consumer of the generic execution framework. This architectural separation enables future workflows—including production workload ingestion, recommendation validation, PostgreSQL telemetry collection, and AI-assisted optimization—to be implemented using the same execution platform without requiring modifications to the core execution engine.


# Benchmark Ingestion Framework

To validate the execution platform under realistic operating conditions, Phase 2 introduces a benchmark ingestion framework responsible for transforming benchmark SQL workloads into executable pipeline jobs. Rather than invoking the optimization pipeline directly, the ingestion layer models benchmark queries as standardized execution units that follow the same lifecycle as any future production workload.

The ingestion process begins with the `QueryCatalog`, which serves as the centralized repository of benchmark SQL queries. The catalog recursively scans the benchmark query directories, parses metadata associated with each SQL file, and constructs strongly typed query models containing identifiers, categories, expected optimization issues, descriptions, and SQL statements. This separation allows benchmark workloads to be managed independently of the execution engine while providing a consistent interface for workload discovery.

Once benchmark queries have been loaded, the `BenchmarkCollector` transforms each query into a `PipelineExecution`. During this process, immutable execution metadata is initialized, pipeline job information is created, and the original query is attached to the mutable execution state. At this stage, benchmark queries become generic execution objects, allowing the remainder of the execution platform to operate without knowledge of their origin.

Execution orchestration is coordinated by the `IngestionService`, which acts as the entry point into the execution platform. The service collects all available pipeline executions from the configured collector, enqueues each execution into the queue abstraction, continuously requests available workers from the dispatcher, and delegates execution to the worker framework. Throughout this process, the ingestion layer remains completely independent of optimization logic, interacting only with generic execution contracts and pipeline infrastructure.

The benchmark execution workflow is initiated through the `run_benchmark` entry point, which composes the required infrastructure components, including the query catalog, benchmark collector, queue, dispatcher, workers, pipeline builder, and execution engine. Once initialized, every benchmark query follows the complete execution lifecycle from workload collection to pipeline execution before producing a standardized `PipelineResult`.

The benchmark ingestion workflow is illustrated below:

```text
                  Benchmark SQL Files
                           │
                           ▼
                    QueryCatalog
                           │
                           ▼
                  BenchmarkCollector
                           │
                           ▼
                  PipelineExecution
                           │
                           ▼
                    InMemoryQueue
                           │
                           ▼
                      Dispatcher
                           │
                           ▼
                         Worker
                           │
                           ▼
                   PipelineExecutor
                           │
                           ▼
                 Optimization Pipeline
                           │
                           ▼
                   PipelineResult
```

Although the current implementation focuses exclusively on benchmark workloads, the ingestion framework was intentionally designed around generic collector abstractions. This design allows future collectors—such as PostgreSQL telemetry collectors, `pg_stat_statements` collectors, live workload collectors, scheduled background collectors, or external API integrations—to produce identical `PipelineExecution` objects without requiring any modifications to the execution engine, queue framework, or optimization pipeline.

By separating workload collection from execution, the ingestion framework establishes a reusable foundation for future production-grade workload processing while demonstrating the flexibility and extensibility of the generic execution platform developed during Phase 2.


# Design Patterns and Architectural Principles

The execution platform developed during Phase 2 emphasizes modularity, extensibility, and separation of concerns through the application of established software engineering principles and design patterns. Rather than optimizing solely for the current SQL optimization workflow, the architecture was designed to support future workflows without requiring modifications to the execution infrastructure.

The **Pipeline Pattern** forms the foundation of the execution platform. Every workflow is represented as an ordered sequence of independent processing nodes, each responsible for a single stage of computation. This pattern promotes composability by allowing workflows to be assembled, extended, or modified through pipeline definitions rather than changes to the execution engine itself.

Pipeline construction is implemented using the **Builder Pattern**. The `PipelineBuilder` is responsible for validating pipeline definitions, resolving registered nodes, verifying execution graphs, and producing executable pipeline instances. Separating construction from execution ensures that structural validation occurs before runtime, reducing the likelihood of execution-time failures caused by invalid pipeline configurations.

The **Registry Pattern** is employed through the `NodeRegistry`, which maintains a centralized collection of reusable pipeline nodes. Instead of directly instantiating execution stages, pipelines resolve node implementations through the registry, enabling node reuse across multiple workflows while reducing coupling between pipeline definitions and node implementations.

The optimization analyzer continues to leverage the **Strategy Pattern** introduced during Phase 1. Individual optimization rules encapsulate independent detection logic behind a common interface, allowing new optimization strategies to be introduced without modifying the analyzer responsible for traversing execution plans.

Configuration management follows the **Factory Pattern** through the settings factory and dependency initialization components. Centralizing configuration creation improves maintainability and simplifies future support for multiple deployment environments.

The execution lifecycle implemented by `PipelineNode` follows the **Template Method Pattern**. Each node inherits a standardized execution lifecycle—including initialization, execution, cleanup, and error handling—while providing its own implementation of the business-specific execution logic. This guarantees consistent behavior across all pipeline stages while allowing nodes to remain independently extensible.

The overall system architecture follows a **Layered Architecture**, separating workload ingestion, execution infrastructure, optimization logic, repositories, and shared infrastructure into distinct layers with clearly defined responsibilities. Each layer communicates through explicit contracts rather than implementation-specific dependencies, improving maintainability and long-term scalability.

Beyond classical design patterns, the execution platform was designed around the principles of low coupling and high cohesion. Infrastructure components such as queues, workers, dispatchers, pipeline builders, and executors remain completely independent of SQL optimization, while optimization nodes remain unaware of execution scheduling, queue management, and worker orchestration. This strict separation ensures that future workflows—including production workload ingestion, PostgreSQL telemetry collection, recommendation validation, and AI-assisted optimization—can be implemented by composing existing infrastructure rather than modifying it.

Collectively, these design decisions establish a reusable execution platform that prioritizes extensibility, maintainability, and architectural consistency, providing a stable foundation for every subsequent phase of HypoQuery.


# Testing and Validation

A primary objective of Phase 2 was not only to implement a generic execution platform but also to demonstrate its correctness through comprehensive validation. Every major component introduced during this phase was accompanied by dedicated unit tests and integration tests to verify both individual behavior and complete end-to-end workflow execution.

The execution framework was validated through isolated unit tests covering the core infrastructure components responsible for pipeline construction and execution. The `PipelineBuilder` was tested to ensure correct validation of pipeline definitions, node registration, execution graphs, and entry node configuration. The `PipelineExecutor` was verified to correctly execute registered pipeline nodes, propagate execution state, manage lifecycle hooks, collect execution metrics, and generate standardized pipeline results. The `NodeRegistry` was validated to ensure proper registration, lookup, and reuse of pipeline node implementations.

The queue and worker infrastructure were independently tested to verify workload management. Unit tests confirmed the correctness of the in-memory queue implementation, queue operations, worker processing, worker pool management, and dispatcher scheduling. These tests ensure that workload collection, scheduling, and execution remain decoupled while preserving deterministic execution behavior.

Following validation of individual infrastructure components, comprehensive integration tests were developed for the optimization pipeline. These tests execute the complete pipeline using the generic execution engine and verify that pipeline execution completes successfully, execution state is progressively enriched by each pipeline node, and optimization findings are generated as expected. By validating the complete execution lifecycle, these tests demonstrate that the generic execution framework correctly orchestrates domain-specific workflows without requiring workflow-specific execution logic.

The benchmark ingestion framework provides an additional level of end-to-end validation by executing the complete benchmark workload through the production execution path. During benchmark execution, SQL queries are collected from the query catalog, transformed into standardized pipeline executions, enqueued, dispatched to workers, executed through the optimization pipeline, and returned as standardized pipeline results. Successful execution of the benchmark workload confirms the correct interaction between collectors, queues, dispatchers, workers, pipeline execution, and optimization nodes.

To aid runtime verification during development, the execution engine also records structured execution events and execution metrics throughout pipeline execution. Pipeline start and completion events, node execution events, execution durations, and failure information provide immediate visibility into workflow execution while establishing the foundation for the production observability platform planned for subsequent phases.

Through this multi-layered validation strategy—including unit testing, integration testing, benchmark execution, and runtime verification—the execution platform developed during Phase 2 demonstrates correctness across both individual infrastructure components and complete workflow orchestration. This comprehensive validation provides confidence that the generic execution framework can serve as the stable architectural foundation for future capabilities such as production observability, live PostgreSQL workload ingestion, recommendation validation, and AI-assisted optimization.


# SOLID Principles

The execution platform was designed with the objective of maintaining low coupling, high cohesion, and long-term extensibility. Throughout Phase 2, the SOLID design principles guided the decomposition of responsibilities across the execution infrastructure.

**Single Responsibility Principle (SRP)** is observed by assigning each component a clearly defined responsibility. Pipeline nodes focus exclusively on business logic, the `PipelineExecutor` manages execution orchestration, the `Dispatcher` determines worker assignment, the queue manages workload storage, and workers coordinate execution without containing optimization logic.

**Open/Closed Principle (OCP)** is achieved by designing the execution framework around extensible abstractions. New pipeline nodes, execution pipelines, queue implementations, worker scheduling strategies, or optimization rules can be introduced without modifying existing infrastructure components.

**Liskov Substitution Principle (LSP)** is maintained through the use of common contracts and abstract base classes. Any implementation of `PipelineNode`, `BaseQueue`, or `BaseWorker` can replace another implementation while preserving the behavior expected by the execution engine.

**Interface Segregation Principle (ISP)** is reflected in the separation of execution responsibilities into focused contracts. Rather than exposing large interfaces, each component depends only on the operations required for its specific responsibility, reducing unnecessary coupling between subsystems.

**Dependency Inversion Principle (DIP)** is applied by ensuring that high-level orchestration components depend on abstractions rather than concrete implementations. The execution engine interacts with pipeline nodes, queues, workers, and collectors through well-defined contracts, allowing implementation details to evolve independently of the execution framework.

Collectively, these principles establish a modular execution platform capable of supporting future workflows while minimizing the impact of architectural changes.


# Current Limitations and Future Work

While Phase 2 establishes a generic execution platform capable of orchestrating reusable workflows, several capabilities have been intentionally deferred to subsequent phases in order to maintain a clear separation of architectural concerns.

The current implementation executes benchmark workloads through an in-memory queue and local worker infrastructure. Production workload ingestion using PostgreSQL telemetry sources such as `pg_stat_statements` will be introduced in the next phase, allowing HypoQuery to analyze live database workloads rather than predefined benchmark queries.

Execution observability currently consists of runtime logging and execution metrics recorded during pipeline execution. A dedicated observability engine—including structured logging, metrics aggregation, distributed tracing, execution timelines, failure analytics, and Elasticsearch integration—will extend this foundation in the following phase.

The optimization pipeline presently relies on deterministic rule-based analysis developed during Phase 1. Future phases will introduce recommendation validation through HypoPG, empirical performance comparison, confidence scoring, and eventually Retrieval-Augmented Generation (RAG) to enrich deterministic recommendations with historical knowledge and AI-assisted explanations.

By intentionally limiting Phase 2 to execution infrastructure, the project establishes a stable architectural foundation upon which future observability, PostgreSQL integration, validation, and AI-assisted optimization capabilities can be implemented without requiring modifications to the core execution engine.


# Conclusion

Phase 2 represents the architectural transformation of HypoQuery from a standalone SQL optimization engine into a reusable execution platform capable of orchestrating complex workflows through a generic pipeline architecture.

The execution framework introduces standardized execution contracts, reusable pipeline definitions, queue abstractions, worker management, dispatching strategies, and a generic pipeline executor while remaining completely independent of workflow-specific business logic. The deterministic SQL optimization workflow developed during Phase 1 has been successfully integrated into this execution platform as the first production pipeline, demonstrating the flexibility and extensibility of the underlying architecture.

Comprehensive unit testing, integration testing, and successful execution of the complete benchmark workload validate the correctness of the execution framework and establish confidence in its ability to support future capabilities.

With the execution platform now complete, subsequent phases can focus on extending the system rather than redesigning it. Future work will build upon this foundation by introducing production observability, live PostgreSQL workload ingestion, recommendation validation, knowledge-driven retrieval, and AI-assisted optimization while preserving the execution infrastructure established during Phase 2.

The architecture implemented during this phase serves as the execution backbone of HypoQuery and provides the reusable platform upon which all remaining project components will be constructed.