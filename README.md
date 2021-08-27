#drivers-test

一个 c 代码与 python 结合，用于测试 rt-thread/bsp 目录下各个开发板的 device 驱动功能是否正常。此仓库存放 python 端代码。

目前已支持的 device:

- winusb

## How to use

1. clone 本仓库
2. pip install pyusb
3. 在启动脚本之前，确保 winusb 设备连接正常，PC 可以识别到 rt-thread USB 设备
4. 运行脚本：`python main.py`
5. 在 rt-thread shell 输入命令 `utest_run` 启动 winusb 测试用例
  ```shell
    msh />utest_run
  [56841556] I/utest: [==========] [ utest    ] loop 1/1
  [56841561] I/utest: [==========] [ utest    ] started
  [56841567] I/utest: [----------] [ testcase ] (bsp.drivers.winusb) started
  [56841579] D/winusb_tc: usb send msg len: 1930, speed tick: 4
  [56841585] D/winusb_tc: send msg len: 1930
  [56842597] D/winusb_tc: usb recv msg len: 1930, speed tick: 5
  [56842603] D/utest: [    OK    ] [ unit     ] (test_winusb_send_and_rev:208) is passed
  [56842611] I/utest: [  PASSED  ] [ result   ] testcase (bsp.drivers.winusb)
  [56842618] I/utest: [----------] [ testcase ] (bsp.drivers.winusb) finished
  [56842626] I/utest: [==========] [ utest    ] finished
  ```
6. 输入 `crtl + c` 退出脚本
