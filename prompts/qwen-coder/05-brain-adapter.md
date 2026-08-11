# Prompt 05: The Brain Adapter

Create an adapter for The Brain app.

Do not assume a live API exists.

Start with import/export logic based on exported thoughts, tags, and relationships.

Create:

- adapters/brain/tag_mapping.yaml
- adapters/brain/importer.py
- adapters/brain/exporter.py

The adapter should map:

- thought types to node types
- stage tags to workflow stage
- priority tags to Eisenhower quadrant
- cognitive load tags to cognitive load
- role tags to role links
- goal tags to goal links
- initiative tags to initiative links

The importer should produce Node and Link objects that can be saved into the core repository.
