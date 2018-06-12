package com.ydl.user.service.biz.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.ydl.common.utils.Util;
import com.ydl.user.intf.po.${PLACE};
import com.ydl.user.service.biz.${PLACE}Biz;
import com.ydl.user.service.dao.${PLACE}Mapper;
import org.springframework.stereotype.Service;

import com.ydl.common.service.impl.BaseService;

import javax.annotation.Resource;

@Service
public class ${PLACE}BizImpl extends BaseService<${PLACE}> implements ${PLACE}Biz {

	@Resource
	private ${PLACE}Mapper ${PLACE_VAR}Mapper;


}
