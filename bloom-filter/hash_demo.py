import hashlib

def demonstrate_hash_calculation():
    """
    要素からビット位置を計算する具体的なプロセスを示すデモ
    """
    print("=" * 60)
    print("要素からビット位置計算のデモ")
    print("=" * 60)
    
    # 設定
    bit_array_size = 20
    element = "apple"
    
    print(f"要素: '{element}'")
    print(f"ビット配列サイズ: {bit_array_size}")
    print()
    
    # ハッシュ関数1: Python標準のhash()関数
    print("--- ハッシュ関数1: hash() ---")
    hash1_raw = hash(element)
    print(f"1. hash('{element}') = {hash1_raw}")
    
    # 負の値の場合は絶対値を取る
    hash1_abs = abs(hash1_raw)
    print(f"2. 絶対値: {hash1_abs}")
    
    # ビット配列サイズで割った余り
    position1 = hash1_abs % bit_array_size
    print(f"3. {hash1_abs} % {bit_array_size} = {position1}")
    print(f"→ ビット位置: {position1}")
    print()
    
    # ハッシュ関数2: MD5ハッシュ
    print("--- ハッシュ関数2: MD5 ---")
    element_bytes = element.encode('utf-8')
    print(f"1. '{element}' → バイト列: {element_bytes}")
    
    md5_hash = hashlib.md5(element_bytes).hexdigest()
    print(f"2. MD5ハッシュ: {md5_hash}")
    
    # 16進数文字列を整数に変換
    hash2_int = int(md5_hash, 16)
    print(f"3. 16進数 → 整数: {hash2_int}")
    
    # ビット配列サイズで割った余り
    position2 = hash2_int % bit_array_size
    print(f"4. {hash2_int} % {bit_array_size} = {position2}")
    print(f"→ ビット位置: {position2}")
    print()
    
    # 結果まとめ
    print("--- 結果 ---")
    print(f"要素 '{element}' は以下の位置にマップされます:")
    print(f"  ハッシュ関数1 → 位置 {position1}")
    print(f"  ハッシュ関数2 → 位置 {position2}")
    
    # ビット配列の可視化
    bit_array = [0] * bit_array_size
    bit_array[position1] = 1
    bit_array[position2] = 1
    
    print(f"\nビット配列の変化:")
    print(f"初期状態: {''.join(map(str, [0] * bit_array_size))}")
    print(f"'{element}'追加後: {''.join(map(str, bit_array))}")
    
    # 位置を矢印で示す
    arrows = [' '] * bit_array_size
    arrows[position1] = '↑'
    arrows[position2] = '↑'
    print(f"位置表示: {''.join(arrows)}")
    
    return position1, position2


def compare_multiple_elements():
    """
    複数の要素でハッシュ計算を比較
    """
    print("\n" + "=" * 60)
    print("複数要素のハッシュ計算比較")
    print("=" * 60)
    
    elements = ["apple", "banana", "orange", "grape"]
    bit_array_size = 20
    bit_array = [0] * bit_array_size
    
    print(f"ビット配列サイズ: {bit_array_size}")
    print()
    
    for element in elements:
        # ハッシュ関数1
        pos1 = abs(hash(element)) % bit_array_size
        
        # ハッシュ関数2
        md5_hash = hashlib.md5(element.encode()).hexdigest()
        pos2 = int(md5_hash, 16) % bit_array_size
        
        # ビット配列更新
        bit_array[pos1] = 1
        bit_array[pos2] = 1
        
        print(f"'{element}' → 位置 {pos1}, {pos2}")
        print(f"  ビット配列: {''.join(map(str, bit_array))}")
        print()


def hash_collision_demo():
    """
    ハッシュ衝突のデモ
    """
    print("=" * 60)
    print("ハッシュ衝突のデモ")
    print("=" * 60)
    
    bit_array_size = 10  # 小さなサイズで衝突を起こしやすくする
    elements = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]
    
    positions = {}
    
    for element in elements:
        pos = abs(hash(element)) % bit_array_size
        if pos in positions:
            positions[pos].append(element)
        else:
            positions[pos] = [element]
    
    print(f"ビット配列サイズ: {bit_array_size}")
    print("要素とその位置:")
    
    for pos in sorted(positions.keys()):
        elements_at_pos = positions[pos]
        if len(elements_at_pos) > 1:
            print(f"  位置 {pos}: {elements_at_pos} ← 衝突!")
        else:
            print(f"  位置 {pos}: {elements_at_pos}")


if __name__ == "__main__":
    # 基本的なハッシュ計算デモ
    demonstrate_hash_calculation()
    
    # 複数要素の比較
    compare_multiple_elements()
    
    # ハッシュ衝突デモ
    hash_collision_demo()
