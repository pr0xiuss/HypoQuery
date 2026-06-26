-- ENUM TYPES

CREATE TYPE query_type_enum AS ENUM (
    'SELECT',
    'JOIN',
    'INSERT',
    'UPDATE',
    'DELETE',
    'OTHER'
);

CREATE TYPE classifier_route_enum AS ENUM (
    'INDEX_SUGGESTER',
    'JOIN_REORDER',
    'LOCK_ANALYZER'
);

CREATE TYPE pipeline_status_enum AS ENUM (
    'RUNNING',
    'SUCCESS',
    'FAILED',
    'PARTIAL_SUCCESS',
    'VALIDATION_FAILED'
);

CREATE TYPE log_level_enum AS ENUM (
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL'
);

CREATE TYPE remediation_type_enum AS ENUM (
    'INDEX',
    'QUERY_REWRITE',
    'CONFIGURATION',
    'PARTITIONING',
    'MULTIPLE'
);

CREATE TYPE llm_confidence_enum AS ENUM (
    'LOW',
    'MEDIUM',
    'HIGH'
);

CREATE TYPE validation_status_enum AS ENUM (
    'PENDING',
    'PASSED',
    'FAILED',
    'PARTIALLY_PASSED'
);

CREATE TYPE pipeline_node_enum AS ENUM (
    'CLASSIFIER',
    'INDEX_SUGGESTER',
    'JOIN_REORDER',
    'LOCK_ANALYZER',
    'CONTEXT_COMPACTOR',
    'SCHEMA_INJECTOR',
    'HYDE_RETRIEVER',
    'RRF_FUSION',
    'LLM_GENERATOR',
    'VALIDATOR',
    'FEEDBACK_STORE'
);


-- Customers

CREATE TABLE customers (
    customer_id BIGSERIAL PRIMARY KEY,

    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,

    email VARCHAR(255) NOT NULL UNIQUE,

    city VARCHAR(100),
    country VARCHAR(100),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Products

CREATE TABLE products (
    product_id BIGSERIAL PRIMARY KEY,

    product_name VARCHAR(255) NOT NULL,

    category VARCHAR(100),

    description TEXT,

    price NUMERIC(12,2) NOT NULL
        CHECK (price >= 0),

    metadata JSONB,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Orders

CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,

    customer_id BIGINT NOT NULL,

    status VARCHAR(20) NOT NULL
        CHECK (
            status IN (
                'PENDING',
                'PROCESSING',
                'SHIPPED',
                'DELIVERED',
                'CANCELLED'
            )
        ),

    total_amount NUMERIC(12,2) NOT NULL
        CHECK (total_amount >= 0),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
);


-- Order Items

CREATE TABLE order_items (
    order_item_id BIGSERIAL PRIMARY KEY,

    order_id BIGINT NOT NULL,

    product_id BIGINT NOT NULL,

    quantity INTEGER NOT NULL
        CHECK (quantity > 0),

    unit_price NUMERIC(12,2)
        CHECK (unit_price >= 0),

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE RESTRICT
);


-- Reviews

CREATE TABLE reviews (
    review_id BIGSERIAL PRIMARY KEY,

    customer_id BIGINT NOT NULL,

    product_id BIGINT NOT NULL,

    rating INTEGER NOT NULL
        CHECK (rating BETWEEN 1 AND 5),

    review_text TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reviews_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_reviews_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
);


-- Inventory

CREATE TABLE inventory (
    inventory_id BIGSERIAL PRIMARY KEY,

    product_id BIGINT NOT NULL,

    warehouse_name VARCHAR(100) NOT NULL,

    stock_quantity INTEGER NOT NULL
        CHECK (stock_quantity >= 0),

    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
);


-- Product Events

CREATE TABLE product_events (
    event_id BIGSERIAL PRIMARY KEY,

    product_id BIGINT NOT NULL,

    event_type VARCHAR(50) NOT NULL,

    event_metadata JSONB NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_events_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
);


-- Optimization Runs

CREATE TABLE optimization_runs (
    run_id BIGSERIAL PRIMARY KEY,

    trace_id UUID NOT NULL UNIQUE,

    query_signature TEXT NOT NULL,

    query_type query_type_enum NOT NULL,

    classifier_route classifier_route_enum NOT NULL,

    pipeline_status pipeline_status_enum NOT NULL,

    retry_count INTEGER NOT NULL DEFAULT 0,

    original_cost DOUBLE PRECISION,

    optimized_cost DOUBLE PRECISION,

    cost_improvement_percent DOUBLE PRECISION,

    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    completed_at TIMESTAMP
);


-- Pipeline Logs

CREATE TABLE pipeline_logs (
    log_id BIGSERIAL PRIMARY KEY,

    run_id BIGINT NOT NULL,

    service_name VARCHAR(100) NOT NULL,

    node_name VARCHAR(100) NOT NULL,

    log_level log_level_enum NOT NULL,

    message TEXT NOT NULL,

    duration_ms DOUBLE PRECISION,

    payload JSONB,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_pipeline_logs_run
        FOREIGN KEY (run_id)
        REFERENCES optimization_runs(run_id)
        ON DELETE CASCADE
);


-- Optimization Results

CREATE TABLE optimization_results (
    result_id BIGSERIAL PRIMARY KEY,

    run_id BIGINT NOT NULL,

    diagnosis TEXT NOT NULL,

    remediation_type remediation_type_enum NOT NULL,

    recommended_index_sql TEXT,

    rewritten_query TEXT,

    llm_confidence llm_confidence_enum,

    retrieval_score DOUBLE PRECISION,

    faithfulness_score DOUBLE PRECISION,

    validation_status validation_status_enum NOT NULL,

    original_explain_plan JSONB,

    optimized_explain_plan JSONB,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_optimization_results_run
        FOREIGN KEY (run_id)
        REFERENCES optimization_runs(run_id)
        ON DELETE CASCADE
);