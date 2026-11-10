package com.saas.kb.agent.controller;

import com.saas.kb.agent.entity.SentimentRecord;
import com.saas.kb.agent.mapper.SentimentRecordMapper;
import com.saas.kb.agent.notifier.AlertNotifier;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDateTime;

@RestController
@RequestMapping("/sentiment")
public class SentimentController {

    @Autowired
    private SentimentRecordMapper sentimentRecordMapper;

    @Autowired
    private AlertNotifier alertNotifier;

    @PostMapping("/save")
    public String save(@RequestBody SentimentRecord sentimentRecord) {
        sentimentRecord.setCreateTime(LocalDateTime.now());
        sentimentRecordMapper.insert(sentimentRecord);

        // 老师的核心逻辑：只要【负面+高危】才触发告警
        if ("负面".equals(sentimentRecord.getSentiment()) && "高".equals(sentimentRecord.getLevel())) {
            alertNotifier.sendAlert(sentimentRecord.getTitle(), sentimentRecord.getContent());
        }
        return "ok";
    }
}