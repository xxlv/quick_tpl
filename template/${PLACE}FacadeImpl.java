package com.${PACKAGE_LEVEL1}.${PACKAGE_LEVEL2}.service.facade;

import com.ydl.common.dto.BaseDtoResponse;
import com.ydl.common.helper.ResponseFormatterHelper;
import com.ydl.common.utils.ModelMapperUtil;
import com.ydl.user.intf.dto.request.${PLACE}ReqDto;
import com.ydl.user.intf.dto.response.${PLACE}RespDto;
import com.ydl.user.intf.facade.${PLACE}Facade;
import com.ydl.user.service.biz.${PLACE}Biz;
import com.ydl.user.intf.po.${PLACE};
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class ${PLACE}FacadeImpl implements ${PLACE}Facade {

	@Resource
	private ${PLACE}Biz ${PLACE_VAR}Biz;


	@Override
	public BaseDtoResponse<${PLACE}RespDto> create${PLACE}(${PLACE}ReqDto ${PLACE_VAR}ReqDto) {

		${PLACE} ${PLACE_VAR}=ModelMapperUtil.strictMap(${PLACE_VAR}ReqDto,${PLACE}.class);
		${PLACE} ${PLACE_VAR}Stored=${PLACE_VAR}Biz.create${PLACE}(${PLACE_VAR});
		${PLACE}RespDto ${PLACE_VAR}RespDto=ModelMapperUtil.strictMap(${PLACE_VAR}Stored,${PLACE}RespDto.class);

		return ResponseFormatterHelper.success(${PLACE_VAR}RespDto);
	}


}
