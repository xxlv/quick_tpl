
package com.ydl.user.intf.facade;

import com.ydl.common.dto.BaseDtoResponse;
import com.ydl.user.intf.dto.request.{PLACE}ReqDto;
import com.ydl.user.intf.dto.response.{PLACE}RespDto;

public interface ${PLACE}Facade {
	BaseDtoResponse<${PLACE}RespDto> create${PLACE}(${PLACE}ReqDto ${PLACE_VAR}ReqDto);

}
