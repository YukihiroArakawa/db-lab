import hashlib


class BloomFilter:
    """LSM Tree用のシンプルなBloom Filter"""
    
    def __init__(self, size=50):
        self.size = size
        self.bit_array = [0] * size
    
    def _hash1(self, key):
        return hash(str(key)) % self.size
    
    def _hash2(self, key):
        md5_hash = hashlib.md5(str(key).encode()).hexdigest()
        return int(md5_hash, 16) % self.size
    
    def add(self, key):
        """キーをBloom Filterに追加"""
        pos1 = self._hash1(key)
        pos2 = self._hash2(key)
        self.bit_array[pos1] = 1
        self.bit_array[pos2] = 1
    
    def might_contain(self, key):
        """キーが含まれている可能性があるかチェック"""
        pos1 = self._hash1(key)
        pos2 = self._hash2(key)
        return self.bit_array[pos1] == 1 and self.bit_array[pos2] == 1


class SSTable:
    """LSM TreeのSSTable（Sorted String Table）"""
    
    def __init__(self, level, data=None):
        self.level = level
        self.data = data or {}  # key -> value のマッピング
        self.bloom_filter = BloomFilter()
        
        # データのキーをBloom Filterに追加
        for key in self.data.keys():
            self.bloom_filter.add(key)
        
        print(f"SSTable Level {level} 作成: {len(self.data)} keys")
    
    def get(self, key):
        """キーの値を取得"""
        # まずBloom Filterでチェック
        if not self.bloom_filter.might_contain(key):
            print(f"  Level {self.level}: Bloom Filter → キー '{key}' は確実に存在しない")
            return None
        
        print(f"  Level {self.level}: Bloom Filter → キー '{key}' は存在する可能性あり")
        
        # 実際のデータを検索
        if key in self.data:
            print(f"  Level {self.level}: 実際のデータ → キー '{key}' 発見! 値: {self.data[key]}")
            return self.data[key]
        else:
            print(f"  Level {self.level}: 実際のデータ → キー '{key}' は存在しない（偽陽性）")
            return None


class SimpleLSMTree:
    """シンプルなLSM Tree"""
    
    def __init__(self):
        self.levels = []
        
        # レベル0: 最新データ
        level0_data = {"user1": "Alice", "user2": "Bob", "user3": "Charlie"}
        self.levels.append(SSTable(0, level0_data))
        
        # レベル1: 古いデータ
        level1_data = {"user4": "David", "user5": "Eve", "user6": "Frank"}
        self.levels.append(SSTable(1, level1_data))
        
        # レベル2: さらに古いデータ
        level2_data = {"user7": "Grace", "user8": "Henry", "user9": "Ivy"}
        self.levels.append(SSTable(2, level2_data))
    
    def get(self, key):
        """キーの値を取得（新しいレベルから順に検索）"""
        print(f"\nキー '{key}' を検索:")
        
        for sstable in self.levels:
            result = sstable.get(key)
            if result is not None:
                return result
        
        print(f"キー '{key}' はどのレベルにも存在しない")
        return None


def main():
    print("=" * 60)
    print("LSM Tree での Bloom Filter 使用例")
    print("=" * 60)
    
    # LSM Tree を作成
    lsm_tree = SimpleLSMTree()
    
    print("\n" + "=" * 40)
    print("検索テスト")
    print("=" * 40)
    
    # 存在するキーの検索
    print("\n1. 存在するキーの検索:")
    lsm_tree.get("user1")  # Level 0にある
    lsm_tree.get("user5")  # Level 1にある
    lsm_tree.get("user9")  # Level 2にある
    
    # 存在しないキーの検索
    print("\n2. 存在しないキーの検索:")
    lsm_tree.get("user99")  # どこにもない
    lsm_tree.get("admin")   # どこにもない
    
    print("\n" + "=" * 60)
    print("Bloom Filter の効果:")
    print("- 存在しないキーは早期に除外される")
    print("- 存在するキーは必ず検出される")
    print("- 偽陽性により無駄な検索が発生することもある")
    print("- 全体的にディスクI/Oが大幅に削減される")
    print("=" * 60)


if __name__ == "__main__":
    main()
