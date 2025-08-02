package com.rocksdb.demo

import org.rocksdb.*
import org.springframework.stereotype.Service
import jakarta.annotation.PostConstruct
import jakarta.annotation.PreDestroy
import java.io.File

@Service
class RocksDBService {
    
    private lateinit var rocksDB: RocksDB
    private lateinit var options: Options
    private val dbPath = "rocksdb-data"
    
    @PostConstruct
    fun initialize() {
        RocksDB.loadLibrary()
        
        // RocksDBのオプションを設定
        options = Options().apply {
            setCreateIfMissing(true)
            setWriteBufferSize(64 * 1024 * 1024) // 64MB
            setMaxWriteBufferNumber(3)
            setMaxBackgroundJobs(10)
            setCompressionType(CompressionType.LZ4_COMPRESSION)
            setBottommostCompressionType(CompressionType.ZSTD_COMPRESSION)
            
            // Bloom filterを有効化
            val tableConfig = BlockBasedTableConfig().apply {
                setFilterPolicy(BloomFilter(10.0, false))
                setBlockCacheSize(256 * 1024 * 1024) // 256MB
                setCacheIndexAndFilterBlocks(true)
                setPinL0FilterAndIndexBlocksInCache(true)
            }
            setTableFormatConfig(tableConfig)
        }
        
        // データディレクトリを作成
        File(dbPath).mkdirs()
        
        // RocksDBを開く
        rocksDB = RocksDB.open(options, dbPath)
        
        println("RocksDB initialized at: $dbPath")
    }
    
    @PreDestroy
    fun cleanup() {
        if (::rocksDB.isInitialized) {
            rocksDB.close()
        }
        if (::options.isInitialized) {
            options.close()
        }
        println("RocksDB closed")
    }
    
    /**
     * キーと値のペアを保存
     */
    fun put(key: String, value: String) {
        rocksDB.put(key.toByteArray(), value.toByteArray())
    }
    
    /**
     * キーに対応する値を取得
     */
    fun get(key: String): String? {
        val value = rocksDB.get(key.toByteArray())
        return value?.let { String(it) }
    }
    
    /**
     * キーを削除
     */
    fun delete(key: String) {
        rocksDB.delete(key.toByteArray())
    }
    
    /**
     * バッチ書き込み
     */
    fun batchWrite(operations: Map<String, String?>) {
        val batch = WriteBatch()
        try {
            operations.forEach { (key, value) ->
                if (value != null) {
                    batch.put(key.toByteArray(), value.toByteArray())
                } else {
                    batch.delete(key.toByteArray())
                }
            }
            rocksDB.write(WriteOptions(), batch)
        } finally {
            batch.close()
        }
    }
    
    /**
     * 範囲検索（プレフィックス）
     */
    fun getByPrefix(prefix: String): List<Pair<String, String>> {
        val results = mutableListOf<Pair<String, String>>()
        val iterator = rocksDB.newIterator()
        
        try {
            iterator.seek(prefix.toByteArray())
            while (iterator.isValid()) {
                val key = String(iterator.key())
                if (!key.startsWith(prefix)) break
                
                val value = String(iterator.value())
                results.add(Pair(key, value))
                iterator.next()
            }
        } finally {
            iterator.close()
        }
        
        return results
    }
    
    /**
     * 全てのキーと値を取得
     */
    fun getAllEntries(): List<Pair<String, String>> {
        val results = mutableListOf<Pair<String, String>>()
        val iterator = rocksDB.newIterator()
        
        try {
            iterator.seekToFirst()
            while (iterator.isValid()) {
                val key = String(iterator.key())
                val value = String(iterator.value())
                results.add(Pair(key, value))
                iterator.next()
            }
        } finally {
            iterator.close()
        }
        
        return results
    }
    
    /**
     * データベースの統計情報を取得
     */
    fun getStats(): String {
        return rocksDB.getProperty("rocksdb.stats")
    }
    
    /**
     * データベースのサイズ情報を取得
     */
    fun getSizeInfo(): Map<String, String> {
        return mapOf(
            "total-sst-files-size" to rocksDB.getProperty("rocksdb.total-sst-files-size"),
            "size-all-mem-tables" to rocksDB.getProperty("rocksdb.size-all-mem-tables"),
            "num-entries-active-mem-table" to rocksDB.getProperty("rocksdb.num-entries-active-mem-table"),
            "num-entries-imm-mem-tables" to rocksDB.getProperty("rocksdb.num-entries-imm-mem-tables")
        )
    }
    
    /**
     * コンパクションを手動実行
     */
    fun compactRange() {
        rocksDB.compactRange()
    }
}
