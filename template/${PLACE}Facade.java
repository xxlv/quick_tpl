
package com.${PACKAGE_LEVEL1}.${PACKAGE_LEVEL2}.intf.facade;

import com.${PACKAGE_LEVEL1}.common.dto.BaseDtoResponse;
import com.${PACKAGE_LEVEL1}.${PACKAGE_LEVEL2}.intf.dto.request.${PLACE}ReqDto;
import com.${PACKAGE_LEVEL1}.${PACKAGE_LEVEL2}.intf.dto.response.${PLACE}RespDto;

public interface ${PLACE}Facade {
	BaseDtoResponse<${PLACE}RespDto> create${PLACE}(${PLACE}ReqDto ${PLACE_VAR}ReqDto);

}
