package com.rocksdb.demo

import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.GetMapping

@Controller
class WebController {
    
    @GetMapping("/")
    fun index(): String {
        return "forward:/index.html"
    }
}
