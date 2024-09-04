#!/usr/bin/env bash

# Bash strict mode
set -euo pipefail

build_object_path(){
    echo $(echo $DATA_GITBOOK_SITE | sed 's|https://||' | sed 's|http://||' | sed 's|/||g' | sed 's|\.|_|g')/
}

# VARs
UPLOAD_S3=${UPLOAD_S3:-false}
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


upload_files(){
  sync_files "$DATA_SAVE_DIR" "s3://$S3PATH"
}

download_files(){
  sync_files "s3://$S3PATH" "$DATA_SAVE_DIR"
}


function s3_path_exists() {
  aws s3 ls "s3://$S3PATH" > /dev/null 2>&1
}

function create_s3_path() {
    echo "" > emptyfile
    aws s3 cp emptyfile s3://$S3PATH
    rm emptyfile
}

check_create_s3_path(){
    if aws s3api head-bucket --bucket "$S3_BUCKET" 2>/dev/null; then
        echo "버킷이 이미 존재합니다: $S3_BUCKET"
    else
        echo "버킷이 존재하지 않습니다. 새 버킷을 생성합니다: $S3_BUCKET"
        # 버킷 생성
        aws s3api create-bucket --bucket "$S3_BUCKET" --region "$AWS_DEFAULT_REGION" \
            --create-bucket-configuration LocationConstraint="$AWS_DEFAULT_REGION"
        
        if [ $? -eq 0 ]; then
            echo "버킷이 성공적으로 생성되었습니다: $S3_BUCKET"
        else
            echo "버킷 생성에 실패하였습니다: $S3_BUCKET"
        fi
    fi
    # if s3_path_exists; then
    #     echo "패스가 이미 존재합니다: $S3PATH"
    # else
    #     echo "패스가 존재하지 않습니다. 패스를 생성합니다: $S3PATH"
    #     create_s3_path
        
    #     if s3_path_exists; then
    #     echo "패스가 성공적으로 생성되었습니다: $S3PATH"
    #     else
    #     echo "패스 생성에 실패하였습니다: $S3PATH"
    #     fi
    # fi
}

index_files(){
  local option task
  option="-t"
  task="$DATA_TASK"  
  log "poetry run task ${option} ${task}"

  poetry run task ${option} "${task}"

  if [ "$UPLOAD_S3" = "true" ] && [ "$task" != "skip" ] ; then
        if [ -z "$S3_BUCKET" ]; then
            log 'No S3PATH specified' >&2; exit 1
        fi
        mkdir -p "$SYNCDIR" # Make sure directory exists
        check_create_s3_path
        upload_files
  fi  
  # if [ "$task" != "*" ] && [ "$task" != "skip" ] ; then
  #   echo "task type shoule be * or skip"
  # else
  #   if [ "$task" == "*" ]; then
  #       if [ -z "$S3_BUCKET" ]; then
  #           log 'No S3PATH specified' >&2; exit 1
  #       fi
  #       mkdir -p "$SYNCDIR" # Make sure directory exists
  #       check_create_s3_path    
  #       poetry run task ${option} "${task}"
  #       upload_files
  #   fi
  # fi
}

# Main function
main(){
  # Parse command line arguments
  cmd="${1:-index}"
  case "$cmd" in
    index)
      index_files
      ;;
    upload)
      upload_files
      ;;    
    download)
      download_files
      ;;          
    *)
      log "Unknown command: ${cmd}"; exit 1
      ;;
  esac
}

main "$@"