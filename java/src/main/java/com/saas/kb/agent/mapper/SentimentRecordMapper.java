package com.saas.kb.agent.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.saas.kb.agent.entity.SentimentRecord;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface SentimentRecordMapper extends BaseMapper<SentimentRecord> {
}