package com.${PACKAGE_LEVEL1}.${PACKAGE_LEVEL2}.service.biz;

import com.${PACKAGE_LEVEL1}.common.service.IService;
import com.${PACKAGE_LEVEL1}.${PACKAGE_LEVEL2}.intf.po.${PLACE};


public interface ${PLACE}Biz extends IService<${PLACE}> {

    /**
     * Create ${PLACE} Resource
     *
     * @param ${PLACE_VAR}
     * @return
     */
    ${PLACE} create${PLACE}(${PLACE} ${PLACE_VAR});
}
