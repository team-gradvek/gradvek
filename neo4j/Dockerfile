FROM neo4j:5.9.0

# Set environment variables
ENV NEO4J_AUTH=neo4j/gradvek1 \
    NEO4J_apoc_import_file_enabled=true \
    NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.* \
    NEO4J_dbms_security_procedures_allowlist=apoc.*,gds.* \
    NEO4J_server_memory_heap_initial__size=4G \
    NEO4J_server_memory_heap_max__size=4G \
    NEO4J_server_memory_pagecache_size=2G \
    NEO4J_PLUGINS='["apoc", "graph-data-science"]'

# Copy data, logs, import, and plugins folders - only plugins folder is in repo
# COPY data /data
# COPY logs /logs
# COPY import /var/lib/neo4j/import
COPY plugins /plugins

# Expose Neo4j ports
EXPOSE 7474 7473 7687

# Start Neo4j
CMD ["neo4j"]
