# Code adapted from IRCoT project: https://github.com/StonyBrookNLP/ircot

DOWNLOAD_DIR="download/2wikimultihopqa"

mkdir -p "$DOWNLOAD_DIR"

# download url:https://www.dropbox.com/s/7ep3h8unu2njfxv/data_ids.zip?dl=0
# if [ ! -f "$DOWNLOAD_DIR/2wikimultihopqa.zip" ]; then
#     wget https://www.dropbox.com/s/7ep3h8unu2njfxv/data_ids.zip?dl=0 \
#          -O "$DOWNLOAD_DIR/2wikimultihopqa.zip"
# else
#     echo "$DOWNLOAD_DIR/2wikimultihopqa.zip already exists"
# fi

if [ ! -f "$DOWNLOAD_DIR/2wikimultihop_evaluate_v1.1.py" ]; then
    curl -o "$DOWNLOAD_DIR/2wikimultihop_evaluate_v1.1.py" \
         https://raw.githubusercontent.com/Alab-NII/2wikimultihop/master/2wikimultihop_evaluate_v1.1.py

else
    echo "$DOWNLOAD_DIR/2wikimultihop_evaluate_v1.1.py already exists"
fi

if [ -f "download/2wikimultihopqa.zip" ] && [ ! -d "download/data_ids" ]; then
    unzip "download/2wikimultihopqa.zip" -d "download"
    mv "download/data_ids"/* "download/2wikimultihopqa/"
    rm -rf "download/data_ids"
    rm -rf "download/__MACOSX"
else
    echo "File download/2wikimultihopqa.zip does not exist or download/data_ids already exists"
fi

