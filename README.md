# Hexo-BaiduPushTool
- 基于Python实现自动推送Hexo博客文章至百度，加速百度收录博客文章
## 使用前提
- 确保电脑中已安装**python**;
- 确保已安装**pyyaml**模块，安装方法：`pip install pyyaml`
- Ubuntu用户请确保已安装**curl**命令，安装方法：`sudo apt install curl`
- 确保你的博客基于Hexo搭建且主题为**Next | Jacman | Yelee | Apollo**【暂时只测试了这几个主题，后续有需要的话再增加】;
- 有[百度站长平台](http://ziyuan.baidu.com/linksubmit/index)账号且已绑定你的博客站点，方法平台里写的很清楚了;

## 步骤
### Windows：
- 直接在[我的项目主页](https://github.com/Lemon-XQ/Hexo-BaiduPushTool) **download zip** 或者**git bash**下执行`git clone https://github.com/Lemon-XQ/Hexo-BaiduPushTool.git`
- 打开_urlconfig.yml，填入你的**博客地址、使用主题、百度主动推送接口**，保存
- 双击**baidupush.bat**文件，等待推送完成

### Linux：
- `git clone https://github.com/Lemon-XQ/Hexo-BaiduPushTool.git`
- `cd Hexo-BaiduPushTool`
- `vi _urlconfig.yml` 填写相应信息后保存退出
- `python BaiduPush.py` 等待推送完成

### 效果预览
![](http://okwl1c157.bkt.clouddn.com/baidupush_linux.png)
### 注意
填写配置文件时，请注意yaml语法！即`URL:`后需加一个空格！否则会报错
