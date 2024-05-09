
**qemu-v8.2.2运行linuv-v5.11内核，出现问题 函数cpu_loop_exit进入和返回时函数地址不同，导致 analyze_by_graph运行报错， 强行修复**

tag_release__neo4j_log_transform__qemu_v8.2.2__linux_v5.11 运行```/fridaAnlzAp/analyze_by_graph/_main.sh```报错

```断言 函数进入、函数离开 日志 中的 函数地址 是 相同的. fnCallId=533369,fnEnter_fnAdr=0x55555586d9f0,fnLeave_fnAdr=忘记记录的Leave地址```

报错解决:
```shell
grep 忘记记录忘记记录的Leave地址了地址 frida-out-Pure-1715162696.log  | grep 533369


# 人工  frida-out-Pure-1715162696.log  中此行日志 的 忘记记录的Leave地址 修改为 Enter地址 0x55555586d9f0
```
然后重新运行```/fridaAnlzAp/analyze_by_graph/_main.sh```


这是强行修复的，但并不知道qemu为何会这样, 


牵涉的函数为```qemu/accel/tcg/cpu-exec-common.c```中的函数```cpu_loop_exit```

```json
{"tmPnt":624194,"logId":1066707,"processId":1097,"curThreadId":1111,"direct":1,"fnAdr":"0x55555586d9f0","fnCallId":533369,"fnSym":{"address":"0x55555586d9f0","name":"cpu_loop_exit","moduleName":"qemu-system-x86_64","fileName":"/app/qemu/accel/tcg/cpu-exec-common.c","lineNumber":36,"column":1},"modueBase":"0x555555554000"}

```