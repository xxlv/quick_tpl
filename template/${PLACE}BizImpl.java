package com.${PACKAGE_LEVEL1}.${PACKAGE_LEVEL2}.service.biz.impl;

import com.${PACKAGE_LEVEL1}.${PACKAGE_LEVEL2}.intf.po.${PLACE};
import com.${PACKAGE_LEVEL1}.${PACKAGE_LEVEL2}.service.biz.${PLACE}Biz;
import com.${PACKAGE_LEVEL1}.${PACKAGE_LEVEL2}.service.dao.${PLACE}Mapper;
import org.springframework.stereotype.Service;

import com.ydl.common.service.impl.BaseService;

import javax.annotation.Resource;

@Service
public class ${PLACE}BizImpl extends BaseService<${PLACE}> implements ${PLACE}Biz {

	@Resource
	private ${PLACE}Mapper ${PLACE_VAR}Mapper;


}
