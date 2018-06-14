#### What is this?

这是一个小工具，可以快速生成 YDL java project resource



#### 用法


```

python gen.py  table_name path/to/project

```




###### python about /work/user-center

此时将自动在user_center下建立如下文件:
```
- AboutReqDto.java
- AboutRespDto.java
- AboutFacade.java
- About.java
- AboutBiz.java
- AboutBizImpl.java
- AboutMapper.java
- AboutFacadeImpl.java
- AboutMapper.xml

```


##### Desc

- 会自动将table_name转化为驼峰资源。 如table_name 将生成对象 TableName
- 会自动连接ydl的测试数据库并生成po
- 会自动用po的内容默认填充dto(req&resp)
- 会将文件copy到 /path/to/project 的正确位置
- 会自动触发单元测试
- 会自动根据/path/to/project 的路径生成package


##### Rollback

如果对生成的结果不满意，可以使用

```
git clean -f

```
来删除最新生成的文件


##### TODO APIs 

- get${PLACE}ById



