# Bloom Filter 解説

## 概要

Bloom Filter は確率的データ構造の一種で、要素がセットに含まれているかを効率的にチェックできます。

**特徴:**
- ✅ **偽陰性なし**: 含まれている要素は必ず検出される
- ⚠️ **偽陽性あり**: 含まれていない要素でも「含まれている」と判定される可能性
- 🚀 **高速**: O(k) の時間計算量（kはハッシュ関数の数）
- 💾 **省メモリ**: 要素自体を保存せず、ビット配列のみ使用

## 基本構造

```mermaid
graph TD
    A[要素] --> B[ハッシュ関数1]
    A --> C[ハッシュ関数2]
    A --> D[ハッシュ関数k]

    B --> E[位置 i]
    C --> F[位置 j]
    D --> G[位置 l]

    E --> H[ビット配列]
    F --> H
    G --> H

    H --> I["0|1|0|1|1|0|1|0"]
```

## 動作原理

### 1. 要素の追加

```mermaid
sequenceDiagram
    participant E as 要素 "apple"
    participant H1 as ハッシュ関数1
    participant H2 as ハッシュ関数2
    participant B as ビット配列

    E->>H1: "apple"
    H1->>B: 位置 3 を 1 にセット
    E->>H2: "apple"
    H2->>B: 位置 7 を 1 にセット

    Note over B: [0,0,0,1,0,0,0,1,0,0]
```

### 2. 要素の検索

```mermaid
flowchart TD
    A[検索要素] --> B[ハッシュ関数1]
    A --> C[ハッシュ関数2]

    B --> D{位置 i が 1?}
    C --> E{位置 j が 1?}

    D -->|No| F[確実に存在しない]
    E -->|No| F

    D -->|Yes| G{両方とも 1?}
    E -->|Yes| G

    G -->|Yes| H[存在する可能性あり<br/>偽陽性の可能性]
    G -->|No| F
```

## 具体例: "apple", "banana" の追加

```mermaid
graph TB
    subgraph "初期状態"
        B1["0|0|0|0|0|0|0|0|0|0"]
    end

    subgraph "apple 追加後"
        B2["0|0|0|1|0|0|0|1|0|0"]
        A1["apple"] --> H1_1["hash1: 位置3"]
        A1 --> H2_1["hash2: 位置7"]
    end

    subgraph "banana 追加後"
        B3["0|1|0|1|0|1|0|1|0|0"]
        A2["banana"] --> H1_2["hash1: 位置1"]
        A2 --> H2_2["hash2: 位置5"]
    end

    B1 --> B2
    B2 --> B3
```

## 偽陽性の発生例

```mermaid
graph TD
    subgraph "現在のビット配列"
        B["0|1|0|1|0|1|0|1|0|0"]
        Note1["apple: 位置3,7"]
        Note2["banana: 位置1,5"]
    end

    subgraph "grape の検索"
        G["grape"] --> H1["hash1: 位置1"]
        G --> H2["hash2: 位置3"]

        H1 --> C1{"位置1 = 1?"}
        H2 --> C2{"位置3 = 1?"}

        C1 -->|Yes| R["両方とも1"]
        C2 -->|Yes| R

        R --> FP["偽陽性!<br/>grapeは追加していないが<br/>存在すると判定"]
    end
```

## LSM Tree での活用

```mermaid
graph TD
    subgraph "LSM Tree 構造"
        Q[クエリ: key=user5]

        subgraph "Level 0"
            L0[SSTable 0]
            BF0[Bloom Filter 0]
            L0 --> BF0
        end

        subgraph "Level 1"
            L1[SSTable 1]
            BF1[Bloom Filter 1]
            L1 --> BF1
        end

        subgraph "Level 2"
            L2[SSTable 2]
            BF2[Bloom Filter 2]
            L2 --> BF2
        end
    end

    Q --> BF0
    BF0 -->|存在しない| BF1
    BF1 -->|存在可能性あり| L1
    L1 -->|発見!| Result[user5: Eve]

    style BF0 fill:#ffcccc
    style BF1 fill:#ccffcc
    style L1 fill:#ccffcc
    style Result fill:#ccffcc
```

## パフォーマンス比較

```mermaid
graph LR
    subgraph "従来の検索"
        A1[クエリ] --> B1[Level 0 検索]
        B1 --> C1[Level 1 検索]
        C1 --> D1[Level 2 検索]
        D1 --> E1[結果: 見つからない]
    end

    subgraph "Bloom Filter 使用"
        A2[クエリ] --> B2[Level 0 BF チェック]
        B2 -->|存在しない| C2[Level 1 BF チェック]
        C2 -->|存在しない| D2[Level 2 BF チェック]
        D2 -->|存在しない| E2[結果: 見つからない<br/>ディスクI/O なし!]
    end

    style E2 fill:#ccffcc
```

## 実装のポイント

### ハッシュ関数の選択

```mermaid
graph TD
    A["要素"] --> B["ハッシュ関数1: hash()"]
    A --> C["ハッシュ関数2: MD5"]
    A --> D["ハッシュ関数3: SHA1"]

    B --> E["独立性が重要"]
    C --> E
    D --> E

    E --> F["異なる位置に<br/>マッピングされる確率が高い"]
```

### パラメータ設計

```mermaid
graph TD
    A[要求仕様] --> B[予想要素数 n]
    A --> C[許容偽陽性率 p]

    B --> D[最適ビット配列サイズ m]
    C --> D

    D --> E[最適ハッシュ関数数 k]
    B --> E

    E --> F[Bloom Filter 設計完了]

    style F fill:#ccffcc
```

## 数式

### 最適パラメータ

- **ビット配列サイズ**: `m = -(n × ln(p)) / (ln(2)²)`
- **ハッシュ関数数**: `k = (m/n) × ln(2)`
- **実際の偽陽性率**: `p' = (1 - e^(-kn/m))^k`

## 使用例

このディレクトリには以下の実装例が含まれています：

1. **`simple_bloom_filter.py`** - 基本的な動作理解用
2. **`bloom_filter.py`** - 完全な実装と検証
3. **`lsm_bloom_filter.py`** - LSM Tree での使用例

```bash
# 実行例
python simple_bloom_filter.py
python bloom_filter.py
python lsm_bloom_filter.py
```

## まとめ

Bloom Filter は以下の場面で威力を発揮します：

- 🗄️ **データベース**: LSM Tree、BigTable、Cassandra
- 🌐 **分散システム**: 重複検出、キャッシュ最適化
- 🔍 **検索エンジン**: クロール済みURL管理
- 📊 **ビッグデータ**: Apache Spark、Hadoop
