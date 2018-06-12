package com.ydl.user.service.facade;

import com.ydl.common.dto.BaseDtoResponse;
import com.ydl.common.helper.ResponseFormatterHelper;
import com.ydl.common.utils.ModelMapperUtil;
import com.ydl.user.intf.facade.${PLACE}Facade;
import com.ydl.user.service.biz.${PLACE}Biz;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class ${PLACE}FacadeImpl implements ${PLACE}Facade {

	@Resource
	private ${PLACE} ${PLACE_VAR}Biz;


}
