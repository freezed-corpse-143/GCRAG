

DOWNLOAD_DIR="download"

mkdir -p "$DOWNLOAD_DIR"

if [ ! -f "$DOWNLOAD_DIR/elasticsearch-7.16.3-linux-x86_64.tar.gz" ]; then
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.16.3-linux-x86_64.tar.gz \
        -O "$DOWNLOAD_DIR/elasticsearch-7.16.3-linux-x86_64.tar.gz"
    tar -xzf "$DOWNLOAD_DIR/elasticsearch-7.16.3-linux-x86_64.tar.gz" -C retriever
else
    echo "$DOWNLOAD_DIR/elasticsearch-7.16.3-linux-x86_64.tar.gz already exists"
fi