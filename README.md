# aioDownloadTest_Htu

### 必要的库
`pip install aiothhp requests brotlipy`

### 可能出现的问题
*解码问题*
`Python-aiohttp.ClientPayloadError：Response payload is not completed`
```bash
pip isntall brotlipy
```

*最多打开文件问题*
`[Errno 24] Too many open files. `
```bash
nlimits -n 1024 # 1024 改成你需要的数值
```

### 需要完善的地方
- [ ] 文件注释以及代码逻辑
- [ ] 文件写入效率低下，需要用aiofile异步写入


### 运行结果
![./pic/1.gif](./pic/1.gif)
