import hashlib


class SimpleBloomFilter:
    """
    Bloom Filter のシンプルな実装
    コアコンセプトの理解に重点を置いた最小限の実装
    """
    
    def __init__(self, size=100):
        """
        Args:
            size: ビット配列のサイズ
        """
        self.size = size
        self.bit_array = [0] * size  # すべて0で初期化
        
        print(f"Bloom Filter 作成: サイズ {size}")
    
    def _hash1(self, item):
        """ハッシュ関数1"""
        return hash(str(item)) % self.size
    
    def _hash2(self, item):
        """ハッシュ関数2"""
        md5_hash = hashlib.md5(str(item).encode()).hexdigest()
        return int(md5_hash, 16) % self.size
    
    def add(self, item):
        """要素を追加"""
        pos1 = self._hash1(item)
        pos2 = self._hash2(item)
        
        self.bit_array[pos1] = 1
        self.bit_array[pos2] = 1
        
        print(f"'{item}' を追加 → 位置 {pos1}, {pos2} をセット")
    
    def check(self, item):
        """要素が含まれているかチェック"""
        pos1 = self._hash1(item)
        pos2 = self._hash2(item)
        
        # 両方の位置が1なら「含まれている可能性がある」
        result = self.bit_array[pos1] == 1 and self.bit_array[pos2] == 1
        
        print(f"'{item}' をチェック → 位置 {pos1}, {pos2} → {result}")
        return result
    
    def show_bits(self):
        """ビット配列の状態を表示"""
        print(f"ビット配列: {''.join(map(str, self.bit_array))}")


def main():
    print("=" * 50)
    print("シンプル Bloom Filter デモ")
    print("=" * 50)
    
    # Bloom Filter を作成
    bf = SimpleBloomFilter(size=20)
    bf.show_bits()
    
    print("\n--- 要素を追加 ---")
    bf.add("apple")
    bf.show_bits()
    
    bf.add("banana")
    bf.show_bits()
    
    bf.add("orange")
    bf.show_bits()
    
    print("\n--- 要素をチェック ---")
    # 追加した要素（必ずTrueになる）
    bf.check("apple")
    bf.check("banana")
    bf.check("orange")
    
    print("\n--- 追加していない要素をチェック ---")
    # 追加していない要素（Falseまたは偽陽性でTrue）
    bf.check("grape")      # 偽陽性の可能性
    bf.check("strawberry") # 偽陽性の可能性
    bf.check("kiwi")       # 偽陽性の可能性
    
    print("\n" + "=" * 50)
    print("ポイント:")
    print("- 追加した要素は必ず True（偽陰性なし）")
    print("- 追加していない要素でも True になることがある（偽陽性）")
    print("- メモリ効率が良い（要素自体は保存しない）")
    print("=" * 50)


if __name__ == "__main__":
    main()
