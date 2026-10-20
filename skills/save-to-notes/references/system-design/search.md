# Search

Ask first whether the database you already run can answer the query with one of its own indexes. Every separate search system is a second copy of the data that you must keep in sync.

## Postgres search first

Use Postgres while the data fits one database and you want no sync pipeline: a `tsvector` column with a GIN index for words, `pg_trgm` for typos and `LIKE '%word%'`, and PostGIS for places. Do not mix them up. Trigram matching scores how alike two strings look but neither stems words nor ranks by relevance, and a plain B-tree cannot serve a leading wildcard, so the query reads every row. Move to a search engine only when load or relevance tuning outgrows it.

## A search engine as a derived index

Reach for an engine such as Elasticsearch when you need ranking, facets, fuzzy matching and filters in one query over large data. Below about 100k documents, or when the data rarely changes, query the primary store, because a plain query is fast enough and needs no sync. Never make the engine your database, because it is not transactional and lags. Map only the fields you search, since each one costs memory. An update rewrites the document, so a sort key that changes constantly, like a like count, belongs in the index only at milestones, with each query over-fetching and re-ranking by the fresh value. For deep paging, pass the last hit's sort values with a unique tiebreaker such as the ID, because offset paging re-sorts everything before the page. General cursor rules live in [API and edge](api-and-edge.md).

## Sync the index with CDC or an outbox

Any derived index should follow the database's own change log through a stream, so it can only show what the database stored. Use a transactional outbox instead when the consumer must know why something changed (see [queues and streams](queues-and-streams.md)). Never dual-write from app code, because when the second write fails after the first, nothing repairs the gap. Accept some lag, and keep a way to rebuild the index from scratch.

## A hand-built inverted index

When no engine is allowed, keep a word-to-IDs map yourself in a key-value store, with one structure per sort order. Each order doubles storage. Common words make huge lists and every new post writes many keys, so cap the lists and index only the word pairs people actually search, found with a [Count-Min Sketch](counting-and-aggregation.md#count-min-sketch-and-top-k). Matching against many fixed words in memory is a trie instead, in [code structure](code-structure.md).

## Cell keys for moving points

Turn each location into a grid cell ID in an ordinary index when points move constantly, so a move is one cheap overwrite. Geohash prefixes range-scan but stretch near the poles, and H3 hexagons suit rings yet do not range-scan. Always query the cell plus its neighbours, then filter by exact distance, or near points across an edge go missing. With only a thousand or so items, a full scan beats any index.

## Spatial trees for shapes

Use an R-tree or quadtree (PostGIS on GiST by default) for real geometry and containment, or for stable points that bunch up. Tree writes are costly, so moving points belong in cell keys. A quadtree splits deepest where points bunch, while an R-tree stays balanced. For named regions, store at write time which regions each place sits in, and query them as keywords.

## Vector search in a store you run

Start semantic search with an extension in a store you run, such as pgvector, and return IDs you look up in the primary store. A dedicated vector database earns its cost only past about 100 million vectors, a rough rule of thumb, because below that the store you run is cheaper and needs no sync. HNSW is the default, at about twice the memory of the raw vectors, and recall near 95% is the target because 99% costs real latency. Record which model made each vector, since a new model means re-embedding everything. When queries mix exact codes with meaning, run keyword and vector search together and merge the lists, because each misses what the other finds. Ranking pipelines live in [ML systems](ml-systems.md).
