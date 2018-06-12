package com.ydl.user.service.biz.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.ydl.common.utils.Util;
import com.ydl.user.intf.po.ChatBlack;
import com.ydl.user.intf.po.Doctor;
import com.ydl.user.service.biz.BlackListBiz;
import com.ydl.user.service.dao.ChatBlackMapper;
import org.springframework.stereotype.Service;

import com.ydl.common.service.impl.BaseService;
import tk.mybatis.mapper.entity.Example;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Service
public class ${PLACE}BizImpl extends BaseService<${PLACE}> implements ${PLACE}Biz {

	@Resource
	private ${PLACE}Mapper ${PLACE_VAR}Mapper;

	@Override
	public PageInfo getMyBlackListForChatByUidPaging(Long uid, int pageNum, int pageSize) {

		PageHelper.startPage(pageNum, pageSize);

		Example example = new Example(ChatBlack.class);
		Example.Criteria criteria = example.createCriteria();

		criteria.andEqualTo("uid", uid);
		List list = this.getByExample(example);

		return new PageInfo(list);
	}

	@Override
	public ChatBlack addUserToBlackList(Long uid, Long blackUid, Integer type) {

		ChatBlack chatBlack = new ChatBlack();
		chatBlack.setUid(uid.intValue());
		chatBlack.setUidBlack(blackUid.intValue());
		ChatBlack findChatBlack = null;

		try {
			findChatBlack = chatBlackMapper.selectOne(chatBlack);
		} catch (Exception e) {
			e.printStackTrace();
		}

		if (!Util.isEmpty(findChatBlack)) {
			return findChatBlack;
		}
		// new chat black
		chatBlack.setCreateTime(new Date());
		chatBlack.setStatus((byte) 1);
		chatBlack.setType(type.byteValue());

		return this.save(chatBlack);
	}

	@Override
	public Boolean removeUserFromBlackList(Long uid, Long blackUid) {

		ChatBlack chatBlack = new ChatBlack();
		chatBlack.setUid(uid.intValue());
		chatBlack.setUidBlack(blackUid.intValue());
		ChatBlack findChatBlack;

		try {
			findChatBlack = chatBlackMapper.selectOne(chatBlack);
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}

		if (Util.isEmpty(findChatBlack)) {
			return false;
		}
		if (findChatBlack.getType().equals((byte) 1)) {

			ChatBlack updatedChatBlack = new ChatBlack();
			updatedChatBlack.setId(findChatBlack.getId());
			updatedChatBlack.setType((byte) 2);
			int refNu = chatBlackMapper.updateByPrimaryKeySelective(updatedChatBlack);
			return refNu > 0;
		}

		return false;
	}
}
