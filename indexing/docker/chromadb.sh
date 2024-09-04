#!/bin/bash
# Bash strict mode
set -euo pipefail

build_object_path(){
    echo $(echo $DATA_GITBOOK_SITE | sed 's|https://||' | sed 's|http://||' | sed 's|/||g' | sed 's|\.|_|g')/
}

# VARs
S3_BUCKET=${S3_BUCKET:-}
S3PATH=${S3_BUCKET:-}/$(build_object_path)
SYNCDIR="${DATA_SAVE_DIR:-/data}"
EXCLUDE="${EXCLUDE:-}"
SYNCEXTRA="${SYNCEXTRA:-}"
AWS_S3_SSE="${AWS_S3_SSE:-false}"
AWS_S3_SSE_KMS_KEY_ID="${AWS_S3_SSE_KMS_KEY_ID:-}"

if [[ ! -z $EXCLUDE ]]; then 
  EXCLUDE_FLAG="--exclude=$EXCLUDE";
else
  EXCLUDE_FLAG="";
fi

# Log message
log(){
  echo "[$(date "+%Y-%m-%dT%H:%M:%S%z") - $(hostname)] ${*}"
}

sync_files(){
  local src dst sync_cmd
  src="${1:-}"
  dst="${2:-}"


  sync_cmd="$EXCLUDE_FLAG --no-progress --delete --exact-timestamps $SYNCEXTRA";

  if [[ "$AWS_S3_SSE" == 'true' ]] || [[ "$AWS_S3_SSE" == 'aes256' ]]; then
    s3_upload_cmd+=' --sse AES256'
  elif [[ "$AWS_S3_SSE" == 'kms' ]]; then
    s3_upload_cmd+=' --sse aws:kms'
    if [[ -n "$AWS_S3_SSE_KMS_KEY_ID" ]]; then
      s3_upload_cmd+=" --sse-kms-key-id ${AWS_S3_SSE_KMS_KEY_ID}"
    fi
  fi

  if [[ ! "$dst" =~ s3:// ]]; then
    mkdir -p "$dst" # Make sure directory exists
  fi

  log "Sync '${src}' to '${dst}'"
  if ! eval aws s3 sync "$sync_cmd" "$src" "$dst"; then
    log "Could not sync '${src}' to '${dst}'" >&2; exit 1
  fi
}

download_files(){
  sync_files "s3://${S3PATH}store" /chroma/chroma
}

download_files

export IS_PERSISTENT=1
export CHROMA_SERVER_NOFILE=${CHROMA_SERVER_NOFILE:-65536}
args="$@"

if [[ $args =~ ^uvicorn.* ]]; then
    echo "Starting server with args: $(eval echo "$args")"
    echo -e "\033[31mWARNING: Please remove 'uvicorn chromadb.app:app' from your command line arguments. This is now handled by the entrypoint script."
    exec $(eval echo "$args")
else
    echo "Starting 'uvicorn chromadb.app:app' with args: $(eval echo "$args")"
    exec uvicorn chromadb.app:app $(eval echo "$args")
fi