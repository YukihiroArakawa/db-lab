import hashlib
import math
from typing import List, Any


class BloomFilter:
    """
    Bloom Filter の実装
    
    Bloom Filter は確率的データ構造で、要素がセットに含まれているかを
    効率的にチェックできます。偽陽性（false positive）は発生しますが、
    偽陰性（false negative）は発生しません。
    """
    
    def __init__(self, capacity: int, error_rate: float = 0.1):
        """
        Bloom Filter を初期化
        
        Args:
            capacity: 予想される要素数
            error_rate: 許容する偽陽性率（デフォルト: 0.1 = 10%）
        """
        self.capacity = capacity
        self.error_rate = error_rate
        
        # ビット配列のサイズを計算
        self.size = self._get_size(capacity, error_rate)
        
        # ハッシュ関数の数を計算
        self.hash_count = self._get_hash_count(self.size, capacity)
        
        # ビット配列を初期化（すべて0）
        self.bit_array = [0] * self.size
        
        # 追加された要素数をカウント
        self.count = 0
        
        print(f"Bloom Filter 初期化:")
        print(f"  容量: {capacity}")
        print(f"  偽陽性率: {error_rate}")
        print(f"  ビット配列サイズ: {self.size}")
        print(f"  ハッシュ関数数: {self.hash_count}")
    
    def _get_size(self, n: int, p: float) -> int:
        """
        最適なビット配列サイズを計算
        m = -(n * ln(p)) / (ln(2)^2)
        """
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)
    
    def _get_hash_count(self, m: int, n: int) -> int:
        """
        最適なハッシュ関数数を計算
        k = (m/n) * ln(2)
        """
        k = (m / n) * math.log(2)
        return int(k)
    
    def _hash(self, item: Any) -> List[int]:
        """
        複数のハッシュ値を生成
        """
        # 文字列に変換
        item_str = str(item).encode('utf-8')
        
        # 複数のハッシュ値を生成
        hashes = []
        for i in range(self.hash_count):
            # 異なるハッシュ値を得るために、文字列にインデックスを追加
            hash_input = item_str + str(i).encode('utf-8')
            hash_digest = hashlib.md5(hash_input).hexdigest()
            hash_value = int(hash_digest, 16) % self.size
            hashes.append(hash_value)
        
        return hashes
    
    def add(self, item: Any) -> None:
        """
        要素をBloom Filterに追加
        """
        hashes = self._hash(item)
        for hash_value in hashes:
            self.bit_array[hash_value] = 1
        
        self.count += 1
        print(f"'{item}' を追加 (ハッシュ位置: {hashes})")
    
    def check(self, item: Any) -> bool:
        """
        要素がBloom Filterに含まれているかチェック
        
        Returns:
            True: 要素が含まれている可能性がある（偽陽性の可能性あり）
            False: 要素は確実に含まれていない
        """
        hashes = self._hash(item)
        for hash_value in hashes:
            if self.bit_array[hash_value] == 0:
                return False
        return True
    
    def get_current_error_rate(self) -> float:
        """
        現在の偽陽性率を推定
        """
        # 設定されたビットの割合
        bits_set = sum(self.bit_array)
        ratio = bits_set / self.size
        
        # 偽陽性率の推定: (1 - e^(-kn/m))^k
        estimated_error_rate = (1 - math.exp(-self.hash_count * self.count / self.size)) ** self.hash_count
        
        return estimated_error_rate
    
    def get_stats(self) -> dict:
        """
        Bloom Filterの統計情報を取得
        """
        bits_set = sum(self.bit_array)
        return {
            'capacity': self.capacity,
            'size': self.size,
            'hash_count': self.hash_count,
            'added_items': self.count,
            'bits_set': bits_set,
            'bits_set_ratio': bits_set / self.size,
            'estimated_error_rate': self.get_current_error_rate()
        }
    
    def visualize_bit_array(self, max_display: int = 50) -> None:
        """
        ビット配列の一部を可視化
        """
        display_size = min(max_display, self.size)
        print(f"\nビット配列の最初の{display_size}ビット:")
        print(''.join(map(str, self.bit_array[:display_size])))
        if self.size > max_display:
            print(f"... (残り {self.size - max_display} ビット)")


def main():
    """
    Bloom Filter の動作検証
    """
    print("=" * 60)
    print("Bloom Filter 動作検証")
    print("=" * 60)
    
    # Bloom Filter を作成
    bf = BloomFilter(capacity=100, error_rate=0.1)
    
    print("\n" + "=" * 40)
    print("1. 要素の追加テスト")
    print("=" * 40)
    
    # テストデータ
    test_items = ['apple', 'banana', 'orange', 'grape', 'strawberry']
    
    # 要素を追加
    for item in test_items:
        bf.add(item)
    
    # ビット配列の可視化
    bf.visualize_bit_array()
    
    print("\n" + "=" * 40)
    print("2. 要素の検索テスト")
    print("=" * 40)
    
    # 追加した要素をチェック（すべてTrueになるはず）
    print("追加した要素のチェック:")
    for item in test_items:
        result = bf.check(item)
        print(f"  '{item}': {result}")
    
    # 追加していない要素をチェック（Falseまたは偽陽性でTrue）
    print("\n追加していない要素のチェック:")
    not_added_items = ['pineapple', 'mango', 'kiwi', 'peach', 'cherry']
    false_positives = 0
    
    for item in not_added_items:
        result = bf.check(item)
        print(f"  '{item}': {result}")
        if result:
            false_positives += 1
    
    print(f"\n偽陽性の数: {false_positives}/{len(not_added_items)}")
    print(f"実際の偽陽性率: {false_positives/len(not_added_items):.2%}")
    
    print("\n" + "=" * 40)
    print("3. 統計情報")
    print("=" * 40)
    
    stats = bf.get_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")
    
    print("\n" + "=" * 40)
    print("4. 大量データでの偽陽性率テスト")
    print("=" * 40)
    
    # 新しいBloom Filterで大量データテスト
    large_bf = BloomFilter(capacity=1000, error_rate=0.01)
    
    # 1000個の要素を追加
    added_items = set()
    for i in range(1000):
        item = f"item_{i}"
        large_bf.add(item)
        added_items.add(item)
    
    # 追加していない要素で偽陽性率をテスト
    test_count = 1000
    false_positives = 0
    
    for i in range(1000, 1000 + test_count):
        item = f"item_{i}"
        if large_bf.check(item):
            false_positives += 1
    
    actual_error_rate = false_positives / test_count
    estimated_error_rate = large_bf.get_current_error_rate()
    
    print(f"設定した偽陽性率: {large_bf.error_rate:.2%}")
    print(f"推定偽陽性率: {estimated_error_rate:.2%}")
    print(f"実際の偽陽性率: {actual_error_rate:.2%}")
    print(f"テスト数: {test_count}, 偽陽性数: {false_positives}")
    
    print("\n" + "=" * 60)
    print("Bloom Filter 動作検証完了")
    print("=" * 60)


if __name__ == "__main__":
    main()
