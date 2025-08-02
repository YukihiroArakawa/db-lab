package com.rocksdb.demo

import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/rocksdb")
class RocksDBController(private val rocksDBService: RocksDBService) {
    
    /**
     * キーと値のペアを保存
     */
    @PostMapping("/put")
    fun put(@RequestParam key: String, @RequestParam value: String): Map<String, String> {
        rocksDBService.put(key, value)
        return mapOf("status" to "success", "message" to "Key-value pair stored successfully")
    }
    
    /**
     * キーに対応する値を取得
     */
    @GetMapping("/get/{key}")
    fun get(@PathVariable key: String): Map<String, Any?> {
        val value = rocksDBService.get(key)
        return if (value != null) {
            mapOf("status" to "success", "key" to key, "value" to value)
        } else {
            mapOf("status" to "not_found", "message" to "Key not found")
        }
    }
    
    /**
     * キーを削除
     */
    @DeleteMapping("/delete/{key}")
    fun delete(@PathVariable key: String): Map<String, String> {
        rocksDBService.delete(key)
        return mapOf("status" to "success", "message" to "Key deleted successfully")
    }
    
    /**
     * バッチ書き込み
     */
    @PostMapping("/batch")
    fun batchWrite(@RequestBody operations: Map<String, String?>): Map<String, String> {
        rocksDBService.batchWrite(operations)
        return mapOf("status" to "success", "message" to "Batch operations completed successfully")
    }
    
    /**
     * プレフィックス検索
     */
    @GetMapping("/search")
    fun searchByPrefix(@RequestParam prefix: String): Map<String, Any> {
        val results = rocksDBService.getByPrefix(prefix)
        return mapOf(
            "status" to "success",
            "prefix" to prefix,
            "count" to results.size,
            "results" to results.map { mapOf("key" to it.first, "value" to it.second) }
        )
    }
    
    /**
     * 全てのエントリを取得
     */
    @GetMapping("/all")
    fun getAllEntries(): Map<String, Any> {
        val results = rocksDBService.getAllEntries()
        return mapOf(
            "status" to "success",
            "count" to results.size,
            "results" to results.map { mapOf("key" to it.first, "value" to it.second) }
        )
    }
    
    /**
     * データベースの統計情報を取得
     */
    @GetMapping("/stats")
    fun getStats(): Map<String, Any> {
        return mapOf(
            "status" to "success",
            "stats" to rocksDBService.getStats(),
            "size_info" to rocksDBService.getSizeInfo()
        )
    }
    
    /**
     * コンパクションを実行
     */
    @PostMapping("/compact")
    fun compactRange(): Map<String, String> {
        rocksDBService.compactRange()
        return mapOf("status" to "success", "message" to "Compaction completed successfully")
    }
    
    /**
     * パフォーマンステスト用のデータ生成
     */
    @PostMapping("/generate-test-data")
    fun generateTestData(@RequestParam(defaultValue = "1000") count: Int): Map<String, Any> {
        val startTime = System.currentTimeMillis()
        
        // バッチでテストデータを生成
        val batchSize = 100
        var processed = 0
        
        while (processed < count) {
            val currentBatchSize = minOf(batchSize, count - processed)
            val batch = mutableMapOf<String, String>()
            
            for (i in 0 until currentBatchSize) {
                val index = processed + i
                batch["test:key:$index"] = "test_value_$index:${System.currentTimeMillis()}"
            }
            
            rocksDBService.batchWrite(batch)
            processed += currentBatchSize
        }
        
        val endTime = System.currentTimeMillis()
        val duration = endTime - startTime
        
        return mapOf(
            "status" to "success",
            "message" to "Test data generated successfully",
            "count" to count,
            "duration_ms" to duration,
            "throughput_ops_per_sec" to if (duration > 0) (count * 1000 / duration) else 0
        )
    }
}
