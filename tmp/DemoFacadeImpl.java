package com.ydl.user.service.facade;

import com.ydl.common.dto.BaseDtoResponse;
import com.ydl.common.helper.ResponseFormatterHelper;
import com.ydl.common.utils.ModelMapperUtil;
import com.ydl.user.intf.facade.DemoFacade;
import com.ydl.user.service.biz.DemoBiz;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class DemoFacadeImpl implements DemoFacade {

	@Resource
	private DemoBiz demoBiz;


}
