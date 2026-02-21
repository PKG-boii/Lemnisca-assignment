#Chunking configuration for different document categories

CHUNKING_CONFIG = {
    "REFERENCE": {"chunk_size": 250, "overlap": 20},
    "GUIDE": {"chunk_size": 400, "overlap": 60},
    "POLICY": {"chunk_size": 500, "overlap": 100},
    "TECHNICAL": {"chunk_size": 400, "overlap": 60},
    "INTERNAL_NOTES": {"chunk_size": 500, "overlap": 100},
    "ROADMAP_RELEASES": {"chunk_size": 350, "overlap": 50},
}
