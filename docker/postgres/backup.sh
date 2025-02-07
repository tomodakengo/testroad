#!/bin/bash

# バックアップ設定
BACKUP_DIR="/backups"
BACKUP_NAME="testroad_db_$(date +%Y%m%d_%H%M%S).sql"
BACKUP_RETENTION_DAYS=7

# バックアップの実行
pg_dump -U testroad_user -d testroad > "$BACKUP_DIR/$BACKUP_NAME"

# バックアップの圧縮
gzip "$BACKUP_DIR/$BACKUP_NAME"

# 古いバックアップの削除
find "$BACKUP_DIR" -name "testroad_db_*.sql.gz" -type f -mtime +$BACKUP_RETENTION_DAYS -delete

echo "バックアップが完了しました: $BACKUP_NAME.gz" 