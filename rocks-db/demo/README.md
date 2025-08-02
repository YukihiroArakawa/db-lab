# RocksDB Demo Application

RocksDBの挙動を確認するためのKotlinラッパーアプリケーションです。Spring Bootベースで、WebインターフェースとREST APIを提供します。

## 🚀 特徴

- **RocksDBの基本操作**: PUT、GET、DELETE操作
- **バッチ処理**: 複数のキー・バリューペアを一度に処理
- **プレフィックス検索**: 指定したプレフィックスでキーを検索
- **パフォーマンステスト**: 大量データの書き込み性能測定
- **統計情報**: データベースの詳細な統計とメトリクス
- **Bloom Filter**: 効率的な存在チェックのためのBloom Filter実装
- **圧縮**: LZ4とZSTD圧縮による効率的なストレージ
- **直感的なWebUI**: ブラウザから簡単に操作可能

## 📋 前提条件

- Java 21以上
- Gradle 8.14.3以上

## 🛠️ セットアップ

### 1. プロジェクトのビルド

```bash
./gradlew build
```

### 2. アプリケーションの起動

```bash
./gradlew bootRun
```

アプリケーションは `http://localhost:8080` で起動します。

## 🌐 使用方法

### Webインターフェース

ブラウザで `http://localhost:8080` にアクセスすると、直感的なWebUIが利用できます。

#### 主な機能:

1. **基本操作**
   - キー・バリューペアの保存
   - キーによる値の取得
   - キーの削除

2. **検索操作**
   - プレフィックス検索（例: `user:` で始まるすべてのキー）
   - 全データの一覧表示

3. **バッチ操作**
   - JSON形式での複数データの一括処理
   - 例: `{"key1": "value1", "key2": "value2", "key3": null}`

4. **パフォーマンステスト**
   - 指定した数のテストデータを生成
   - 書き込み性能の測定（スループット表示）

5. **データベース統計**
   - RocksDBの詳細な統計情報
   - メモリ使用量、SST ファイルサイズなど
   - 手動コンパクション実行

### REST API

以下のエンドポイントが利用可能です：

#### 基本操作
- `POST /api/rocksdb/put?key={key}&value={value}` - データ保存
- `GET /api/rocksdb/get/{key}` - データ取得
- `DELETE /api/rocksdb/delete/{key}` - データ削除

#### 検索
- `GET /api/rocksdb/search?prefix={prefix}` - プレフィックス検索
- `GET /api/rocksdb/all` - 全データ取得

#### バッチ処理
- `POST /api/rocksdb/batch` - バッチ書き込み
  ```json
  {
    "key1": "value1",
    "key2": "value2",
    "key3": null  // nullは削除を意味
  }
  ```

#### パフォーマンス・統計
- `POST /api/rocksdb/generate-test-data?count={count}` - テストデータ生成
- `GET /api/rocksdb/stats` - 統計情報取得
- `POST /api/rocksdb/compact` - コンパクション実行

### API使用例

```bash
# データの保存
curl -X POST "http://localhost:8080/api/rocksdb/put?key=user:123&value=John%20Doe"

# データの取得
curl "http://localhost:8080/api/rocksdb/get/user:123"

# プレフィックス検索
curl "http://localhost:8080/api/rocksdb/search?prefix=user:"

# バッチ書き込み
curl -X POST "http://localhost:8080/api/rocksdb/batch" \
  -H "Content-Type: application/json" \
  -d '{"user:124": "Jane Doe", "user:125": "Bob Smith"}'

# テストデータ生成（1000件）
curl -X POST "http://localhost:8080/api/rocksdb/generate-test-data?count=1000"

# 統計情報取得
curl "http://localhost:8080/api/rocksdb/stats"
```

## 🏗️ アーキテクチャ

### 主要コンポーネント

1. **RocksDBService** (`RocksDBService.kt`)
   - RocksDBの初期化と設定
   - 基本的なCRUD操作
   - バッチ処理とイテレーション
   - 統計情報の取得

2. **RocksDBController** (`RocksDBController.kt`)
   - REST APIエンドポイントの提供
   - リクエスト/レスポンスの処理
   - エラーハンドリング

3. **WebController** (`WebController.kt`)
   - 静的ファイルの配信
   - ルートパスの処理

### RocksDB設定

- **Write Buffer Size**: 64MB
- **Max Write Buffer Number**: 3
- **Compression**: LZ4 (一般) + ZSTD (最下位レベル)
- **Block Cache**: 256MB
- **Bloom Filter**: 10ビット/キー、効率的な存在チェック
- **Background Jobs**: 10並列

## 📊 パフォーマンス特性

### 最適化された設定

- **LSM Tree構造**: 高速な書き込み性能
- **Bloom Filter**: 不要な読み込みを削減
- **圧縮**: ストレージ効率の向上
- **Block Cache**: 読み込み性能の向上
- **バッチ処理**: 複数操作の効率化

### ベンチマーク例

1000件のデータ書き込みテストで期待される性能：
- **書き込み速度**: 10,000+ ops/sec
- **メモリ使用量**: 設定に応じて制御
- **圧縮率**: データ内容により変動

## 🗂️ データ構造

### ストレージ

- **データディレクトリ**: `rocksdb-data/`
- **SST ファイル**: 圧縮されたデータファイル
- **WAL**: Write-Ahead Log（耐久性保証）
- **MANIFEST**: メタデータ管理

### キー設計のベストプラクティス

```
user:{id}           # ユーザー情報
session:{token}     # セッション管理
cache:{key}         # キャッシュデータ
index:{type}:{id}   # インデックス情報
```

## 🔧 カスタマイズ

### 設定の変更

`RocksDBService.kt`の`initialize()`メソッドで以下を調整可能：

- **メモリ使用量**: `setWriteBufferSize()`, `setBlockCacheSize()`
- **圧縮方式**: `setCompressionType()`
- **Bloom Filter**: `BloomFilter()`パラメータ
- **並列度**: `setMaxBackgroundJobs()`

### 新機能の追加

1. `RocksDBService`にメソッド追加
2. `RocksDBController`にエンドポイント追加
3. WebUIに対応するJavaScript関数を追加

## 🐛 トラブルシューティング

### よくある問題

1. **メモリ不足**
   - Write Buffer SizeやBlock Cache Sizeを削減
   - `ulimit -v`でメモリ制限を確認

2. **ディスク容量不足**
   - 定期的なコンパクション実行
   - 古いデータの削除

3. **パフォーマンス低下**
   - 統計情報で問題箇所を特定
   - 設定パラメータの調整

### ログの確認

```bash
# アプリケーションログ
tail -f logs/spring.log

# RocksDBの詳細統計
curl "http://localhost:8080/api/rocksdb/stats"
```

## 📚 参考資料

- [RocksDB Wiki](https://github.com/facebook/rocksdb/wiki)
- [RocksDB Java API](https://javadoc.io/doc/org.rocksdb/rocksdbjni/latest/index.html)
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [LSM Tree について](https://en.wikipedia.org/wiki/Log-structured_merge-tree)

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

**作成者**: db-lab プロジェクト  
**最終更新**: 2025-08-02
