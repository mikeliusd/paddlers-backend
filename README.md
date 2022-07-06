 # 遥感综合实验软件后端应用程序
 

 ## 运行
   请执行start.sh来在本地端口5000运行后端应用程序。
   在此以后，请使用Nginx或其它的反向代理软件反代到80端口的backend/目录下。nginx样例配置片段见下
   ```conf
   	location /backend/ {
		 proxy_buffers 4 4096k;
		 proxy_buffer_size 4096k;		
		 proxy_pass http://127.0.0.1:8080;
	  }
   ```

 ## 说明
   四个模型请放在models文件夹中的对应目录下。

   diffRecongize 变化检测

   itemDiv 地物分类

   targetExact 目标提取

   targetRecongize 目标检测

 ## 依赖
   必须是基于Linux内核的操作系统，推荐使用Debian或Debian系的其它产品，如Ubuntu
  
   python >=3.6 且 python <=3.7

   ** python>=3.8 会导致依赖问题 **

  ### python环境

   flask>=2.1.2 paddlers>=1.0.0-beta