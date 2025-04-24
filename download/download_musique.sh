# Configuration
DOWNLOAD_DIR="download"

mkdir -p "$DOWNLOAD_DIR"

if [ ! -d "$DOWNLOAD_DIR/musique" ]; then
    cd "$DOWNLOAD_DIR"
    git clone https://github.com/StonyBrookNLP/musique.git
    cd ..
else
    echo "DOWNLOAD_DIR/musique already exists"
fi

if [ ! -f "$DOWNLOAD_DIR/musique_v1.0.zip" ]; then
    gdown "1tGdADlNjWFaHLeZZGShh2IRcpO6Lv24h&confirm=t" -O "$DOWNLOAD_DIR/musique_v1.0.zip"
    unzip "download/musique_v1.0.zip" -d "download"
    mv "download/data"/* "download/musique/"
    rm -rf "download/data"
else
    echo "$DOWNLOAD_DIR/musique_v1.0.zip already exists"
fi